import pandas as pd
import datetime,os

class RawTest:
    def __init__(self,sample:dict):
        self.sample=sample
    
    def sheet_test(self): #milti-sheets detect
        multisheets={}
        for i in self.sample:
            if isinstance(self.sample[i], dict):
                identical=all([set(self.sample[i][list(self.sample[i].keys())[0]].columns) == set(self.sample[i][df].columns) for df in self.sample[i]])
                multisheets[i]=identical
        return multisheets

    def column_test(self): #df detect
        columns={}
        benchmark=list(self.sample[list(self.sample.keys())[0]].columns)
        columns[','.join([str(element) for element in benchmark])]=[list(self.sample.keys())[0]]
        for i in self.sample:
            if isinstance(self.sample[i], dict)==False:
                if list(self.sample[i].columns)!=benchmark:
                    columns[','.join([str(element) for element in list(self.sample[i].columns)])]=[i]
                    benckmark=list(self.sample[i].columns)
                else:
                    columns[','.join([str(element) for element in benchmark])].append(i)
        return columns
    
