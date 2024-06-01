# EVENTTIKS README

EVENTTIKS is a hobby project that started when I was looking for a free app to send and scan event tickets. There was no good working free app with the features I needed, so I decided to develop an app myself.

## Project Overview
This project consists of two main scripts:

1. A script to generate unique tickets-codes, store them, and email them to participants.
2. A script to host a website where the tickets can be scanned by people at the entrance of an event.

Additionally, there is a supporting Python file that can easily send SQL commands to the database for manual adjustments if needed.

Anyone with basic knowledge of Python should be able to use and understand this system. 
If there are still any questions or uncertainties, you can always email me at m.m.borghouts@student.tue.nl.

**Todo:**
- Convert the script that sends the tickets to a web page for better user-friendliness.
- Convert to English.
- Improve webpage layout now that AI tools have gotten so much better.

## HOW TO: Generate Tickets
1. Create a Gmail address from which you want to send the emails containig the tickets. Adjust the settings of this Gmail account so that the Python script is allowed to log in and send emails. See this post: [Stack Overflow link](https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j).
2. Make an Excel file containg the information of all participants who should get a ticket in their mail. This exel file should have a name and email column with the column name in the first row. Place this Excel file in the “EventTiks” folder and rename it to "participants.xlsx".
3. Open generate_tickets.py and do the user input in the first few lines
4. Ensure the database is online,  use a free cloudbase database at [Clever Cloud](https://console.clever-cloud.com/)
5. If the script runs without errors, it will prompt for a password. Enter the 16-character password you created in step 1. Once you enter the correct password, all emails will be sent immediately!

## HOW TO: Verify Tickets
To verify the tickets, you can run host_website_for_ticket_verification.py on your laptop or, even better, on a small computer like a Raspberry Pi. This can always be on, for example, in a locked cabinet. When you run the script, the computer will host the website. People at the door can log in with a username and password to verify ticket codes.

1. The script should run immediately. Ensure the database connection is correct by checking the connection details.
2. The script outputs an IP address where the website runs. To make the web server accessible from another location, such as the entrance of InVivo or the Villa, you need the external IP address and the corresponding port number of the Pi. Use "ipconfig" in your terminal to view IP addresses. Make the IP address static or adjust the port number via the modem. This is not possible at the university unless the intern of the board can arrange it. Most likely, the Pi will need to be placed at someone's home.

