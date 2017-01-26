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
        if s1 == 0:
            self.pi.set_PWM_dutycycle(23, 0) 
        else:
            self.pi.set_PWM_dutycycle(23, 50) 
            self.pi.set_PWM_frequency(23, s1)
        if s2 == 0:
            self.pi.set_PWM_dutycycle(24, 0) 
        else:
            self.pi.set_PWM_dutycycle(24, 50) 
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
    # - - - - - hardwarePWMtest - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def hardwarePWMtest(self):
        self.pi.hardware_PWM(19, 500, 500000) 
        time.sleep(1.5)
        self.pi.hardware_PWM(19, 1000, 500000) 
        time.sleep(1.5)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - bitBangTest - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def bitBangTest(self):
        self.signalMixing(500,0,1.0)
        self.signalMixing(1000,0,1.0)
        self.resetPWM()
        self.pi.write(24,0)
        while True:
            self.pi.write(23,0)
            time.sleep(0.0002)
            self.pi.write(23,1)
            time.sleep(0.0002)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - waveTest  - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def waveTest(self):
        #self.pi.wave_tx_stop() # stop waveform 
        self.pi.wave_clear() # clear any existing waveforms
        G1 = 23
        NONE = 0
        wave=[]
        
        for i in range(1000):
            #                         ON     OFF   DELAY (usec)
            wave.append(pigpio.pulse(1<<G1, NONE, 200 + i))
            wave.append(pigpio.pulse(NONE, 1<<G1, 200 + i))
        
        self.pi.wave_add_generic(wave)
        waveId = self.pi.wave_create()
        self.pi.wave_send_once(waveId)
        

        time.sleep(2)
        self.pi.wave_tx_stop() # stop waveform

        

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - update  - - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def update(self):
        #self.cycleTime = 5000
        #self.startTime = self.getTimeInMilliSecs()
        #while self.startTime + self.cycleTime > self.getTimeInMilliSecs():
        
        self.resetPWM()
        #self.bitBangTest()
        #self.hardwarePWMtest() 
       
        self.waveTest()


        #while True:
        #    self.updatePWM()
        #    time.sleep(0.02)

        #self.testing1()
        #self.randomizedSound()
        #self.resetPWM()

    # - - - - - - - - - - - - - - - - - -
    # - - - get time in Millisecs - - - - 
    # - - - - - - - - - - - - - - - - - -
    def getTimeInMilliSecs(self):
        return int(time.time()*1000)

    # - - - - - - - - - - - - - - - - - -
    # - - - - - - reset PWM - - - - - - - 
    # - - - - - - - - - - - - - - - - - -
    def resetPWM(self):
        for pin in self.pinList:
            self.pi.set_PWM_frequency(pin, 1000)
            self.pi.set_PWM_range(pin, 200)
            self.pi.set_PWM_dutycycle(pin, 0) 


bitSoundGen = BitSoundGenerator()
bitSoundGen.update()


# - - - - - - - - - - - - - - - - 
# - - - - - - MEMO  - - - - - - -
# - - - - - - - - - - - - - - - -

# [LED] White -> GPIO 24
# [SPEAKER] Gray -> GPIO 23

# the only way to write out to the serial is to either use the 
# wave function or (maybe) one of the hardware serials.

# What about that hardware PWM.
# That sounds like a rather interesting thing, doesn't it.
# With it we can output any frequency we want!
# this is huge. One question here is what should we use as souce.
# but enough talk, let's just try hardware PWM!




