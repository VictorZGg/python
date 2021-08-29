# -*- coding: utf-8 -*-
"""
Created on Thu Jun 10 10:56:39 2021

@author: zengg
"""


from math import log
import operator


################## 获取信息熵###############
def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def createDataSet():
    dataSet = [[1,1,'yes'],
               [1,1,'yes'],
               [1,0,'no'],
               [0,1,'no'],
               [0,1,'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

myDat, labels = createDataSet()
# dataSet = myDat
calcShannonEnt(myDat)

myDat[0][-1] = 'maybe'
calcShannonEnt(myDat)

############# 划分数据集 #############

def splitDataSet(dataSet, axis, value):# 待划分数据集，划分数据集特征，需返回特征值
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            # 保留除对比特征以外的其他特征
            retDataSet.append(reducedFeatVec)
    return retDataSet

splitDataSet(myDat, 0, 1)
splitDataSet(myDat, 0, 0)
# axis = 0
# value = 1

########### 选择最好的数据集划分方式 #############

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0])-1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
            print ('信息增益更新至：'+ str(infoGain))
            print ('当前最佳特征：第%s个'%str(i))
    return bestFeature # 第n个是最适合用于划分数据集的特征
        
chooseBestFeatureToSplit(myDat)
# 最适合划分的特征：放在第一个组


############# 创建决策树 ##############

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys(): classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), \
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
    
def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet\
        (dataSet, bestFeat, value), subLabels)
    return myTree

# dataSet = myDat
myTree = createTree(myDat, labels)

############ 画图 ##################

import machinelearning.treePlotter
machinelearning.treePlotter.createPlot()





