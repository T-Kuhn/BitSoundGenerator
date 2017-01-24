import time
import math
import pigpio
import random

# - - - - - - - - - - - - - - - - 
# - - - BitSoundGenerator - - - -
# - - - - - - - - - - - - - - - -
class BitSoundGenerator:
    # - - - - - - - - - - - - - - - - - -
    # - - - - - - CONSTRUCTOR - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def __init__(self):
        self.pi = pigpio.pi('localhost', 8888)
        self.pinList = [23, 24]
        self.freqList = [10,20,40,50,80,100,160,200,250,320,400,500,800,1000,1600,2000,4000,80000]
        self.theta = 0.0
        for pin in self.pinList:
            self.pi.set_mode(pin, pigpio.OUTPUT) 
        self.setupPWM()
    # - - - - - - - - - - - - - - - - - -
    # - - - - - - Setup PWM - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def setupPWM(self):
        self.pi.set_PWM_frequency(23, 10)
        self.pi.set_PWM_range(23, 100)
        self.pi.set_PWM_dutycycle(23, 50) 

        self.pi.set_PWM_frequency(24, 1000)
        self.pi.set_PWM_range(24, 100)
        self.pi.set_PWM_dutycycle(24, 50) 

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - Mono Tone - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def monoTone(self):
        self.pi.set_PWM_dutycycle(24, 50)
        self.pi.set_PWM_dutycycle(23, 50)

    # - - - - - - - - - - - - - - - - - -
    # - - - -  send Serial Wave - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def sendSerialWave(self):
        self.pi.wave_clear() # clear any existing waveforms
        # self.pi.wave_get_max_pulses() <- This gives us 12000. Meaning that we can
        # use waves with up to 12000 pulses.
        # print self.pi.wave_get_max_micros() <- this gives us 1800 secs. Which is crazy.
        # this is possibly starnge.
        self.pi.wave_add_serial(23, 200, 'tari')
        f500 = self.pi.wave_create() # create and save id
        self.pi.wave_send_repeat(f500)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - update PWM  - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def updatePWM(self):
        fakeList = [5];
        for entry in self.freqList:
            self.pi.set_PWM_frequency(24, entry)
            for ent in self.freqList:
                if ent == entry:
                    self.pi.set_PWM_dutycycle(24, 0) 
                else:
                    self.pi.set_PWM_dutycycle(24, 50) 
                    self.pi.set_PWM_frequency(23, ent)
                    time.sleep(0.1)
            time.sleep(0.1)
        
    # - - - - - - - - - - - - - - - - - -
    # - - - - - - testing 1 - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def testing1(self):
        # First, we produce a 1 signal 250Hz tone
        # for 1 second
        self.pi.set_PWM_dutycycle(23, 50) 
        self.pi.set_PWM_dutycycle(24, 0) 
        self.pi.set_PWM_frequency(23, 250)
        time.sleep(5)
        # Then, we try the same with 500
        self.pi.set_PWM_frequency(23, 500)
        time.sleep(5)
        # Then, we try the same with 250 + 500
        self.pi.set_PWM_dutycycle(23, 50) 
        self.pi.set_PWM_dutycycle(24, 50) 
        self.pi.set_PWM_frequency(23, 250)
        self.pi.set_PWM_frequency(24, 500)
        time.sleep(5)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - testing 2 - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def testing2(self):
        # First, we produce a 1 signal 1000Hz tone
        # for 1 second
        self.pi.set_PWM_dutycycle(23, 50) 
        self.pi.set_PWM_dutycycle(24, 0) 
        self.pi.set_PWM_frequency(23, 1000)
        self.pi.set_PWM_frequency(24, 200)
        time.sleep(1)
        # Then, we compare with mixed signal 1
        self.pi.set_PWM_dutycycle(23, 50) 
        self.pi.set_PWM_dutycycle(24, 50) 
        self.pi.set_PWM_frequency(23, 1000)
        self.pi.set_PWM_frequency(24, 2000)
        time.sleep(1)
        # Then, we compare with mixed signal 2
        self.pi.set_PWM_dutycycle(23, 50) 
        self.pi.set_PWM_dutycycle(24, 50) 
        self.pi.set_PWM_frequency(23, 500)
        self.pi.set_PWM_frequency(24, 1000)
        time.sleep(1)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - signalMixing - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def signalMixing(self, s1, s2, dur):
        self.pi.set_PWM_frequency(23, s1)
        self.pi.set_PWM_frequency(24, s2)
        time.sleep(dur)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - testing 3 - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def testing3(self):
        self.signalMixing(250,500,1.0)
        self.signalMixing(400,800,1.0)
        self.signalMixing(500,1000,1.0)
        self.signalMixing(800,1600,1.0)
        time.sleep(1)
        self.signalMixing(400,1600,1.0)

    # - - - - - - - - - - - - - - - - - -
    # - - - - randomized Sound  - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def randomizedSound(self):
        while True:
            freq1 = random.choice(self.freqList)
            freq2 = random.choice(self.freqList)
            if freq1 == freq2:
                self.pi.set_PWM_dutycycle(24, 0) 
                self.signalMixing(freq1, freq2, random.randint(1,2)/10.0)
            else:
                self.pi.set_PWM_dutycycle(24, 50) 
                self.signalMixing(freq1, freq2, random.randint(1,2)/10.0)


    # - - - - - - - - - - - - - - - - - -
    # - - - - - - update  - - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def update(self):
        #self.cycleTime = 5000
        #self.startTime = self.getTimeInMilliSecs()
        #while self.startTime + self.cycleTime > self.getTimeInMilliSecs():


        while True:
            self.updatePWM()
            # sleep for 500ms
            time.sleep(0.02)

        self.testing1()

        self.randomizedSound()
        
        self.testing1()
        self.testing3()

        self.resetPWM()

    # - - - - - - - - - - - - - - - - - -
    # - - - get time in Millisecs - - - - 
    # - - - - - - - - - - - - - - - - - -
    def getTimeInMilliSecs(self):
        return int(time.time()*1000)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - reset PWM - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def resetPWM(self):
        self.pi.wave_tx_stop()
        self.pi.wave_clear() # clear any existing waveforms
        for pin in self.pinList:
            self.pi.set_PWM_frequency(pin, 200)
            self.pi.set_PWM_range(pin, 1000)
            self.pi.set_PWM_dutycycle(pin, 0) 


bitSoundGen = BitSoundGenerator()
#bitSoundGen.monoTone()
#bitSoundGen.sendSerialWave()
#bitSoundGen.sendGenericWave()
bitSoundGen.update()


# - - - - - - - - - - - - - - - - 
# - - - - - - MEMO  - - - - - - -
# - - - - - - - - - - - - - - - -

# [LED] White -> GPIO 24
# [SPEAKER] Gray -> GPIO 23

# so if we bitbanged that thing once every 1ms...
# ... we would get a 1000Hz tone!

# By bitbanging the thing out on the same
# sample frequency we can get back the exact same 1 bit sound sample
# we recorded before using that mic.



