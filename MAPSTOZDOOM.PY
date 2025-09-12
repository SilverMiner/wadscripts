#!/usr/bin/env python3

#21:25 08.03.2025 SilverMiner convert Heretic maps to MBF
#15:45 16.03.2025 add 3 modes
#15:34 27.05.2025 LIST ACTIONS

#PATIENTA = 'H:\\Games\\gzdoom413\\thewarprc1mapstopatch.wad'
#PATIENTA = "H:\\Games\\dsda262\\Eviternity II RC1.wad"
#PATIENTA = "H:\\Games\\Doom\\PL2.WAD"
#PATIENTA = "H:\Games\Doom\VAUMOD\MAPS\MAP01.WAD"
#PATIENTA = "H:\\Games\\Doom\\BLITZ.WAD"
#PATIENTA = "H:/Games/Doom/templeaa.wad"
PATIENTA = "H:/Games/Doom/RMG_CITY.wad"
from sys import argv
from omg import *
from omg.mapedit import *
import math
import copy
from hashlib import sha256

#GLOBAL CONSTANTS 16:01 30.05.2025
#STYPEMASK = 4192 #(1 << 5) | (1 << 6) | (1 << 12)
STYPEMASK = 96

#GLOBAL VARIABLES 14:31 30.05.2025
mapnames = []
terrainflats ={}
flatsonmbf21secs = set()

#chaska is tag to type dict
chaskaglobal = {}

#index to type
sitotypeglobal = {}

#index to tx_floor
sitoflatglobal = {}


#BRANCHES 18:48 30.05.2025
indexglobal = {}
tagglobal = {}

#TERRAIN NEEDED 14:40 31.05.2025
terrainneedglobal = {}
newtoformerglobal = {}
terrainneedset = set()

def findmbf21lines(map):
    ed = MapEditor(map)   
    for ld in ed.linedefs:
        if ld.action>=1024 and ld.action<=1026:
            print(map)
            break


def findmbf21sectors(map, name):
    global mapsdict
    mbf21secs = set()
    sitotype = {}
    sitoflat = {}
    chaska = {}
    
    ed = MapEditor(map)
    
    for si, sec in enumerate(ed.sectors):
        #if sec.tag!=0:
        if sec.tag in chaska:
            chaska[sec.tag].add(sec.type)
        else:
            chaska[sec.tag] = {sec.type}
        if sec.type & 4096:
            #mbf21secs.add((si, sec.tag))
            mbf21secs.add(si)
            #flatsonmbf21secs.add({sec.tx_floor:sec.type & STYPEMASK})
            #flatsonmbf21secs.add(sec.tx_floor)
            
        
    #no need to do this -> mbf21secs.discard(0)
    #i can access these sectors as well 14:19 30.05.2025

    #naxyu on nuzhen esli est btag i bindex 19:12 30.05.2025
    #mapsdict[name] = mbf21secs

    filtered_data = {
    key: num
    for key, value in chaska.items()
    if len(value) == 1
    for num in value
    if (num & 4096) != 0
}
    chaska = filtered_data
    if chaska: chaskaglobal[name] = chaska
    
    

    btag,bindex = set(),set()
    
    for si in mbf21secs:
        if ed.sectors[si].tag not in chaska.keys():
            sitotype[si]=ed.sectors[si].type
            sitoflat[si]=ed.sectors[si].tx_floor
            bindex.add(si)
            flatsonmbf21secs.add(ed.sectors[si].tx_floor)

    yetindices = mbf21secs - bindex
    for i3 in yetindices:
        btag.add(ed.sectors[i3].tag)
    #btag = []
    

    if bindex: indexglobal[name] = sorted(bindex)
    if btag: tagglobal[name] = sorted(btag)
    if sitotype: sitotypeglobal[name] = sitotype
    if sitoflat: sitoflatglobal[name] = sitoflat
    

                
                      
'''
inwad = WAD()
inwad.from_file(PATIENTA)
#for name in inwad.maps.find("*"):
for name in inwad.maps:
        listmapactions(name)
print(usedtags, usedactions)
'''

mode = 0
pattern = "*"

def getdonebyindex(si, sectype, flatone):
    global terrainflats,terrainneedglobal,newtoformerglobal,terrainneedset
    si2 = si if si!=0 else 32768
    flatfour = terrainflats.get(flatone,[f'{si} {sectype} {flatone}']*4)[sectype]
    terrainneedglobal[flatfour]=sectype
    newtoformerglobal[flatfour]=flatone
    terrainneedset.add(flatfour)
    
    return f'floortext(-{si2},"{flatfour}");\n'
    
