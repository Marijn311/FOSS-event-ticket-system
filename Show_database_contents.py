"""
Ticket systeem 
Made by Marijn Borghouts
"""
import mysql.connector
#pip3 install mysql-connector-python-rf

# Connect to database
mydb = mysql.connector.connect(
  host="balbwuq2vgphmafftda4-mysql.services.clever-cloud.com",  #To manage database type this IP followed by :8080 in a browser and login with these credentials.
  user="u0rzyyrzeczuua0e",
  password="0gAOcli6gNMMMn3zzz31",
  database="balbwuq2vgphmafftda4",
  port="3306",
)

# Create cursor in the database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)

# Print all the tickets that are in the database.
query = "SELECT * FROM Tickets ORDER BY name ASC"
mycursor.execute(query)
mydb.commit() 
result = mycursor.fetchall()
for row in result:
    print(row)
    print("\n")


# Print all the accounts that are in the database
query = "SELECT * FROM Accounts ORDER BY id ASC"
mycursor.execute(query)
mydb.commit() 
result = mycursor.fetchall()
for row in result:
    print(row)
    print("\n")