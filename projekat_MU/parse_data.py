import pandas as pd
import numpy as np
import csv
import glob

def parse_all_csv():
    interesting_files = glob.glob("D://Fax//8_semestar//Masinsko_ucenje//projekat//dataset//PremierLeague/*.csv")
    with open(r'D://Fax//8_semestar//Masinsko_ucenje//projekat//dataset/all_PL.csv', 'ab') as fw:
        writer = csv.writer(fw)
        with open(interesting_files[0], 'r') as f:
            fileReader = csv.reader(f)
            for row in fileReader:
                res_16 = row[2:23]
                writer.writerow(res_16)
        for filename in interesting_files[1:len(interesting_files)]:
            with open(filename, 'r') as f:
                fileReader = csv.reader(f)
                next(fileReader, None)
                for row in fileReader:
                    res_16 = row[2:23]
                    writer.writerow(res_16)
        fw.close()

def read_csv():
    df = pd.read_csv("D://Fax//8_semestar//Masinsko_ucenje//projekat//dataset//all_PL.csv")
    return df