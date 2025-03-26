import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
# ---------------------------
# 1. Load the dataset
# ---------------------------
# Note: Adjust the file path if needed
df = pd.read_csv("diabetic_data.csv")

# Check the dataset structure and summary statistics
print("Dataset Info:")
print(df.info())
print("\nDataset Description:")
print(df.describe(include='all'))

# ---------------------------
# 2. Detect and correct missing values
# ---------------------------
print("\nMissing values per column before correction:")
print(df.isnull().sum())

# For each column with missing values, fill with mode (for objects) or median (for numerics)
for col in df.columns:
    if df[col].isnull().sum() > 0:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna(df[col].median(), inplace=True)

print("\nMissing values per column after correction:")
print(df.isnull().sum())

# ---------------------------
# 3. Create target variables
# ---------------------------
# Create a binary target variable: 0 if 'NO' (not readmitted), 1 otherwise.
df['readmitted_binary'] = df['readmitted'].apply(lambda x: 0 if x.strip() == 'NO' else 1)

# For multiclass, we will factorize the original readmitted column.
df['readmitted_factorized'], readmitted_uniques = pd.factorize(df['readmitted'])
print("\nClasses in 'readmitted':", list(readmitted_uniques))

# ---------------------------
# 4. Prepare feature set
# ---------------------------
# Drop the original target columns from features. (Keep the features only.)
features = df.drop(columns=['readmitted', 'readmitted_binary', 'readmitted_factorized'])

# --- Handle ordinal variables ---
# For example, the "age" variable is given as ranges. Here we map them to numeric values.
# Adjust this mapping if your dataset uses different interval labels.
age_mapping = {
    '[0-10)': 0, '[10-20)': 1, '[20-30)': 2, '[30-40)': 3,
    '[40-50)': 4, '[50-60)': 5, '[60-70)': 6, '[70-80)': 7,
    '[80-90)': 8, '[90-100)': 9
}
if 'age' in features.columns:
    features['age'] = features['age'].map(age_mapping)

# --- One-hot encode categorical variables ---
# Identify categorical columns (remaining as objects) and convert them using pd.get_dummies.
categorical_cols = features.select_dtypes(include=['object']).columns
features = pd.get_dummies(features, columns=categorical_cols, drop_first=True)

# ---------------------------
# 5. Partition the data into training and test sets
# ---------------------------
# For binary classification
X_bin = features.copy()
y_bin = df['readmitted_binary']

X_train_bin, X_test_bin, y_train_bin, y_test_bin = train_test_split(
    X_bin, y_bin, test_size=0.3, random_state=42
)

# ---------------------------
# 6. Train and evaluate the decision tree for binary classification
# ---------------------------
clf_bin = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
clf_bin.fit(X_train_bin, y_train_bin)

train_score_bin = clf_bin.score(X_train_bin, y_train_bin)
test_score_bin = clf_bin.score(X_test_bin, y_test_bin)

print("\nBinary Classification:")
print("Training Accuracy: {:.3f}".format(train_score_bin))
print("Test Accuracy: {:.3f}".format(test_score_bin))

# Plot and save the binary decision tree to a PNG file
plt.figure(figsize=(20, 10))
plot_tree(clf_bin, feature_names=X_bin.columns, class_names=['Not Readmitted', 'Readmitted'], filled=True)
plt.title("Decision Tree - Binary Classification")
plt.savefig("decision_tree_binary.png")
plt.close()

# ---------------------------
# 7. Train and evaluate the decision tree for multiclass classification
# ---------------------------
X_multi = features.copy()
y_multi = df['readmitted_factorized']

X_train_multi, X_test_multi, y_train_multi, y_test_multi = train_test_split(
    X_multi, y_multi, test_size=0.3, random_state=42
)

clf_multi = DecisionTreeClassifier(criterion='entropy', max_depth=4, random_state=42)
clf_multi.fit(X_train_multi, y_train_multi)

train_score_multi = clf_multi.score(X_train_multi, y_train_multi)
test_score_multi = clf_multi.score(X_test_multi, y_test_multi)

print("\nMulticlass Classification:")
print("Training Accuracy: {:.3f}".format(train_score_multi))
print("Test Accuracy: {:.3f}".format(test_score_multi))

# Plot and save the multiclass decision tree to a PNG file.
# Use the unique class names extracted from the factorization.
plt.figure(figsize=(20, 10))
plot_tree(clf_multi, feature_names=X_multi.columns, class_names=[str(cls) for cls in readmitted_uniques], filled=True)
plt.title("Decision Tree - Multiclass Classification")
plt.savefig("decision_tree_multiclass.png")
plt.close()
