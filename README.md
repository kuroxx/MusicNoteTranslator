# MusicNoteTranslator (MNT)

Python code that uses Optical Music Recognition (OMR) to interpret monophonic music score sheets and then translates them into alternative music notation formats (i.e. Letter, Solfege, Cipher). It is built using Flask and uses the TensorFlow model  -  [https://github.com/calvozaragoza/tf-deep-omr](https://github.com/calvozaragoza/tf-deep-omr).

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Prerequisites

Please install (if required) the following before running the project:

- Flask
- Flask wtf-forms
- TensorFlow

## Installing

1. Install the required dependencies by typing the following in terminal:

```
pip install Flask
pip install Flask-WTF
pip install --upgrade tensorflow
```

2. Simply download or clone this project using:

```
git clone
```

## Running

The main application is stored in the file `main.py`. 
Run this project by typing the following in terminal:

```
python main.py
```

## Testing

To run unittest on code, type the following in the Terminal:

```
python -m unittest tests/test.py 
```

# Built With

- [Flask](http://flask.pocoo.org/) - Python microframework 

# Acknowledgments

- [https://github.com/calvozaragoza/tf-deep-omr](https://github.com/calvozaragoza/tf-deep-omr)