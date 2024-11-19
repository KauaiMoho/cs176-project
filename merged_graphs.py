# Cleaning: Removing duplicates, filling missing values, etc. - DONE
# Filtering subsets of your data with explanations. - DONE
# Sorting your data with explanations. - TODO
# Merging data in different ways with explanations. - DONE (concat)
# Visualizing data using at least five types of visualizations (e.g., scatter plots, bar charts, histograms, line charts, boxplots, etc). - TODO
# Pivoting or stacking your data with explanations. - TODO


import pandas as pd
import matplotlib.pyplot as plt

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
print(data_chsl_cleaned)

def removeOutliers(df, column):
    Max = df[column].quantile(0.75) + 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    Min = df[column].quantile(0.25) - 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    return df[(df[column] > Min) & (df[column] < Max)]


print(data_chsl.columns)
##removing outliers from data_iran
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Heart rate')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Systolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Diastolic blood pressure')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Blood sugar')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'CK-MB')
data_iran_cleaned = removeOutliers(data_iran_cleaned, 'Troponin')

#removing outliers from data_chsl
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'cp')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'trestbps')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'chol')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'fbs')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'restecg')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'thalach')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'oldpeak')

data_iran_cleaned = data_iran.loc[(data_iran["Blood sugar"] < 541) & (data_iran["Result"] == "positive")]

# age, sex, heart rate, systolic/diastolic blood pressure, blood sugar - Merge into one dataset
data_framingham_cleaned_diseased.rename(columns={"SEX": "Sex", "AGE": "Age", "DIABP": "D_BP", "SYSBP": "S_BP", "HEARTRTE": "Heart rate", "GLUCOSE": "Blood sugar"}, inplace=True)
data_iran_cleaned.rename(columns={"Gender": "Sex", "Systolic blood pressure": "S_BP", "Diastolic blood pressure": "D_BP"}, inplace=True)
data_fi_merged = pd.concat([data_framingham_cleaned_diseased,data_iran_cleaned], ignore_index=True).loc[:,['Age','Sex','S_BP','D_BP','Heart rate','Blood sugar']]
#TODO - Merge CHSL data


#Visualization to show biases for MERGED data - By Karma Luitel
# Age biases and Gender biases

fig, ax = plt.subplots(ncols=2)

bins = [0, 15, 30, 45, 60, 75,  90]
bin_labels = ['1-14', '14-29', '29-44', '44-59', '59-74', '74+']
data_fi_merged['Age_Category'] = pd.cut(data_fi_merged['Age'], bins, right=False, labels=bin_labels)

ax[0].pie(data_fi_merged['Sex'].value_counts(), labels=['Male', 'Female'], autopct='%.1f%%')
ax[1].pie(data_fi_merged['Age_Category'].value_counts(), labels=bin_labels, autopct='%.1f%%')
ax[0].set_title('Sex Distribution (Diseased)')
ax[1].set_title('Age Distribution (Diseased) (years)')

fig.tight_layout()
plt.show()