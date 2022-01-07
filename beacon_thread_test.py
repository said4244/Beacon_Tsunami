from scapy.all import Dot11, Dot11Beacon, Dot11Elt, RadioTap, sendp, hexdump, RandMAC

import time, sys, multiprocessing

class CreateBeacon:

  def __init__(self, ssid, number):

    #info for frame
    self.ssid = ssid
    self.number = number
    self.addr = RandMAC()
    self.iface = 'wlan0mon'

    self.dot11 = Dot11(type=0, subtype=8, 
    addr1='ff:ff:ff:ff:ff:ff', 
    addr2 = self.addr,
    addr3 = self.addr)

    #Beacon layer
    self.beacon = Dot11Beacon(cap='ESS+privacy')

    #Information Element
    self.essid = Dot11Elt(ID='SSID', info=self.ssid, len=len(self.ssid))
    self.rsn = Dot11Elt(ID='RSNinfo', info=(
    '\x01\x00'
    '\x00\x0f\xac\x02'
    '\x02\x00'
    '\x00\x0f\xac\x04'
    '\x00\x0f\xac\x02'
    '\x01\x00'
    '\x00\x0f\xac\x02'
    '\x00\x00'))

    #all layers stacked
    self.frame = RadioTap()/self.dot11/self.beacon/self.essid/self.rsn
  def Send(self):
    sendp(self.frame, inter=0.050, iface=self.iface, loop=1)



# class SendBeacon:
#   def __init__(self, frame):
#     self.frame = frame
  
#   def Send(self):

#     sendp(self.frame, inter=0.050, iface=self.iface, loop=1)



class MultiProcessBeacon:
  def __init__(self, ssid, number):
    self.ssid = ssid
    self.number = number

  def MultiProcessSend(self):
    for i in range(self.number):
      Beacon = CreateBeacon(ssid=self.ssid[i], number=self.number)
      i += 1
      str(i)
      # i = multiprocessing.Process(target=SendBeacon.Send, args=Beacon.frame)
      for _ in range(3):    #sending out the same beacon 3 times because for some reason sending only 1 beacon does not always work
        try:
          i = multiprocessing.Process(target=Beacon.Send)
          i.start()
        except KeyboardInterrupt:
          print('processes stopped')
          time.sleep(1)



class InputMain():
  def __init__(self):

    input_number = input('Enter how many fake AP\'s do you want (In intregers): ')#int(4)
    #intreger input handeling
    try:
      int(input_number)
      if int(input_number) == 0:
        print('well goodbye then....')
        time.sleep(1)
        sys.exit()
    except ValueError:
      print("ValueError detected; number of fake AP(s) = 1")
      time.sleep(1)
      input_number = int(1)
    

    input_ssid = []#('s-one', 's-two', 's-three', 's-fore') #we'll make it first a list so we can append stuff to it
    for n in range(int(input_number)):
      n += 1 #because it starts with 0
      ask_ssid = input('Name SSID for AP number ' + str(n)+': ')

      if len(ask_ssid) > 32:
        print('Maximum length of ssid exceeded.')
        ask_ssid = ask_ssid[32]
      input_ssid.append(ask_ssid)

    tuple(input_ssid)
    
    self.given_number = int(input_number)
    self.given_ssid = input_ssid
    passInfo_toMulti = MultiProcessBeacon(ssid=self.given_ssid, number=self.given_number)
    passInfo_toMulti.MultiProcessSend()

start = InputMain()