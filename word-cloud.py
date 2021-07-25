#!/usr/bin/env python3
import argparse
import messages.core
import numpy as np
import pandas as pd
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("--mask")
parser.add_argument("--colours")
parser.add_argument("--scale", type=int)
args = parser.parse_args()

dataFrame = pd.read_csv(messages.core.CSV_FILE_NAME,  delimiter=',', quotechar='|')

text = " ".join(content for content in dataFrame.content).replace(messages.core.NEW_LINE_REPLACEMENT,'\n')
stopWords = set(STOPWORDS)
stopWords.update('P', 'D', 'O', 'Y', 'L', 'xxx', 'x', 'Yeah ')

if args.mask:
    mask = np.array(Image.open(f"masks/{args.mask}.png"))
else:
    mask = None

if args.colours:
    colours = ImageColorGenerator(np.array(Image.open(f"colours/{args.colours}.png")))
else:
    colours = None

print(f"Generating Word Cloud from {len(text):,} words from \'{messages.core.CSV_FILE_NAME}\'.")

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
print('Generated Word Cloud. Saving image.')
    
wordCloud.to_file('word-cloud.png')
print('Saved Word Cloud to \'word-cloud.png\'.')

# plt.figure(figsize=[19,9], tight_layout=True, frameon=False)
# plt.imshow(wordCloud, interpolation='bilinear')
# plt.axis('off')
# plt.show()