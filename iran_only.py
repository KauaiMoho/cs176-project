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


#heartRateOutlierUpperBound = data_chsl["Heart Rate"].quantile(0.75) + 1.5 * (data_chsl["Heart Rate"].quantile(0.75) - data_chsl["Heart Rate"].quantile(0.25))
def drop_outliers(df_original, cols): #ROHIT can u check this function to see if its correct
    df = df_original.copy()
    for col in cols:
        quartile_1 = df[col].quantile(0.25)
        quartile_3 = df[col].quantile(0.75)
        iqr = quartile_3 - quartile_1
        df[col] = df.loc[(df[col] > (quartile_1 - (1.5 * iqr))) & (df[col] < (quartile_3 + (1.5 * iqr))), col]
    return df

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

#Visualization to show healthy/unhealthy levels of biomarkers in Framingham - By Karma Luitel - WIP
fig1, ax1 = plt.subplots(ncols=2, nrows=2)

check_subset = ['TOTCHOL', 'BMI', 'SYSBP', 'DIABP']
data_framingham_boxplot = drop_outliers(data_framingham_cleaned, check_subset)
for col in check_subset:
    data_framingham_boxplot[col].replace(0.0, pd.NA, inplace=True)
data_framingham_boxplot.dropna(subset=check_subset, inplace=True)

ax1[0][0].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'TOTCHOL'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'TOTCHOL']])
ax1[0][0].set_xticklabels(['Diseased', 'Healthy'])
ax1[0][0].set_ylabel('Total Cholesterol')
ax1[0][0].set_title('Diseased/healthy Cholesterol')

ax1[0][1].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'BMI'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'BMI']])
ax1[0][1].set_xticklabels(['Diseased', 'Healthy'])
ax1[0][1].set_ylabel('BMI')
ax1[0][1].set_title('Diseased/healthy BMI')

ax1[1][0].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'DIABP'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'DIABP']])
ax1[1][0].set_xticklabels(['Diseased', 'Healthy'])
ax1[1][0].set_ylabel('Diastolic Blood Pressure')
ax1[1][0].set_title('Diseased/healthy Diastolic Blood Pressure')

ax1[1][1].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'SYSBP'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'SYSBP']])
ax1[1][1].set_xticklabels(['Diseased', 'Healthy'])
ax1[1][1].set_ylabel('Systolic Blood Pressure')
ax1[1][1].set_title('Diseased/healthy Systolic Blood Pressure')

fig.tight_layout()
fig1.tight_layout()
plt.show()





