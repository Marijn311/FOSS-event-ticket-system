# Event Ticket Manager

This is a hobby project that originated from my need for a free app to send and scan event tickets. I couldn't find a suitable free app with the features I needed, so I decided to develop one myself. Everything is web-based, and the code is freely available for anyone to use, modify, and host.

All you need is a simple computer (e.g., an old PC, laptop, or Raspberry Pi) to host the website. Below you'll find information about the app's features, usage instructions, and how to host it.

## Features

1. **Free and Open Source**  
   A completely free and open-source app for managing event tickets.

2. **Web-Based Interface**  
   - Everything runs in a web browser. No external apps or software are needed.
   - Multiple users can scan and manage tickets simultaniously with instead synchronisation. 

3. **Secure Authentication**  
   - Login screen with session management ensures that only authorized users can manage tickets.  
   - Passwords are hashed and stored securely in a password-protected database.

4. **Randomly Generated Ticket Codes**  
   - Tickets are generated with easy-to-remember 3-letter codes.  
   - The app generates 17,576 possible combinations (26³). For an event with 200 guests, only 1 in ~88 codes will be valid, making guessing ineffective.  
   - Code length is customizable for more combinations.  
   - Using letter codes (instead of QR codes) saves battery for scanners and ensures the app works in dark environments or with broken phone cameras.

5. **Resilient Data Storage**  
   - Ticket data is stored in a free, cloud-based database.  
   - Data remains intact even if the website crashes or goes offline.

6. **Simple User Interface**  
     1. **Landing Page**: A straightforward landing page with three buttons to access the app's main functions:
     2. **Send Tickets**  
        - Fill out a form and upload an Excel file containing names and emails of guests.  
        - Tickets are generated and emailed automatically with personalised salutation and ticket-code.
     3. **View Ticktes**
        - See all tickets for an event in a table, with their status (valid/used).
        - Keeping track of is present and who is not (yet).
     4. **Scan Tickets**  
        - Use the scanner at the entrance by entering the guest's 3-letter code.  
        - Valid tickets will turn green and become invalid after scanning; invalid or already-used tickets will turn red.


## How to Host the Web App

To host the web app, all you need is a basic computer or a micro-computer like a Raspberry Pi. Follow the steps below to set it up:

1. **Clone the Repository**  
   git clone https://github.com/your-repo/event-ticket-manager.git
   

2. **Install Dependencies**  
   - Ensure you have Python and the required packages installed:
   

3. **Set Up Database**  
   - The app uses a cloud-based database, so no local setup is required.
   - I suggest to use Clever Cloud's free dev plan. you only get a few MB storage but that is more than enough to only save some text.
   - Ensure your database credentials are configured at the top of the host_website script.

4. **Run the Web App**  
   - python3 host_website.py
   
5. **Port Forwarding**  
   - If you want the app to be accessible externally, you need to configure port forwarding on your router.
   - Access your router settings and forward the appropriate port to the device hosting the app.  
   - You may also want to set up a static internal IP address to ensure your device's IP doesn’t change.

6. **Gmail Automation Code**
   - In order to allow third parties (Python scripts) to acces your Gmail account to send automated emails you need to change some settings and enter an extra code. See the following stack overflow link.
(https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j)

7. **Secure HTTPS connection**
   - Make sure you use secure connections if you want to deploy this irl.


## Manual Database Adjustments

A supporting Python file allows you to manually send SQL commands to the database for advanced operations, such as modifying ticket data or user permissions.


# Setting up a Free Domain and SSL Certificate

This guide will walk you through the process of setting up a free domain name with DuckDNS and obtaining a free SSL certificate from Let's Encrypt for your Raspberry Pi web server.

## 1. Getting a Free Domain with DuckDNS

1. Go to [DuckDNS](https://www.duckdns.org/) and sign in using your preferred method (Google, GitHub, etc.).

2. Once logged in, you'll see a field to enter a subdomain. Choose a name and check its availability.

3. Click "add domain" to create your free domain (e.g., `yourname.duckdns.org`).

4. Note down the token provided by DuckDNS. You'll need this to update your IP address.

5. On your Raspberry Pi, create a script to update your IP address:

   ```bash
   sudo nano /usr/local/bin/duckdns-update.sh
   ```

   Add the following content (replace with your details):

   ```bash
   #!/bin/bash
   echo url="https://www.duckdns.org/update?domains=yourname&token=YOUR_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -
   ```

6. Make the script executable:

   ```bash
   sudo chmod 700 /usr/local/bin/duckdns-update.sh
   ```

7. Set up a cron job to run this script every 5 minutes:

   ```bash
   sudo crontab -e
   ```

   Add this line:

   ```bash
   */5 * * * * /usr/local/bin/duckdns-update.sh >/dev/null 2>&1
   ```

## 2. Obtaining a Free SSL Certificate with Let's Encrypt

1. Install Certbot (Let's Encrypt client) on your Raspberry Pi:

   ```bash
   sudo apt-get update
   sudo apt-get install certbot
   ```

2. Obtain the SSL certificate:

   ```bash
   sudo certbot certonly --standalone -d yourname.duckdns.org
   ```

   Follow the prompts to complete the process.

3. Your certificates will be stored in `/etc/letsencrypt/live/yourname.duckdns.org/`.

4. Set up auto-renewal:

   ```bash
   sudo crontab -e
   ```

   Add this line to renew the certificate twice daily:

   ```bash
   0 */12 * * * certbot renew --quiet
   ```

## 3. Configuring The Flask App

Update your Flask application to use the new SSL certificate:

