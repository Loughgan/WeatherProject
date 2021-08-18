import serial

#setting up the serial input reading
ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM6'
ser.open()
#reading each line as it should be in the order: Humidity>Pressure>Temp F>Temp C
try:
	h = str(ser.readline())
	p = str(ser.readline())
	f = str(ser.readline())
	c = str(ser.readline())
	#processing the strings to remove useless characters
	h = h[h.index("H"):h.index("\\")]
	p = p[p.index("P"):p.index("\\")]
	f = f[f.index("F"):f.index("\\")]
	c = c[c.index("C"):c.index("\\")]
	#printing the data for viewing purposes
	print(h)
	print(p)
	print(f)
	print(c)
except:
	print("Oopsie! Logan goof'd!")
ser.close()
print(ser)
print ("Serial Test Done")