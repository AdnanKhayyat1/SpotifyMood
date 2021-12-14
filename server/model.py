# -*- coding: utf-8 -*-
"""472GroupProject.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1teBP343Sd0RNiyWN6NzDsXz4bwOcUq8N

# Song Mood Group Project
"""

import random
import sys
import os
from scipy.io import arff
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import AgglomerativeClustering
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import json
from statistics import mean
from sklearn.utils import shuffle
from sklearn.model_selection import ShuffleSplit
from joblib import dump, load
import requests
import wget

from constants import CLIENT_ID, CLIENT_SECRET

"""## Data Import"""

# All Moods: ['happy', 'sad', 'energetic', 'chill', 'romantic']
# All Features: ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']

def getData(moods, features):
    if not os.path.exists('./song_mood_data.json'):
        wget.download('https://raw.githubusercontent.com/landiinii/SongMoodML-472/main/song_mood_data.json', out='./song_mood_data.json') 
    dataset = json.load(open('./song_mood_data.json'))
    data = []
    targets = []
    for dataPoint in dataset:
        point = []
        if dataPoint['mood'] in moods:
          targets.append(dataPoint['mood'])
          del dataPoint['mood']
          for att in sorted(set(features)):
              point.append(dataPoint[att])
          data.append(point)
    return np.array(data).astype(np.float64), targets


def splitTrainTest(X, y, percent=0.85):
    data, targets = shuffle(X, y)
    trainingInputs = X[:round(len(X) * percent)]
    trainingTargets = y[:round(len(y) * percent)]
    testInputs = X[round(len(X) * percent):]
    testTarget = y[round(len(y) * percent):]
    return trainingInputs, trainingTargets, testInputs, testTarget


def oneHotEncode(targets):
    targetsMLP = []
    labelsList = list(sorted(set(targets)))
    for item in targets:
      temp = [0]*len(labelsList)
      temp[labelsList.index(item)] = 1
      targetsMLP.append(temp)
    targetsMLP = np.array(targetsMLP).reshape(-1, len(labelsList))
    return targetsMLP


def normalize(data):
      maxes = []
      mins = []
      for i in range(len(data[0])):
          maxes.append(max(data[:, i:i + 1].flatten()))
          mins.append(min(data[:, i:i + 1].flatten()))
      for row in data:
          for i in range(len(row)):
              row[i] = (row[i]-mins[i])/(maxes[i]-mins[i])
      return data, maxes, mins


def crossValidation(data, targets, k, model):
    data, targets = shuffle(data, targets)
    inputs = len(data[0])
    outputs = len(targets[0])
    splits = {}
    numb = round(len(data) / k)
    accuracies = {}
    totalTrain = 0
    totalTest = 0
    for i in range(k):
        trainData = np.concatenate((data[:i * numb, :], data[(i + 1) * numb:, :]), axis=0).reshape(-1, inputs)
        trainTargets = np.concatenate((targets[:i * numb], targets[(i + 1) * numb:]), axis=None).reshape(-1, outputs)
        testData = data[i * numb:(i + 1) * numb, :].reshape(-1, inputs)
        testTargets = targets[i * numb:(i + 1) * numb].reshape(-1, outputs)


        model.fit(trainData, trainTargets)
        trainedAcc = model.score(trainData, trainTargets)
        testedAcc = model.score(testData, testTargets)
        accuracies["Group " + str(1 + i)] = {
            'Train': trainedAcc,
            'Test': testedAcc,
        }
        totalTrain += trainedAcc
        totalTest += testedAcc

    accuracies['Averages'] = {
        'Train': totalTrain / k,
        'Test': totalTest / k
    }

    return accuracies




