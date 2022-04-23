#!/usr/bin/env python3
# Copyright 2022 Ali Raheem
# MIT License

import pandas

filename = "blue.csv"
outputFilename = "blue_deltas.csv"

data = pandas.read_csv(filename)

deltas = pandas.DataFrame()

col = data['1']
for colName in data.iloc[:, 1:]:
    deltasTemp = []
    i = 0
    for card in data[colName]:
        ii = data[colName][col == card].index[0]
        deltasTemp.append(ii - i)
        i += 1
    deltas[int(colName) - 1] = deltasTemp

deltas.to_csv(outputFilename)
