# Sentence Pretreatment
The goal of this repo is to present the method I used to perform pretreatment on the text corpus that I used for my research project. This repo does not contain the data structure nor the extracting algorithm!
This algorithm has been designed to use [TAC2008](https://tac.nist.gov//2008/index.html) corpus as source data, and text files for testing purposes.

### Installation
Once you've cloned the repo, you will need to install the nltk Python3 package using `pip3 install -U nltk`.
Then go into the python3 terminal and execute the following:
```console
>>>import nltk
>>>nltk.download()
```
Once it's done, you should be good to go.

### Using the code
This code has been designed to run with Python3 using the following command:
```console
python3 [path] [xmlMode]
```
If you don't intend to use a xml file or a folder containing xml files, but rather txt files, make sure to note that sentence extraction does not currently support sentence extraction from txt file.
The path should be the one of a folder containing source files, or the one of a source file itself.
