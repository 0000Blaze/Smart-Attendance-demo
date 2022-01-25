#made to handle the csv file
#1. split classes AB and CD studnets
#2. add the new transfer students

from operator import index
from statistics import variance
import pandas as pd

def splitClasses():
    chuck_size = 48
    batch_no = 1

    for chunk in pd.read_csv('records.csv',chunksize=chuck_size):
        chunk.to_csv('record'+ str(batch_no) + '.csv',index=False)
        batch_no = batch_no + 1

variable = input("Choose:\n 1.Split classes\n 2.Added new students\n")
variable_int = int(variable)
if variable_int == 1:
    splitClasses()
elif variable_int == 2:
    pass
else:
    print("\n SOME ERROR OCCURED\n")