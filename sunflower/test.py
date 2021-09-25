import pandas as pd
import datetime,os
import numpy as np
import copy

class RawTest:
    def __init__(self,sample:dict):
        self.sample=sample
    
    def sheet_test(self): #milti-sheets detect
        result=[]
        for i in self.sample:
            if isinstance(self.sample[i], dict):
                allcol=set.union(*[set(list(self.sample[i][j].columns)) for j in self.sample[i].keys()])
                comcol=set.intersection(*[set(list(self.sample[i][j].columns)) for j in self.sample[i].keys()])
                if allcol!=comcol:
                    test=self.column_test(self.sample[i])
                    test['File']=i
                    result.append(test)
        result = pd.concat(result)
        return result

    def column_test(self,sample): #df detect
        sample_dict=copy.deepcopy(sample)
        dict_instance=[]
        for i in sample_dict:
            if isinstance(sample_dict[i], dict):
                dict_instance.append(i)
        for i in dict_instance:
            sample_dict.pop(i,None)      
        file_col=[]
        commoncol=set.intersection(*[set(list(sample_dict[i].columns)) for i in sample_dict.keys()])
        cat=0
        for i in sample_dict:
            if isinstance(sample_dict[i], dict)==False:
                extra=set.union(*[set(list(sample_dict[i].columns)),commoncol])-set.intersection(*[set(list(sample_dict[i].columns)),commoncol])
                file_col.append([i,list(commoncol),list(sample_dict[i].columns),list(extra)])
        test_result=pd.DataFrame(
                                columns=['Filename','Common Col','Files Columns','Extra Columns'],
                                data=file_col
                                )
        return test_result
        




                   
        
