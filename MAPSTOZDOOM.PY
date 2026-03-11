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
#PATIENTA = "H:/Games/Doom/RMG_CITY.wad"
#PATIENTA = "H:/Games/Doom/belot.wad"
#PATIENTA = "H:/Games/Doom/AdMortem_v1.5.6.wad"
#PATIENTA = "H:/Games/Doom/300lnmas.wad"
#PATIENTA = "H:/Games/Doom/SNOWBALL INSANITY [WINNKAR].wad"
#PATIENTA = "H:/Games/Doom/nt2f.wad"
#PATIENTA = 'H:/Games/Doom/The Warp RC1.wad'
#PATIENTA = 'H:/Games/Doom/andeimos_v1.1.wad'
PATIENTA = 'H:/Games/Doom/uacprime.wad'
PATIENTB = "H:/Games/Doom/DOOM2.wad"
anim_speeds = []
SECTYPE2NAMES = {
0:'FLR4096',
1:'FLR4128',
2:'FLR4160',
3:'FLR4192',
4:'FLR8192',
5:'FLR12288',
6:'FLR12320',
7:'FLR12352',
8:'FLR12384',
    }
SECTYPE3NAMES = {
0:'kill plr w/o prot-n',
1:'kill plr',
2:'kill plrs exit',
3:'kill plrs secret'
    }

warnings = ''
xlatStream = '' #22:19 16.01.2026

from sys import argv
from omg import *
from omg.mapedit import *
import math
import copy
from hashlib import sha256

#GLOBAL CONSTANTS 16:01 30.05.2025
#STYPEMASK = 4192 #(1 << 5) | (1 << 6) | (1 << 12)
STYPEMASK = 96

anim_parsed = []
anim_ranges = []
anim_good = []

#GLOBAL VARIABLES 14:31 30.05.2025
mapnames = []
terrainflats ={}
flatsonmbf21secs = set()

#tagtotype is tag to type dict
tagtotypeglobal = {}

#index to type
sitotypeglobal = {}

#index to tx_floor
sitoflatglobal = {}

#17:44 28.12.2025
#dict of dicts of si -> z_floor
sitoheightglobal = {}
heightglobal = {}

#21:10 16.01.2026
mbf21skiesglobal = {}


#BRANCHES 18:48 30.05.2025
indexglobal = {}
tagglobal = {}

#TERRAIN NEEDED 14:40 31.05.2025
terrainneedglobal = {}
newtoformerglobal = {}
terrainneedset = set()
def typetoa(num: int) -> int:
    """
    Вычисляет значение по формуле:
    -1 + (есть бит12?1:0) + (есть бит13?5:0) + ((число & 0x60) >> 5)
    """
    # Проверка бита 12 (нумерация битов с 0, так что бит 12 = 1 << 12)
    bit12 = 1 if (num & (1 << 12)) else 0
    
    # Проверка бита 13 (1 << 13)
    bit13 = 1 if (num & (1 << 13)) else 0
    
    if not (bit12 or bit13):
        return 0
    
    # Получаем биты 5 и 6 (0x60 = 01100000 в двоичной)
    bits_5_6 = (num & 0x60) >> 5
    
    # Вычисляем результат
    result = -1 + bit12 * 1 + bit13 * 5 + bits_5_6
    
    return result

def findmbf21lines(map):
    ed = MapEditor(map)   
    for ld in ed.linedefs:
        if ld.action>=1024 and ld.action<=1026:
            print(map)
            break

def problemnyj(sec):
    #4096 i 4128 ne problemnije. 4160 i 4192 problemnije
    da = sec.tx_floor == 'F_SKY1' and sec.type & 4096 and sec.type & 64 and sec.tag == 0
    return da

mbf21Stream = ''

