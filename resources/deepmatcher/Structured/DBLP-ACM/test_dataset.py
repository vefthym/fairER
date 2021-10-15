import pandas as pd
import os
import sys
import csv
import re
if __name__ == '__main__':    
    file1= open('tableB.csv', 'r')
    while True:
        line = file1.readline()
        if not line:
            break
        line = re.sub('".*?"','',line)
        if(line.count(',')!= 4):
            print('ERROR')
