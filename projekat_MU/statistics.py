import pandas as pd
from sklearn import preprocessing as pp


def label_encode(row):
    if(row.FTR == 'H'):
        return 1
    elif(row.FTR == 'A'):
        return -1
    else:
        return 0

def handle_data(df, condition):
    #df = pd.read_csv("D://Fax//8_semestar//Masinsko_ucenje//projekat//dataset//PremierLeague/E02014-2015.csv")
    droped = df.ix[:, :23]
    droped = droped.drop(['Div', 'Date'], axis=1)

    new_table = pd.DataFrame(columns=('Team', 'HGS', 'AGS', 'HAS', 'AAS', 'HGC', 'AGC', 'HDS', 'ADS',))
    res_home = droped.groupby('HomeTeam')
    res_away = droped.groupby('AwayTeam')
    new_table.Team = res_home.HomeTeam.all().values
    new_table.HGS = res_home.FTHG.sum().values
    new_table.HGC = res_home.FTAG.sum().values
    new_table.AGS = res_away.FTAG.sum().values
    new_table.AGC = res_away.FTHG.sum().values

    num_games = df.shape[0] / 2000

    avg_hs = df.FTHG.sum() * 1.0 / df.shape[0]
    avg_as = df.FTAG.sum() * 1.0 / df.shape[0]
    avg_hc = avg_as
    avg_ac = avg_hs
    new_table.HAS = (new_table.HGS / num_games) / avg_hs
    new_table.AAS = (new_table.AGS / num_games) / avg_as
    new_table.HDS = (new_table.HGC / num_games) / avg_hc
    new_table.ADS = (new_table.AGC / num_games) / avg_ac

    if(condition == "old"):
        X_train, y_train, X_test, y_test,x,y = past_stats_table(droped, new_table, condition)
        return X_train, y_train, X_test, y_test,x,y
    else:
        test = past_stats_table(droped,new_table,condition)
        return test

def past_stats_table(droped,new_table, condition):
    past_stats = droped.sort_index(ascending=True)
    past_stats = past_stats[['HomeTeam', 'AwayTeam', 'FTR', 'FTHG', 'FTAG', 'HS', 'AS', 'HC', 'AC']]

    #past_stats = past_stats.sort_index(ascending=True)
    #past_stats = past_stats.reset_index().drop(['index'], axis=1)
    #past_stats = past_stats.sort_index(ascending=True)

    past_stats["pHS"] = 0.0
    past_stats["pHC"] = 0.0
    past_stats["pAS"] = 0.0
    past_stats["pAC"] = 0.0
    past_stats["pHG"] = 0.0
    past_stats["pAG"] = 0.0

    calculated_past = calc_past_performance(past_stats)
    calculated_all = calc_attack_defense_strength(calculated_past,new_table)

    outcome = calculated_all.drop(['FTHG', 'FTAG', 'HS', 'AS', 'HC', 'AC'], axis=1)
    outcome["Result"] = outcome.apply(lambda row: label_encode(row), axis=1)
    #outcome.sort_index(inplace=True)
    print outcome

    num_games = calculated_all.shape[0] - 890

    X_train = outcome[['pHS', 'pHC', 'pAS', 'pAC', 'pHG', 'pAG', 'HAS', 'HDS', 'AAS', 'ADS']].loc[
              0:num_games]
    y_train = outcome['Result'].loc[0:num_games]
    if (condition == "new"):
        X_test = outcome[['pHS', 'pHC', 'pAS', 'pAC', 'pHG', 'pAG', 'HAS', 'HDS', 'AAS', 'ADS']].tail(1)
        #print outcome.tail(1)
        #print(X_test)
        return pp.normalize(X_test)
    else:
        X_test = outcome[['pHS', 'pHC', 'pAS', 'pAC', 'pHG', 'pAG', 'HAS', 'HDS', 'AAS', 'ADS']].loc[
                 num_games:]
    y_test = outcome['Result'].loc[num_games:]

    x = outcome[['pHS', 'pHC', 'pAS', 'pAC', 'pHG', 'pAG', 'HAS', 'HDS', 'AAS', 'ADS']]
    y = outcome['Result']
    return pp.normalize(X_train), y_train, pp.normalize(X_test), y_test,x,y

def calc_past_performance(past_stats):
    k = 4
    list = []
    for i in range(0,past_stats.shape[0] - 1, 1):
        row = past_stats.loc[i]
        ht = row.HomeTeam
        at = row.AwayTeam

        #print past_stats.tail(i - 1)
        ht_stats = past_stats.head(i)
        ht_stats = ht_stats[((past_stats.HomeTeam == ht) | (past_stats.AwayTeam == ht))].tail(k)
        #ht_stats = ht_stats.tail(k)
        #print ht_stats
        at_stats = past_stats.head(i)
        at_stats = at_stats[(past_stats.HomeTeam == at) | (past_stats.AwayTeam == at)].tail(k)
        #print ht_stats.shape[0]

        past_stats.set_value(i, 'pHC', (
            ht_stats[ht_stats["AwayTeam"] == ht].sum().HC + ht_stats[ht_stats["HomeTeam"] == ht].sum().HC) / k)
        past_stats.set_value(i, 'pAC', (
            at_stats[at_stats["AwayTeam"] == at].sum().HC + at_stats[at_stats["HomeTeam"] == at].sum().HC) / k)
        past_stats.set_value(i, 'pHS', (
            ht_stats[ht_stats["AwayTeam"] == ht].sum().HS + ht_stats[ht_stats["HomeTeam"] == ht].sum().AS) / k)
        past_stats.set_value(i, 'pAS', (
            at_stats[at_stats["AwayTeam"] == at].sum().HS + at_stats[at_stats["HomeTeam"] == at].sum().AS) / k)
        past_stats.set_value(i, 'pHG', (
            ht_stats[ht_stats["AwayTeam"] == ht].sum().FTAG + ht_stats[ht_stats["HomeTeam"] == ht].sum().FTHG) / k)
        past_stats.set_value(i, 'pAG', (
            at_stats[at_stats["AwayTeam"] == at].sum().FTAG + at_stats[at_stats["HomeTeam"] == at].sum().FTHG) / k)
    list.append(past_stats[['pHS', 'pHC', 'pAS', 'pAC', 'pHG', 'pAG']])
    #print("--------------------------")
    #print list
    return past_stats

def calc_attack_defense_strength(past_stats,new_table):
    f_HAS = []
    f_HDS = []
    f_AAS = []
    f_ADS = []
    for index, row in past_stats.iterrows():
        # print row
        f_HAS.append(new_table[new_table['Team'] == row['HomeTeam']]['HAS'].values[0])
        f_HDS.append(new_table[new_table['Team'] == row['HomeTeam']]['HDS'].values[0])
        f_AAS.append(new_table[new_table['Team'] == row['HomeTeam']]['AAS'].values[0])
        f_ADS.append(new_table[new_table['Team'] == row['HomeTeam']]['ADS'].values[0])

    past_stats['HAS'] = f_HAS
    past_stats['HDS'] = f_HDS
    past_stats['AAS'] = f_AAS
    past_stats['ADS'] = f_ADS
    print(past_stats)
    return past_stats