def findmbf21sectors(map, name):
    global mapsdict, warnings, mbf21Stream
    mbf21lines = {}
    
    mbf21secs = set()
    mbf21skies = set() #21:06 16.01.2026
    sitotype = {}
    sitoflat = {}
    tagtotype = {}
    #17:32 28.12.2025
    sitoheight = {}

    #17:41 28.12.2025
    minheight = 0x7FFF
    
    #18:55 28.12.2025
    #minheight for all sectors except deadly
    #maxheight is for only deadly sectors
    maxheight = -32768

    ed = MapEditor(map)
    '''
    for ld in ed.linedefs:
        #if ld.action>=1024 and ld.action<=1026:
        if ld.flags&4096 or ld.flags&8192:
            mbf21lines[ld.flags]=name
    for key, value in mbf21lines.items():
        warnings += f'//{value} has {key}\n'
    '''
        
    for si, sec in enumerate(ed.sectors):
        warndone = False
        if problemnyj(sec):
            maxheight = max(maxheight, sec.z_floor)
            warnings += '//problemsky ' + name + f' {SECTYPE3NAMES.get((ed.sectors[si].type & 0x60) >> 5)} {ed.sectors[si].type} ' + str(si) + '\n'
            warndone = True
        else:
            minheight = min(minheight, sec.z_floor)
            
        sitoheight[si] = sec.z_floor
        
        if sec.tag in tagtotype:
            tagtotype[sec.tag].add(sec.type)
        else:
            tagtotype[sec.tag] = {sec.type}

        if sec.type & 8192:
            mbf21secs.add(si)
            warnings += '//' + name + f' {ed.sectors[si].type} si:{si} tag:{ed.sectors[si].tag}\n'
            if not sec.tag:
                warnings += '//ACHTUNG!'
            
        if sec.type & 4096:
            mbf21secs.add(si)
            if sec.tx_floor == 'F_SKY1':
                mbf21skies.add(sec.type & 4192)
            if not warndone:
                warnings += '//' + name + f' {SECTYPE3NAMES.get((ed.sectors[si].type & 0x60) >> 5)} {ed.sectors[si].type} si:{si} tag:{ed.sectors[si].tag}\n'
            #if (sec.type & 0x60) >> 5 < 2:
            #    maxheight
            
        
    #no need to do this -> mbf21secs.discard(0)
    #i can access these sectors as well 14:19 30.05.2025

    #naxyu on nuzhen esli est btag i bindex 19:12 30.05.2025
    #mapsdict[name] = mbf21secs

    filtered_data = {
    key: num
    for key, value in tagtotype.items()
    if len(value) == 1
    for num in value
    if (num & 4096) != 0
    #if (num & 12288) != 0
}
    tagtotype = filtered_data
    if tagtotype: tagtotypeglobal[name] = tagtotype
    
    

    btag,bindex = set(),set()
    
    for si in mbf21secs:
        if ed.sectors[si].tag not in tagtotype.keys():
            sitotype[si]=ed.sectors[si].type
            sitoflat[si]=ed.sectors[si].tx_floor
            bindex.add(si)
            flatsonmbf21secs.add(ed.sectors[si].tx_floor)
                
    yetindices = mbf21secs - bindex
    for i3 in yetindices:
        btag.add(ed.sectors[i3].tag)

    if bindex & btag:
        print('achtung')
        exit(0)

    for x in (4096, 4128):
        mbf21skies.discard(x)
    warnings += '//' + name + f' {mbf21skies}\n'

    if bindex: indexglobal[name] = sorted(bindex)
    if btag: tagglobal[name] = sorted(btag)
    if sitotype: sitotypeglobal[name] = sitotype
    if sitoflat: sitoflatglobal[name] = sitoflat
    if sitoheight: sitoheightglobal[name] = sitoheight
    heightglobal[name] = minheight, maxheight
    if mbf21skies: mbf21skiesglobal[name] = mbf21skies
    

                
                      
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
    flatfour = terrainflats.get(flatone,[f'{si} {sectype} {flatone}']*9)[sectype]
    terrainneedglobal[flatfour]=sectype
    newtoformerglobal[flatfour]=flatone
    terrainneedset.add(flatfour)
    
    return f'floortext(-{si2},"{flatfour}");\n'
    
