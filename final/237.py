def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, currentPrice):
    import numpy as np
    # Using short RSI and long RSI to decide action
    # If short RSI>param[1] -> sell
    # If short RSI<param[2] -> buy
    # Else if short RSI > long RSI -> buy
    # Else if short RSI < long RSI -> sell
 
    pastPriceVec = dailyOhlcvFile['close']
    pastPriceVec = np.array(pastPriceVec)
 
    import numpy as np
    action=0        # actions=1(buy), -1(sell), 0(hold), with 0 as the default actions
 
    param=[5, 120, 30, 70]
    windowSize = param[0]
 
    dataLen=len(pastPriceVec)        # Length of the data vector
    if dataLen<=param[0]:
        return action
    longrsi=None
 
 
    U = pastPriceVec[-windowSize:] - pastPriceVec[-windowSize-1:-1]  # Up
    D = -U  # Down
    for i in range(0, windowSize):
        if U[i] < 0:
            U[i] = 0
        else:
            D[i] = 0
    sumU = np.sum(U)
    sumD = np.sum(D)
    rsi = (sumU/(sumU+sumD))*100
 
    U=[]
    D=[]
    if(param[3]<len(pastPriceVec)):
        U = pastPriceVec[-param[3]:] - pastPriceVec[-param[3]-1:-1]  # Up
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
 
 
    if(rsi>param[1]):
        action=-1
    elif(rsi<param[2]):
        action=1
    elif(longrsi):
        if(rsi>longrsi):
            action=1
        elif(rsi<longrsi):
            action=-1
    return action