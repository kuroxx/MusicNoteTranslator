"""
main_utils.py contains useful functions required in the main Flask app.
"""

def create_imgpath(filenameArr, UPLOAD_FOLDER):
  if len(filenameArr) == 0 :
    imgpath = ''
  else:
    imgpath = UPLOAD_FOLDER + filenameArr[-1]  

  return imgpath

def split_strings(listRange, stringsDict, delim):
  """
  Splits strings in a dictionary.
  
  :param listRange str: List of keys to iterate over.
  :param stringsDict str: Dictionary of strings to split.
  :param delim str: Delimiter for splitting the string.
  :return: Array of the split strings.
  """
  splitResultsArr = []

  for x in listRange:
    splitResultsArr.append(stringsDict[x].rsplit(delim, 1))

  return splitResultsArr

def categorise_symbols(splitStrDict, keyList, resultsDict, arrIndex):
  for i in range(len(splitStrDict)):
    for k in keyList:
      if (splitStrDict[i][0] == "barline"):
        resultsDict["barline"].append(splitStrDict[i][0])
        break
      elif (splitStrDict[i][0] == k):
        resultsDict[k].append(splitStrDict[i][arrIndex])

  return resultsDict  

  # categorise_symbols(splitNotes, musicNotesKeyList, translationResults, notation)
  # # Add translated note
  # for i in range(len(splitNotes)):
  #   for k in musicNotesKeyList:
  #     if (splitNotes[i][0][:1] == k) :
  #       translationResults.append(musicNotesDict[k][notation])

  #       # translationResults['0'].append(musicNotesDict[k][0])
  #       # translationResults['1'].append(musicNotesDict[k][1])
  #       # translationResults['2'].append(musicNotesDict[k][2])


  # categorise_symbols(splitResults, musicSymbolsKeyList, musicSymbolsDict, 1)

  #   # Categorise note symbols
  # for i in range(len(splitResults)):
  #   for k in musicSymbolsKeyList:
  #     if (splitResults[i][0] == "barline"):
  #       musicSymbolsDict["barline"].append(splitResults[i][0])
  #       break
  #     elif (splitResults[i][0] == k):
  #       musicSymbolsDict[k].append(splitResults[i][1])
