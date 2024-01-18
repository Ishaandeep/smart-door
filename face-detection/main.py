import cv2
import os 
import numpy as np
from picamera2 import Picamera2
import time
from time import sleep
import RPi.GPIO as GPIO
from gpiozero import AngularServo, Button
from RPLCD.i2c import CharLCD
from telegram.ext import Updater ,CommandHandler
from telegram import Bot
import requests
from concurrent.futures import ThreadPoolExecutor


button = Button(26)
i=0
c=0
val =0
doorState = 0 #0 means closed, 1 means open
ownerState = 0 # 0 means not present
led_pin = 29
led_door = 31
buzzer_pin=32

with open("/home/ishaan/.local/share/.telegram_BotToken", 'r') as BotToken:
    doorBot = BotToken.read().rstrip()

cam = Picamera2()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN) 
GPIO.setup(11, GPIO.IN) 
GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(led_door, GPIO.OUT)

servo = AngularServo(18, min_pulse_width=0.0006, max_pulse_width=0.0023)
lcd = CharLCD(i2c_expander='PCF8574',address=0x27,port=1,cols=16,rows=2,dotsize=8)
lcd.clear()
config = cam.create_still_configuration()
cam.configure(config)
updater = Updater(token = doorBot)
dispatcher= updater.dispatcher
bot = Bot(token = doorBot)
bot.send_message(chat_id = "<group_chatID>", text = "!!Welcome Your Smart Door bell is Working \n Press /user to view all commands!!")



def blink_morse_code(morse_code):
	# print("Inside morese blink")

    for symbol in morse_code:
		# print("blink")
        if symbol == ".":
            # Dot, short blink
            GPIO.output(led_pin, GPIO.HIGH)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(led_pin, GPIO.LOW)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.2)
        elif symbol == "-":
            # Dash, long blink
            GPIO.output(led_pin, GPIO.HIGH)
            GPIO.output(buzzer_pin, GPIO.HIGH)
            time.sleep(0.6)
            GPIO.output(led_pin, GPIO.LOW)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.2)
        elif symbol == " ":
            # Space between words
            time.sleep(0.4)

def sos():
# Define the Morse code for SOS
	print("Inside SOS")
	morse_code = "... --- ..."
	try:
		start = time.time()+15
		while time.time()<start:
			blink_morse_code(morse_code)
			# Space between SOS signals
			time.sleep(1)

	except KeyboardInterrupt:
		pass

def checkIntrusion():
	global doorState

	while True:
		if GPIO.input(7) == 0:
			# print(res)
			start = time.time() + 5
			while time.time() <start:
				if GPIO.input(11) == 0 and doorState == 0:
					display(["!! Intrusion  !!",""])
					bot.send_message(chat_id = "<group_chatID>", text = "!!! Intrusion !!!")
					sos()
					display(["      Smart     ","   Door Bell"])
			
def isknown():
	#Parameters
	list1=[]
	id = 0
	font = cv2.FONT_HERSHEY_COMPLEX
	height=1
	boxColor=(0,0,255)      #BGR- GREEN
	nameColor=(255,255,255) #BGR- WHITE
	confColor=(255,255,0)   #BGR- TEAL

	face_detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	recognizer = cv2.face.LBPHFaceRecognizer_create()
	recognizer.read('trainer/trainer.yml')
	names = ['None', 'Ayush', 'None', 'None']

	cam.preview_configuration.main.size = (640, 360)
	cam.preview_configuration.main.format = "RGB888"
	cam.preview_configuration.controls.FrameRate=30
	cam.preview_configuration.align()
	cam.configure("preview")
	cam.start()

	while len(list1)!=10:
			
			frame=cam.capture_array()

			frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			
			faces = face_detector.detectMultiScale(
							frameGray,      # The grayscale frame to detect
							scaleFactor=1.1,# how much the image size is reduced at each image scale-10% reduction
							minNeighbors=5, # how many neighbors each candidate rectangle should have to retain it
							minSize=(150, 150)# Minimum possible object size. Objects smaller than this size are ignored.
							)
			for(x,y,w,h) in faces:
					namepos=(x+5,y-5) #shift right and up/outside the bounding box from top
					confpos=(x+5,y+h-5) #shift right and up/intside the bounding box from bottom
					#create a bounding box across the detected face
					cv2.rectangle(frame, (x,y), (x+w,y+h), boxColor, 3) #5 parameters - frame, topleftcoords,bottomrightcooords,boxcolor,thickness
				
					id, confidence = recognizer.predict(frameGray[y:y+h,x:x+w])
					print(confidence)
					list1.append(int(confidence))

					print(list1)
					
	print(list1)
	if sum(list1)/10 >60:
		return True
	else:
		return False

def known():
	# global doorState
	print("In known")
	display(["     Welcome","     Home"])
	if doorState ==0:
		# doorState=1
		operateLock(1)
		return
	print("Exit Known")



