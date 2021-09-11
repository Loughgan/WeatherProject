import serial
import datetime

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
	while i < 3:
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
	#printing the data for viewing purposes
		print(h)
		print(p)
		print(f)
		print(c)
		i += 1
except:
	print("Oopsie! Logan goof'd!")
file.close()
ser.close()
print(ser)
print ("Serial Test Done")