#bytag done 12:08 31.05.2025
def getdonebytagold(tag, sectype):
#tag, amount, damagetype, interval, leaky     
    if sectype == 0:
        return f'Sector_SetDamage({tag},999,14,1,0);\n' #kill if no radsuit or invul
    
    elif sectype == 1:
        return f'Sector_SetDamage({tag},1000,1000,1,255);\n' #instadeath

    elif sectype == 2:
        return f'Sector_SetDamage({tag},1,20,1,255);\n' #exit normal

    elif sectype == 3:
        return f'Sector_SetDamage({tag},1,25,1,255);' #secret exit

#21:44 11.03.2026
def getdonebytag(tag, sectype):
    damage_params = {
        0: (999, 14, 1, 0),    # kill if no radsuit or invul
        1: (1000, 1000, 1, 255), # instadeath
        2: (1, 20, 1, 255),     # exit normal
        3: (1, 25, 1, 255),     # secret exit
    }
    
    params = damage_params.get(sectype)
    if params:
        return f'Sector_SetDamage({tag},{params[0]},{params[1]},{params[2]},{params[3]});\n'
    return ''
    
scriptStream = (
    '//FS BEGIN\n'
    '[SCRIPTS]\n'
                'int lnum = levelnum();\n'
'script 254 {\n'
   'int helth = trigger.objhealth();\n'
   'if (helth<=10)\n'
   '{\n'
    'healobj(trigger, 100-helth)\n;'
    '}\n'
#    '}\n'
#                'script 1 {\n'
                )
#17:30 28.12.2025 opiszu a to ja zabyl:
#jest localnyje slovari, a jest globalnyje
def genFSGLOBAL():
    global scriptStream, warnings, xlatStream
    for name in mapnames:
        heightHackNotUsed = True
        #xlatHackNotUsed = True
        xlatHackPossible = False
        hacksectypes = set() #22:04 16.01.2026
        
        mbf21uniq = mbf21skiesglobal.get(name, set())
        if len(mbf21uniq) < 2:
            xlatHackPossible = True
        else:
            temp271 = f'//{name} has 2 types of sky exits\n'
            warnings += temp271
            xlatStream += temp271
            
        lnum = int(name[3:])
        
        
        btag = tagglobal.get(name, {})
        bindex = indexglobal.get(name, {})

        sitotype = sitotypeglobal.get(name, {})
        sitoflat = sitoflatglobal.get(name, {})

        tagtotype = tagtotypeglobal.get(name, {})

#17:51 28.12.2025
        minheight, maxheight = heightglobal.get(name, {})
        sitoheight = sitoheightglobal.get(name, {})
        
        scriptStream += (f'if (lnum=={lnum})'
                         '{\n'
                         )
        for si in bindex:
            situpeja = sitotype.get(si, 0)
            #typea = (situpeja & 0x60) >> 5
            typea = typetoa(situpeja)
            flatone = sitoflat.get(si, '')
            
            # Основной случай - не sky или не тот тип
            if (typea > 1 and flatone != 'F_SKY1') or typea > 3:
                scriptStream += getdonebyindex(si, typea, flatone)
                continue
            
            # Обработка F_SKY1 с typea < 2
            if flatone == 'F_SKY1':
                
                #if situpeja & 4096 or situpeja & 4128:
                if typea < 2:
                    pass
                    #warnings += f'//{name} {si} deadly sky should be resolved by xlat\n'
                elif typea == 2:
                    warnings += f'//{name} {si} normal exit sky\n'
                elif typea == 3:
                    warnings += f'//{name} {si} secret exit sky\n'

                if typea > 1 and xlatHackPossible and situpeja not in hacksectypes:
                    #warnings += f'//{name} XLAT HACK SKY {"SECRET" if typea == 3 else "NORMAL"}EXIT\n\
