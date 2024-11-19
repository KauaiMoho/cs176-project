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

def removeOutliers(df, column):
    print("remove Outliers", column)
    Max = df[column].quantile(0.75) + 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    Min = df[column].quantile(0.25) - 1.5 * (df[column].quantile(0.75) - df[column].quantile(0.25))
    print(column, Max, Min)
    print(df[(df[column] > Min) & (df[column] < Max)])
    return df[(df[column] > Min) & (df[column] < Max)]


#removing outliers from data_chsl
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'cp')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'trestbps')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'chol')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'restecg')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'thalach')
data_chsl_cleaned = removeOutliers(data_chsl_cleaned, 'oldpeak')

print(data_chsl_cleaned)


fig, ax = plt.subplots(ncols=2, figsize=(12, 8))

# Define a color map for chest pain types
chest_pain_colors = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "red"
}

# Map the chest pain types to labels for the legend
chest_pain_labels = {
    0: "Typical Angina",
    1: "Atypical Angina",
    2: "Non-anginal Pain",
    3: "Asymptomatic"
}

sp = ax[0]

# Iterate over chest pain types to plot data
for chest_pain_type, color in chest_pain_colors.items():
    subset = data_chsl_cleaned[data_chsl_cleaned["cp"] == chest_pain_type]
    sp.scatter(
        subset["age"],
        subset["thalach"],
        label=chest_pain_labels[chest_pain_type],
        color=color,
        alpha=0.8
    )

# Customize the plot
sp.set_title("Age vs Maximum Heart Rate Achieved by Chest Pain Type")
sp.set_xlabel("Age")
sp.set_ylabel("Maximum Heart Rate Achieved")
sp.legend(title="Chest Pain Type")

sp = ax[1]
# Prepare data for the plot
angina_groups = [0, 1]  # 0: No, 1: Yes
labels = ["No Exercise-Induced Angina", "Exercise-Induced Angina"]
data = [data_chsl_cleaned[data_chsl_cleaned["exang"] == group]["oldpeak"] for group in angina_groups]

# Create the box plot
sp.boxplot(data, labels=labels, patch_artist=True, boxprops=dict(facecolor="lightblue"))

# Customize the plot
sp.set_title("Distribution of Oldpeak by Exercise-Induced Angina")
sp.set_xlabel("Exercise-Induced Angina")
sp.set_ylabel("Oldpeak (ST Depression)")

# Show the plot
fig.tight_layout()
plt.show()