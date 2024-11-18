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

#Visualization to show healthy/unhealthy levels of biomarkers in Framingham - By Karma Luitel
fig1, ax1 = plt.subplots(ncols=2, nrows=2)

check_subset = ['GLUCOSE', 'TOTCHOL', 'BMI']
data_framingham_boxplot = drop_outliers(data_framingham_cleaned, check_subset)
data_framingham_boxplot.loc[:,check_subset].replace(0, pd.NA, inplace=True)
data_framingham_boxplot.dropna(subset=check_subset,inplace=True)

ax1[0][0].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'GLUCOSE'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'GLUCOSE']])
ax1[0][0].set_xticklabels(['Diseased', 'Healthy'])
ax1[0][0].set_ylabel('Glucose')
ax1[0][0].set_title('Diseased/healthy Glucose')

ax1[0][1].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'TOTCHOL'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'TOTCHOL']])
ax1[0][1].set_xticklabels(['Diseased', 'Healthy'])
ax1[0][1].set_ylabel('Total Cholesterol')
ax1[0][1].set_title('Diseased/healthy Cholesterol')

ax1[1][0].boxplot([data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 1), 'BMI'], data_framingham_boxplot.loc[(data_framingham_boxplot['PREVCHD'] == 0), 'BMI']])
ax1[1][0].set_xticklabels(['Diseased', 'Healthy'])
ax1[1][0].set_ylabel('BMI')
ax1[1][0].set_title('Diseased/healthy BMI')

fig.tight_layout()
fig1.tight_layout()
plt.show()