#//sector {situpeja} = dDamage_LavaWimpy\n'
                    hacksectypes.add(situpeja)
                    xlatStream += f'//{name} XLAT HACK sector {situpeja} = dDamage_LavaWimpy;\n'
                    xlatStream += f'//501 = WALK|REP,Exit_{"Normal" if typea == 2 else "Secret"} (0)\n'
                    continue
                    
                
                if typea > 1 and heightHackNotUsed and not xlatHackPossible:
                    if maxheight <= minheight:
                        warnings += f'//{name} {si} {situpeja} HEIGHT HACK APPLIED\n'
                        if typea == 2:
                            scriptStream += f'''while(1==1) {{
                    if (trigger.objz <= {maxheight}) {{
                        exitlevel();
                    }}
                    wait(20);
                }}
                '''
                            heightHackNotUsed = False
                        elif typea == 3:
                            scriptStream += f'''while(1==1) {{
                    if (trigger.objz <= {maxheight}) {{
                        exitsecret();
                    }}
                    wait(20);
                }}
                '''
                            heightHackNotUsed = False
                        
                    else:
                        warnings += f'//{name} {si} deadly sky UNRESOLVABLE\n'
                
            
        for tag in btag:
            typeb = (tagtotype.get(tag, 0)&0x60)>>5
            scriptStream += getdonebytag(tag, typeb)

        
        scriptStream += 'return();}\n'
    scriptStream += ('}\n'
#'startscript(1);\n'
'startscript(254);\n'
'//FS END\n'
                     )
    
    print(scriptStream)

suffixes3 = [4096, 4128, 4160, 4192, 8192, 12288, 12320, 12352, 12384]
TERRAINPROTO = (
'''//TN BEGIN
splash SPL8192
{
	smallclass		SPL8192
	smallclip		0
	smallsound		None
	baseclass		SPL8192
	chunkclass		None
	chunkxvelshift	0
	chunkyvelshift	0
	chunkzvelshift	0
	chunkbasezvel	1
	sound			None
	noalert
}
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

terrain FLR8192
{
splash SPL8192
}

terrain FLR12288
{
DamageType Massacre
DamageAmount 1000
AllowProtection
splash SPL8192
}
terrain FLR12320
{
DamageType Massacre
DamageAmount 1000
splash SPL8192
}
terrain FLR12352
{
DamageType Exit
DamageAmount 1000
splash SPL8192
}
terrain FLR12384
{
DamageType Disintegrate
DamageAmount 1000
splash SPL8192
}
'''
    )


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

animStream = ''

def hashSilver(x):
    #return f"F{int(hash(x)) % 10_000_000:07d}"
    sha256_hash = hashlib.sha256(str(x).encode('utf-8')).hexdigest()
    return f"F{int(sha256_hash, 16) % 10_000_000:07d}"

def generateWordHashedList(x):
    return [hashSilver(x + str(s)) for s in suffixes3]

def parse_animated_lump(anim_lump):

    records = []
    while True:
        record_type = anim_lump[0]
        if record_type == 255:
            break
        is_flat = record_type == 0
        is_wall_texture = record_type in [1, 3]

        # Извлечение строк
        last_texture = anim_lump[1:10].split(b'\x00')[0].decode('utf-8')
        first_texture = anim_lump[10:20].split(b'\x00')[0].decode('utf-8')

        # Извлечение скорости анимации
        speed = int.from_bytes(anim_lump[19:23], 'little')
        records.append((first_texture.encode('utf-8'), last_texture.encode('utf-8'), speed))
        anim_lump = anim_lump[23:]
        
    return records
def doAnimEntry(word, wordHashed, x):
    global anim_ranges, anim_good, anim_speeds

    simple_list = [item for tup in anim_ranges for item in tup]
    #vid: str, str, int
    #print('simple_list', simple_list)
    entryStream = f'flat optional {wordHashed}\n'

    speed = anim_speeds[x]

    seekForPart = False
    memorizeWhere = 0
    whereInGood = 0
    waitForIf = False
    
    for i,anim in enumerate(anim_good[x:]):
        if anim == word:
            seekForPart = True
            waitForIf = True
        else:
            waitForIf = False
        if seekForPart:
            entryStream += f'pic {anim} tics {speed}\n'
            
            if waitForIf == False and anim in simple_list:
                memorizeWhere = simple_list.index(anim) - 1
                whereInGood = i
                break
            
    whok = simple_list[memorizeWhere]

    foundLeftPart = False
    for i,anim in enumerate(anim_good):
        if anim == word:
            break
        if anim == whok:
            foundLeftPart = True
        if foundLeftPart:
            entryStream += f'pic {anim} tics {speed}\n'
            
    return entryStream
    

