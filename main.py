#!/usr/bin/env python3

from flask import Flask, render_template, request
from flask import redirect, url_for, flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug.utils import secure_filename
from wtforms import SubmitField
from wtforms import validators
import pickle
import ctc_predict as predict
from main_utils import create_imgpath, split_strings, categorise_symbols, translate_notes

app = Flask(__name__)
app.secret_key = '5236f7f7898da7adf878a072baf96bb1254627050c8c4c91'
UPLOAD_FOLDER = 'static/images/'
temp_filenames = [""]

class UploadForm(FlaskForm):
  file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

@app.route("/")
@app.route("/index")
def index():
  """Renders index page."""
  return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
  """Runs TF model if flask form is valid on submit."""

  form = UploadForm()

  if form.validate_on_submit():
    filename = secure_filename(form.file.data.filename)
    form.file.data.save(UPLOAD_FOLDER + filename)
    flash('File "{}" successfully uploaded'.format(filename))
    
    temp_filenames.append(filename)

    # Run tf model
    predict.main(UPLOAD_FOLDER + filename)

    return redirect(url_for('display_results'))
  return render_template('file_upload.html', form=form)

@app.route('/results')
@app.route('/results/<notation>')
def display_results(notation=0):
  """Translates and displays image, prediction and translation results."""

  symbols_dict = {
    "barline": [], 
    "clef": [], 
    "timeSignature": [], 
    "keySignature": [], 
    "rest": [], 
    "multirest": [], 
    "note": [], 
    "gracenote": []
    }
  
  symbols_key_list = ["barline", "clef", "timeSignature", "keySignature", "rest", "multirest", "note", "gracenote"]
  
  # Load dictionary    
  prediction_results = pickle.load( open( "save.p", "rb" ) )

  split_Arr1 = split_strings(prediction_results.keys(), prediction_results, '-')
  categorise_symbols(split_Arr1, symbols_key_list, symbols_dict, 1)

  notes_dict = {
    "A" : ["A", "La", "6"],
    "B" : ["B", "Ti", "7"],
    "C" : ["C", "Do", "1"],
    "D" : ["D", "Re", "2"],
    "E" : ["E", "Mi", "3"],   
    "F" : ["F", "Fa", "4"],
    "G" : ["G", "So", "5"],     
  }

  notes_key_list = ["A", "B", "C", "D", "E", "F", "G"]

  # Split dictionary strings
  notes_dict_range = range(len(symbols_dict["note"]))
  split_Arr2 = split_strings(notes_dict_range, symbols_dict["note"], '_')

  # Categorise and translate notes
  translation_let = translate_notes(split_Arr2, notes_key_list, notes_dict, 0)
  translation_sol = translate_notes(split_Arr2, notes_key_list, notes_dict, 1)
  translation_num = translate_notes(split_Arr2, notes_key_list, notes_dict, 2)

  imgpath = create_imgpath(temp_filenames, UPLOAD_FOLDER)

  return render_template('results.html', imgpath=imgpath, prediction_results=prediction_results, translation_let=translation_let, translation_sol=translation_sol, translation_num=translation_num)

@app.route('/camera')
@app.route('/handwrite')
def temp():
  """Temporary placeholder for future features."""
  return render_template('temp.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)