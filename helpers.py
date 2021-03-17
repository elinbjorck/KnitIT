import mysql.connector as con

def createDatabase(name, cursor):
    try:
        cursor.execute(f"CREATE DATABASE {name} DEFAULT CHARACTER SET 'utf8'")
    except con.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def insertCSVtoTable(nameOfTable, fileReader, insertString, dataTypesList, cursor):
    
    #This function itterates over every line in row in the csv reader. 
    #To use it you must send in a filereader where you already picked out the first row,
    #the one containing the names of the columns.

    for attributeList in fileReader:

        try:
            cursor.execute(insertString, attributeList)

        except con.Error as err:
            print(err)
        
def buildInsertString(tableName, attributeList):

    #Builds a string with the propper mqtt syntax to insert data in to a table

    numberOfAttributes = len(attributeList)
    return "INSERT INTO " +  tableName + "(" + ", ".join(attributeList) + ") " + "VALUES (" + "%s, "*(numberOfAttributes-1) + "%s)"

def buildTableInitiatingString(name, nameList, listOfDatatypes, primaryKey):

    #Builds a string with the proper mqtt syntax to initiate a new table in a database
    #Doing string concatination like this is slow but I dont care at the moment as It wil not be used many times

    tableString = f"CREATE TABLE `{name}` (" 
    tableString += f"`{nameList[0]}` {listOfDatatypes[0]} NOT NULL AUTO_INCREMENT, "
    i = 1
    for name in nameList[1:]:
        tableString += f"`{name}` {listOfDatatypes[i]}, "
        i += 1
    tableString += f"PRIMARY KEY (`{primaryKey}`))"
    return tableString

