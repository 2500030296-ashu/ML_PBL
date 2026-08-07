import os
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# Read Dataset
# ---------------------------------------

file_path = "uploads/student_placement_prediction_dataset_2026.csv"

if not os.path.exists(file_path):
    print("Dataset not found!")
    exit()

df = pd.read_csv(file_path)

# ---------------------------------------
# Age Distribution
# ---------------------------------------

plt.figure(figsize=(10, 6))
plt.hist(df["age"], bins=10, edgecolor="black")
plt.title("Age Distribution")
plt.xlabel("Age")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# ---------------------------------------
# CGPA Distribution
# ---------------------------------------

plt.figure(figsize=(10, 6))
plt.hist(df["cgpa"], bins=10, edgecolor="black")
plt.title("CGPA Distribution")
plt.xlabel("CGPA")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# ---------------------------------------
# Box Plot for Age
# ---------------------------------------

plt.figure(figsize=(6, 8))
plt.boxplot(df["age"])
plt.title("Box Plot of Age")
plt.ylabel("Age")
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()

# ---------------------------------------
# Bar Chart for Branch
# ---------------------------------------

plt.figure(figsize=(10, 6))
df["branch"].value_counts().plot(kind="bar")
plt.title("Students by Branch")
plt.xlabel("Branch")
plt.ylabel("Number of Students")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()
plt.show()