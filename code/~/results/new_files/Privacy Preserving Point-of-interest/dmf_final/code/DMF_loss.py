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

def initFactorVectors(rows, columns):
    return np.random.randn(rows, columns) / math.sqrt(columns)

def initBiases(number):
    return [0] * number

def initLatentVectors(rows, columns):
    return np.random.randn(rows, columns) / math.sqrt(columns)

def initItemVectors4Types(cityUsers, userNum, itemNum, featureK):
    itemVectors4Users = {}
    for city in cityUsers:
        users = cityUsers[city].split(';')
        tmp = np.random.randn(itemNum, featureK) / math.sqrt(featureK)
        for user in users:
            itemVectors4Users[int(user) - 1] = tmp
    return itemVectors4Users

def computeLoss(dataset, userVectors, itemVectors, itemVectors4Types, LambdaU, LambdaV, LambdaZ, itemNum):
    totalLoss = 0.0
    for row in dataset:
        userID = int(row['userID'])
        itemID = int(row['itemID'])
	rating = 1.0
	userVector = np.array(userVectors[userID - 1])
        itemComVector = np.array(itemVectors[itemID - 1])
	itemPerVector = itemVectors4Types[userID - 1][itemID - 1]
        curItemVector = itemComVector + itemPerVector
	predictedRating = predictRating(userVector, curItemVector, 1)
	error = computeError(rating, predictedRating)
	userReg = LambdaU * np.dot(userVector, userVector)
	itemComReg = LambdaV * np.dot(itemComVector, itemComVector)
	itemPerReg = 0.0
	for item in range(itemNum):
	    iv = np.array(itemVectors4Types[userID - 1][item])	
	    itemPerReg += LambdaZ * np.dot(iv, iv)
	totalLoss += 0.5 * error * error + 0.5 * userReg + 0.5 * itemComReg + 0.5 * itemPerReg
    return totalLoss


def train(userNum, itemNum, neighborNum, cityUsers, featureK, trainSet, testSet, testRank, epochs, LambdaU, LambdaV, LambdaZ, alpha, lrDecay, topK, filePrefix, isSave, data, negativeNum, log):

    userVectors = initLatentVectors(userNum, featureK)
    itemVectors = initLatentVectors(itemNum, featureK)
    itemVectors4Types = initItemVectors4Types(cityUsers, userNum, itemNum, featureK)

    finalEpoch = epochs

    lastRMSE = 1000
    totalStart = time.time()
    for epoch in range(finalEpoch):
        random.shuffle(trainSet)
        start = time.time()
        for row in trainSet:
            userID = int(row['userID'])
            itemID = int(row['itemID'])
	    city = row['city']
            rating = 1.0

            # Since list index in python starts from 0 and user ID
            # in MovieLens dataset start from 1, all IDs should minus one.
            userVector = userVectors[userID - 1]
            itemComVector = itemVectors[itemID - 1]

            # prepare for update latent factor for current user
            itemPerVector = itemVectors4Types[userID - 1][itemID - 1]
            curItemVector = itemComVector + itemPerVector
            predictedRating = predictRating(userVector, curItemVector, data)
            error = computeError(rating, predictedRating)

            # calculate the gradients of user and item
            deltaU = LambdaU * userVector - error * curItemVector
            deltaV = LambdaV * itemComVector - error * userVector
            deltaZ = LambdaZ *  itemPerVector- error * userVector

            # update the preferences of user
            userVector -= alpha * deltaU
            itemComVector -= alpha * deltaV
            itemPerVector -= alpha * deltaZ

            # randomly select k neighbor from the current city
	    curCityUsers = cityUsers[city].split(';')
	    if len(curCityUsers) < neighborNum:
		neighbors = random.sample(curCityUsers, len(curCityUsers))
	    else:
	        neighbors = random.sample(curCityUsers, neighborNum)
            for nb in neighbors:
                if int(nb) != userID:
                    NBitemVector = itemVectors4Types[int(nb) - 1][itemID - 1]
                    NBitemVector -= alpha * deltaV

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
                itemPerVector = itemVectors4Types[userID - 1][itemID - 1]
                curItemVector = itemComVector + itemPerVector
                predictedRating = predictRating(userVector, curItemVector, data)
                error = computeError(rating, predictedRating)
                deltaU = LambdaU * userVector - error / negativeNum * curItemVector
                deltaV = LambdaV * itemComVector - error * userVector
                deltaZ = LambdaZ *  itemPerVector- error * userVector

                userVector -= alpha * deltaU
                itemPerVector -= alpha * deltaZ
                itemComVector -= alpha * deltaV
                for nb in neighbors:
		    if int(nb) != userID:
                        NBitemVector = itemVectors4Types[int(nb) - 1][itemID - 1]
                        NBitemVector -= alpha * deltaV
	# compute loss
	# trainLoss = computeLoss(trainSet, userVectors, itemVectors, itemVectors4Types, LambdaU, LambdaV, itemNum)
        trainLoss = 0.0
	testLoss = computeLoss(testSet, userVectors, itemVectors, itemVectors4Types, LambdaU, LambdaV, LambdaZ, itemNum)

        end = time.time()

	print 'train loss: ' + str(trainLoss) + ' , testi loss: ' + str(testLoss) + ', ' + str(end - start)
        log.write('train loss: ' + str(trainLoss) + ' , testi loss: ' + str(testLoss) + ', ' + str(end - start) + '\n')
        log.flush()
        if epoch % 10 == 0:
            alpha = alpha * lrDecay

    totalEnd = time.time()
    print 'RMSE of MF for testing set:', testRMSE
    print 'time cost: ', totalEnd - totalStart

