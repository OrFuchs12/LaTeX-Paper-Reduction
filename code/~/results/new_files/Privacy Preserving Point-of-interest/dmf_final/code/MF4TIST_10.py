import random
import numpy as np
import math
import time
import utils


def predictRating(pu, qi, data):
    predictedRating = np.dot(pu, qi)
    if data == 1:
        maxR = 1
        minR = 0
    else:
        maxR = 5
        minR = 1
    if predictedRating > maxR:
        predictedRating = maxR
    elif predictedRating < minR:
        predictedRating = minR
    return predictedRating


def computeError(realRating, predictedRating):
    return realRating - predictedRating


def computeRMSE(dataset, userVectors, itemVectors, data):
    rmse = 0
    rmseOld = 0
    oldCount = 0
    rmseNew = 0
    newCount = 0
    count = 0
    for row in dataset:
        userID = int(row['userID'])
        itemID = int(row['itemID'])
        rating = float(row['rating'])
        # Since list index in python starts from 0 and user ID
        # in MovieLens dataset start from 1, all IDs should minus one.
        userVector = userVectors[userID - 1]
        itemVector = itemVectors[itemID - 1]
        predictedRating = predictRating(userVector, itemVector, data)
        error = computeError(rating, predictedRating)
        temp = error ** 2
        rmse += temp
        count += 1
    rmse /= count  # len(dataset)
    rmse = math.sqrt(rmse)
    return rmse, rmseNew, rmseOld, count, newCount, oldCount


def initFactorVectors(rows, columns):
    return np.random.randn(rows, columns) / math.sqrt(columns)

def initBiases(number):
    return [0] * number

# compute P@5, R@5, P@10, R@10
def computePrecision(test4Rank, userVectors, itemVectors, itemNum, data):
    precision5 = 0.0
    precision10 = 0.0
    recall5 = 0.0
    recall10 = 0.0

    rightUserNum = 0
    for userID in test4Rank:

        ratings = {}

        # predict all the ratings for userID
        for itemID in range(itemNum):
            userVector = userVectors[userID - 1]
            itemVector = itemVectors[itemID - 1]
            predictedRating = predictRating(userVector, itemVector, data)
            ratings[itemID] = predictedRating

        # rank items based on ratings, desc
        sortedRating = sorted(ratings, key=lambda k: ratings[k], reverse=True)

        items4Rank = test4Rank[userID]
        hit = 0
        index = 0
        for item_predict in sortedRating:
            for iRating_true in items4Rank:
                item = iRating_true.split(',')[0]
                if int(item) == int(item_predict):
                    hit += 1
                    break
            index += 1
            if index == 5:
                break

        precision5 += float(hit) / 5.0
        recall5 += float(hit) / float(len(items4Rank))

        hit = 0
        index = 0
        for item_predict in sortedRating:
            for iRating_true in items4Rank:
                item = iRating_true.split(',')[0]
                if int(item) == int(item_predict):
                    hit += 1
                    break
            index += 1
            if index == 10:
                break

        precision10 += float(hit) / 10.0
        recall10 += float(hit) / float(len(items4Rank))

    precision5 /= len(test4Rank)
    precision10 /= len(test4Rank)
    recall5 /= len(test4Rank)
    recall10 /= len(test4Rank)
    return precision5, recall5, precision10, recall10

def train(userNum, itemNum, featureK, trainSet, testSet, trainRank, testRank, epochs, LambdaU, LambdaV, alpha, lrDecay, filePrefix, isSave, data, negativeNum, log):

    userVectors = initFactorVectors(userNum, featureK)
    itemVectors = initFactorVectors(itemNum, featureK)

    finalEpoch = epochs

    lastRMSE = 1000
    totalStart = time.time()
    for epoch in range(finalEpoch):
        random.shuffle(trainSet)
        start = time.time()
        for row in trainSet:
            userID = int(row['userID'])
            itemID = int(row['itemID'])
            rating = float(row['rating'])

            # Since list index in python starts from 0 and user ID
            # in MovieLens dataset start from 1, all IDs should minus one.
            userVector = userVectors[userID - 1]
            itemVector = itemVectors[itemID - 1]
            predictedRating = predictRating(userVector, itemVector, data)
            # print predictedRating, rating
            error = computeError(rating, predictedRating)
            #            print usersBias[userID - 1],itemsBias[itemID - 1]
            temp = userVector.copy()
            userVector += alpha * (error * itemVector - LambdaU * userVector)
            itemVector += alpha * (error * temp - LambdaV * itemVector)

            # negative sample #m items, and take their weight as 1/m
            negativeItems = []
            cnt = 0
            while True:
                item = random.randint(1, itemNum)
                if item not in negativeItems and item != itemID:
                    negativeItems.append(item)
                    cnt += 1
                if cnt == negativeNum:
                    break

            # update negative model
            for itemID in negativeItems:
                rating = 0.0
                userVector = userVectors[userID - 1]
                itemVector = itemVectors[itemID - 1]
                predictedRating = predictRating(userVector, itemVector, data)
                error = computeError(rating, predictedRating)
                temp = userVector.copy()
                userVector += alpha * (error / negativeNum * itemVector - LambdaU * userVector)
                itemVector += alpha * (error / negativeNum * temp - LambdaV * itemVector)


        # print usersBias