def mlpModel(dataset, targetset):
    songMoods = MLPClassifier(momentum=0.45, early_stopping=False, learning_rate_init=0.03, hidden_layer_sizes=(80, 80, 80, 80))
    accuracies = crossValidation(dataset, targetset, 5, songMoods)
    # Print Accuracy
    df = pd.DataFrame.from_dict(data=accuracies, orient='index')
    fig, ax = plt.subplots()
    fig.patch.set_visible(False)
    fig.set_size_inches(20, 3)
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, rowLabels = df.index, loc='center')
    plt.title("MLP Final Accuracies Happy v Sad")
    plt.show()

    return accuracies['Averages']['Test']



"""## KNN: Classifier"""

def knnModel(knnData, knnTargets, ike):

    skWeighted = KNeighborsClassifier(n_neighbors=9, weights='distance')
    skNoWeights = KNeighborsClassifier(n_neighbors=9, weights='uniform')
    accuraciesWeighted = crossValidation(knnData, knnTargets, 5, skWeighted)
    accuraciesNoWeights = crossValidation(knnData, knnTargets, 5, skNoWeights)

    # return max(accuraciesWeighted['Averages']['Test'], accuraciesNoWeights['Averages']['Test'])
    # return accuraciesWeighted['Averages']['Test'], accuraciesNoWeights['Averages']['Test']
    return accuraciesNoWeights

# data, targets = getData(['happy', 'sad', 'energetic', 'chill', 'romantic'], ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence'])


def ikeTest():
    weightedAccuracies = []
    unweightedAccuracies = []
    for ike in k_values:
      sys.stdout.write('\r')
      sys.stdout.write(str(ike))
      sys.stdout.flush()
      w, n = knnModel(knnData, knnTargets, ike)
      weightedAccuracies.append(w)
      unweightedAccuracies.append(n)
    return np.array(weightedAccuracies), np.array(unweightedAccuracies)


"""# Feature Selection"""

