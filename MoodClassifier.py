from 472groupproject import getData, oneHotEncode, MLPClassifier
import numpy as np
class SongMoodClassifier:

    def __init__(self):
        pass
    
    def getModels(self):
        moods = ['chill', 'energetic']
        features =  ['loudness', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']
        data, targets = getData(moods, features)
        dataMLP = np.array(data).astype(np.float64)
        targetsMLP = np.array(oneHotEncode(targets)).astype(np.int)
        chillEnergetic = MLPClassifier(momentum=0.45, early_stopping=False, learning_rate_init=0.03, hidden_layer_sizes=(80, 80, 80, 80))
        print(chillEnergetic.fit(dataMLP, targetsMLP).score(dataMLP, targetsMLP))

        data, targets = getData(['happy', 'sad'], features)
        dataMLP = np.array(data).astype(np.float64)
        targetsMLP = np.array(oneHotEncode(targets)).astype(np.int)
        happySad = MLPClassifier(momentum=0.45, early_stopping=False, learning_rate_init=0.03, hidden_layer_sizes=(80, 80, 80, 80))
        print(happySad.fit(dataMLP, targetsMLP).score(dataMLP, targetsMLP))