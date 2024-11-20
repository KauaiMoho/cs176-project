# Cleaning: Removing duplicates, filling missing values, etc. - DONE
# Filtering subsets of your data with explanations. - DONE
# Sorting your data with explanations. - DONE
# Merging data in different ways with explanations. - DONE
# Visualizing data using at least five types of visualizations (e.g., scatter plots, bar charts, histograms, line charts, boxplots, etc). - TODO
# Pivoting or stacking your data with explanations. - DONE


import pandas as pd
import matplotlib.pyplot as plt

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit
data_framingham = pd.read_csv('heart_disease_framingham.csv')
 
#drop data with missing values in blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['GLUCOSE'])
# set male = 1, female = 0
data_framingham_cleaned.loc[(data_framingham_cleaned['SEX'] == 2)] = 0
data_framingham_cleaned.reset_index(inplace=True)

#setup data_iran clean
data_iran_cleaned = data_iran.copy()
data_iran_cleaned = data_iran.loc[(data_iran_cleaned["Blood sugar"] < 541)]

#data_chsl clean setup
data_chsl_cleaned = data_chsl.copy()
data_chsl_cleaned = data_chsl_cleaned.loc[(data_chsl_cleaned['trestbps'] > 0)]

##getting rid of outliers
def removeOutliers(df, column):
    Max = df[column].quantile(0.75) + 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    Min = df[column].quantile(0.25) - 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    return df[(df[column] > Min) & (df[column] < Max)]

##removing outliers from data_iran
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Heart rate')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Systolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Diastolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Blood sugar')

#removing outliers from data_chsl
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'trestbps')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'thalach')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'fbs')

#removing outliers from data_framhingham
data_framingham_cleaned = removeOutliers(data_framingham_cleaned, 'HEARTRTE')
data_framingham_cleaned = removeOutliers(data_framingham_cleaned, 'SYSBP')
data_framingham_cleaned = removeOutliers(data_framingham_cleaned, 'DIABP')
data_framingham_cleaned = removeOutliers(data_framingham_cleaned, 'GLUCOSE')

# age, sex, heart rate, systolic/diastolic blood pressure, blood sugar - Merge into one dataset
data_framingham_cleaned.rename(columns={"SEX": "Sex", "AGE": "Age", "DIABP": "D_BP", "SYSBP": "S_BP", "HEARTRTE": "Heart rate", "GLUCOSE": "Blood sugar"}, inplace=True)
data_iran_cleaned.rename(columns={"Gender": "Sex", "Systolic blood pressure": "S_BP", "Diastolic blood pressure": "D_BP"}, inplace=True)
data_fi_merged = pd.concat([data_framingham_cleaned,data_iran_cleaned], ignore_index=True).loc[:,['Age','Sex','S_BP','D_BP','Heart rate','Blood sugar']]

#merging chsl data with data_fi_merged
data_chsl_cleaned.rename(columns={"age": "Age", "sex": "Sex", "trestbps": "D_BP", "fbs": "Blood sugar", "thalach": "Heart Rate"}, inplace=True)
common_columns = list(set(data_fi_merged.columns) & set(data_chsl_cleaned.columns))
data_chsl_cleaned = data_chsl_cleaned[common_columns]
data_all = pd.merge(data_fi_merged, data_chsl_cleaned, on=(common_columns), how="outer")
data_all['Sex'].replace(0, 'Female', inplace=True)
data_all['Sex'].replace(1, 'Male', inplace=True)
data_all = data_all.loc[(data_all != 0).all(axis=1)]


pd.plotting.scatter_matrix(data_all[['Age','Sex','S_BP','D_BP','Heart rate','Blood sugar']], alpha=0.5, figsize=(8, 8), diagonal='hist')
plt.suptitle('Scatter Matrix of All Data')

##showinig the linear relationship
fig, ax = plt.subplots()
ax.scatter(data_all.S_BP, data_all.D_BP)
ax.set_xlabel("Systolic blood pressure mmHg")
ax.set_ylabel("Diastolic blood pressure mmHg")
ax.set_title("Systolic vs Diastolic blood pressure in patients")

#Visualization to show biases for MERGED data - By Karma Luitel
# Age biases and Gender biases

fig, ax = plt.subplots(ncols=2)

bins = [0, 40, 60, 80, 100]
bin_labels = ['1-39', '40-59', '60-79', '80-99']
data_all['Age_Category'] = pd.cut(data_all['Age'], bins, right=False, labels=bin_labels)
ax[0].pie(data_all['Sex'].value_counts(), labels=data_all['Sex'].value_counts().index, autopct='%.1f%%')
ax[1].pie(data_all['Age_Category'].value_counts(), labels=data_all['Age_Category'].value_counts().index, autopct='%.1f%%')
ax[0].set_title('Merged Sex Distribution ')
ax[1].set_title('Merged Age Distribution (years)')

fig.tight_layout()

data_reshaped = data_all.reset_index(drop=True)
data_reshaped.drop('S_BP', axis=1, inplace=True)
data_reshaped = data_reshaped.pivot(columns='Sex').stack().swaplevel()

data_reshaped.loc['Male'].hist()
plt.suptitle('Male Merged Data')
plt.tight_layout()

data_reshaped.loc['Female'].hist()
plt.suptitle('Female Merged Data')
plt.tight_layout()
plt.show()



