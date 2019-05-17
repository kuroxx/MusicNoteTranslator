import unittest
from main_utils import create_imgpath, split_strings, categorise_symbols, translate_notes

class FlaskTestCase(unittest.TestCase):

# Tests 
  def test_create_imgpath(self):
    UPLOAD_FOLDER = '/static/images/'
    self.assertEqual(create_imgpath(['test.png'], UPLOAD_FOLDER), '/static/images/test.png')
    self.assertEqual(create_imgpath([''], UPLOAD_FOLDER), '/static/images/')
    
  def test_split_strings(self):
    string_arr = ['note-A4_half']
    self.assertEqual(split_strings(range(len(string_arr)), string_arr, '-'), [['note', 'A4_half']])
    # int_arr = [1,2,3]
    # self.assertRaises(split_strings(range(len(int_arr)), int_arr, '-'), "Array value needs to be string!")

  def test_categorise_symbols(self):
    split_arr = [['barline'], ['rest', 'half'], ['note', 'A4_half'], ['note', 'C2_half']]
    symbols_key_list = ['rest', 'note']

    symbols_dict = {
        'barline': [],
        'rest': [], 
        'note': []
        } 

    self.assertEqual(categorise_symbols(split_arr, symbols_key_list, symbols_dict, 1), {'barline': ['barline'], 'rest' : ['half'], 'note' : ['A4_half', 'C2_half']})

  def test_translate_notes(self):
    translation_reference = {
    "A" : ["A", "La", "6"],
    "B" : ["B", "Ti", "7"],
    "C" : ["C", "Do", "1"],
    "D" : ["D", "Re", "2"],
    "E" : ["E", "Mi", "3"],   
    "F" : ["F", "Fa", "4"],
    "G" : ["G", "So", "5"],     
    }
    key_list = ["A", "B", "C", "D", "E", "F", "G"]
    notation = 0
    arr_to_translate = [['A4','half'],['C2','half']]

    self.assertEqual(translate_notes(arr_to_translate, key_list, translation_reference, notation), ["A", "C"])

if __name__ == '__main__':
  unittest.main()