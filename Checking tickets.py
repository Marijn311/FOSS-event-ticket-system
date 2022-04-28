import mysql.connector
#pip3 install mysql-connector-python-rf
from termcolor import colored

# Connect to database
mydb = mysql.connector.connect(
  host="localhost",  #To manage database type this IP followed by :8080 in a browser and login with these credentials.
  user="root",
  password="marijn",
  database="Tickets",
  port="3308",
)

# Create cursor in that database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)

# Now check if a code is in the database and if it is still valid
while True: 
    given_code = input(str("please enter code:"))
    query="SELECT EXISTS(SELECT * FROM Tickets WHERE (code='" + given_code + "' AND valid=1));"
    mycursor.execute(query)
    mydb.commit()
    result = mycursor.fetchone()  
    # Make the results more userfriendly to read
    if result[0] == 1:
        message=colored("This code is VALID", 'green')
        #If the code is was valid then it has been used, so we need to update the validity of the code in the database
        query="UPDATE Tickets SET valid=0 WHERE code='" + given_code + "';"
        mycursor.execute(query)
        mydb.commit()
    else:
        message=colored("This code is WRONG (or has been used)", 'bright red' )
    print(message)
    



