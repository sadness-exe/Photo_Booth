import RPi.GPIO as GPIO
import time
from picamera import PiCamera
from time import sleep
from PIL import Image
from PIL import Image, ImageDraw
from twython import Twython

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4,GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()
camera.rotation=180

segments = (16,20,3,21,15,2,26,14)
for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)
digits = (12,1,7,8)
for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)
 
num = {' ':(0,0,0,0,0,0,0),
    '0':(1,1,1,1,1,1,0),
    '1':(0,1,1,0,0,0,0),
    '2':(1,1,0,1,1,0,1),
    '3':(1,1,1,1,0,0,1),
    '4':(0,1,1,0,0,1,1),
    '5':(1,0,1,1,0,1,1),
    '6':(1,0,1,1,1,1,1),
    '7':(1,1,1,0,0,0,0),
    '8':(1,1,1,1,1,1,1),
    '9':(1,1,1,1,0,1,1),
    'y':(0,1,1,1,0,1,1),
    'e':(1,0,0,1,1,1,1),
    't':(0,0,0,1,1,1,1)}

def stitch():
    imageList = []
    Logo = Image.open('/home/manaciomatth/Python/Photo Booth/SUinterlock.png')
    Logo = Logo.resize((100,100))
    for i in range(4):
        imageList.append((Image.open('/home/manaciomatth/Python/Photo Booth/image%s.jpg' % i)).resize((500,500)))

    newImage = Image.new('RGB', (2000,500), (0, 0, 0))

    for j in range(4):
        newImage.paste(imageList[j], (0+500*j,0))

    draw = ImageDraw.Draw(newImage)
    VERT = 5
    HORZ = 2
    for j in range(VERT):
        if j == 0 or j == 4:
            draw.line((0+500*j,0,0+500*j,500), fill = (0,0,0), width=40)
        if j >= 1 or j<=3:
            draw.line((0+500*j,0,0+500*j,500), fill = (0,0,0), width=20)
    for h in range(HORZ):
        draw.line((0,0+500*h,2000,0+500*h), fill = (0,0,0), width=40)
        
    newImage.paste(Logo, (1900,400))
    newImage.save('/home/manaciomatth/Python/Photo Booth/finish.jpg')

def tweet():
    C_key = "feyRhfc4GDUGUfacSa5tewRqE" 
    C_secret = "vPBlYHv6Z5CeJYppz0N9I3f3mIA4m109MaV44uveFM74GEDPQ5" 
    A_token = "1193344979071954944-NFBnr0VBjYkd9ClUxsef7doXO3nrKb" 
    A_secret = "QpNLWZDAIY8CbF2XakW49ro1pfhg7jpKZXsegYKq2QVXA" 

    myTweet = Twython(C_key,C_secret,A_token,A_secret) 

    photo = open('/home/manaciomatth/Python/Photo Booth/finish.jpg', 'rb') 
    response = myTweet.upload_media(media=photo)
    myTweet.update_status(status='Checkout this totally yeeted out image!', media_ids=[response['media_id']])

def countdown():
    for digit in range(4):
         for loop in range(0,7):
                GPIO.output(segments[loop], num[displayString[digit]][loop])
                if digit == 0:
                    GPIO.output(14,1)
                else:
                    GPIO.output(14,0)
         GPIO.output(digits[digit], 0)
         time.sleep(0.0001)
         GPIO.output(digits[digit], 1)

def message():
    for digit in range(4):
         for loop in range(0,7):
             GPIO.output(segments[loop], num[displayString[digit]][loop])
         GPIO.output(digits[digit], 0)
         time.sleep(0.0001)
         GPIO.output(digits[digit], 1)

exe = True
if exe == True:
    exe = False
    while True:
        inputState = GPIO.input(4)
        if inputState == False:
            for i in range(4):
                camera.start_preview(alpha=200)
                x = 5000
                while x >= 0:
                    displayString = str(x).rjust(4)
                    if x == 0:
                        displayString = 'yeet'
                    countdown()
                    x -= 1
                x = 500
                while x >= 0:
                    if x<= 200:
                        displayString = 'yeet'
                    message()
                    x -= 1
                camera.capture('/home/manaciomatth/Python/Photo Booth/image%s.jpg' % i)
                camera.stop_preview()
                stitch()
            tweet() 
    exe = True
    
try:
    pass
finally:
    GPIO.cleanup()


