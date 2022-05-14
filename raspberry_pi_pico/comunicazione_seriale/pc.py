import serial

pico = serial.Serial(port='/dev/ttyACM0', baudrate=115200)

pico.write(f"X#N;".encode())

run = True
s = ""
while run:
    ch = pico.read().decode() 
    if ch != "\n" and ch != "\r":
        if ch == ";":
            run = False
        else:
            s += ch
            
print(s)
