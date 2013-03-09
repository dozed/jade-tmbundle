import sublime, sublime_plugin, subprocess

class HtmlToJadeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.set_status('html2jade', "html2jade")
    command = 'html2jade -s'

    p = subprocess.Popen(command, bufsize=-1, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    result, err = p.communicate(self.view.substr(self.view.sel()[0]).encode('utf-8'))

    if result != "":
      self.view.replace(edit, self.view.sel()[0], result.decode('utf-8'))
      sublime.set_timeout(self.clear,0)
    else:
      self.view.set_status('html2jade', "html2jade: "+err)
      sublime.set_timeout(self.clear,10000)

  def clear(self):
    self.view.erase_status('html2jade')