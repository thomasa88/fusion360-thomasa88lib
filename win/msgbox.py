# Message box functions
#
# This file is part of thomasa88lib, a library of useful Fusion 360
# add-in/script functions.
#
# Copyright (c) 2020 Thomas Axelsson
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import adsk
import ctypes
# Must explicitly include wintypes for code to work at Fusion start-up
import ctypes.wintypes

user32 = ctypes.WinDLL('user32', use_last_error=True)
_hook_factory = ctypes.WINFUNCTYPE(ctypes.wintypes.LPARAM,
                            ctypes.c_int,
                            ctypes.wintypes.WPARAM, ctypes.wintypes.LPARAM)

# https://stackoverflow.com/a/31396340/106019
class CWPRETSTRUCT(ctypes.Structure):
    _fields_ = (('lResult', ctypes.wintypes.LPARAM),
                ('lParam', ctypes.wintypes.LPARAM),
                ('wParam', ctypes.wintypes.WPARAM),
                ('message', ctypes.c_uint),
                ('hwnd', ctypes.wintypes.HWND))

LPCWPRETSTRUCT = ctypes.POINTER(CWPRETSTRUCT)

# Icons
MB_ICONERROR = 0x00000010
MB_ICONQUESTION = 0x00000020
MB_ICONWARNING = 0x00000030
MB_ICONINFORMATION = 0x00000040
    
# Button configurations
MB_ABORTRETRYIGNORE = 0x00000002
MB_CANCELTRYCONTINUE = 0x00000006
MB_HELP = 0x00004000
MB_OK = 0x00000000
MB_OKCANCEL = 0x00000001
MB_RETRYCANCEL = 0x00000005
MB_YESNO = 0x00000004
MB_YESNOCANCEL = 0x00000003

# Default button
MB_DEFBUTTON1 = 0x00000000
MB_DEFBUTTON2 = 0x00000100
MB_DEFBUTTON3 = 0x00000200
MB_DEFBUTTON4 = 0x00000300

# Button IDs
IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDRETRY = 4
IDIGNORE = 5
IDYES = 6
IDNO = 7
IDTRYAGAIN = 10
IDCONTINUE = 11

WM_INITDIALOG = 0x0110

WH_CALLWNDPROCRET = 12

user32.CallNextHookEx.restype = ctypes.wintypes.LPARAM
user32.CallNextHookEx.argtypes = (ctypes.wintypes.HHOOK,
                                  ctypes.c_int,
                                  ctypes.wintypes.WPARAM,
                                  ctypes.wintypes.LPARAM)

user32.UnhookWindowsHookEx.argtypes = (ctypes.wintypes.HHOOK,)
user32.UnhookWindowsHookEx.restype = ctypes.wintypes.BOOL

user32.SetWindowsHookExW.restype = ctypes.wintypes.HHOOK
user32.SetWindowsHookExW.argtypes = (ctypes.c_int,
                                        _hook_factory,
                                        ctypes.wintypes.HINSTANCE,
                                        ctypes.wintypes.DWORD)

user32.GetDlgItem.argtypes = (ctypes.wintypes.HWND, ctypes.c_int)
user32.GetDlgItem.restype = ctypes.wintypes.HWND

user32.GetActiveWindow.restype = ctypes.wintypes.HWND

def custom_msgbox(text, caption, dlg_type, label_map={}):
    '''Wrapper for MessageBox that allows setting button labels (Windows-only)

    https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxw
    '''
    win_thread_id = ctypes.windll.kernel32.GetCurrentThreadId()

    # This must not go out of scope as long as the hook is active
    c_hook = _hook_factory(_create_hook(label_map))

    hook_handle = user32.SetWindowsHookExW(WH_CALLWNDPROCRET, c_hook,
                                           ctypes.wintypes.HINSTANCE(0),
                                           win_thread_id)
    #error = ctypes.get_last_error()

    main_window = user32.GetActiveWindow()
    ret = user32.MessageBoxW(main_window, text, caption, dlg_type)
    if hook_handle:
        user32.UnhookWindowsHookEx(hook_handle)
    
    return ret

def _create_hook(label_map):
    def hook(n_code, w_param, l_param):
        if n_code < 0:
            return user32.CallNextHookEx(None, n_code, w_param, l_param)
        try:        
            msg = ctypes.cast(l_param, LPCWPRETSTRUCT)[0]
            if msg.message == WM_INITDIALOG:
                buf = ctypes.create_unicode_buffer(10)
                user32.GetClassNameW(msg.hwnd, buf, len(buf))
                class_name = buf.value
                if class_name == '#32770':
                    for ctl_id, label in label_map.items():
                        _set_dialog_ctl_text(msg.hwnd, ctl_id, label)
        except Exception as e:
            print(f"{NAME} Hook error:", e)
        finally:
            return user32.CallNextHookEx(None, n_code, w_param, l_param)
    return hook

def _set_dialog_ctl_text(parent_hwnd, control_id, text):
    ctl_hwnd = user32.GetDlgItem(parent_hwnd, control_id)
    if ctl_hwnd:
        user32.SetWindowTextW.argtypes = (ctypes.wintypes.HWND,
                                            ctypes.wintypes.LPCWSTR)
        user32.SetWindowTextW.restype = ctypes.wintypes.BOOL
        user32.SetWindowTextW(ctl_hwnd, text)