#        trainRMSE, rmseNew, rmseOld, count, newCount, oldCount = computeRMSE(trainSet, userVectors, itemVectors, data)
        testRMSE, testRmseNew, testRmseOld, count, newCount, oldCount = computeRMSE(testSet, userVectors, itemVectors, data)
        end = time.time()

        if epoch % 5 == 0:
            p5, r5, p10, r10 = computePrecision(testRank, userVectors, itemVectors, itemNum, data)
            end = time.time()
            print epoch, testRMSE, p5, r5, p10, r10, end - start
            log.write(str(epoch) + ',' + str(testRMSE) + ',' + str(p5) + ',' + str(
                r5) + ',' + str(p10) + ',' + str(r10) + ',' + str(end - start) + '\n')
        else:
            print epoch, testRMSE, end - start
            log.write(str(epoch) + ',' + str(testRMSE) + ',' + str(end - start) + '\n')

        log.flush()
        # if lastRMSE < testRMSE or lastRMSE - testRMSE < 0.00001:
        #    break
        if lastRMSE > testRMSE:
            lastRMSE = testRMSE
            # else:
            #    break

        # deday learning rate
        if epoch % 10 == 0:
            alpha = alpha * lrDecay

    totalEnd = time.time()
    print 'RMSE of MF for testing set:', testRMSE
    print 'time cost: ', totalEnd - totalStart
    if isSave:
        folder = str(LambdaU) + '_' + str(LambdaV)
        import os
        savePre = filePrefix + folder + '/'
        print 'save data in', savePre
        savePre += 'MF_'
        if not os.path.exists(savePre):
            os.makedirs(savePre)
        print 'save params...'
        utils.saveNumpyMatrix(savePre + 'usersVector.npy', userVectors)
        utils.saveNumpyMatrix(savePre + 'itemsVector.npy', itemVectors)
        print 'params saved'

    return testRMSE

def readFile(path):
    uiratings = []
    with open(path) as fd:
        for line in fd:
            rec = line.strip().split(',')
            uiratings.append({'userID': rec[0], 'itemID': rec[1], 'rating': 1})
    return uiratings

def readFile4Rank(path):
    uiRatings = {}
    with open(path) as fd:
        for line in fd:
            rec = line.strip().split(',')
            user = int(rec[0])
            item = int(rec[1])
            rating = int(rec[3])
            if not uiRatings.has_key(user):
                uiRatings[user] = []
            uiRatings[user].append(str(item) + ',' + str(rating))
    return uiRatings

def generateUsers2Rank(userNum, userNum2Rank):
    users = []
    cnt = 0
    while True:
        user = random.randint(1, userNum)
        if user not in users:
            users.append(user)
            cnt += 1
        if cnt == userNum2Rank:
            break
    return users

def readFile4RankRandom(path, users2Rank):
    uiRatings = {}
    with open(path) as fd:
        for line in fd:
            rec = line.strip().split(',')
            user = int(rec[0])
            item = int(rec[1])
            rating = 1
            if user in users2Rank:
                if not uiRatings.has_key(user):
                    uiRatings[user] = []
                uiRatings[user].append(str(item) + ',' + str(rating))
    return uiRatings

def main():
    filePrefix = '/home/chaochao.ccc/work/mf_exp/data/tist/v9/'

    trainSet = readFile(filePrefix + 't_ccc_dmf_tist_train_data5.txt')
    testSet = readFile(filePrefix + 't_ccc_dmf_tist_test_data5.txt')

    userNum = 6524 
    itemNum = 3197
    featureK = 10 
    epochs = 200
    LambdaU = 0.1
    LambdaV = 0.1
    alpha = 0.1
    lrDecay = 1 
    isSave = False
    data = 1  # max rating is 1
    userNum2Rank = 500
    negativeNum = 3

    users2Rank = generateUsers2Rank(userNum, userNum2Rank)

    trainRank = readFile4RankRandom(filePrefix + 't_ccc_dmf_tist_train_data5.txt', users2Rank)
    testRank = readFile4RankRandom(filePrefix + 't_ccc_dmf_tist_test_data5.txt', users2Rank)

    output = filePrefix + 'mf-tist-lambda-' + str(LambdaU) + '-k-' + str(featureK) + '.txt'
    log = open(output, 'w')

    print 'epoch, testRMSE, p5, r5, p10, r10, time per iter'
    log.write('epoch, testRMSE, p5, r5, p10, r10, time per iter\n')

    train(userNum, itemNum, featureK, trainSet, testSet, trainRank, testRank, epochs, LambdaU, LambdaV, alpha, lrDecay, filePrefix, isSave, data, negativeNum, log)
    log.close

if __name__ == '__main__':
    main()
