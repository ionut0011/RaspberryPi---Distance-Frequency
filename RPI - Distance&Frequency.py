#importing needed libraries for the project
import RPi.GPIO as GPIO
import time
import pigpio

# .BOARD is setting the pins as the ones on the board (e.g. 1-40)
# .BCM is setting the pins as the Broadcom SOC channel (e.g. GPIO24 is the pin18 as .BOARD)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
pi = pigpio.pi()

# defining the pins used by the hardware components
Segments = (a, b, c, d, e, f, g, dot) = (26, 22, 11, 13, 15, 24, 7, 35)
Digits = (D1, D2, D3, D4) = (32, 40, 38, 37)
Trig = 16
Echo = 18	
Buzzer = 18

# here we set the trigger pin as OUTPUT and echo pin as INPUT
GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

# here we set the digits & segments pins as OUTPUT and to HIGH
for d in Digits:
        GPIO.setup(d, GPIO.OUT)
        GPIO.output(d, GPIO.HIGH)

for s in Segments:
        GPIO.setup(s, GPIO.OUT)
        GPIO.output(s, GPIO.LOW)
	
# here we've got 14 vectors for the values we gonna send out to the 4 digit 7 segment display in order to display a specific number/letter
# it's pretty long, i know :(
def display_segment(number, dot):
	null = [0,0,0,0,0,0,0,0]
	zero = [1,1,1,1,1,1,0,0]
	one = [0,1,1,0,0,0,0,0]
	two = [1,1,0,1,1,0,1,0]
	three = [1,1,1,1,0,0,1,0]
	four = [0,1,1,0,0,1,1,0]
	five = [1,0,1,1,0,1,1,0]
	six = [1,0,1,1,1,1,1,0]
	seven = [1,1,1,0,0,0,0,0]
	eight = [1,1,1,1,1,1,1,0]
	nine = [1,1,1,1,0,1,1,0]
	n = [0,1,1,0,1,1,1]
	u = [0,1,1,1,1,1,0]
	l = [0,0,0,1,1,1,0]
    	

        if number == 1:
        	for i in range(8):
			GPIO.output(Segments[i], one[i])
	     		if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 2:
        	for i in range(8):
        		GPIO.output(Segments[i], two[i])
    			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 3:
        	for i in range(8):
        		GPIO.output(Segments[i], three[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 4:
        	for i in range(8):
        		GPIO.output(Segments[i], four[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 5:
        	for i in range(8):
        		GPIO.output(Segments[i], five[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 6:
        	for i in range(8):
        		GPIO.output(Segments[i], six[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 7:
        	for i in range(8):
        		GPIO.output(Segments[i], seven[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 8:
        	for i in range(8):
        		GPIO.output(Segments[i], eight[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 9:
        	for i in range(8):
        		GPIO.output(Segments[i], nine[i])
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)
        elif number == 0:
        	for i in range(8):
        		GPIO.output(Segments[i], zero[i]) 
			if i == 7 and dot == 1:
				GPIO.output(Segments[i], 1)      
        elif number == 10:
		for i in range(7):
			GPIO.output(Segments[i], n[i])
        elif number == 11:
		for i in range(7):
			GPIO.output(Segments[i], u[i])
        elif number == 12:
		for i in range(7):
			GPIO.output(Segments[i], l[i])
    

# here's the function i am using to display a digit
def display_digit(digit, number, dot):
    
	display_segment(number, dot)
	GPIO.output(Digits[digit], GPIO.LOW)
	time.sleep(0.0007)
	GPIO.output(Digits[digit], GPIO.HIGH)

# the function to display the distance/frequency on the 4digit7segment display
def display_distance(number, type):
	#type = 0 => frecventa
	#type = 1 => cm
	if number < 1000:
		n3 = (int)((number * 10) % 10)
		n2 = (int)((number) % 10)
		n1 = (int)((number // 10) % 10)
		n0 = (int)(number // 100)
		#print("n0 =",n0," n1=",n1," n2=",n2," n3=",n3)
		if type == 1:	
			if n0 != 0:
				display_digit(0,n0,0)
			display_digit(1,n1,0)
			display_digit(2,n2,1)
			display_digit(3,n3,0)
		elif type == 0:
			if n0 !=0:
				display_digit(0,n0,0)
			elif n0 == 0:
				display_digit(0,0,0)	
			display_digit(1,n1,0)
			display_digit(2,n2,0)
			display_digit(3,10,0) #hertz

	if number>=1000:
		display_digit(0,10,0)
		display_digit(1,11,0)
		display_digit(2,12,0)
		display_digit(3,12,0)

# the function that gets the distance between 2 objects
def get_distance():
	GPIO.output(Trig, GPIO.HIGH)
	time.sleep(0.00001)
	GPIO.output(Trig, GPIO.LOW)

	start = time.time()
	stop = time.time()
	while GPIO.input(Echo) == 0:
		start = time.time()
	while GPIO.input(Echo) == 1:
		stop = time.time()

	duration = stop-start
	distance = 34300/2 * duration

	print ("Distance = %.2f" % distance)
	return distance
try:
	buzzer = 0
	freq = 0
	while True:
		sleeper = 0
		if buzzer == 0:
			# some self-made formula for the distance => frequency conversion so the output frequency won't be too high
			distance = get_distance()
			if distance > 0 and distance < 150:
				freq = distance * 3
			elif distance > 500 and distance < 1000:
				freq = distance / 2
			elif distance > 1000:
				freq = 250
			elif distance > 150 and distance < 500:
				freq = distance
			
			while sleeper < 1500:
				display_distance(distance,1)
				sleeper = sleeper + 1
		if buzzer == 1:
			pi.hardware_PWM(Buzzer, freq, 500000)
			while sleeper < 500:
				display_distance(freq, 0)
				sleeper = sleeper + 1	
		if buzzer == 0:
			buzzer = 1
		elif buzzer == 1:
			buzzer = 0		
			pi.hardware_PWM(Buzzer,0,0)

# exception
except KeyboardInterrupt:
	pass

# stopping the buzzer
pi.hardware_PWM(Buzzer, 0, 0)

GPIO.cleanup()