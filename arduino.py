#https://www.learnrobotics.org/blog/communication-between-arduino-python/
import serial
import time
import numpy as np

class Arduino():
    def __init__(self):
        # Arduino setup
        print('Program started')
        self.arduino = serial.Serial('/dev/cu.usbserial-14110', baudrate=9600, timeout=1)
        print('Established serial connection to Arduino')
        self.CONFIGURED = False
        self.outputs = list(np.ones(5)*535)
        print(self.outputs)

    def read(self):
            arduino_data = self.arduino.readline()
            arduino_data = str(arduino_data.decode("utf-8"))
            if not self.CONFIGURED:
                print("configuring...",arduino_data) 
                time.sleep(1)
                self.CONFIGURED = True
                self.outputs.append(520)
                print("done")
            else:
                self.outputs.append(int(arduino_data))

            print(len(self.outputs), self.outputs[-4:-1])

            if self.outputs[-2] < 600 and self.outputs[-2] > 400 and self.outputs[-1] < 600 and self.outputs[-1] > 400 and self.outputs[-0] < 600 and self.outputs[-0] > 400:
                return 0

            if self.outputs[-2] > 600 and self.outputs[-1] > 600:# long blow
                self.outputs = list(np.ones(5)*535)    
                return 1
                
            elif self.outputs[-2] < 400 and self.outputs[-1] < 400: # long breath
                self.outputs = list(np.ones(5)*535)
                return 2
            elif self.outputs[-3] < 600 and self.outputs[-2] > 600 and self.outputs[-1] < 600: #short blow
                self.outputs = list(np.ones(5)*535)    
                return 3

            elif self.outputs[-3] > 400 and self.outputs[-2] < 400 and self.outputs[-1] > 400: #short breath
                self.outputs = list(np.ones(5)*535)    
                return 4
                

    def stop(self):
        self.arduino.close()
        print('Connection closed')
        print('<----------------------------->')