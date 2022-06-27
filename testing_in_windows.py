#import badger2040
import qrcode
import time
import random
import uuid
from totp import totp
import os
#import badger_os
#import machine



def random_base32(length=32, chars = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')) -> str:
    # Note: the otpauth scheme DOES NOT use base32 padding for secret lengths not divisible by 8.divisible by 8.
    if length < 32:
        raise ValueError("Secrets should be at least 160 bits")

    return ''.join(
        random.choice(chars)
        for _ in range(length)
    )

def otp(b):
        time_current=int(time.time())

        print("time_current",time_current)
        (password, expiry) = totp(time_current, b, step_secs=30, digits=6)
        
        return password


#display = badger2040.Badger2040()
secret_key=random_base32()
print(secret_key)
value=0
val_a=0

def generate_qr():
        # Check that the qrcodes directory exists, if not, make it

    try:
        os.mkdir("qrcodes")
    except OSError:
        pass


    #generating otp
    timebased_otp=otp(secret_key)
    print(timebased_otp)
    
    
    text = open("qrcodes/qrcode.txt", "w")

    if value!=0:
        # make a UUID based on the host address and current time
        #micropythonuuid= machine.unique_id()
        micropythonuuid=uuid.uuid1()
        text.write(f"""https://api-loyalty.otherlink.io?user={micropythonuuid}?passcode={timebased_otp}\nDetails :\n*{timebased_otp}\n*micropythonuuid : {micropythonuuid}\n*  \n* """)
        text.flush()
        text.seek(0)
    else:
        #micropythonuuid= machine.unique_id()
        #micropythonuuid = machine.unique_id()
        micropythonuuid=uuid.uuid1()
        text.write(f"""otpauth://totp/Otherlink.io:micropythonuuid@otherlink.io?secret={secret_key}&issuer=Otherlink.io&algorithm=SHA1&digits=6&period=30\nDetails\n*{micropythonuuid}\n*SecretKey : {secret_key}\n* \n* """)
        text.flush()
        text.seek(0)
        

    # Load all available QR Code Files
    try:
        CODES = [f for f in os.listdir("qrcodes") if f.endswith(".txt")]
        TOTAL_CODES = len(CODES)
        print("TOTAL_CODES : ",TOTAL_CODES)
    except OSError:
        pass


    print(f'There are {TOTAL_CODES} QR Codes available:')
    for codename in CODES:
        print(f'File: {codename}')


    #generating qr code
    code = qrcode.QRCode()



    state = {
        "current_qr": 0
    }


    def measure_qr_code(size, code):
        w, h = code.get_size()
        module_size = int(size / w)
        return module_size * w, module_size


    def draw_qr_code(ox, oy, size, code):
        size, module_size = measure_qr_code(size, code)
        display.pen(15)
        display.rectangle(ox, oy, size, size)
        display.pen(0)
        for x in range(size):
            for y in range(size):
                if code.get_module(x, y):
                    display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


    def draw_qr_file(n):
        display.led(128)
        file = CODES[n]
        codetext = open("qrcodes/{}".format(file), "r")

        lines = codetext.read().strip().split("\n")
        code_text = lines.pop(0)
        title_text = lines.pop(0)
        detail_text = lines

        # Clear the Display
        display.pen(15)  # Change this to 0 if a white background is used
        display.clear()
        display.pen(0)

        code.set_text(code_text)
        size, _ = measure_qr_code(128, code)
        left = top = int((badger2040.HEIGHT / 2) - (size / 2))
        draw_qr_code(left, top, 128, code)

        left = 128 + 5

        display.thickness(2)
        display.text(title_text, left, 20, 0.5)
        display.thickness(1)

        top = 40
        for line in detail_text:
            display.text(line, left, top, 0.4)
            top += 10

        if TOTAL_CODES > 1:
            for i in range(TOTAL_CODES):
                x = 286
                y = int((128 / 2) - (TOTAL_CODES * 10 / 2) + (i * 10))
                display.pen(0)
                display.rectangle(x, y, 8, 8)
                if state["current_qr"] != i:
                    display.pen(15)
                    display.rectangle(x + 1, y + 1, 6, 6)
        display.update()


 
    #draw_qr_file(state["current_qr"])


#draw_clock()


generate_qr()

#time.sleep(6)

#button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_UP)
#button=button_b.value()
button=int(input("enter value"))

if button == 1:
    value=1
    while True:
        if val_a!=0:
            time.sleep(30)
        generate_qr()
        val_a +=1
    
else:
    print("error")
    

        




