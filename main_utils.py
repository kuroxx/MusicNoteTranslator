"""
main_utils.py contains useful functions required in the main Flask app.
"""

def create_imgpath(filename_arr, UPLOAD_FOLDER):
  """
  Creates path to image.

  :param filename_arr str: Array containing lits of filenames.
  :param UPLOAD_FOLDER str: Path to folder where image should be saved.
  :return: String of the image path.
  """
  if len(filename_arr) == 0 :
    imgpath = ''
  else:
    imgpath = UPLOAD_FOLDER + filename_arr[-1]  

  return imgpath

def split_strings(key_list, strings_dict, delim):
  """
  Splits strings in a dictionary.
  
  :param key_list str: List of keys to iterate over.
  :param strings_dict str: Dictionary of strings to split.
  :param delim str: Delimiter for splitting the string.
  :return: Array of the split strings.
  """
  splitResultsArr = []

  for x in key_list:
    splitResultsArr.append(strings_dict[x].rsplit(delim, 1))

  return splitResultsArr

def categorise_symbols(unsorted_dict, key_list, results_dict, arr_index):
  """
  Categorise items in a dictionary.

  :param unsorted_dict str: Dictionary of unsorted items.
  :param key_list str: List of keys to iterate over.
  :param results_dict str: Dictionary with predefined key categories to append new items to.
  :param arr_index int: Indicates which index value of the array to append to the dictionary.
  :return: Dictionary with categorised items.
  """
  for i in range(len(unsorted_dict)):
    for k in key_list:
      if (unsorted_dict[i][0] == "barline"):
        results_dict["barline"].append(unsorted_dict[i][0])
        break
      elif (unsorted_dict[i][0] == k):
        results_dict[k].append(unsorted_dict[i][arr_index])

  return results_dict  

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
