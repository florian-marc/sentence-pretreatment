import os
import sys

import xml.etree.ElementTree as et

from operator import itemgetter

import nltk
from nltk.corpus import stopwords	#list of stopwords in all languages supported
from nltk.tokenize import RegexpTokenizer
from nltk.probability import FreqDist
from nltk.stem import PorterStemmer

class sentence:
	def __init__(self, wordList, sentenceNumber, sourceDocPath):
		self.list = wordList
		self.number = sentenceNumber
		self.doc = sourceDocPath

class textFilePretreatment:
	def __init__(self, file):

		self.tokenized_sentences = []
		
		#Opening file and replacing carriage return by space
		brexit_text =file.read().replace('\n', ' ')
		
		#Initializing tokenizer	
		tokenizer = RegexpTokenizer(r'\w+')
		#Initializing Stemmer (not supported yet)
		ps = PorterStemmer()

		#Tokenizing sentences
		tokenized_words=tokenizer.tokenize(brexit_text.lower())
		self.sentences=nltk.sent_tokenize(brexit_text.lower())

		filtered_tokenized_words=[]
		filtered_tokenized_sentences = []

		#Removing stopwords from text
		for word in tokenized_words:
			if  word not in stopwords.words('english'):
				filtered_tokenized_words.append(ps.stem(word))

		for b_sentence in self.sentences:
			filtered_tokenized_sentences.append([ps.stem(word) for word in tokenizer.tokenize(b_sentence) if word not in stopwords.words('english')])

        #Creating the fdist dictionnary
		fdist_words = FreqDist(filtered_tokenized_words)
		self.fdist_dict = dict(fdist_words.most_common(fdist_words.N()))
		for k in self.fdist_dict.keys():
			print(k + "," + str(self.fdist_dict[k]))
		i = 0
		for filtered_sentence in filtered_tokenized_sentences:
			self.tokenized_sentences.append(sentence(sorted(filtered_sentence,key= lambda x: self.fdist_dict.get(x), reverse = True), i, file))
			i+=1

class xmlFilePretreatment:
#Pretreatment on a xml file
	def __init__(self, path, isFile, param = "lemm"):
		self.path = path
		self.rawSentences = []
		self.tokenized_sentences = []
		self.fdist_dict = {}
		self.param = param
		if(isFile):
			self.addSentences(self.path)
		
	def addSentences(self, path):
		t = et.parse(path)
		tree = t.getroot()
		sentences = tree.findall(".//" + self.param)
		i = 0
		for s in sentences:
			if self.param == "raw":
				splited_s = s.text.split(":")
				if len(splited_s) is 1:
					self.rawSentences.append(sentence(splited_s[0], i, path))
				else:
					self.rawSentences.append(sentence(splited_s[1], i, path))
			else:
				if self.param == "lem":
					splited_s = s.text.split("  ")
					if len(splited_s) is 1:
						self.rawSentences.append(sentence(splited_s[0], i, path))
					else:
						self.rawSentences.append(sentence(splited_s[1], i, path))
				
				else:
					if self.param == "bigrams":
						if s.text is not None:						#some bigrams are empty
							self.rawSentences.append(sentence(s.text, i, path))
			i += 1

	def treatSentences(self):
		allText = ""
		tokenizer = RegexpTokenizer(r'\w+')
		for s in self.rawSentences:
			allText += s.sent.lower() + '.'

		tokenizedText = tokenizer.tokenize(allText.lower())
		filtered_tokenized_words = []
		for word in tokenizedText:
			if word not in stopwords.words('english'):
				if word != "@card@":
					filtered_tokenized_words.append(word)
		fdist_words = FreqDist(filtered_tokenized_words)
		self.fdist_dict = dict(fdist_words.most_common(fdist_words.N()))

		filtered_tokenized_sentences = []
		for s in self.rawSentences:
			filtered_tokenized_sentences.append(sentence([word for word in tokenizer.tokenize(s.sent.lower()) if word not in stopwords.words('english')], s.number, s.doc))
		for filtered_sentence in filtered_tokenized_sentences:
			self.tokenized_sentences.append(sentence(sorted(filtered_sentence.list,key = lambda x: self.fdist_dict.get(x), reverse = True), filtered_sentence.number, filtered_sentence.doc))

class job:
	def __init__(self, path, xmlMode = None):
		initial_path = path
		self.isFile = os.path.splitext(path)[1] != '' #is the path a directory?
		if(self.isFile):
			if os.path.splitext(path)[1] == '.txt':
				p = textFilePretreatment(open(path, 'r'))
			else:
				if os.path.splitext(path)[1] == '.xml':
					p = xmlFilePretreatment(path, self.isFile, xmlMode)
					p.treatSentences()
		else:
			path = "u08_corr/" + path + "/" + path + "-A"
			p = xmlFilePretreatment(path, self.isFile, xmlMode)
			for file in os.listdir(path):
				if os.path.splitext(file)[1] == '.xml' and os.path.splitext(file)[0] != 'concat':
					p.addSentences(path + '/' + file)
			p.treatSentences()
        #self.dataStruct = 
		self.outputSentences = [] #sorted(, key = itemgetter(0, 1))
		self.extractSentences(initial_path)

	def extractSentences(self, outputPath):
		file = open(os.getcwd()+ "/results/" + outputPath + "_system.txt", "w")
		path = ""
		tree = None	
		for s in self.outputSentences:
			if s[1] != path:
				path = s[1]
				tree = et.parse(path).getroot()
			file.write(tree.findall(".//*[@id='" + str(s[0]) + "']/raw")[0].text + "\n")
		file.close()

def main(arg1, arg2):
    j = job(arg1,arg2)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])