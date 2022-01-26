#made to handle the csv file
#1. split classes AB and CD studnets
#2. add the new transfer students

from itertools import count
from operator import index
from statistics import variance
import pandas as pd
from csv import writer

def splitClasses():
    chuck_size = 48
    batch_no = 1
    text = "AB"

    for chunk in pd.read_csv('PUL075BCT.csv',chunksize=chuck_size):
        if batch_no == 1:
            chunk.to_csv('PUL075BCT'+ text + '.csv',index=False)
        else:
            text = "CD"
            chunk.to_csv('PUL075BCT'+ text + '.csv',index=False)
        batch_no = batch_no + 1
    print("\nSuccesful split into two records\n")

def addNewStudents():
    #added required students record
    dataAB=[
        [96,'PUL075BCT097   ','BIBEK BASHYAL'],
        [98,'PUL075BCT098   ','SAUGAT KAFLE']
    ]

    dataCD =[
        [97,'PUL075BCT098   ','ACHYUT BURLAKOTI'],
        [99,'PUL075BCT100   ','SIJAL BARAL']
    ]

    # Open our existing CSV file for AB class
    with open('PUL075BCTAB.csv', 'a',newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerows(dataAB)
        f_object.close()

    # Open our existing CSV file for CD class
    with open('PUL075BCTCD.csv', 'a',newline='') as f_object:
        writer_object = writer(f_object)
        writer_object.writerows(dataCD)
        f_object.close()
    
    print("\nSuccesful added new students in AB and CD\n")

try:
    splitClasses()
    addNewStudents()
except:
    print("\n SOME ERROR OCCURED\n")