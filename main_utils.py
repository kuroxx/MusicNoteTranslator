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

def split_strings(key_list, strings_to_split, delim):
  """
  Splits strings in a dictionary.
  
  :param key_list str: List of keys to iterate over.
  :param strings_to_split str: Dictionary of strings to split.
  :param delim str: Delimiter for splitting the string.
  :return: Array of the split strings.
  """
  splitResultsArr = []

  for x in key_list:
    splitResultsArr.append(strings_to_split[x].rsplit(delim, 1))

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

def translate_notes(arr_to_translate, key_list, translation_reference, notation):
  """
  Creates new array with translated items.

  :param arr_to_translate str: Array of items to translate. 
  :param key_list str: List of keys to iterate over.
  :param translation_reference str: Dictionary containing reference for translations.
  :param notation int: Indicates which index position to reference translation from dictionary. 
  :return: Array with translated items.
  """
  translation_results = []

  for i in range(len(arr_to_translate)):
    for k in key_list:
      if (arr_to_translate[i][0][:1] == k) :
        translation_results.append(translation_reference[k][notation])        

  return translation_results 