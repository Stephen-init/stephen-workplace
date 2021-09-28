import luigi
import luigi
from luigi import Task,Target,Parameter,LocalTarget,IntParameter
from luigi import local_target
import pandas as pd
from sunflower.config import *
from sunflower.core import *
from sunflower.test import *
import os

global payslips
payslips=Raw(user['stephen']['raw'],payslip['files']).folder_reader()

class ReadRaw(Task):
    file_name=Parameter()
    index=IntParameter()
    def output(self):
        outputfolder= r"/Users/stephen/Documents/Stephen-ETL/output"
        path=os.path.join(outputfolder,"dataset"+str(self.index)+'.csv')
        return LocalTarget(path,format=luigi.format.Nop)
    
    def run(self):
        input_path=self.file_name
        data=pd.read_excel(input_path)
        data['source']=self.file_name.split('/')[-1]
        with self.output().open('wb') as ofile:
            data.to_csv(ofile)

class GroupData(Task):
    def output(self):
        return LocalTarget('dataset.csv',format=luigi.format.Nop)
    
    def run(self):
        input_path=payslips
        counter=1
        for file in input_path:
            target=yield ReadRaw(file,counter)
            counter=counter+1
        alldf=[]
        outputfolder=r"/Users/stephen/Documents/Stephen-ETL/output"
        for file in os.listdir(outputfolder):
            df=pd.read_csv(os.path.join(outputfolder,file),encoding= 'unicode_escape')
            alldf.append(df)
        dataset=pd.concat([i for i in alldf])
        with self.output().open('wb') as ofile:
            dataset.to_csv(ofile)

class TestData(Task):
    def requires(self):
        return GroupData()

    def output(self):
        outputfolder= r"/Users/stephen/Documents/Stephen-ETL/Tests"
        path=os.path.join(outputfolder,'test_result.xlsx')
        return LocalTarget(path,format=luigi.format.Nop)

    def run(self):
        outputfolder= r"/Users/stephen/Documents/Stephen-ETL/output"
        data=Raw(outputfolder,tests['files']).read_files()
        coltest=RawTest(data).column_test(data)
        valuetest=RawTest(data).missing_values_table()

        with self.output().open('wb') as ofile:
            with pd.ExcelWriter(ofile) as writer:  # doctest: +SKIP
                coltest.to_excel(writer,sheet_name='Column Test')
                valuetest.to_excel(writer,sheet_name='Value Test')


if __name__=='__main__':
    luigi.run(['TestData'])