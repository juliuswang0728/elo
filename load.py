import json
import pickle
import collections

with open('train_eu.pickle', 'rb') as fp:
    headlines = pickle.load(fp)
    #json_string = json.load(fp)

i = 0
#print(len(headlines))
#exit()
for headline in headlines:
    print(headline)

