import pandas as pd

#read file
raw=pd.read_excel('Sample Super Data.xlsx',sheet_name=None)
dup_df,na_df={},{}

#data quality check
def quality_check(raw):
    for i in raw.keys():
        ##check dups
        dup_df[i]=raw[i].loc[raw[i].duplicated(keep=False)==True]
        raw[i]=raw[i].loc[raw[i].duplicated(keep=False)==False]
        
        ##check NaN vals
        na_df[i]=raw[i].loc[raw[i].isna().any(axis=1)==True]
        raw[i]=raw[i].loc[raw[i].isna().any(axis=1)==False]
        
        #change data types
        for col in raw[i].columns:
            if raw[i][col].dtype == 'object':
                try:
                    raw[i][col] = pd.to_datetime(raw[i][col])
                except ValueError:
                    pass
            elif 'amount' in col:
                raw[i][col].transform(pd.to_numeric, errors='coerce')
    return dup_df,na_df
quality_check(raw)

#data intergration
#payslips
raw['Payslips']['year']=raw['Payslips']['end'].dt.year
raw['Payslips']['quarter']=raw['Payslips']['end'].dt.quarter
payslip=raw['Payslips'].loc[raw['Payslips']['code'].isin(raw['PayCodes'].loc[raw['PayCodes']['ote_treament']=='OTE']['pay_code'].tolist())]
payslip['Super Payable']=round(payslip['amount']*0.095,2)
#Disbursement
raw['Disbursements']['date_ref']=raw['Disbursements']['payment_made']-pd.DateOffset(days=28)
raw['Disbursements']['year']=raw['Disbursements']['date_ref'].dt.year
raw['Disbursements']['quarter']=raw['Disbursements']['date_ref'].dt.quarter
#merge 
Quarter_report=pd.merge(
        payslip.groupby(['employee_code','year','quarter']).sum(),
        raw['Disbursements'].groupby(['employee_code','year','quarter']).sum(),
        how="outer",
        on=['employee_code', 'year','quarter']).fillna(0)
Quarter_report['variance']=Quarter_report['Super Payable']-Quarter_report['sgc_amount']
Quarter_report.columns=['OTE amount','Super Payable','Disbursement','Variance']
Quarter_report=Quarter_report.reindex().groupby(['employee_code','year','quarter']).sum()

Quarter_report.to_csv("result.csv")
payslip.groupby(['employee_code','year','quarter']).sum().to_csv("payslip.csv")
raw['Disbursements'].groupby(['employee_code','year','quarter']).sum().to_csv("Disbursements.csv")

