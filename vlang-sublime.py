import sublime
import sublime_plugin
import os
import threading
import subprocess

run_output = None

def setup_output(window):
	global run_output

	# To prevent a new tab every time, let's reuse the output window.
	if run_output is None:
		run_output = window.new_file()
		run_output.set_scratch(True)
		run_output.set_name('V')

	window.focus_view(run_output)

	return run_output

class VCommand(sublime_plugin.WindowCommand):
	def run(self, cmd, output=True):
		# Make sure we get the file path before we open a new tab.
		cur_view = self.window.active_view()
		file = cur_view.file_name()
		module = os.path.dirname(cur_view.file_name())

		# Substitute variables. It would be nice to use
		# sublime.expand_variables() here instead, but that does not escape
		# spaces in paths.
		variables = sublime.active_window().extract_variables()
		cmd = "v " + cmd
		for variable in variables:
			cmd = cmd.replace('${' + variable + '}', '"' + variables[variable] + '"')

		view = None
		if output:
			view = setup_output(self.window)
			view.run_command('insert_view', { 'string': '$ ' + cmd + '\n' })

		runner = Runner(cmd, os.environ['SHELL'], os.environ.copy(), view, output)
		runner.start()

class InsertViewCommand(sublime_plugin.TextCommand):
	def run(self, edit, string=''):
		self.view.set_read_only(False)
		self.view.insert(edit, self.view.size(), string)
		self.view.set_read_only(True)

class Runner(threading.Thread):
	def __init__(self, command, shell, env, view, output):
		self.stdout = None
		self.stderr = None
		self.command = command
		self.shell = shell
		self.env = env
		self.view = view
		self.output = output
		threading.Thread.__init__(self)

	def run(self):
		proc = subprocess.Popen(
			[self.shell, '-ic', self.command],
			shell=False,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			universal_newlines=True,
			env=self.env
		)

		while True:
			out = proc.stdout.read(1)
			if out == '' and proc.poll() != None:
			 	break
			if out != '' and self.output:
			 	self.view.run_command('insert_view', { 'string': out })
		
		if self.output:
			self.view.run_command('insert_view', { 'string': '\n' })
