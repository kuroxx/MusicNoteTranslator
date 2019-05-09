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

app = Flask(__name__)
app.secret_key = '5236f7f7898da7adf878a072baf96bb1254627050c8c4c91'
UPLOAD_FOLDER = 'static/images/'
temp_filenames = [""]

class UploadForm(FlaskForm):
  file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

@app.route("/")
@app.route("/index")
def index():
  """
  Returns index page.
  """
  return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload_file():
  """
  Returns flask form once it has been validated.
  """

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
  """
  Returns image path, prediction and translation results.
  """

  # Define image path
  if len(temp_filenames) == 0 :
    imgpath = ''
  else:
    imgpath = UPLOAD_FOLDER + temp_filenames[-1]  

  # Load dictionary    
  predictionResults = pickle.load( open( "save.p", "rb" ) )
  
  musicSymbolsDict = {
    "barline": [], 
    "clef": [], 
    "timeSignature": [], 
    "keySignature": [], 
    "rest": [], 
    "multirest": [], 
    "note": [], 
    "gracenote": []
    }
  
  musicSymbolsKeyList = ["barline", "clef", "timeSignature", "keySignature", "rest", "multirest", "note", "gracenote"]

  splitResults = []

  for i in predictionResults.keys():
    splitResults.append(predictionResults[i].rsplit('-', 1))

  # Categorise note symbols
  for i in range(len(splitResults)):
    for k in musicSymbolsKeyList:
      if (splitResults[i][0] == "barline"):
        musicSymbolsDict["barline"].append(splitResults[i][0])
        break
      elif (splitResults[i][0] == k):
        musicSymbolsDict[k].append(splitResults[i][1])
  # print(musicSymbolsDict)

  musicNotesDict = {
    "A" : ["A", "La", "6"],
    "B" : ["B", "Ti", "7"],
    "C" : ["C", "Do", "1"],
    "D" : ["D", "Re", "2"],
    "E" : ["E", "Mi", "3"],   
    "F" : ["F", "Fa", "4"],
    "G" : ["G", "So", "5"],     
  }

  musicNotesKeyList = ["A", "B", "C", "D", "E", "F", "G"]

  splitNotes = []
  translationResults = []

  # 0 = Letter, 1 = Solfege, 2 = Cipher
  notation = 1

  for i in range(len(musicSymbolsDict["note"])):
    splitNotes.append(musicSymbolsDict["note"][i].rsplit("_", 1))

  # Add translated note
  for i in range(len(splitNotes)):
    for k in musicNotesKeyList:
      if (splitNotes[i][0][:1] == k) :
        translationResults.append(musicNotesDict[k][notation])
        
        # translationResults['0'].append(musicNotesDict[k][0])
        # translationResults['1'].append(musicNotesDict[k][1])
        # translationResults['2'].append(musicNotesDict[k][2])

  print (translationResults)

  return render_template('results.html', predictionResults=predictionResults, imgpath=imgpath, translationResults=translationResults)

@app.route('/camera')
@app.route('/handwrite')
def temp():
  """
  Temporary placeholder for future features.
  """
  return render_template('temp.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)