def buttonPressed():
	global c
	global val
	print("Button Pressed")
	imgAdd = takeImage("guest",c)
	files = {'photo':open(imgAdd,'rb')}
	bot.send_message(chat_id = "<group_chatid>", text = "Someone at the Door") # replace with you chat id
	resp = requests.post('https://api.telegram.org/bot<token>/sendPhoto?chat_id=<group chat id >',files=files) # Replace token and chat_id with your bots token and chatid
	print(resp.status_code)
	print(GPIO.input(7))
	c+=1
	val = 1


def unknown():
	global val
	if ownerState == 0:
		display([   "Owner","Absent"])

	val = GPIO.input(7)
	while val == 0:
		val = GPIO.input(7)
		# print(button.when_pressed)
		button.when_pressed = buttonPressed
		if val == 1:
			return
	print("Exit unknown")

def userHandler(update , topic):
	topic.bot.send_message(chat_id = update.effective_chat.id,text = "Commands are :\n /open : To open Door \n /peepHole : To Peak door \n /close : To close Door \n /notHome : To set you are Not Home \n /home : To Set you are home")
	return

def userHandlerOpen(update , topic):
	if doorState != 1:
		operateLock(1)

	GPIO.output(29,True)
	time.sleep(2)
	GPIO.output(29,False)
	topic.bot.send_message(chat_id = update.effective_chat.id,text = "Door is Now Open")
	return

def userHandlerClose(update , topic):
	if doorState != 0:
		operateLock(0)
		# sleep(1)
	topic.bot.send_message(chat_id = update.effective_chat.id,text = "Door is Now Close")
	return

def OwnerStateAbsent(update , topic):
	global ownerState
	ownerState = 0
	operateLock(0)
	topic.bot.send_message(chat_id = update.effective_chat.id,text = "Owner Not at Home state set!!!")
	return

def OwnerStatePresent(update , topic):
	global ownerState
	ownerState = 1
	operateLock(0)
	topic.bot.send_message(chat_id = update.effective_chat.id,text = "Owener is at home state set!!!")
	return

def userPeepHole(update , topic):
	global i
	imgAdd = takeImage("peakView",i)
	files = {'photo':open(imgAdd,'rb')}
	bot.send_message(chat_id = "<group_chatID>", text = "Heres the view from peep hole")
	resp = requests.post('https://api.telegram.org/bot<token>/sendPhoto?chat_id=<group chat id >',files=files) # Replace token and chat_id with your bots token and chatid
	print(resp.status_code)
	i+=1
	return

def takeImage(person,c):

    cam.start()
    cam.capture_file(f"{person}{c}.jpg")
    cam.stop()
    return f"/home/ishaan/Desktop/smart-door/face-detection/{person}{c}.jpg"

def display(dis):
	lcd.clear()
	lcd.write_string(dis[0])
	lcd.crlf()
	lcd.write_string(dis[1])
	time.sleep(1)

def operateLock(state):
	global doorState
	doorState = state
	if doorState == 1:
		servo.angle = 90
		GPIO.output(led_door,True)
		display(["!!! Welcome !!!",""])
		# GPIO.output(buzzer_pin, GPIO.HIGH)
		# time.sleep(0.6)
		# GPIO.output(buzzer_pin, GPIO.LOW)
	elif doorState == 0:
		servo.angle = -90
		GPIO.output(led_door,False)
		display(["      Smart     ","   Door Bell"])

dispatcher.add_handler(CommandHandler('user',userHandler))
dispatcher.add_handler(CommandHandler('open',userHandlerOpen))
dispatcher.add_handler(CommandHandler('close',userHandlerClose))
dispatcher.add_handler(CommandHandler('home',OwnerStatePresent))
dispatcher.add_handler(CommandHandler('notHome',OwnerStateAbsent))
dispatcher.add_handler(CommandHandler('peepHole',userPeepHole))
# updater.start_polling()

def main():
	global doorState
	operateLock(0)
	display(["      Smart     ","   Door Bell"])
	start , end, timeStayed = 0,0,0
	flag = False
			
	while True:
		val = GPIO.input(7)
		# print(val)
		if val == 0:
			start = time.time()
			while val!=1:	
				val = GPIO.input(7)
				timeStayed = time.time()-start
				if timeStayed >= 3:
					res =isknown()
					# res = True
					cam.stop()
					cv2.destroyAllWindows()
					print(timeStayed,res)
					sleep(1)
					if res == True:
						known()
					else:
						unknown()
					print("Out")
					# GPIO.output(buzzer_pin, GPIO.HIGH)
					# time.sleep(1)
					# GPIO.output(buzzer_pin, GPIO.LOW)

					start =0
					break
			updater.start_polling()
		# GPIO.cleanup() 

def smartSystem():
	with ThreadPoolExecutor() as executor:
		f1 =executor.submit(main)
		f2= executor.submit(checkIntrusion)
if __name__=="__main__":
	smartSystem()
	
