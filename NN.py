import pandas as pd
data=pd.read_csv('final_data.csv')

#imports

from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
from sklearn.neural_network import MLPClassifier
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest,chi2,mutual_info_classif
from sklearn.decomposition import PCA
from sklearn.utils import resample

def model(X_train,X_test,y_train,y_test):
    mlp = MLPClassifier(hidden_layer_sizes=(500,500,200,100),max_iter=500,activation='logistic',verbose=True,learning_rate='adaptive',random_state=123)
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)
    mlp.fit(X_train,y_train)
    pred=mlp.predict(X_test)
    count_0,count_1=0,0
    for i in y_train:
        if i==0:
            count_0+=1
        if i==1:
            count_1+=1
    print("train majority class: ",count_0," train minority class: ",count_1)
    print("*"*90,"\n","Validation on train data")
    pred_train=mlp.predict(X_train)
    print(confusion_matrix(y_train,pred_train))
    print(classification_report(y_train,pred_train))
    print(accuracy_score(pred_train,y_train))

    print("*"*90,"\n","Validation on test data")
    print(confusion_matrix(y_test,pred))
    print(classification_report(y_test,pred))
    print(accuracy_score(pred,y_test))

    return mlp,X_test,y_test,p_values,scores,pred

#Upsample the majority class to deal with low response rate.
df_majority = data[data.res==0]
df_minority = data[data.res==1]
print(df_majority.shape)
print(df_minority.shape)
df_minority_train=df_minority[:81]
df_minority_ups_train = resample(df_minority_train,
                                replace=True,     # sample with replacement
                                 n_samples=2000,    # to match majority class
                                 random_state=123)
df_train=pd.concat([df_majority[:4648],df_minority_ups_train])
df_test=pd.concat([df_majority[4648:],df_minority[81:]])

#Create train and test datasets
X_train=df_train.drop(['res','ACC_ID'],axis=1)
user_id_train=df_train['ACC_ID']
X_test=df_test.drop(['res','ACC_ID'],axis=1)
user_id_test=df_test['ACC_ID']
y_train=df_train['res']
y_test=df_test['res']

#Using Sklearn KBest to select top 50 features
try:
    no_features=int(input("Deafult features selected is 50 press enter if you dont wish to change else enter the value"))
except:
    no_features=50

test = SelectKBest(score_func=mutual_info_classif,k=no_features)
fit = test.fit(X_train.as_matrix(),y_train.as_matrix())
p_values=test.pvalues_
scores=test.scores_
X_train = fit.transform(X_train.as_matrix())
X_test=fit.transform(X_test.as_matrix())

#Train the model
mlp,X_test,y_test,p_values,scores,pred=model(X_train,X_test,y_train.as_matrix(),y_test.as_matrix())
class_0=[]
class_1=[]
c=0

while(True):
    generate=input("Generate csv of probability scores?(y/n)")
    if generate=="y":
        for i in lmodel.predict_proba(X_test):
            class_0.append(i[0])
            class_1.append(i[1])
        pd.DataFrame({'user_id':user_id_test,'Prob_classNegative':class_0,'Prob_classPositive':class_1,'actual':y_test,'pred':pred}).to_csv("analysis.csv")
        break
    if generate=="n":
        break
    else:
        print("invalid choice")
