import pandas as pd
import calendar
df = pd.read_csv('shopping.csv')

dataset = ()
evidence = []
labels = []

month_no = {v: k for k, v in enumerate(calendar.month_abbr)}
month_no.pop('Jun')
month_no['June'] = 6

for index, row in df.iterrows():
    record = [row['Administrative'], row['Administrative_Duration'], row['Informational'], row['Informational_Duration'], row['ProductRelated'],
              row['ProductRelated_Duration'], row['BounceRates'], row['ExitRates'], row['PageValues'], row['SpecialDay'], month_no[row['Month']] - 1,
              row['OperatingSystems'], row['Browser'], row['Region'], row['TrafficType'], int(row['VisitorType'] == 'Returning_Visitor'), int(row['Weekend'] == 'TRUE')]
    labels.append(int(row['Revenue']=='TRUE'))
    evidence.append(record)