def main(args):
    global pattern,mode,scriptStream,terrainflats,\
    terrainneedglobal,anim_good,anim_ranges,\
    animStream,anim_speeds,mbf21Stream,\
    texStream,xlatStream,tagtotypeglobal,sitotypeglobal
    inwad = WAD()
    #outwad = WAD()
	#0:45 28.12.2025
	
    if (len(args) < 2):
        inwad.from_file(PATIENTA)
    else:
        #print ("Loading %s..." % args[0])
        inwad.from_file(PATIENTA)
        
    isIwadAvailable = False
    try:
        iwad = WAD()
        iwad.from_file(PATIENTB)
        isIwadAvailable = True
    except Exception:
        print('guga')

    iwadflatlist=list(iwad.flats)
    pwadflatlist = [flat for flat in iwadflatlist if flat not in list(inwad.flats)] + list(inwad.flats)
    if 'ANIMATED' in inwad.data.keys():
        anim_lump = inwad.data['ANIMATED'].data
        anim_parsed = parse_animated_lump(anim_lump)
        anim_ranges = [(start.decode('ascii'), end.decode('ascii'), speed) for start, end, speed in anim_parsed]
        for start_name, end_name, sped in anim_ranges:
            try:
                start_idx = pwadflatlist.index(start_name)
                end_idx = pwadflatlist.index(end_name)
                
                # Добавляем все элементы между start_idx и end_idx включительно
                anim_good.extend(pwadflatlist[start_idx:end_idx + 1])
                anim_speeds.extend([sped] * (end_idx - start_idx + 1))
            except ValueError:
                # Если какого-то из элементов нет в списке, пропускаем
                continue

    # Убираем дубликаты, если диапазоны пересекаются

    #18:36 11.01.2026 razrulivanije widescreen stbarov
    if "STBAR" in inwad.graphics.keys():
        stbar = inwad.graphics["STBAR"]
        if stbar.width!=320:
            texStream += f'Texture "STBAR", {stbar.width}, {stbar.height}\n\
    {{\nOffset {stbar.width//2-160}, {stbar.height//2-16}\n\
    Patch "STBAR", 0, 0\n}}\n'
    
    if (len(args) >= 3):
            for arg in args[2:]:
                    if arg in mode_map:
                            mode = mode_map.get(arg, 0)
                    else:
                            pattern = arg
                        
    for name in inwad.maps.find(pattern):
        mapnames.append(name)
        findmbf21sectors(inwad.maps[name], name)

    #print(tagtotypeglobal)
    
    #tx_floor to set of 4 terrain flats dict

    for word in flatsonmbf21secs:
        wordHashedList = generateWordHashedList(word)
        terrainflats[word] = wordHashedList
        if word in anim_good:
            gugh = anim_good.index(word)
            for wordHashed in wordHashedList:
                if wordHashed in terrainneedset:
                    animStream += doAnimEntry(word, wordHashed, gugh)

    
    #print(terrainflats, terrainneedglobal, sitotypeglobal)
    #print(indexglobal,tagglobal)
    #print(tagtotypeglobal)
    #print(sitotypeglobal)
    print('sitotypeglobal:',sitotypeglobal,'tagtotypeglobal:',tagtotypeglobal)
    
    genFSGLOBAL()
    genTERRAIN()
    genTEXTURES()
    #genANIMDEFS()
            
    if animStream:
        print('//ANIMDEFS BEGIN\n',animStream,'//ANIMDEFS END\n',sep='\n')

    print(warnings)
    print(mbf21Stream)
    print(xlatStream)
    
    

if __name__ == "__main__":
    main(argv[1:])

#23:40 12.02.2026
#itak kak resolvit ekszon 8192. nado ponimat kuda on primenajetsa.

#17:59 07.03.2026
#ja ponael czo delat. no kod zdes oczen uze samobytnyj.
