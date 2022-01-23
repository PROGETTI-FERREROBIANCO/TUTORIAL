from machine import Pin
from utime import sleep
import _thread
import micropython
import select
import sys

micropython.kbd_intr(-1)

motori = {
    "X":Pin(0, Pin.OUT),
    "Y":Pin(1, Pin.OUT),
    "Z_SX":Pin(2, Pin.OUT),
    "Z_DX":Pin(3, Pin.OUT),
    "N":Pin(25, Pin.OUT) # pin led integrato
    }

blocco = _thread.allocate_lock()
pausa = 0.005

def muovi_altro_motore(id_motore):
    with blocco:
        motori[id_motore].value(1)
        sleep(pausa)
        motori[id_motore].value(0)
        sleep(pausa)

def main():
    while True:
        dati = ""
        run = True
        while run:
            while sys.stdin in select.select([sys.stdin], [], [], 0)[0]:        
                ch = sys.stdin.read(1)
                if ch != "\n" and ch != "\r":
                    if ch == ";":
                        run = False
                    else:
                        dati += ch
            
        # nel caso si volesse fare muove un solo motore si passa N come secondo motore
        dato1 = dati.split("#")[0]
        dato2 = dati.split("#")[1]
        
        blocco.acquire()
        _thread.start_new_thread(muovi_altro_motore, (dato2,))
        blocco.release()
        
        motori[dato1].value(1)
        sleep(pausa)
        motori[dato1].value(0)
        sleep(pausa)
        
        print("ok;")
        
        
main()