def readFile(path):
    uiratings = []
    with open(path) as fd:
        for line in fd:
            rec = line.strip().split(',')
            uiratings.append({'userID': rec[0], 'itemID': rec[1], 'city':rec[2], 'rating': 1})
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

def readCityUser(path):
    uiratings = {}
    with open(path) as fd:
        for line in fd:
            rec = line.strip().split(',')
            city = rec[0]
            users = rec[1]
            uiratings[city] = users
    return uiratings


def main():
    filePrefix = '/home/chaochao.ccc/work/mf_exp/data/kb/v9/'

    trainSet = readFile(filePrefix + 't_ccc_dmf_kb_train_data4.txt')
    testSet = readFile(filePrefix + 't_ccc_dmf_kb_test_data4.txt')

    cityUsers = readCityUser(filePrefix + 't_ccc_dmf_kb_city4.txt')

    userNum = 5996
    itemNum = 7404
    featureK = 10
    epochs = 200
    LambdaU = 0.1
    LambdaV = 0.1
    LambdaZ = 0.1
    alpha = 0.1
    lrDecay = 1
    isSave = False
    data = 1  # max rating is 1
    topK = 10
    userNum2Rank = 500
    negativeNum = 5
    neighborNum = 2

    users2Rank = generateUsers2Rank(userNum, userNum2Rank)

    testRank = readFile4RankRandom(filePrefix + 't_ccc_dmf_kb_test_data4.txt', users2Rank)

    output = filePrefix + 'dmf-kb-loss-n' + str(neighborNum) + '-lambda-' + str(LambdaU) + '-top-' + str(topK) +'-k-' + str(featureK) + '.txt'
    log = open(output, 'w')

    print 'epoch, trainRMSE, testRMSE, precision, recall, f1, time per iter'
    log.write('epoch, trainRMSE, testRMSE, precision, recall, f1, time per iter\n')
    train(userNum, itemNum, neighborNum, cityUsers, featureK, trainSet, testSet, testRank, epochs, LambdaU, LambdaV, LambdaZ, alpha, lrDecay, topK, filePrefix, isSave, data, negativeNum, log)
    log.close

if __name__ == '__main__':
    main()
