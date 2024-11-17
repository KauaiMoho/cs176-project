import pandas as pd
import matplotlib.pyplot as plt

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv')
data_framingham = pd.read_csv('heart_disease_framingham.csv')

print(data_iran.columns)
print(data_chsl.columns)
print(data_framingham.columns)

# age, sex, heart rate, resting/diastolic blood pressure, blood sugar
# data_merged_lossless = data_iran.concat()

#Heart Rate Outliers

#heartRateOutlierUpperBound = data_chsl["Heart Rate"].quantile(0.75) + 1.5 * (data_chsl["Heart Rate"].quantile(0.75) - data_chsl["Heart Rate"].quantile(0.25))

data_iran_cleaned = data_iran.loc[(data_iran["Blood sugar"] < 541) & (data_iran["Result"] == "positive")]

print(data_iran_cleaned)

#pd.plotting.scatter_matrix(data_iran, alpha=0.5, figsize=(10, 10), diagonal='hist')
#plt.show()