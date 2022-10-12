"""
Ticket systeem 
Made by Marijn Borghouts
"""
import random 
import string
import smtplib
import pandas as pd
import mysql.connector # pip3 install mysql-connector-python-rf

"""
Connect to database
This is a very small database that is hosted online on "clever cloud".
Clever cloud offers a free hosted database for very small developer testing.
It can store something like 10MB but that is enough for this purpose.
"""
mydb = mysql.connector.connect(
  host="balbwuq2vgphmafftda4-mysql.services.clever-cloud.com",  
  user="u0rzyyrzeczuua0e",
  password="0gAOcli6gNMMMn3zzz31",
  database="balbwuq2vgphmafftda4",
  port="3306",
)

# Create cursor in the database, this is an object needed to send and retrieve info from the database
mycursor = mydb.cursor(buffered=True)

# Load email list 
# This locations has to be adjusted depending on where the "participants" excel file is safed
# There should be 2 columns with "Names" and "Email" as first row (header)
loaded_exel = pd.read_excel (r'C:/Users/20192010/Downloads/deelnemers.xlsx') 
email_list = loaded_exel['Email'].tolist()
names_list = loaded_exel['Names'].tolist() 

"""
For privacy reasons it is better to not put more information than a first name in the database.
It is not neccesary for the script to work anyways. 
'Email' has to be the header (value of first row) of a column. The same goes for "Names" etc
"""

# Generate random codes
def generate_code():
    code_length=3 
    """
    With 3 letters in a code there are 26^3=17.576 possible combinations. 
    # Assume a party or other activity has a maximum of 200 guests than one in 17.576/200=~88 codes are valid, 
    # so guessing won't effectively work. It is always possible to change the code length to create more possible combinations. 
    # Using letter codes instead of QR codes saves phone battery for the scanner. Besides, people can remember three letters
    # so you do not need to wait for everyone to take out there phone at the door.
    """
    random_code = ''.join(random.choices(string.ascii_letters,k=code_length))
    random_code = random_code.upper()
    return random_code

"""
To send an email the following section is used. (Be aware that it may end up in the spam folder. This still needs to be fixed)
You need to allow less secure apps to acces gmail in your gmail settings in order to allow this script to send mails via your account.
I suggest making a new gmail account when we use this more often for Prot activities.

Google recently inceased security: https://stackoverflow.com/questions/72478573/sending-and-email-using-python-problem-causes-by-last-google-policy-update-on
So you no longer use your normal google password, but a randomly generated pass specifically for sending emails via Python
"""
sender_email= 'marijnborghouts@gmail.com'
password = input(str("Please enter gmail (google) password. BE AWARE!!!; entering a correct password will automatically send out all the mails!!!:"))
# Aplication specific 16 character password is: kyrgxwhgbpluclua

# # Clear out the Tickets table before filling it again (* did not work so I just dirty fixed it by taking valid!=5, since this includes all table entries)
# query = "DELETE FROM Tickets WHERE valid!=5"
# mycursor.execute(query)
# mydb.commit()


#BE AWARE: This system has not yet been fully tested. I once got a random error after sending like 90ish mails. 
# Maybe it was a time-out error. This may mean that the participant list has to be cut in 2 or 3 seperate files.
# Setup the email connection
with smtplib.SMTP('smtp.gmail.com', 587) as smtp: #587 is the port number, in my case atleast
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(sender_email, password)
    valid_codes=[]  
    for i in range(len(email_list)):
        receiver_email=email_list[i]
        save_code = generate_code()
        # As long as the generated random code already exists, make a new code
        while save_code in valid_codes:
            save_code = generate_code()
        valid_codes.append(save_code)
        # Here you write the actual message that people get in the mail    
        subject = 'Toegangscode voor BMT-feest'
        body = f'Beste {names_list[i]},\n\n Leuk dat je naar het BMT-Feest komt. \nJouw unieke toegangscode is: {save_code} \n\n Veel plezier, \n De Fissacom' 
        message = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(sender_email, receiver_email, message)
        
        # Add the ticket that has been send out to the database
        query = "INSERT INTO Tickets (name, email, code, valid) VALUES (%s, %s, %s, %s)"
        val = (names_list[i], receiver_email, save_code, True)
        mycursor.execute(query, val)
        mydb.commit()
        
print('Emails with tickets have succesfully been send.')

#Somehow geeft het exporteren van de deelnemerslijst soms dubbele entries
#met de namen werken is kut. Voortaan op de ticket site wil ik emails weergeven