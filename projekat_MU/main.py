import predict
import parse_data
import statistics
from sklearn.externals import joblib
import pandas as pd
import cPickle

def predict_new_match():
    with open('D://Fax//8_semestar//Masinsko_ucenje//projekat/projekat_MU/model.pkl', 'rb') as fid:
        clf = cPickle.load(fid)
    #clf = joblib.load('D://Fax//8_semestar//Masinsko_ucenje//projekat/projekat_MU/model.pkl')
    HomeTeam = "Man City"
    AwayTeam = "Man United"
    #list = ['E0','13/08/05',HomeTeam,AwayTeam,0,4,'A',0,4,'A','',2,0,0,0,0,0,0,0,0,0,0,0]
    df = parse_data.read_csv()
    new_match = pd.DataFrame([['E0','13/08/05',HomeTeam,AwayTeam,0,0,'D',0,0,'D','',0,0,0,0,0,0,0,0,0,0,0,0]], columns=df.columns)
    df1 = df.append(new_match, ignore_index=True)
    print df1
    test = statistics.handle_data(df1,"new")
    pred = clf.predict(test)
    s = undo_label_enc(pred)
    print s
    print(pred)

def undo_label_enc(pred):
    if (pred[0] == 1):
        return "Home"
    elif (pred[0] == -1):
        return "Away"
    else:
        return "Draw"

if __name__ == "__main__":
    #df = parse_data.read_csv()
    #X_train, y_train, X_test, y_test,x,y = statistics.handle_data(df,"old")
    #predict.validate(x,y)
    #predict.predict(X_train,y_train,X_test,y_test)
    predict_new_match()