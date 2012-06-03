#!/usr/bin/env python

# Solving the virtual machine placement problem using 
# simulated annealing algorithm
from __future__ import division  
import math
import random


import data

VM_MAX = 100
PM_MAX = 100
vm_list = []

SA_MAX = VM_MAX * PM_MAX * 100
MAX = 100
T = 100000

prob_count = 0

def init():
    """ initialization """
    vlist = []
    for i in range(VM_MAX):
        vlist.append(data.VM())
    return vlist

def sa(state):
    """ simulated annealing """
    term = 0

    cur_state = state
    cur_value = get_value(cur_state)
    # best_state = cur_state
    # best_value = cur_value

    
    temperature = cur_value * VM_MAX * PM_MAX # the initial temperature 
    abs_temperature = temperature * 1e-20

    while term < SA_MAX and temperature > abs_temperature:
        # neighbors = get_neighbors(cur_state)
        # neighbor = random.choice(neighbors)
        neighbor = get_neighbor(cur_state)
        new_value = get_value(neighbor)
        # for ne in neighbors:
        #     tvalue = get_value(ne)
        #     if tvalue < new_value:
        #         neighbor = ne
        #         new_value = tvalue

        if downhill(cur_value,new_value,temperature):
            # if new_value < best_value:
            #     best_value = new_value
            #     best_state = neighbor

            cur_state = neighbor
            cur_value = new_value
        term += 1
        temperature = cooldown(temperature,term)
        # print cur_value


    return cur_state

def cooldown(t,k): 
    # return t / math.log(1+k)
    return 0.89*t

def downhill(cur,new,t):
    global prob_count
    delta = new - cur
    if delta < 0:
        # if delta < 0 then take the new state
        # print new
        return True
    elif math.exp(-delta/t) > random.random():
        # prob_count+=1
        # print new,"*"
        return True
    return False

def get_neighbors(state):
    neighbors = []
    for i in range(10):
        neighbors.append(get_neighbor(state))
    return neighbors

