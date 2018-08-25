import sublime, sublime_plugin, os, re

class importcssCommand(sublime_plugin.TextCommand):
  def run(self, edit):

    # get path and name of main file
    mainFilePath = self.view.file_name().rsplit('\\', 1)[0]
    mainFileFullName = self.view.file_name().rsplit('\\', 1)[1]
    mainFileName = self.view.file_name().rsplit('\\', 1)[1].split('.')[0]
    minifiedFileName = mainFileName + '.min.css'

    # change the current working directory
    os.chdir(mainFilePath)

    # create(rewrite) new minified file
    createFile = os.path.join(mainFilePath, minifiedFileName)
    with open(createFile, 'w'):
      pass
    sublime.active_window().open_file(minifiedFileName)

    # get paths from main file
    with open (mainFileFullName, 'r') as mainFile:
      mainFileContent = mainFile.read().replace('"', "'")
    importPaths = re.findall(r'\'(.+?)\'', mainFileContent)

    # search for urls, conversion and writing to a file
    for path in importPaths:
      with open (path, 'r') as importFile:
        importFileContent = importFile.read()
        importFileUrls = [groups[0] for groups in re.findall(r'(url\((?![\'"]?(?:data|http):)[\'"]?([^\'"\)]*)[\'"]?\))', importFileContent)]
        cssPath = path.rsplit('/', 1)[0]

        if importFileUrls:
          for importFileUrl in importFileUrls:
            imageReplaceString = re.findall(r'\((.*)\)', importFileUrl)[0]
            image = imageReplaceString.replace('"', '').replace("'", '')
            importFileContent = importFileContent.replace(imageReplaceString, '"' + cssPath + '/' + image + '"');
            if importFileUrl == importFileUrls[-1]:
              with open(minifiedFileName, 'a') as minifiedFile:
                minifiedFile.write(importFileContent)
        else:
          with open(minifiedFileName, 'a') as minifiedFile:
            minifiedFile.write(importFileContent)

