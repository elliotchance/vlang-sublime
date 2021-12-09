import sublime
import sublime_plugin
import os
import threading
import subprocess

run_output = None

class RunCurrentFileCommand(sublime_plugin.WindowCommand):
	def run(self):
		global run_output

		# Make sure we get the file path before we open a new tab.
		cur_view = self.window.active_view()
		file = cur_view.file_name()

		# To prevent a new tab every time, let's reuse the output window.
		if run_output is None:
			run_output = self.window.new_file()
			run_output.set_scratch(True)
			run_output.set_name('v run')

		self.window.focus_view(run_output)

		cmd = 'v run "' + file + '"'
		run_output.run_command('insert_view', { 'string': '$ ' + cmd + '\n' })

		runner = Runner(cmd, os.environ['SHELL'], os.environ.copy(), run_output)
		runner.start()

class InsertViewCommand(sublime_plugin.TextCommand):
	def run(self, edit, string=''):
		self.view.set_read_only(False)
		self.view.insert(edit, self.view.size(), string)
		self.view.set_read_only(True)

class Runner(threading.Thread):
	def __init__(self, command, shell, env, view):
		self.stdout = None
		self.stderr = None
		self.command = command or ''
		self.shell = shell or ''
		self.env = env or ''
		self.view = view or None
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
			if out != '':
			 	self.view.run_command('insert_view', { 'string': out })
		
		self.view.run_command('insert_view', { 'string': '\n' })
