# -*- coding: utf-8 -*-
"""
Ticket systeem 
Made by Marijn Borghouts
"""
import random 
import string
import smtplib
import pandas as pd
import mysql.connector #pip3 install mysql-connector-python-rf
from werkzeug.security import generate_password_hash


# Connect to database
mydb = mysql.connector.connect(
  host="balbwuq2vgphmafftda4-mysql.services.clever-cloud.com",  
  user="u0rzyyrzeczuua0e",
  password="0gAOcli6gNMMMn3zzz31",
  database="balbwuq2vgphmafftda4",
  port="3306",
)
# Create cursor in that database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)


### The following commands can be selectively uncommented and run to augment the database ###

# # Delete table called Tickets
# query = "DROP TABLE Tickets"
# mycursor.execute(query)
# mydb.commit()


# # Create table called Tickets
# query = "CREATE TABLE Tickets (name VARCHAR(30) NOT NULL, email VARCHAR(30) NOT NULL, code VARCHAR(50) PRIMARY KEY, valid TINYINT(1))"
# mycursor.execute(query)
# mydb.commit()



# #change maximum allowable characters
# query = "ALTER TABLE Tickets MODIFY email VARCHAR(100) NOT NULL"
# mycursor.execute(query)
# mydb.commit()


# # Create table called Accounts
# query = "CREATE TABLE Accounts (id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, username VARCHAR(30) NOT NULL, password VARCHAR(200) NOT NULL)"
# mycursor.execute(query)
# mydb.commit()

"""
EVERYBODY CAN LOGIN WITH THE SAME PASSWORD AND USERNAME AND THEN CREATE THEIR OWN SESSION VARIABLES
SO NO ACCOUNTS TABLE IS NEEDED. I JUST HARDCODE ONE FIXED USERNAME AND PASSWORD.

I COULD ALSO WRITE A QUERY TO DELETE OR ADJUST A SPECIFIC RECORD IN THE TICKETS TABLE, IF NEEDED.
"""

# # Add a user for the checking tickets website
# # MAKE SURE TO HASH THE PASSWORD THAT GOES INTO THE DATABASE!
# username_acc = 'Fissacom'
# password_raw = 'VoVoorMarijn'
# password_acc = generate_password_hash(password_raw)

# query = f"INSERT INTO Accounts (username, password) VALUES ('{username_acc}', '{password_acc}')"
# mycursor.execute(query)
# mydb.commit()


# # Add tickets to the database
# query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
# val = (naam, email, code, True)
# mycursor.execute(query, val)
# mydb.commit()

