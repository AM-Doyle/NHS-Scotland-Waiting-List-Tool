import sys
import csv
import sqlite3


def main():

    # promp user for command line input
    if len(sys.argv) != 4:
        print('Usage: python dbinsert.py DataToInput.csv databasename.db tablename')
        sys.exit(1)

    # set db as database requested
    con = sqlite3.connect(sys.argv[2])
    db = con.cursor()

    # get column titles from csv
    with open(sys.argv[1], 'r') as csvfile:
        # get csv data in memory
        csvread = csv.reader(csvfile)
        csvlist = list(csvread)
        # get the number of columns
        titlenumber = len(csvlist[0])
        # get the number of rows
        csvrowcount = sum(1 for row in csvlist)
        titlelist = ''
        tlntxt = ''
        valuesphold = ''
        #add w to the start of the columns with numbers
        for i in range(0, titlenumber):
            csvlist[0][i] = csvlist[0][i].lower()
            if csvlist[0][i][0].isdigit():
                csvlist[0][i] = 'w' + csvlist[0][i]
        # create a string of the column names and one for ?
        for i in range(0, titlenumber):
            if i < titlenumber - 1:
                titlelist = titlelist + csvlist[0][i] + ', '
                tlntxt = tlntxt + csvlist[0][i] + ', '
                valuesphold = valuesphold + '?, '
            else:
                titlelist = titlelist + csvlist[0][i]
                tlntxt = tlntxt + csvlist[0][i]
                valuesphold = valuesphold + '?'

        # create te table with correct titles and name
        db.execute("CREATE TABLE "+sys.argv[3]+" ("+titlelist+");")
        for j in range(0, csvrowcount):
            db.executemany("INSERT INTO "+sys.argv[3]+" ("+titlelist+") VALUES("+valuesphold+");", [csvlist[j]])
            con.commit()

main()