from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import cPickle

def predict(X_train, y_train, X_test, y_test):
    randomForest = RandomForestClassifier(random_state=42, verbose=5, max_features=0.5)
    knn = KNeighborsClassifier(n_neighbors=13)
    svc = LinearSVC(C=1.0, random_state=42, verbose=5)
    naiveBayes = MultinomialNB(alpha=0.001)

    rf = randomForest.fit(X_train, y_train)
    y_pred = rf.predict(X_train)
    accRF = accuracy_score(y_pred, y_train)
    print "Random Forestt: ",accRF

    knnM = knn.fit(X_train, y_train)
    y_pred = knnM.predict(X_train)
    accKNN = accuracy_score(y_pred, y_train)
    print "KNN: ",accKNN

    nb = naiveBayes.fit(X_train, y_train)
    y_pred = nb.predict(X_train)
    accNB = accuracy_score(y_pred, y_train)
    print "NaiveBayes: ",accNB

    svcM = svc.fit(X_train, y_train)
    save_best_model(svcM)
    y_pred = svcM.predict(X_test)
    accSVC = accuracy_score(y_pred, y_test)
    print "SVC: ",accSVC

def validate(x, y):
    x_t, x_v, y_t, y_v = train_test_split(x, y, test_size=0.3, random_state=None)
    rf,knn, nb, svm = predict(x_t,y_t,x_v, y_v)
    print rf
    print knn
    print nb
    print svm

def save_best_model(model):
    with open('D://Fax//8_semestar//Masinsko_ucenje//projekat/projekat_MU/model.pkl', 'wb') as fid:
        cPickle.dump(model, fid)
    #joblib.dump(model, 'D://Fax//8_semestar//Masinsko_ucenje//projekat/projekat_MU/model.pkl')

