#!/usr/bin/env python3
# Copyright 2022 Ali Raheem
# MIT License
import pandas
from PIL import Image, ImageDraw, ImageFont

filename = "blue.csv"

nodeSize = (200, 64)
lineColour = (249,143,33)
finalLineColour =  (215,25,25)
backgroundColour =  (205,214,220)
textColour = (0, 0, 0)
cardFont = ImageFont.truetype("./CARDS.TTF", 48) # https://freefontsdownload.net/free-playing_cards-font-16939.htm
cards = pandas.read_csv(filename)
textFont = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf", 28) # Change this for a suitable system font

#for col in cards: # This should be equal for every row.
numCards = len(pandas.unique(cards['1']))

numShuffles = len(cards.columns)
plot = Image.new('RGB', (numShuffles * nodeSize[0], numCards * nodeSize[1]), backgroundColour)
draw = ImageDraw.Draw(plot)

nodes = []
i = 0
startingOrder = list(cards['1'])
cardNames = "mlkjihgfedcbaZYXWVUTSRQPONzyxwvutsrqponMLKJIHGFEDCBA" # Order this to suit the cardFont
for card in startingOrder:
    x = nodeSize[0]/2
    y = nodeSize[1]/2 + (i * nodeSize[1])
    cardColour = (255, 0, 0) if (card[0] == 'H' or card[0] == 'D') else (0, 0, 0)
    draw.text((x/4, y - nodeSize[1]/2 + 2), cardNames[i], fill=cardColour, font=cardFont)
    nodes.append((x, y))
    i += 1
    cards.replace(card, i, inplace=True)

startPos = nodes.copy()

x = nodeSize[0]/2 + nodeSize[0]
for deck in cards.iloc[:, 1:]:
    draw.text((x-nodeSize[0]/8, 0), str(int(deck) - 1), fill=textColour, font=textFont)
    y = nodeSize[1]/2
    for card in cards[deck]:
        card = int(card)
        lastPosX, lastPosY = nodes[card - 1]
        curPos = (x, y)
        draw.line([nodes[card - 1], curPos], fill=lineColour, width = 5);
        nodes[card - 1] = curPos
        y += nodeSize[1]
    x += nodeSize[0]

i = 0
for finalPos in nodes:
    draw.line([startPos[i], finalPos], fill=finalLineColour, width = 5)
    x, y = finalPos
    y -= nodeSize[1]/2
    cardColour = (255, 0, 0) if (startingOrder[i][0] == 'H' or startingOrder[i][0] == 'D') else (0, 0, 0)
    draw.text((x + nodeSize[0]/8, y + 2), cardNames[i], fill=cardColour, font=cardFont)
    i += 1

plot.save('shuffles.png', quality=95)