def get_neighbor(state):
    """ find several neighbors in search space """
    new_state = []
    for s in state:
        new_state.append(s)
    for i in range(len(vm_list)//10):
        #random_swap(new_state)
        #random_reassign(new_state)
        shuffle(new_state)
    return new_state

def shuffle(state):
    src = random.randint(0,VM_MAX-1)
    des = random.randint(0,PM_MAX-1)
    v = vm_list[src]
    p = get_plist(state)[des]
    count = 0
    while not available(v,p):
        des = random.randint(0,PM_MAX-1)
        p = get_plist(state)[des]
        count += 1
    state[src] = des

def random_reassign(state):
    src = random.randint(0,len(state)-1) # pick one vm to reassign
    # des = state[random.randint(0,len(state)-1)] # pick one pm as the destination
    des = random.randint(0,PM_MAX-1)
    count = 0
    while not assignable(src,des,state) and count < MAX:
        des = state[random.randint(0,len(state)-1)]
        count += 1
    state[src] = des
    return

def assignable(src,des,state):
    temp_pm_list = get_plist(state)
    p = temp_pm_list[des]
    v = vm_list[src]
    if p.c_used + v.c_req <= p.c_total and p.r_used + (v.r_req * v.r_expt) <= p.r_total:
        return True

    return False


def get_plist(state):
    plist=[]
    for i in range(PM_MAX):
        plist.append(data.PM()) # plist initialize
    
    for i,s in enumerate(state):
        assign(vm_list[i],plist[s]) # plist info update

    return plist

def get_value(state):
    """ calculate the current state's value """
    # Reconstruct PM_LIST
    plist = get_plist(state)

    # value = ram_stdev(plist) * cpu_stdev(plist) * count_conflicts(plist) * count_active(plist) * 100
    value = count_active(plist)
    # value = ram_stdev(plist) * count_active(plist) * count_conflicts(plist)
    return value

def cpu_stdev(plist):
    s = 0.0 # sum
    s2 = 0.0 # square sum
    count = 0 # only count active
    for p in plist:
        if is_active(p):
            count += 1
            frac = p.c_used/p.c_total
            s += frac
            s2 += frac*frac
    mean = s / count
    stdev = math.sqrt((s2/count) - (mean*mean))
    return stdev

def ram_stdev(plist):
    s = 0.0 # sum
    s2 = 0.0 # square sum
    count = 0 # only count active
    for p in plist:
        if is_active(p):
            frac = p.r_used/p.r_total
            count += 1
            s += frac
            s2 += frac*frac
    mean = s / count
    stdev = math.sqrt((s2/count) - (mean*mean))
    return stdev
    

def count_active(plist):
    count  = 0
    for p in plist:
        if is_active(p):
            count += 1
    count = count / VM_MAX
    return count

def count_conflicts(plist):
    n = 0
    s = 0

    for p in plist:
        if p.r_used > p.r_total:
            s += p.r_used/p.r_total
            n += 1
    if n == 0:
        return 1
    value = s/n
    return value

def is_active(p):
    return p.c_used > 0 or p.r_used > 0

def first_fit(vlist):
    """ Using first fit approach """
    # cause PM list is as long as VM list
    # the ff approach can always succeed
    plist = []
    for i in range(PM_MAX):
        plist.append(data.PM())

    state = [0] * VM_MAX
    for vi,v in enumerate(vlist):
        for pi,p in enumerate(plist):
            if available(v,p):
                assign(v,p) # udpate pm info
                state[vi] = pi
                break
    return state

def random_fit(vlist):
    """ Using a random fit approach """
    plist = []
    for i in range(PM_MAX):
        plist.append(data.PM())

    state = [0] * VM_MAX
    for vi,v in enumerate(vlist):
        pi = random.randint(0,PM_MAX-1)
        p = plist[pi]
        while not available(v,p):
            pi = random.randint(0,PM_MAX-1)
            p = plist[pi]
        assign(v,p)
        state[vi] = pi
    return state

def available(v,p):
    return v.c_req + p.c_used <= p.c_total and v.r_req*v.r_expt + p.r_used <= p.r_total
    # return v.c_req + p.c_used <= p.c_total

def no_share_available(v,p):
    return v.c_req + p.c_used <= p.c_total and v.r_req + p.r_used <= p.r_total


def assign(v,p):
    p.c_used += v.c_req
    p.r_used += v.r_req

def is_valid(state):
    plist = get_plist(state)
    for p in plist:
        if p.c_used > p.c_total:
            return False
    return True

    

# state = sa(init("rf"))
# plist = get_plist(state)
# print count_active(plist),ram_stdev(plist),cpu_stdev(plist),count_conflicts(plist)
# value = get_value(state)

# print "Value: ",value
# # state = init()
# # plist = get_plist(state)
# # print count_active(plist),cpu_stdev(plist),ram_stdev(plist),count_active(plist)*cpu_stdev(plist)*ram_stdev(plist)


# ff_state = init("ff")
# ff_value = get_value(ff_state)
# ff_plist = get_plist(ff_state)
# print count_active(ff_plist),ram_stdev(ff_plist),cpu_stdev(ff_plist),count_conflicts(ff_plist)
# # plist = get_plist(ff_state)
# # print count_active(plist),cpu_stdev(plist),ram_stdev(plist),count_active(plist)*cpu_stdev(plist)*ram_stdev(plist)
# print "Value: ",ff_value

def test(nv,np):
    global VM_MAX
    global PM_MAX
    global vm_list
    VM_MAX = nv
    PM_MAX = np
    print nv,np

    vm_list = init()
    sa_state = sa(random_fit(vm_list))
    ff_state = first_fit(vm_list)

    plist = get_plist(state)
    count = count_active(plist)
    ram = ram_stdev(plist)
    cpu = cpu_stdev(plist)
    conf = count_conflicts(plist)
    value = get_value(state)

    print count,ram,cpu,conf
    print value
    print '***'

def test(nv,np):
    global vm_list
    global VM_MAX
    global PM_MAX
    VM_MAX = nv
    PM_MAX = np

    vm_list = init()
    state = random_fit(vm_list)
    state = sa(state)
    ff_state = first_fit(vm_list)
    plist = get_plist(state)
    ff_plist = get_plist(ff_state)
    
    value = get_value(state)
    ff_value = get_value(ff_state)
    
    ca = count_active(plist)
    ff_ca = count_active(ff_plist)
    
    ram = ram_stdev(plist)
    ff_ram = ram_stdev(ff_plist)
    
    cpu = cpu_stdev(plist)
    ff_cpu = cpu_stdev(ff_plist)
    
    cc = count_conflicts(plist)
    ff_cc = count_conflicts(ff_plist)

    print "$ N_v = %d $ & SA & %.3f & %.3f & %.3f & %.3f & %.3f \\\\ " %(nv,value,ca,ram,cpu,cc)
    print "$ N_v = %d $ & FF & %.3f & %.3f & %.3f & %.3f & %.3f \\\\ " %(nv,ff_value,ff_ca,ff_ram,ff_cpu,ff_cc)
    print "\\hline"


for n in range(100,1100,100):
    for i in range(5):
        test(n,n)
