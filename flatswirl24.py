#done at 20:04 01.09.2025 UTC+3 SilverMiner
from math import sin, pi, floor
import copy

offset = [0]*4096
distortedflat = [255]*4096

flatname = 'WTRA.dat'
flatarray = []

def displace_amount(location, PERIOD = 64, AMP = 4, PHASE_SHIFT = 0):
    phi = PHASE_SHIFT / 360.0
    return AMP*sin(2 * pi * (location/PERIOD - phi))

#def ripple_vertical(x,y,)

with open(flatname, 'rb') as flat:
    normalflat = flat.read()
    

# horizontal ripple    
for phase_shift in range (45, 360+45, 45):
    for y in range (0, 64):
        for x in range (0, 64):
            x1 = x + displace_amount(location = y, PERIOD = 64, AMP = 4, PHASE_SHIFT = phase_shift)
            x1 = floor(x1)
            x1 &= 63
            offset[(y<<6)+x] = (y<<6) + x1
            
    for i in range(0, 4096):
        if distortedflat[i] != normalflat[offset[i]]:
            distortedflat[i] = normalflat[offset[i]]
    flatarray.append(copy.deepcopy(distortedflat))

perdun = copy.deepcopy(flatarray * 3)

# x,y -> y,x transformation
for k in range (0, 24):
    kal = 30 * (k % 12)
    perdun2 = copy.deepcopy(perdun[k])
    for x in range (0, 64):
        for y in range (0, 64):
            perdun[k][(x<<6)+y] = perdun2[(y<<6) + x]
            
    for y in range (0, 64):
        for x in range (0, 64):
            y1 = y + displace_amount(location = x, PERIOD = 64, AMP = 6, PHASE_SHIFT = kal)
            y1 = floor(y1)
            y1 &= 63
            offset[(y<<6)+x] = (y1<<6) + x
            
    perdun2 = copy.deepcopy(perdun[k])
    for x in range (0, 64):
        for y in range (0, 64):
            perdun[k][(x<<6)+y] = perdun2[(y<<6) + x]
            
    for i in range(0, 4096):
        if distortedflat[i] != perdun[k][offset[i]]:
            distortedflat[i] = perdun[k][offset[i]]
            
    durak = bytearray(distortedflat)
    vihod = open('GUIA'+str(k+1), 'wb')
    vihod.write(durak)
    vihod.close()
        