def findFeats(moods):
    MLPFeatures = ['loudness', 'danceability', 'acousticness', 'duration_ms', 'energy', 'instrumentalness', 'key',
               'liveness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
    KNNFeatures = ['loudness', 'danceability', 'acousticness', 'duration_ms', 'energy', 'instrumentalness', 'key',
               'liveness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']
    selectedMoods = moods
    MLPselectedFeats = []
    KNNselectedFeats = []
    accuraciesMLP = []
    accuraciesKNN = []
    while True:
        bestMLPAcc = 0.0
        bestMLPFeat = "No More"
        index = 1
        for f in MLPFeatures:
            MLPselectedFeats.append(f)
            data, targets = getData(selectedMoods, MLPselectedFeats)
            MLPselectedFeats.pop()
            acc = mlpModel(np.array(data).astype(np.float64), np.array(oneHotEncode(targets[:])).astype(int),0.5,0.01)
            if acc > bestMLPAcc:
                bestMLPAcc = acc
                bestMLPFeat = f
            maxPercent = index / len(MLPFeatures)
            index += 1
            i = round(maxPercent * 50)
            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %d%%" % ('=' * i, 2 * i))
            sys.stdout.flush()
        if bestMLPFeat == "No More":
            break
        accuraciesMLP.append(bestMLPAcc)
        MLPselectedFeats.append(bestMLPFeat)
        MLPFeatures.remove(bestMLPFeat)
        print(" -- ", MLPselectedFeats, " = ", bestMLPAcc)

    while True:
        bestKNNAcc = 0.0
        bestMLPFeat = "No More"
        index = 1
        for f in KNNFeatures:
            KNNselectedFeats.append(f)
            data, targets = getData(selectedMoods, KNNselectedFeats)
            KNNselectedFeats.pop()
            acc = knnModel(np.array(data).astype(np.float64), np.array(oneHotEncode(targets[:])).astype(int),9)
            if acc > bestKNNAcc:
                bestKNNAcc = acc
                bestMLPFeat = f
            maxPercent = index / len(KNNFeatures)
            index += 1
            i = round(maxPercent * 50)
            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %d%%" % ('=' * i, 2 * i))
            sys.stdout.flush()
        if bestMLPFeat == "No More":
            break
        accuraciesKNN.append(bestKNNAcc)
        KNNselectedFeats.append(bestMLPFeat)
        KNNFeatures.remove(bestMLPFeat)
        print(" -- ", KNNselectedFeats, " = ", bestKNNAcc)

    return accuraciesMLP, accuraciesKNN


# happy v sad = Duration, key, tempo, time signature
# ['loudness', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

"""# Graph Attributes"""

def graphAtts(moods=[], features=[]):
    # get and prep data
    features.sort()
    data, labels = getData(moods, features)
    data = normalize(data)
    x = np.asarray(data[:, :1])
    y = np.asarray(data[:, 1:2])
    labels = np.asarray(labels)

    # set style and limits, create plot and labels
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots(figsize=(8, 6))
    point_style = 'o'
    plt.ylabel(features[0])
    plt.xlabel(features[1])
    plt.title(features[0] + " + " + features[1] + ' (normalized)')
    plt.xlim(0, 1)
    plt.ylim(0, 1)

    # plot em
    plot_list = []
    for l in np.unique(labels):
        idx = np.where(labels == l)
        plot_list.append(ax.plot(x[idx[0]], y[idx[0]], point_style, label=str(l))[0])
    plt.legend()
    plt.show()

class Cache:
    def __init__(self):
        self.FEATURES =  ['loudness', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'speechiness', 'valence']

        self.hp_model = self.generate_models(['happy','sad'])
        self.ce_model = self.generate_models(['chill','energetic'])
    def generate_models(self,labels):
        data, targets = getData(labels, self.FEATURES)
        dataMLP = np.array(data).astype(np.float64)
        targetsMLP = np.array(oneHotEncode(targets)).astype(np.int)
        model = MLPClassifier(momentum=0.45, early_stopping=False, learning_rate_init=0.03, hidden_layer_sizes=(80, 80, 80, 80))

        score = model.fit(dataMLP, targetsMLP).score(dataMLP, targetsMLP)
        if labels[0] == 'happy':
            self.hp_score = score
        else:
            self.ce_score = score
        return model

    """# Server response generator"""
    def model_showcase(self,plist_id):
        mapper = {}

        auth_response = requests.post('https://accounts.spotify.com/api/token', {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        })
        print('MODEL SHOWCASE - ', plist_id)
        auth_response_data = auth_response.json()


        headers = {'Authorization': 'Bearer {token}'.format(token=auth_response_data['access_token'])}

        BASE_URL = 'https://api.spotify.com/v1/'

        r = requests.get(BASE_URL + 'playlists/' + plist_id, headers=headers)
        r = r.json()
        track_ids = ''
        pl_length = 100
        if len(r['tracks']['items']) < 100:
            pl_length = len(r['tracks']['items'])
        for i in range(pl_length):
            obj = r['tracks']['items'][i]
            if obj['track'] is not None:
                track_ids += obj['track']['id']
                track_ids += '%2C'
        track_ids = track_ids[:-3]
        r = requests.get(BASE_URL + 'audio-features/?ids=' + track_ids, headers=headers)
        r = r.json()['audio_features']
        for obj in r:
            del obj['id']
            del obj['type']
            del obj['uri']
            del obj['track_href']
            del obj['analysis_url']

        ceSum = np.zeros((1, 2))
        hsSum = np.zeros((1, 2))
        for item in r:
            test_point = []
            for att in sorted(set(self.FEATURES)):
                test_point.append(item[att])
            ceSum += self.ce_model.predict_proba(np.array(test_point).astype(np.float64).reshape(1, -1))
            hsSum += self.hp_model.predict_proba(np.array(test_point).astype(np.float64).reshape(1, -1))
        hs = np.round(100*np.round(hsSum, 0)/len(r))
        ce = np.round(100*np.round(ceSum, 0)/len(r))
        mapper[plist_id] = [hs[0][0], hs[0][1], ce[0][1], ce[0][0]]
        return mapper
    
    def wrapped_fetch(self,plist_id):
        try:
            return self.model_showcase(plist_id)
        except:
            return None