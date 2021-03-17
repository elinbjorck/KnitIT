import mysql.connector as con
import csv
import os
import math
import helpers as h

DB_NAME = "knitITDatabase"
USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"
startOfFilePath = os.getcwd() + "/Data/"  ##This is supposed to be everything that comes before "name.csv" in the Data file paths

try: 

    cnx = con.connect(user = USER, password = PASSWORD,  host = HOST, database = DB_NAME)
    cursor = cnx.cursor()
    
except con.errors.Error as error:

    if error.errno == con.errorcode.ER_BAD_DB_ERROR:
        cnx = con.connect(user = USER, password = PASSWORD,  host = HOST)
        cursor = cnx.cursor()

        print(f"Database: '{DB_NAME}' does not exist")
        print(f"Making a database called '{DB_NAME}'")
        h.createDatabase(DB_NAME, cursor)
        cnx = con.connect(user = USER, password = PASSWORD,  host = HOST, database = DB_NAME)
        cursor = cnx.cursor()
        

        print(f"{DB_NAME} database was created")

#DTL stands for data type List. its needen when generating queries to fill the tables.

DTLConstruction = ["int", "varchar(80)", "int", "varchar(200)", "varchar(100)"]
DTLDecoration = ["int", "varchar(80)", "varchar(200)", "varchar(100)", "int", "int"]
DTLGarment = ["int", "varchar(80)", "int", "int", "int", "int"]
DTLGarmentConstruction = ["int", "int", "int", "Varchar(100)"]
DTLGarmentConstructionDecoration = ["int", "int", "int", "varchar(80)"]
DTLGarmentType = ["int", "varchar(80)"]
DTLGarmentTypePart = ["int", "int", "int", "int", "int"]
DTLPart = ["int", "varchar(80)"]

TABLES = {}

TABLES["Construction"] = DTLConstruction
TABLES["Decoration"] = DTLDecoration
TABLES["Garment"] = DTLGarment
TABLES["GarmentConstruction"] = DTLGarmentConstruction
TABLES["GarmentConstructionDecoration"] = DTLGarmentConstructionDecoration
TABLES["GarmentType"] = DTLGarmentType
TABLES["GarmentTypePart"] = DTLGarmentTypePart
TABLES["Part"] = DTLPart

for name in TABLES:

    path = startOfFilePath + name + ".csv"
    csvFile = open(path, "r")
    csvFileReader = csv.reader(csvFile, skipinitialspace=True)
    dataList = TABLES[name]
    primaryKey = "ID"

    #Picking out the first row is important. We need the names of the columns to make 'insertString' and 'tableCreationString'
    #We also want the first row out of the way when we are to insert the data from the file in the database.
    firstRow = csvFileReader.__next__()
    tableCreationString = h.buildTableInitiatingString(name, firstRow, dataList, primaryKey)
    print(tableCreationString)
    insertString = h.buildInsertString(name, firstRow)
    print(insertString)

    try:
        print(f"Creating table {name}: ")
        cursor.execute(tableCreationString)
        h.insertCSVtoTable(name, csvFileReader, insertString, dataList, cursor)
        print("OK")
        csvFile.close()
        cnx.commit()
    except con.Error as err:
        if err.errno == con.errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)

cursor.close()
cnx.close()