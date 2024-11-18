import pandas as pd
import matplotlib.pyplot as plt

data_iran = pd.read_csv('heart_disease_iran.csv')
data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit
data_framingham = pd.read_csv('heart_disease_framingham.csv')
 
#drop data with missing values in blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['GLUCOSE', 'TOTCHOL', 'LDLC'])
#isolate patients with heart disease at exam
data_framingham_cleaned = data_framingham_cleaned.loc[data_framingham_cleaned['PREVCHD'] == 1] 
# set male = 1, female = 0
data_framingham_cleaned.loc[(data_framingham_cleaned['SEX'] == 2)] = 0
#reset index
data_framingham_cleaned.reset_index(inplace=True)

#heartRateOutlierUpperBound = data_chsl["Heart Rate"].quantile(0.75) + 1.5 * (data_chsl["Heart Rate"].quantile(0.75) - data_chsl["Heart Rate"].quantile(0.25))
data_iran_cleaned = data_iran.loc[(data_iran["Blood sugar"] < 541) & (data_iran["Result"] == "positive")]

# age, sex, heart rate, systolic/diastolic blood pressure, blood sugar - Merge into one dataset
data_framingham_cleaned.rename(columns={"SEX": "Sex", "AGE": "Age", "DIABP": "D_BP", "SYSBP": "S_BP", "HEARTRTE": "Heart rate", "GLUCOSE": "Blood sugar"}, inplace=True)
data_iran_cleaned.rename(columns={"Gender": "Sex", "Systolic blood pressure": "S_BP", "Diastolic blood pressure": "D_BP"}, inplace=True)
data_fi_merged = pd.concat([data_framingham_cleaned,data_iran_cleaned], ignore_index=True).loc[:,['Age','Sex','S_BP','D_BP','Heart rate','Blood sugar']]
#TODO - Merge CHSL data

#Visualization to show biases - By Karma Luitel
# AGE BIASES
# GENDER BIASES

fig, ax = plt.subplots(ncols=3)

bins = [0, 15, 30, 45, 60, 75,  90]
bin_labels = ['1-14', '14-29', '29-44', '44-59', '59-74', '74+']
data_fi_merged['Age_Category'] = pd.cut(data_fi_merged['Age'], bins, right=False, labels=bin_labels)

ax[0].pie(data_fi_merged['Sex'].value_counts(), labels=['Male', 'Female'])
ax[1].pie(data_fi_merged['Age_Category'].value_counts(), labels=bin_labels)
ax[0].set_title('Sex Distribution')
ax[1].set_title('Age Distribution (years)')

#Interpolated missing LDLC values for Framingham data - By Karma Luitel

#pd.plotting.scatter_matrix(data_framingham_cleaned[['TOTCHOL', 'HDLC', 'LDLC', 'BMI', 'Blood sugar']], alpha=0.5, figsize=(10, 10), diagonal='hist')
#From scatter matrix, notice a linear relationship between HDLC and LDLC, begin calculating least squares regression
ax[2].scatter(data_framingham_cleaned['TOTCHOL'], data_framingham_cleaned['LDLC'])
ax[2].set_title('Total Chloestrol to LDLC')
ax[2].set_xlabel('Total Chloestrol')
ax[2].set_ylabel('LDLC')

#find least squares regression of two given sets of data
def find_best_fit(a, b):
    n = len(a)
    sum_a = sum(a)
    sum_b = sum(b)
    sum_a_squared = 0
    sum_a_b = 0
    for i in range(n):
        sum_a_squared += a[i]**2
        sum_a_b += a[i]*b[i]
    m = ((sum_a_b*n)-(sum_b*sum_a))/((sum_a_squared*n)-(sum_a**2))
    c = (sum_b-(m*sum_a))/n
    return (m,c)

#find least squares regression of framingham data
m, c = find_best_fit(data_framingham_cleaned['TOTCHOL'], data_framingham_cleaned['LDLC'])
y_fit = []
for i in range(len(data_framingham_cleaned['TOTCHOL'])):
    y_fit.append((m*data_framingham_cleaned['TOTCHOL'][i]) + c)

#plot least squares regression it to verify it is accurate onto graph
ax[2].plot(data_framingham_cleaned['TOTCHOL'], y_fit)

#interpolate missing LDLC values in data_framingham using calc least square regression function from earlier
data_framingham_interpolated = data_framingham.dropna(subset=['GLUCOSE', 'TOTCHOL'])
data_framingham_interpolated = data_framingham_interpolated.loc[data_framingham_interpolated['PREVCHD'] == 1] 
data_framingham_interpolated.loc[(data_framingham_interpolated['SEX'] == 2)] = 0
data_framingham_interpolated.reset_index(inplace=True)
data_framingham_interpolated['LDLC'].fillna(-1, inplace=True)
data_framingham_interpolated.loc[data_framingham_interpolated['LDLC'] == -1, 'LDLC'] = data_framingham_interpolated['TOTCHOL'] * m + c

#ADD FUTURE CODE PAST THIS LINE



fig.tight_layout()
plt.show()