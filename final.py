import serial
import datetime
import time
import email, smtplib, ssl
import asyncio
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#The email addresses for the sender and receiver emails
sender = "beterbohnson@gmail.com"
receiver = "beterbohnson@gmail.com"

#setting up email
port = 465  # For SSL
password = input("Type your password and press enter: ")
# Create a secure SSL context
context = ssl.create_default_context()

#setting up the serial input reading
ser = serial.Serial()
ser.baudrate = 9600
ser.port = '/dev/ttyACM0'
ser.open()

looper = true
while (true):
	#setting up email formatting    
	msg = MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receiver
	
	i = 0
	#a loop to be run 24 times to get 24 reading which will each be one hour apart
	while (i < 24):
		#reading from the arduino
		h = str(ser.readline())
		p = str(ser.readline())
		f = str(ser.readline())
		c = str(ser.readline())
		#Getting the time these were received
		d = datetime.datetime.now()
		if (i = 0):
			#on the first reading, create a file named after the date to then write the days data to
			filename = str(d.month) + "-" + str(d.day) + "-" + str(d.year) + ".txt"
			#setting the subject of the email to the date the data is gathered from
			msg['Subject'] = filename
			#writing the date to the first line of the file
			file = open(filename,"w+")
			file.write(str(filename) + "\n")
			file.close
		#processing the strings to remove useless characters
		h = h[h.index("H"):h.index("\\")]
		p = p[p.index("P"):p.index("\\")]
		f = f[f.index("F"):f.index("\\")]
		c = c[c.index("C"):c.index("\\")]
		#adding the time of the readings, and the readings themselves to the file
		file = open(filename,"a")
		file.write(str(d.strftime("%H")) + ":" + d.strftime("%M") + ":" + d.strftime("%S") + "\n")
		file.write(h + "\n" + p + "\n" + f + "\n" + c + "\n")
		file.close()
		
		i += 1
		
	#24 reading have now been carried out
	#setting up the file to be attached to the email
	with open(filename, "rb") as file:
		part = MIMEBase("application", "octet-stream")
		part.set_payload(file.read())
	encoders.encode_base64(part)
	part.add_header(
		"Content-Disposition",
		"attachment; filename= " + filename,
		)
	msg.attach(part)
	
	#Setting the email message from the email formatting structure
	message = msg.as_string()
	
	#logging in and sending the email
	with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		server.login(sender, password)
		server.sendmail(sender, receiver, message)
		
ser.close()
	
	
	
	
	
	
