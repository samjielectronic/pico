from mfrc522 import MFRC522
from machine import Pin
import utime

led_1=Pin(16,Pin.OUT)
led_2=Pin(17,Pin.OUT)

led_1.value(0)
led_2.value(0)

def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
    
              
reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

print("")
print("Please place card on reader")
print("")



PreviousCard = [0]

try:
    while True:

        reader.init()
        (stat, tag_type) = reader.request(reader.REQIDL)
        #print('request stat:',stat,' tag_type:',tag_type)
        if stat == reader.OK:
            (stat, uid) = reader.SelectTagSN()
            if uid == PreviousCard:
                continue
            if stat == reader.OK:
                print("Card detected {}  uid={}".format(hex(int.from_bytes(bytes(uid),"little",False)).upper(),reader.tohexstring(uid)))
                defaultKey = [255,255,255,255,255,255]
                reader.MFRC522_DumpClassic1K(uid, Start=0, End=64, keyA=defaultKey)
                print("Done")
                PreviousCard = uid
            else:
                pass
            if uid==[0x09, 0x99, 0x73, 0xA2]:#insert your id card or tag
                led_1.value(1)
                led_2.value(0)
            if uid==[0xF7, 0x5D, 0x4C, 0x62]:#insert your id card or tag
                led_1.value(0)
                led_2.value(1) 
        else:
            PreviousCard=[0]
        utime.sleep_ms(50)                

except KeyboardInterrupt:
    pass