#bytag done 12:08 31.05.2025
def getdonebytag(tag, sectype):
    
    if sectype == 0:
        return f'Sector_SetDamage({tag},999,14,1,0);\n' #kill if no radsuit or invul
    
    elif sectype == 1:
        return f'Sector_SetDamage({tag},1000,1000,1,255);\n' #instadeath

    elif sectype == 2:
        return f'Sector_SetDamage({tag},1,20,1,255);\n' #exit normal

    elif sectype == 3:
        return f'Sector_SetDamage({tag},1,25,1,255);' #secret exit
    
scriptStream = (
    '//FS BEGIN\n'
    '[SCRIPTS]\n'
                'int lnum = levelnum();\n'
'script 106 {\n'
   'int helth = trigger.objhealth();\n'
   'if (helth<=10)\n'
   '{\n'
    'healobj(trigger, 100-helth)\n;'
    '}\n'
    '}\n'
                'script 1 {\n'
                )
def genFSGLOBAL():
    global scriptStream
    for name in mapnames:
        lnum = int(name[3:])
        
        
        btag = tagglobal.get(name, {})
        bindex = indexglobal.get(name, {})

        sitotype = sitotypeglobal.get(name, {})
        sitoflat = sitoflatglobal.get(name, {})

        tagtotype = chaskaglobal.get(name, {})
        
        scriptStream += (f'if (lnum=={lnum})'
                         '{\n'
                         )
        for si in bindex:
            typea = (sitotype.get(si, 0)&0x60)>>5
            flatone = sitoflat.get(si, '')
            scriptStream += getdonebyindex(si, typea, flatone)
        for tag in btag:
            typeb = (tagtotype.get(tag, 0)&0x60)>>5
            scriptStream += getdonebytag(tag, typeb)

        
        scriptStream += 'return();}\n'
    scriptStream += ('}\n'
'startscript(1);\n'
'startscript(106);\n'
'//FS END\n'
                     )
    
    print(scriptStream)

TERRAINPROTO = (
'''//TN BEGIN
terrain FLR4096
{
DamageType Massacre
DamageAmount 1000
AllowProtection
}
terrain FLR4128
{
DamageType Massacre
DamageAmount 1000
}
terrain FLR4160
{
DamageType Exit
DamageAmount 1000
}
terrain FLR4192
{
DamageType Disintegrate
DamageAmount 1000
}
'''
    )

SECTYPE2NAMES = {
0:'FLR4096',
1:'FLR4128',
2:'FLR4160',
3:'FLR4192'
    }
terrainStream = copy.deepcopy(TERRAINPROTO)
def genTERRAIN():
    global terrainneedglobal,terrainStream
    #NEW FLATNAME : SECTYPE 14:47 31.05.2025

    for flatname, sectype in terrainneedglobal.items():
        terrainStream += f'floor {flatname} {SECTYPE2NAMES.get(sectype,"wtf")}\n'
    terrainStream += '//TN END'
    print(terrainStream)



texStream = '//TX BEGIN\n'
def genTEXTURES():
    global terrainneedglobal,texStream,terrainneedset
    
    for fa in terrainneedset:
        oldname = newtoformerglobal.get(fa,'wtf')
        texStream += f'Flat"{fa}",64,64' + '{' + f'Patch"{oldname}"'+',0,0}\n'
        
    texStream += '//TX END\n'
    print(texStream)
    
def funca(dicta):
    has1 = hash(dicta.keys())
    has2 = hash(dicta.values())
    has3 = has1^has2
    return f'F{int(has3) % 10_000_000:07d}'

def hashSilver(x):
    #return f"F{int(hash(x)) % 10_000_000:07d}"
    sha256_hash = hashlib.sha256(str(x).encode('utf-8')).hexdigest()
    return f"F{int(sha256_hash, 16) % 10_000_000:07d}"
def funcb(x):
    has1 = hashSilver(x+'fire')
    has2 = hashSilver(x+'earth')
    has3 = hashSilver(x+'air')
    has4 = hashSilver(x+'water')
    return [has1,has2,has3,has4]

def main(args):
    global pattern,mode,scriptStream,terrainflats,terrainneedglobal
    inwad = WAD()
    #outwad = WAD()    
    if (len(args) < 2):
        inwad.from_file(PATIENTA)
    else:
        #print ("Loading %s..." % args[0])
        inwad.from_file(PATIENTA)
        
    if (len(args) >= 3):
            for arg in args[2:]:
                    if arg in mode_map:
                            mode = mode_map.get(arg, 0)
                    else:
                            pattern = arg
                        
    for name in inwad.maps.find(pattern):
        mapnames.append(name)
        findmbf21sectors(inwad.maps[name], name)

    #print(chaskaglobal)
    
    #tx_floor to set of 4 terrain flats dict
    terrainflats = {
    word: funcb(word)
    for word in flatsonmbf21secs
    }
    #print(terrainflats)

    #print(indexglobal,tagglobal)
    
    genFSGLOBAL()
    genTERRAIN()
    genTEXTURES()
    

if __name__ == "__main__":
    main(argv[1:])

