def myStrategy(pastData, currPrice, stockType):
   import numpy as np
   import talib as ta

   action=0
   dataLen=len(pastData)
   if dataLen==0:
       return action
   if(stockType=='LQD'):
       param=[28, 76, 29]
   elif(stockType=='SPY'):
       param=[21, 82, 26]
   elif(stockType=='DSI'):
       param=[3, 78, 15]
   elif(stockType=='IAU'):
       param=[6, 92, 24]
   rsi = ta.RSI(pastData, param[0])

   if(rsi[-1]>param[1]):
       action=-1
   elif(rsi[-1]<param[2]):
       action=1
   return action
