#!/usr/bin/env python3
import argparse
import re
import messages.core
import os
import nltk
from nltk.corpus import stopwords

import matplotlib.pyplot as pyplot

parser = argparse.ArgumentParser()
parser.add_argument("--mask")
parser.add_argument("--colours")
parser.add_argument("--scale", type=int)
parser.add_argument("--plot", action='store_true')
parser.add_argument("--file", action='store_true')
parser.add_argument("--open", action='store_true')
args = parser.parse_args()

if not os.path.isfile(messages.core.CSV_FILE_NAME):
    raise ValueError(f'Cannot build Word Cloud without \'{messages.core.CSV_FILE_NAME}\'. Please run import.py first.')

dataFrame = messages.core.readCsvFile()

text = ' '.join(content for content in dataFrame.content)
text = re.sub('[^a-zA-Z]', ' ', text)

stopWords = set(map(str.strip, open('stopwords.txt', 'r').readlines()))
stopWords.update(stopwords.words('english'))

tokenized = list(filter(
    lambda word: word not in stopWords,
    nltk.tokenize.word_tokenize(text)))
    
print(f"Read {len(tokenized):,} words from \'{messages.core.CSV_FILE_NAME}\'.")

distribution = nltk.probability.FreqDist(tokenized)
print(distribution.most_common(10))

distribution.plot(100,cumulative=False)
pyplot.show()