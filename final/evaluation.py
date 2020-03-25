import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
from myStrategy import myStrategy

alldailyOhlcv = pd.read_csv(sys.argv[1]) #2202
minutelyOhlcv = pd.read_csv(sys.argv[2])
win = 0
winScore = 0
lose = 0
loseScore = 0
draw = 0
sumRate = []
for i in range(200, 2203, 14):
    dailyOhlcv = alldailyOhlcv[0:i]
    capital = 500000.0
    capitalOrig=capital
    transFee = 100
    evalDays = 14
    action = np.zeros((evalDays,1))
    realAction = np.zeros((evalDays,1))
    total = np.zeros((evalDays,1))
    total[0] = capital
    Holding = 0.0
    openPricev = dailyOhlcv["open"].tail(evalDays).values
    clearPrice = dailyOhlcv.iloc[-3]["close"]
    for ic in range(evalDays,0,-1):
        dailyOhlcvFile = dailyOhlcv.head(len(dailyOhlcv)-ic)
        #dateStr = dailyOhlcvFile.iloc[-1,0]
        #minutelyOhlcvFile = minutelyOhlcv.head((np.where(minutelyOhlcv.iloc[:,0].str.split(expand=True)[0].values==dateStr))[0].max()+1)
        action[evalDays-ic] = myStrategy(dailyOhlcvFile,dailyOhlcvFile,openPricev[evalDays-ic])
        currPrice = openPricev[evalDays-ic]
        if action[evalDays-ic] == 1:
            if Holding == 0 and capital > transFee:
                Holding = (capital-transFee)/currPrice
                capital = 0
                realAction[evalDays-ic] = 1
        elif action[evalDays-ic] == -1:
            if Holding > 0 and Holding*currPrice > transFee:
                capital = Holding*currPrice - transFee
                Holding = 0
                realAction[evalDays-ic] = -1
        elif action[evalDays-ic] == 0:
            realAction[evalDays-ic] = 0
        else:
            assert False
        if ic == 3 and Holding > 0: #遇到每個月的第三個禮拜三要平倉，請根據data的日期自行修改
            capital = Holding*clearPrice - transFee
            Holding = 0

        total[evalDays-ic] = capital + float(Holding>0) * (Holding*currPrice-transFee)

    returnRate = (total[-1] - capitalOrig)/capitalOrig*10000
    # print(10000*returnRate)
    sumRate.append(returnRate[0])
    if(returnRate>0):
        win+=1
        winScore+=returnRate
    elif(returnRate<0):
        lose+=1
        loseScore+=returnRate
    else:
        draw+=1
print(sumRate[:])
weight = [i for i in range(1, len(sumRate)+1)]
print("\n## Upload Score: ", returnRate)
print("Win: ", win, winScore/win, "  ")
print("Lose: ", lose, loseScore/lose, "  ")
print("Draw: ", draw, "  ")
print("Return: ", sum(sumRate)/len(sumRate), "  ")
print("Weight Return: ", sum(np.multiply(sumRate, weight))/sum(weight), "  \n")