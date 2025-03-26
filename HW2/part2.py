import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pydotplus
import sklearn.tree as tree
# for a multi-class tree, call this function like this:
#@ writegraphtofile(clf, featurenames, dirname+graphfilename)

def writegraphtofile(clf, featurelabels, filename):
     dot_data = tree.export_graphviz(clf, feature_names=featurelabels, out_file=None)
     graph=pydotplus.graph_from_dot_data(dot_data)
     graph.write_png(filename)



data = pd.read_excel("AlienMushrooms.xlsx")

X = data.iloc[:, :-1]
y = data.iloc[:, -1]

clf = DecisionTreeClassifier(criterion="entropy")
clf.fit(X, y)

writegraphtofile(clf, featurelabels=X.columns, filename='./graphfilename')

score = clf.score(X, y)
print("Training accuracy:", score)
