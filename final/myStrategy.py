def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, currentPrice):
    import numpy as np
    import talib
 
    pastPriceVec = (dailyOhlcvFile['open']+dailyOhlcvFile['close'])/2
    pastPriceVec = np.array(pastPriceVec)
 
    action=0        # actions=1(buy), -1(sell), 0(hold), with 0 as the default actions
 
    param=[5, 20, 30, 85, 100]
    shortWindow = param[0]
    longWindow = param[1]
    rsiAlpha = param[2]
    rsiBeta = param[3]
    maAlpha = param[4]

    collectMA = []
    for window in range(5, 201, 5):
        collectMA.append(talib.EMA(pastPriceVec, window)[-1])
    shortMA = talib.MA(pastPriceVec, shortWindow)[-1]
    longMA = talib.MA(pastPriceVec, longWindow)[-1]
 
    dataLen=len(pastPriceVec)        # Length of the data vector
    if dataLen<=param[0]:
        return action
    longrsi=None
 
 
    U = pastPriceVec[-shortWindow:] - pastPriceVec[-shortWindow-1:-1]  # Up
    D = -U  # Down
    for i in range(0, shortWindow):
        if U[i] < 0:
            U[i] = 0
        else:
            D[i] = 0
    sumU = np.sum(U)
    sumD = np.sum(D)
    rsi = (sumU/(sumU+sumD))*100
 
    U=[]
    D=[]
    if(longWindow<len(pastPriceVec)):
        U = pastPriceVec[-longWindow:] - pastPriceVec[-longWindow-1:-1]  # Up
        D = -U  # Down
    else:
        U = pastPriceVec[1:len(pastPriceVec)] - pastPriceVec[0:len(pastPriceVec)-1]  # Up
        D = -U
 
    for i in range(0, len(U)):
        if U[i] < 0:
            U[i] = 0
        else:
            D[i] = 0
    sumU = np.sum(U)
    sumD = np.sum(D)
    longrsi = (sumU/(sumU+sumD))*100

    voteBuy = 0
    voteSale = 0


    for i in range(len(collectMA)):
        if(currentPrice >= collectMA[i]):
            voteBuy += 1
        elif(currentPrice < collectMA[i]):
            voteSale += 1
    
    print(rsi, longrsi)
    if(rsi<rsiAlpha):
        action = 1
    elif(rsi>rsiBeta):
        action = -1
    elif(longrsi):
        if(rsi>longrsi and (voteSale<voteBuy or currentPrice-longMA<-maAlpha)):
            action=1
        elif(rsi<longrsi and (voteSale>voteBuy or currentPrice-longMA>maAlpha)):
            action=-1
    return action