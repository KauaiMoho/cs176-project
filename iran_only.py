import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit
data_framingham = pd.read_csv('heart_disease_framingham.csv')
 
#drop data with missing values in blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['GLUCOSE', 'TOTCHOL', 'LDLC'])
# set male = 1, female = 0
data_framingham_cleaned.loc[(data_framingham_cleaned['SEX'] == 2)] = 0
data_framingham_cleaned.reset_index(inplace=True)
#isolate patients with heart disease at exam
data_framingham_cleaned_diseased = data_framingham_cleaned.loc[data_framingham_cleaned['PREVCHD'] == 1] 

##getting rid of outliers
data_iran_cleaned = data_iran
data_chsl_cleaned = data_chsl
print(data_iran_cleaned)

def removeOutliers(df, column):
    Max = df[column].quantile(0.75) + 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    Min = df[column].quantile(0.25) - 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    return df[(df[column] > Min) & (df[column] < Max)]


print(data_iran.columns)
##removing outliers from data_iran
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Heart rate')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Systolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Diastolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Blood sugar')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'CK-MB')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Troponin')

#fig, ax = plt.subplots(ncols=2)
#pd.plotting.scatter_matrix(data_iran_cleaned[['Age', 'Gender', 'Heart rate', "Systolic blood pressure", "Diastolic blood pressure", "Blood sugar", "CK-MB", "Troponin"]], alpha=0.5, figsize=(8, 8), diagonal='hist')
#plt.suptitle('Scatter Matrix of Iran Data')



data_iran_postive = data_iran_cleaned[data_iran_cleaned.Result == "positive"]
data_iran_postive.set_index(["Age"], inplace=True)
data_iran_postive.sort_index(inplace=True) #sorting
print(data_iran_postive)

data_iran_negative = data_iran_cleaned[data_iran_cleaned.Result == "negative"]
data_iran_negative.set_index(["Age"], inplace=True)
data_iran_negative.sort_index(inplace=True) #sorting
print(data_iran_negative)

plt.scatter(data_iran_postive.index, data_iran_postive["Troponin"], label="Had Heart disease", color = "blue", alpha=0.5)
plt.scatter(data_iran_negative.index, data_iran_negative["Troponin"], label="Did not have Heart disease", color="red", alpha=0.5)
plt.title("Troponin Levels on Various Ages")
plt.plot(np.unique(data_iran_postive.index), np.poly1d(np.polyfit(data_iran_postive.index, data_iran_postive["Troponin"], 1))(np.unique(data_iran_postive.index)), color = "blue")
plt.plot(np.unique(data_iran_negative.index), np.poly1d(np.polyfit(data_iran_negative.index, data_iran_negative["Troponin"], 1))(np.unique(data_iran_negative.index)), color = "red")

plt.xlabel("Age")
plt.ylabel("Troponin I ng/mL")
plt.legend()

plt.show()





