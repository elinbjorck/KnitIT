import helpers as h
import mysql.connector as con
import csv
import os
import math

DB_NAME = "knitITDatabase"
USER = "root"
PASSWORD = "root"
HOST = "127.0.0.1"

def newGarment(cursor):
    garmentType = ""
    name = ""
    YarnTestHeight = ""
    YarnTestHeight = ""
    YarnTestWeight = ""

    cursor.execute("SELECT name, numberofparts FROM partspertype")

    garmentTypes = cursor.fetchall()

    i = 1
    for thing in garmentTypes:
        print(f"({i}) {thing[0]}, parts required: {thing[1]}")
        i += 1
    print("Quit (0)")
    
    garmentType = askForNumber("What would you like to do?", 0, len(garmentTypes))
    if garmentType == 0:
        return False
    askForRequiredConstructions(garmentType, cursor)

def askForRequiredConstructions(garmentTypeId, cursor)
    constructions = ()

    cursor.execute("SELECT p.name, partid FROM garmenttypepart AS gtp "
                   "JOIN part AS p ON p.id = gtp.partid "
                   "WHERE gtp.garmenttypeid = %s and gtp.required = 1", (garmentTypeId,))

    partsNeeded = cursor.fetchall()
    for part in partsNeeded:
        

def askForOptionalConstructions():
    pass

def askForNumber(message, min, max):
    choice = input(message)

    if not choice.isdigit():
        print("Your choice must be a number")
        choice = askForNumber(message, min, max)
        

    choice = int(choice)

    if choice > max or choice < min:
        print("That choice is not available")
        choice = askForNumber(message, min, max)

    return choice
    



cnx = con.connect(user = USER, password = PASSWORD,  host = HOST, database = DB_NAME)
cursor = cnx.cursor()

keepGoing = True

while keepGoing:
    keepGoing = newGarment(cursor)