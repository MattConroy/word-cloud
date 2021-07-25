#!/usr/bin/env python3
import argparse
import messages.core
import os
import numpy
import pandas
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

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

dataFrame = pandas.read_csv(messages.core.CSV_FILE_NAME,  delimiter=',', quotechar='|')

text = " ".join(content for content in dataFrame.content).replace(messages.core.NEW_LINE_REPLACEMENT,'\n')
stopWords = set(STOPWORDS)
stopWords.update('P', 'D', 'O', 'Y', 'L', 'xxx', 'x', 'Yeah ')

if args.mask:
    mask = numpy.array(Image.open(f"masks/{args.mask}.png"))
else:
    mask = None

if args.colours:
    colours = ImageColorGenerator(numpy.array(Image.open(f"colours/{args.colours}.png")))
else:
    colours = None

print(f"Read {len(text):,} words from \'{messages.core.CSV_FILE_NAME}\'.")

wordCloud = WordCloud(
        width = 1280,
        height = 720,
        mask=mask,
        scale=args.scale or 4,
        min_font_size=4,
        max_words=1000,
        stopwords=stopWords,
        color_func=colours,
        background_color=None,
        mode='RGBA',
    ).generate(text)
print('Generated Word Cloud.')

if args.file:
    wordCloud.to_file('word-cloud.png')
    print('Saved Word Cloud to \'word-cloud.png\'.')
    if args.open:
        os.system("start word-cloud.png")

if args.plot:
    pyplot.figure(figsize=[12,6], tight_layout=True, frameon=False)
    pyplot.imshow(wordCloud, interpolation='bilinear')
    pyplot.axis('off')
    pyplot.show()