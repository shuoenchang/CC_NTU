#!/usr/bin/env python
# coding: utf-8
 
# In[ ]:
 
 
encoding="big5"
import sys
import csv
 
 
# In[ ]:
 
 
#filename = "Daily_2018_08_20.csv"
filename = sys.argv[1]
price=[]
month = None
with open(filename, encoding="big5") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row[1].find("TX")==0:
            if((int(row[3])>=84500) & (int(row[3])<=134500)):
                if((not month) | (month==row[2])):
                    month = row[2]
                    price.append(row[4])
        del row
print(int(price[0]), int(max(price)), int(min(price)), int(price[-1]))