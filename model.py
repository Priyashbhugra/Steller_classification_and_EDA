import pandas as pd, numpy as np
import pickle
from sklearn.metrics import f1_score, accuracy_score
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# Read data from csv file
df = pd.read_csv("Skydata_pro.csv")

# Convert string class labels to int
labels = df["class"].to_numpy()
labEncoder = LabelEncoder()
labels = labEncoder.fit_transform(labels)

# Drop labels which are not important for making decisions
df= df.drop(['objid', 'run', 'rerun', 'camcol', 'field', 'camcol', 'specobjid','plate', 'mjd','fiberid','class' ] ,axis=1)


def normalize(df):
    return MinMaxScaler().fit(df).transform(df)

df = df.fillna(0)

def remove_outliers(df):
    """
    This function detecs outlier and removes it from the current dataframe.
    """
    headers = list(df)
    df = StandardScaler().fit(df).transform(df)
    isOutlier = LocalOutlierFactor().fit_predict(df)
    cleanData = df[np.where(isOutlier == 1)]
    cleanLabels = labels[np.where(isOutlier == 1)]
    print(f"Percentage of data considered outliers: {((df.shape[0]-cleanData.shape[0])/df.shape[0])*100}%")
    return cleanData, cleanLabels , headers

print("Detecting outliers")
df_data_without_outliers, df_labels_without_outliers , headers = remove_outliers(df)

#Splitting the data into a training and test set. 
X_train, X_test, y_train, y_test = train_test_split(df_data_without_outliers ,df_labels_without_outliers , test_size = 0.2)
print("Train test split completed")

def get_metrics(preds, y_true):
  """
  This function calculates the F1 Score , F1 Mirco and F1 MAcro score. As this is a class imbalance problem we have to look at multiple metrics instead of one.
  """
  acc_score = accuracy_score(y_true, preds)
  f1_w = f1_score(y_true, preds, average = "weighted")
  f1_macro = f1_score(y_true, preds, average = "macro")
  f1_micro = f1_score(y_true, preds, average = "micro")
  print("Test ACC: {}".format(acc_score))
  print("F1 WEIGHTED: {}".format(f1_w))
  print("F1 MACRO: {}".format(f1_macro))
  print("F1 MICRO: {}".format(f1_micro))

#  We used Random forest classifier after tesing multiple models
np.random.seed(42)
lr_clf = LogisticRegression().fit(X_train, y_train)
score = lr_clf.score(X_train, y_train)
print('Training Accuracy: %.3f' % (score*100))

print("On Test Set")
pred = lr_clf.predict(X_test)
get_metrics(pred, y_test)

Pkl_Filename = "LogisticRegression_Model.pkl"  
with open(Pkl_Filename, 'wb') as file:  
    pickle.dump(lr_clf, file)