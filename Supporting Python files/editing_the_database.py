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


#-------------------The following commands can be selectively uncommented to augment the database-------------------------------------------------------

# # Show all tables in the database
# query = "SHOW TABLES"
# mycursor.execute(query)
# tables = mycursor.fetchall()
# for table in tables:
#   print(table)


# # Add an entry to the Accounts table
# username = "user1"
# password = "password1"
# hashed_password = generate_password_hash(password)

# query = "INSERT INTO Accounts (username, password) VALUES (%s, %s)"
# val = (username, hashed_password)
# mycursor.execute(query, val)
# mydb.commit()


# # Show all columns in the Accounts table
# query = "SHOW COLUMNS FROM Accounts"
# mycursor.execute(query)
# columns = mycursor.fetchall()
# for column in columns:
#   print(column)


# Show all entries in the Accounts table
query = "SELECT * FROM Accounts"
mycursor.execute(query)
accounts = mycursor.fetchall()
for account in accounts:
  print(account)

# # Clear out the Tickets table before filling it again 
# query = "DELETE FROM Tickets WHERE valid!=5"
# mycursor.execute(query)
# mydb.commit()
# print("Cleared out the tickets table")

# # Delete table called Tickets
# query = "DROP TABLE Tickets"
# mycursor.execute(query)
# mydb.commit()


# # Create table called Tickets
# query = "CREATE TABLE Tickets (name VARCHAR(100) NOT NULL, email VARCHAR(100) NOT NULL, code VARCHAR(50) PRIMARY KEY, valid TINYINT(1))"
# mycursor.execute(query)
# mydb.commit()
# print('created table')


# #change maximum allowable characters
# query = "ALTER TABLE Tickets MODIFY email VARCHAR(100) NOT NULL"
# mycursor.execute(query)
# mydb.commit()


# # Add a ticket to the database
# query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
# val = ("Martijn Peeters", "gingwatmis", "KKO", True)
# mycursor.execute(query, val)
# mydb.commit()
# print('added code')
