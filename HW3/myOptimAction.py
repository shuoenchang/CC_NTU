'''
using DP to solve the question
'''

import numpy as np

def myOptimAction(priceMat, transFeeRate):

    cash = 1000
    hold = 0
    # user definition
    nextDay = 1
    dataLen, stockCount = priceMat.shape  # day size & stock count   
    stockHolding = [[],[],[],[]]  # Mat of stock holdings
    actionMat = []  # An k-by-4 action matrix which holds k transaction records.
    moneyHolding = []
    for stock in range(stockCount):
        stockHolding[stock].append([cash*(1-transFeeRate)/priceMat[0][stock], stock])
    moneyHolding.append([cash, -1])

    for day in range(1, dataLen-1) :
        dayPrices = priceMat[day]  # Today price of each stock
        
        # find if sell or not
        maxMoney = moneyHolding[day-1][0]
        sellFrom = -1
        for stock in range(stockCount):
            if maxMoney < stockHolding[stock][day-1][0] * dayPrices[stock] * (1-transFeeRate):
                maxMoney = stockHolding[stock][day-1][0] * dayPrices[stock] * (1-transFeeRate)
                sellFrom = stock
        moneyHolding.append([maxMoney, sellFrom])

        # find if buy or not
        for stock in range(stockCount):
            maxAmount = stockHolding[stock][day-1][0]
            buyFrom = stock
            for cmp_stock in range(stockCount):
                tempMoney = stockHolding[cmp_stock][day-1][0] * dayPrices[cmp_stock] * (1-transFeeRate)
                newAmount = tempMoney*(1-transFeeRate)/dayPrices[stock]
                if maxAmount < newAmount:
                    buyFrom = cmp_stock
                    maxAmount = newAmount
            if maxAmount < moneyHolding[day-1][0]*(1-transFeeRate)/dayPrices[stock]:
                buyFrom = -1
                maxAmount = moneyHolding[day-1][0]*(1-transFeeRate)/dayPrices[stock]
            stockHolding[stock].append([maxAmount, buyFrom]) 
     
    # Must sell at last day
    dayPrices = priceMat[dataLen-1]
    maxMoney = moneyHolding[dataLen-2][0]
    sellFrom = -1
    for stock in range(stockCount):
        if maxMoney < stockHolding[stock][day-1][0] * dayPrices[stock] *(1-transFeeRate):
            maxMoney = stockHolding[stock][day-1][0] * dayPrices[stock] *(1-transFeeRate)
            sellFrom = stock
        moneyHolding.append([maxMoney, sellFrom])
        stockHolding[stock].append([0, stock])
            
    states = np.zeros(dataLen, dtype=int)
    states[-1] = -1 # set as sell as the end
    for day in range(dataLen-1, 0, -1):
        stateNow = states[day]
        if stateNow < 0:
            states[day-1] = moneyHolding[day][1]
        else:
            states[day-1] = stockHolding[stateNow][day][1]
        
    # for i in range(dataLen):
    #     print(states[i], end=',')
    
    if states[0] != -1:
        actionMat.append([0, -1, states[0], cash])
    for day in range(1, dataLen):
        if states[day-1] == -1 and states[day] != -1: # buy from cash
            actionMat.append([day, states[day-1], states[day], moneyHolding[day-1][0]])
        elif states[day-1] != states[day]: # buy from other or sell to cash
            stock = states[day-1]
            actionMat.append([day, states[day-1], states[day], stockHolding[stock][day-1][0]*priceMat[day][stock]])
    #print(actionMat)

    return actionMat

    