import smbus, time
#import RoboPiLib as RPL
bus = smbus.SMBus(1)
# I2C address 0x29
# Register 0x12 has device ver. 
# Register addresses must be OR'ed with 0x80
bus.write_byte(0x29,0x80|0x12)
ver = bus.read_byte(0x29)
# version # should be 0x44
if ver == 0x44:
 print "Device found\n"
 bus.write_byte(0x29, 0x80|0x00) # 0x00 = ENABLE register
 bus.write_byte(0x29, 0x01|0x02) # 0x01 = Power on, 0x02 RGB sensors enabled
 bus.write_byte(0x29, 0x80|0x14) # Reading results start register 14, LSB then MSB
 while True:
  data = bus.read_i2c_block_data(0x29, 0)
  clear = clear = data[1] << 8 | data[0]
  red = data[3] << 8 | data[2]
  green = data[5] << 8 | data[4]
  blue = data[7] << 8 | data[6]
  if clear < 2000:
    primary = "No Object Found"
    #RPL.servoWrite(0,1)
  else:
    #RPL.servoWrite(0,0)
    if red > 25000 and green > 25000 and blue > 25000:
      primary = "white"



    elif red > blue and red > green:
      if blue > 5000 and green > 5000:
        if blue > green:
          primary = "pink"
        elif green > blue:
          primary = "orange"
      else:
        primary = "red"
    elif blue > red and blue > green:
      if red > 5000 and green > 5000:
        if red > green:
          primary = "purple"
	elif green > red:
	  primary = "turquoise"
      else:
	primary = "blue"
    elif green > red and green > blue:
      if green - red < 2000 and green - blue < 1000:
        primary = "black"
      elif red - green < 2000 and red -blue < 35000:
        primary = "yellow"
      else:
        primary = "green"
    else:
      primary = "undefined"
  crgb = "C: %s, R: %s, G: %s, B: %s\nPrimarily: %s" % (clear, red, green, blue, primary)
  print crgb
  time.sleep(1)
else: 
 print "Device not found\n"
