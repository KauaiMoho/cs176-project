import pandas as pd
import matplotlib.pyplot as plt

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit
data_framingham = pd.read_csv('heart_disease_framingham.csv')
 
#drop data with missing values in cloestrol and blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['GLUCOSE'])
#isolate patients with heart disease at exam
data_framingham_cleaned = data_framingham_cleaned.loc[data_framingham_cleaned['PREVCHD'] == 1] 

# age, sex, heart rate, resting/diastolic blood pressure, blood sugar
# data_merged_lossless = data_iran.concat()


#heartRateOutlierUpperBound = data_chsl["Heart Rate"].quantile(0.75) + 1.5 * (data_chsl["Heart Rate"].quantile(0.75) - data_chsl["Heart Rate"].quantile(0.25))

data_iran_cleaned = data_iran.loc[(data_iran["Blood sugar"] < 541) & (data_iran["Result"] == "positive")]

print(data_iran_cleaned)

