#https://www.learnrobotics.org/blog/communication-between-arduino-python/
import serial
import time
class Arduino():
    def __init__(self):
        # Arduino setup
        print('Program started')
        self.arduino = serial.Serial('COM7', baudrate=9600, timeout=1)
        print('Established serial connection to Arduino')
        self.CONFIGURED = False

    def read(self):
            arduino_data = self.arduino.readline()
            arduino_data = str(arduino_data.decode("utf-8"))
            if not self.CONFIGURED:
                print("configuring...",arduino_data) 
                time.sleep(1)
                self.CONFIGURED = True
                return 530
                print("done")
            else:
                arduino_data = int(arduino_data)
                return arduino_data
                #print(arduino_data, type(arduino_data))
                #if arduino_data > 600:
                #    print("\nRIGHT\n")
                #    return "RIGHT"
                #elif arduino_data < 400:
                #    print("\nLEFT\n")
                #    return "LEFT"
    def stop(self):
        self.arduino.close()
        print('Connection closed')
        print('<----------------------------->')