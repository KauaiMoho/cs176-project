import pandas as pd
import matplotlib.pyplot as plt

data_chsl = pd.read_csv('heart_disease_chsl.csv') #Manit

#drop duplicate rows in dataframe
data_chsl_cleaned = data_chsl.drop_duplicates()

#create subplot
fig, ax = plt.subplots(ncols=2, figsize=(12, 8))

# map chest pain to color
chest_pain_colors = {
    0: "blue",
    1: "green",
    2: "orange",
    3: "red"
}

# map chest pain number to chest pain name
chest_pain_labels = {
    0: "Typical Angina",
    1: "Atypical Angina",
    2: "Non-anginal Pain",
    3: "Asymptomatic"
}

#set sp to graph in 0 position
sp = ax[0]

#iterate over chest pain types
for chest_pain_type, chest_pain_label in chest_pain_labels.items():
    subset = data_chsl_cleaned[data_chsl_cleaned["cp"] == chest_pain_type]
    sp.scatter(
        subset["age"],
        subset["thalach"],
        label=chest_pain_label,
        color=chest_pain_colors[chest_pain_type],
        alpha=0.8
    )

#set labels for graph
sp.set_title("Age vs Maximum Heart Rate Achieved by Chest Pain Type")
sp.set_xlabel("Age")
sp.set_ylabel("Maximum Heart Rate Achieved")
sp.legend(title="Chest Pain Type")

#set sp to graph in 1st postition
sp = ax[1]

labels = ["No Exercise-Induced Angina", "Exercise-Induced Angina"]
#get data for maximum heart rate, for angina caused by exercise, and not caused by exercise
data = [data_chsl_cleaned[data_chsl_cleaned["exang"] == group]["thalach"] for group in [0, 1]]

#create box plot
sp.boxplot(data, labels=labels, patch_artist=True, boxprops=dict(facecolor="lightblue"))

#set labels for graph
sp.set_title("Maximum Heart Rate by Angina Categories")
sp.set_xlabel("Angina Categories")
sp.set_ylabel("Maximum Heart Rate Achieved")

#show the plot
fig.tight_layout()
plt.show()