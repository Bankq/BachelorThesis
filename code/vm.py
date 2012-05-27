# class definition of Virtual machine request
import random
import Global as g

class VM:

    def __init__(self):
        self.c_req = random.uniform(g.__VM_CPU_LOWER__,g.__VM_CPU_UPPER__)
        self.r_req = random.uniform(g.__VM_RAM_LOWER__,g.__VM_RAM_UPPER__)
        self.r_expt = random.uniform(g.__VM_RAM_EXPECTATION_LOWER__,g.__VM_RAM_EXPECTATION_UPPER__)
    
    def test(self):
        print "____ VM _____"
        print "CPU: ",self.c_req
        print "RAM: ",self.r_req
        print "RAM EXPECTATION: ", self.r_expt


