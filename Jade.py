import sublime
import sys
from os import path
from subprocess import Popen, PIPE
from sublime_plugin import TextCommand, WindowCommand

settings = sublime.load_settings('Jade.sublime-settings')

def run(cmd, args = [], source="", cwd = None, env = None):
  if not type(args) is list:
    args = [args]
  if sys.platform == "win32":
    proc = Popen([cmd]+args, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
    stat = proc.communicate(input=source)
  else:
    if env is None:
      env = {"PATH": settings.get('binDir', '/usr/local/bin')}
    if source == "":
      command = [cmd]+args
    else:
      command = [cmd]+args
    proc = Popen(command, env=env, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stat = proc.communicate(input=source)
  okay = proc.returncode == 0
  return {"okay": okay, "out": stat[0], "err": stat[1]}

def brew(args, source):
  return run("jade", args=args, source=source)

def isJade(view = None):
  if view is None:
    view = sublime.active_window().active_view()
  return 'source.jade' in view.scope_name(0)

class TextJ():
  @staticmethod
  def all(view):
    return view.substr(sublime.Region(0, view.size()))
  @staticmethod
  def sel(view):
    text = []
    for region in view.sel():
      if region.empty():
        continue
      text.append(view.substr(region))
    return "".join(text)

  @staticmethod
  def get(view):
    text = TextJ.sel(view)
    if len(text) > 0:
      return text
    return TextJ.all(view)
  
class CompileAndDisplayJadeCommand(TextCommand):
  def is_enabled(self):
    return isJade(self.view)

  def run(self, edit, **kwargs):
    opt = kwargs["opt"]
    args = [opt]
    res = brew(args, TextJ.get(self.view))
    output = self.view.window().new_file()
    output.set_scratch(True)
    if opt == '-P':
      output.set_syntax_file('Packages/HTML/HTML.tmLanguage')
    if res["okay"] is True:
      output.insert(edit, 0, res["out"])
    else:
      output.insert(edit, 0, res["err"].split("\n")[0])