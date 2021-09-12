import serial
import datetime
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "beterbohnson@gmail.com"
receiver = "beterbohnson@gmail.com"


#setting up email
port = 465  # For SSL
password = input("Type your password and press enter: ")
# Create a secure SSL context
context = ssl.create_default_context()

#setting up email formatting    
msg = MIMEMultipart()

msg['From'] = sender
msg['To'] = receiver


#setting up the serial input reading
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM6'
ser.open()
#creating a time and a file named after the date to then write the days data to
d = datetime.datetime.now()
filename = str(d.month) + "-" + str(d.day) + "-" + str(d.year) + ".txt"
file = open(filename,"w+")
#reading each line as it should be in the order: Humidity>Pressure>Temp F>Temp C
i = 0
try:
	#while i < 3:
		h = str(ser.readline())
		p = str(ser.readline())
		f = str(ser.readline())
		c = str(ser.readline())
	#Getting the time these were received
		d = datetime.datetime.now()
	#processing the strings to remove useless characters
		h = h[h.index("H"):h.index("\\")]
		p = p[p.index("P"):p.index("\\")]
		f = f[f.index("F"):f.index("\\")]
		c = c[c.index("C"):c.index("\\")]
	#writing the data and corresponding time to the file (also printing time for viewing)
		print(d.month,"/",d.day,"/",d.year," at ",d.strftime("%H"),":",d.strftime("%M"),":",d.strftime("%S"),sep="")
		file.write(str(d.strftime("%H")) + ":" + d.strftime("%M") + ":" + d.strftime("%S") + "\n")
		file.write(h + "\n" + p + "\n" + f + "\n" + c + "\n\n")
		file.close()
	#printing the data for viewing purposes
		print(h)
		print(p)
		print(f)
		print(c)

		#setting the subject of email and adding contents and file attachment (file will be only thing in final implementation, no content)
		msg['Subject'] = str(d.month) + "/" + str(d.day) + "/" + str(d.year)
		msg.attach(MIMEText(str(d.strftime("%H")) + ":" + d.strftime("%M") + ":" + d.strftime("%S") + "\n" + h + "\n" + p + "\n" + f + "\n" + c + "\n\n", "plain"))
		
		#setting up the file to be attached to the email
		with open(filename, "rb") as attachment:
			part = MIMEBase("application", "octet-stream")
			part.set_payload(attachment.read())
		encoders.encode_base64(part)
		part.add_header(
			"Content-Disposition",
			f"attachment; filename= {filename}",
			)
		msg.attach(part)

		#Setting the email message from the email formatting structure
		message = msg.as_string()
		
		#logging in and sending the email
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
		    server.login(sender, password)
		    server.sendmail(sender, receiver, message)

		i += 1
except:
	print("Oopsie! Logan goof'd!")
ser.close()
print(ser)
print ("Serial Test Done")