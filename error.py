# Error wrapper. Prints a message in the debug console. Can show a message box (optional)
#
# Typically used instead of try/except in the base of event handlers and run()/stop().
# This allows for less clutter as most cases will always need to be handled the same

import adsk.core
import traceback, getpass
import os, re, sys
# Avoid Fusion namespace pollution
from . import utils, manifest

class ErrorCatcher():
	'''	Showing a messagebox is disabled in debugging, by default,
		to avoid the case where Fusion is stopped and the debugger
		fails to reattach on Restart.
		---

		## __init__

		msgbox_in_debug: Show an error message box also when debugging.
		msg_prefix: Prefix error message with this text. E.g. with
					add-in name and version.

		#### Usage:
		to always have the same options-
		
		Globally, set:
			error_catcher_ = ErrorCatcher()

		In function use:
			with error_catcher_:
				code that can throw
	'''
	def __init__(self, msgbox_in_debug=False, msg_prefix=''):
		self.msgbox_in_debug = msgbox_in_debug
		self.msg_prefix = msg_prefix

	def __enter__(self): self.caller_file = utils.get_caller_path()

	def __exit__(self, exctype, value, traceb):
		if not traceb: return
		app ,ui = utils.AppObjects()

		# Only keep the AddIns/Scripts part of the path
		caller = re.sub(r'.*API[/\\]', '', self.caller_file)
		tb_str = ''.join(traceback.format_exception(exctype, value, traceb))
		# Shorten file paths, to compact the message
		tb_str = re.sub(r'"[^"]+/(?:API/AddIns|Api/Python)', '"', tb_str)
		# Attempt to scrub the user's username from the traceback, if any remains
		tb_str = tb_str.replace(getpass.getuser(), '<user>')

		message = (f'{self.msg_prefix} error: {value}\n\n' +
					'Copy this message by taking a screenshot. ' +
					'Describe what you did to get this error or record a video.\n\n' +
					'-' * 50 + '\n\n' +
					f'Fusion 360 v. {app.version}\n' +
					f'{caller} failed: \n\n' +
					tb_str)
		print(message)

		in_debugger = hasattr(sys, 'gettrace') and sys.gettrace()
		if ui and (not in_debugger or self.msgbox_in_debug):
			print("Also showed in message box.")
			ui.messageBox(message)
		else: print("Not shown in message box.")
		return True # Exception handled


def _error_catcher_wrapper(class_self_Ref, func):
	def catcher(func_self, args):
		with class_self_Ref.error_catcher: func(args)
	return catcher
