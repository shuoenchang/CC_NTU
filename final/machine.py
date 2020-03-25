def myStrategy(dailyOhlcvFile, minutelyOhlcvFile, currentPrice):
    import numpy as np
    from sklearn.svm import SVR
    from sklearn.linear_model import LinearRegression, SGDRegressor
    from sklearn.preprocessing import PolynomialFeatures, StandardScaler
    from xgboost import XGBClassifier
 
    pastPriceVec = dailyOhlcvFile['close']
    pastPriceVec = np.array(pastPriceVec)
 
    action=0        # actions=1(buy), -1(sell), 0(hold), with 0 as the default actions
 
 
 
 
    lin_regressor = SGDRegressor(max_iter=50000)
    poly = PolynomialFeatures(5)
    OhlcvFile = np.array(dailyOhlcvFile)
    startTrain=len(OhlcvFile)//2
    x_train = OhlcvFile[-startTrain:-1, 1:]
    x_train_open = OhlcvFile[-startTrain+1:, 1]
    x_train_open = x_train_open.reshape(-1,1)
    x_train = np.append(x_train, x_train_open, axis=1)
 
    ss_x = StandardScaler()

    x_transform = poly.fit_transform(x_train)
    x_transform = ss_x.fit_transform(x_transform)
    
    # x = x.reshape(-1,1)
    y_train = []
    for i in range(-startTrain+1, 0):
        if OhlcvFile[i, 4]-OhlcvFile[i, 1]>2:
            y_train.append(1)
        else:
            y_train.append(0)
    # y_train = OhlcvFile[-startTrain+1:, 4]
    xgbc = XGBClassifier()
    xgbc.fit(x_train,y_train)

    x_test = OhlcvFile[-1,1:]
    x_test = np.append(x_test, currentPrice)
    x_test = x_test.reshape(1,-1)
    x_test_transform = poly.fit_transform(x_test)
    x_test_transform = ss_x.transform(x_test_transform)
    y_preds = xgbc.predict(x_test)
    print(currentPrice, x_test, y_preds, currentPrice-y_preds)
 
    # clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    # clf.fit(x, y)
    
    if y_preds==1:
        action = 1
    elif y_preds==0:
        action = -1
 
    return action