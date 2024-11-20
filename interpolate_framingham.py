import pandas as pd
import matplotlib.pyplot as plt

#File by Karma Luitel

data_framingham = pd.read_csv('heart_disease_framingham.csv')
#drop data with missing values in blood sugar cols
data_framingham_cleaned = data_framingham.dropna(subset=['TOTCHOL', 'LDLC'])
# set male and female 
data_framingham_cleaned['SEX'].replace(2, 'F', inplace=True)
data_framingham_cleaned['SEX'].replace(1, 'M', inplace=True)
#remove 0 vals
data_all = data_framingham_cleaned.loc[(data_framingham_cleaned != 0).all(axis=1)]
#reset index
data_framingham_cleaned.reset_index(inplace=True)

#Interpolated missing LDLC values for Framingham data - By Karma Luitel
fig, ax = plt.subplots(ncols=2)
pd.plotting.scatter_matrix(data_framingham_cleaned[['TOTCHOL', 'HDLC', 'LDLC', 'BMI', 'GLUCOSE']], alpha=0.5, figsize=(10, 10), diagonal='hist')
plt.suptitle('Scatter Matrix of Framingham Data')

#From scatter matrix, notice a linear relationship between HDLC and LDLC, begin calculating least squares regression
ax[0].scatter(data_framingham_cleaned['TOTCHOL'], data_framingham_cleaned['LDLC'])
ax[0].set_title('Total Chloestrol to LDLC (Framingham)')
ax[0].set_xlabel('Total Chloestrol')
ax[0].set_ylabel('LDLC')

#data has no outliers in testing.

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
ax[0].plot(data_framingham_cleaned['TOTCHOL'], y_fit)

#interpolate missing LDLC values in data_framingham using calc least square regression function from earlier
data_framingham_interpolated = data_framingham.dropna(subset=['TOTCHOL']) 
data_framingham_interpolated.loc[(data_framingham_interpolated['SEX'] == 2)] = 0
data_framingham_interpolated.reset_index(inplace=True)
data_framingham_interpolated['LDLC'].fillna(-1, inplace=True)
data_framingham_interpolated.loc[data_framingham_interpolated['LDLC'] == -1, 'LDLC'] = data_framingham_interpolated['TOTCHOL'] * m + c
data_framingham_interpolated['LDLC'].replace(0, pd.NA, inplace=True)
data_framingham_interpolated.dropna(subset=['LDLC'],inplace=True)

ax[1].boxplot([data_framingham_interpolated.loc[(data_framingham_interpolated['PREVCHD'] == 1), 'LDLC'], data_framingham_interpolated.loc[(data_framingham_interpolated['PREVCHD'] != 1), 'LDLC']])
ax[1].set_xticklabels(['Diseased', 'Healthy'])
ax[1].set_ylabel('LDLC')
ax[1].set_title('Diseased/healthy LDLC (Interpolated)')

fig.tight_layout()
plt.show()