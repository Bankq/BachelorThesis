import random
from math import ceil
import Global as g

class VM:
    """ Virtual Machine"""
    def __init__(self):
        self.c_req = ceil(random.uniform(g.__VM_CPU_LOWER__,g.__VM_CPU_UPPER__))
        # self.c_req = random.choice([1.0,2.0,4.0])
        self.r_req = random.uniform(g.__VM_RAM_LOWER__,g.__VM_RAM_UPPER__)
        self.r_expt = random.uniform(g.__VM_RAM_EXPECTATION_LOWER__,g.__VM_RAM_EXPECTATION_UPPER__)
    
    def display_info(self):
        print self.c_req,self.r_req, self.r_expt


class PM:
    """ Physical Machine """
    def __init__(self):
        self.c_total = g.__PM_CPU__
        self.r_total = g.__PM_RAM__
        self.c_used = 0
        self.r_used = 0.0

    def display_info(self):
        print "CPU: ",self.c_used,"/",self.c_total
        print "RAM: ",self.r_used,"/",self.r_total
