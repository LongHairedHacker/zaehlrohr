import socket, time
from PIL import Image, ImageFont, ImageDraw
import sys
import fileinput

UDPHOST="2001:67c:20a1:1063:ba27:ebff:fe86:8697"
UDPPORT=2323

FPS = 3

IMG_SIZE = (60, 120)
FONT_SIZE = 8

C_BLACK = (255, 255, 255)#(0, 0, 0)
C_WHITE = (0, 0, 0)      #(255, 255, 255)

sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

def list2byte(l):
    byte = 0
    i = 0
    for i in range(8):
        byte += 2**(7-i) if l[i] else 0
    return byte

def array2packet(a):
    return str(bytearray([list2byte(a[i*8:i*8+8]) for i in range(len(a)/8)]))

def str2array(event):
    image = Image.new("RGBA", IMG_SIZE, C_BLACK)
    draw = ImageDraw.Draw(image)
    draw.fontmode = "1" # No AA
    font = ImageFont.load_default()
    # font = ImageFont.truetype("FreeSans.ttf", FONT_SIZE)

    draw.text((3,1), "seiden", font=font, fill=C_WHITE)
    draw.text((3,9), "strasse", font=font, fill=C_WHITE)
    #draw.text((3,24), "top", font=font, fill=C_WHITE)
    draw.text((3,33), "cpasule", font=font, fill=C_WHITE)
    draw.text((3,42), "update:", font=font, fill=C_WHITE)
    draw.text((3,60), "%sm/s" % str(event["velocity"])[0:4], font=font, fill=C_WHITE)
    draw.text((3,69), "%s..." % event["start"][0:5], font=font, fill=C_WHITE)
    draw.text((3,78), "%s..." % event["end"][0:5], font=font, fill=C_WHITE)

    image = image.rotate(-90)

    image.show()

    imgmap = []
    for pixel in image.getdata():
        r, g, b, a = pixel
        if r == 255:
            imgmap.append(1)
        else:
            imgmap.append(0)
    return imgmap

#while True:


event = {"velocity" : 3.13456, "start" : "cbase", "end" : "EsterStock"}

sock.sendto(array2packet(str2array(event)), (UDPHOST, UDPPORT))
#array2packet(str2array(event))
print "Send !"
    #time.sleep(1.0/FPS)
