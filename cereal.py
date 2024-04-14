import serial

ser = serial.Serial('/dev/ttyACM0',9600, timeout=1)
while True:
  read_serial=ser.readline()
  # s[0] = int (read_serial,16)
  # print(s)
  print(read_serial)