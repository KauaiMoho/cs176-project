import pandas as pd
import matplotlib.pyplot as plt

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit
data_framingham = pd.read_csv('heart_disease_framingham.csv')
 
#File by Karma Luitel

#drop data with missing values in blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['TOTCHOL', 'LDLC'])
# set male and female 
data_framingham_cleaned['SEX'].replace(2, 'F', inplace=True)
data_framingham_cleaned['SEX'].replace(1, 'M', inplace=True)
#remove 0 vals
data_all = data_framingham_cleaned.loc[(data_framingham_cleaned != 0).all(axis=1)]
#reset index
data_framingham_cleaned.reset_index(inplace=True)

def drop_outliers(df_original, cols):
    df = df_original.copy()
    for col in cols:
        quartile_1 = df[col].quantile(0.25)
        quartile_3 = df[col].quantile(0.75)
        iqr = quartile_3 - quartile_1
        df[col] = df.loc[(df[col] > (quartile_1 - (1.5 * iqr))) & (df[col] < (quartile_3 + (1.5 * iqr))), col]
    return df

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

fig1.tight_layout()
plt.show()