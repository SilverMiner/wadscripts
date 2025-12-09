# (deh3dec150535) 21:13 20.05.2025 UTC+3 SilverMiner:
# started making this python script on May 6 2025 17:47 UTC+3
from sys import argv
from dataclasses import dataclass, fields
import copy
from collections import defaultdict
#from typing import List
vivod=''
newdecorate=''
wha = 'H:\\Compilers\\dehacked2decorate\\BaseTables\\'
#patient = 'H:\\Compilers\\dehacked2decorate\\DEHACKEDblitz.txt'
#patient = "H:\\Games\\Doom\\desultoryzdoom\\decohack\\dehacked.deh"
#patient = "H:\\Games\\dsda262\\DEHACKEDEVITERNITY2.txt"
#patient = "H:/Games/Doom/templeaaaaDEHACKED.txt"
#patient = "H:/Games/Doom/DEHACKEDmishka.txt"
#patient = "H:/Games/Doom/DEHACKEDRMG_City.txt"
#patient = "H:/Games/Doom/dbp50stalk17.bex"
patient = "H:/Games/Doom/DEHACKEDadmortem.txt"
files = ['base_states2.dat','base_things.dat']
labelDict = {}

sprAliases = {}

#1:28 21.06.2025
sfxAliases = {}

curwepnammotype = -1
curwepnammouse = -1
curactor = -1


def BUKVATABLE(num):
    if num < 0:
        return "Invalid input: number must be non-negative"
    
    if num < 29:
        return chr(65 + num)  # A-Z
    else:
        #return "Out of range"
        return num
def int32tofixed(x):
    return round(x / 65536.0, 4)
def getActorName(num):
    try:
        return ZDOOMNAMES[num]
    except Exception:
        return "Deh_Actor_{x}".format(x=num-1)
        
def getSoundName(num):
    DSFX = 'dehextra/sound'
    if num <= 141:
        return ZDOOMSOUNDNAMES[num]
    elif num >= 500:
        tempright = "{:03d}".format(num - 500)
        return DSFX+tempright
    return ""
MBFFLAGS = {
    0x00000001: "SPECIAL",
    0x00000002: "SOLID",
    0x00000004: "SHOOTABLE",
    0x00000008: "NOSECTOR",
    0x00000010: "NOBLOCKMAP",
    0x00000020: "AMBUSH",
    0x00000040: "JUSTHIT",
    0x00000080: "JUSTATTACKED",
    0x00000100: "SPAWNCEILING",
    0x00000200: "NOGRAVITY",
    0x00000400: "DROPOFF",
    0x00000800: "PICKUP",
    0x00001000: "NOCLIP",
    0x00002000: "SLIDE",
    0x00004000: "FLOAT",
    0x00008000: "TELEPORT",
    0x00010000: "MISSILE",
    0x00020000: "DROPPED",
    0x00040000: "SHADOW",
    0x00080000: "NOBLOOD",
    0x00100000: "CORPSE",
    0x00200000: "INFLOAT",
    0x00400000: "COUNTKILL",
    0x00800000: "COUNTITEM",
    0x01000000: "SKULLFLY",
    0x02000000: "NOTDMATCH",
    #0x04000000: "TRANSLATION1",
    #0x08000000: "TRANSLATION2",
    0x10000000: "TOUCHY",
    #0x20000000: "BOUNCES",
    0x40000000: "FRIENDLY",
    #0x80000000: "TRANSLUCENT"
}
MBF21FLAGS = {
    0x00000001: "LOWGRAVITY",# "LOGRAV",
    0x00000002: "SHORTMISSILERANGE",#"SHORTMRANGE",
    #0x00000004: "DMGIGNORED",
    0x00000008: "NORADIUSDMG",
    0x00000010: "FORCERADIUSDMG",
    #0x00000020: "HIGHERMPROB",
    #0x00000040: "RANGEHALF",
    #0x00000080: "NOTHRESHOLD",
    #0x00000100: "LONGMELEE",
    0x00000200: "BOSS",
    #0x00000400: "MAP07BOSS1",
    #0x00000800: "MAP07BOSS2",
    #0x00001000: "E1M8BOSS",
    #0x00002000: "E2M8BOSS",
    #0x00004000: "E3M8BOSS",
    #0x00008000: "E4M6BOSS",
    #0x00010000: "E4M8BOSS",
    0x00020000: "RIPPER", #"RIP",
    0x00040000: "FULLVOLACTIVE" #"FULLVOLSOUNDS"
}
def get_flags_diff(flags_a, flags_b, flagtable = MBFFLAGS):
    flags_diff = flags_a ^ flags_b
    result = []
    znak = ''
    for flag in sorted(flagtable.keys()):
        if flags_diff & flag:
            znak = '+' if flags_b & flag else '-'
            result.append(f"{znak}{flagtable.get(flag,'')}")
    if flags_diff & 0x00040000:
        if flagtable == MBFFLAGS:
            result.append('RenderStyle OptFuzzy\nAlpha 0.5')
    if flags_diff & 0x20000000:
        if flagtable == MBFFLAGS:
            result.append('BounceType Grenade')
    if flags_diff & 0x80000000:
        if flagtable == MBFFLAGS:
            result.append('RenderStyle Translucent\nAlpha 0.5')
    if flags_b & 0x00004000:
        if flagtable == MBFFLAGS:
            result.append('+NOBLOCKMONST')

    return "\n".join(result)

def flags_to_list_of_strings(flags_a, flags_b, flagtable = MBFFLAGS):
    flags_diff = flags_a ^ flags_b
    result = []
    #znak = ''
    for flag in sorted(flagtable.keys()):
        if flags_diff & flag:
            #znak = '+' if flags_b & flag else '-'
            result.append(f"{flagtable.get(flag,'')}")
    return result
def flags_for_checks(flags_a, flags_b, flagtable = MBFFLAGS):
    
    flags_diff = flags_a ^ flags_b
    Vflags,Xflags = [],[]
    for flag in sorted(flagtable.keys()):
        if flags_diff & flag:
            if flags_b & flag:
                Vflags.append(f"{flagtable.get(flag,'')}")
            else:
                Xflags.append(f"{flagtable.get(flag,'')}")
                
    return Xflags,Vflags

ZDOOMSOUNDNAMES = [
    "",
	"weapons/pistol",
	"weapons/shotgf",
	"weapons/shotgr",
	"weapons/sshotf",
	"weapons/sshoto",
	"weapons/sshotc",
	"weapons/sshotl",
	"weapons/plasmaf",
	"weapons/bfgf",
	"weapons/sawup",
	"weapons/sawidle",
	"weapons/sawfull",
	"weapons/sawhit",
	"weapons/rocklf",
	"weapons/bfgx",
	"imp/attack",
	"imp/shotx",
	"plats/pt1_strt",
	"plats/pt1_stop",
	"doors/dr1_open",
	"doors/dr1_clos",
	"plats/pt1_mid",
	"switches/normbutn",
	"switches/exitbutn",
	"*pain100",
	"demon/pain",
	"grunt/pain",
	"vile/pain",
	"fatso/pain",
	"pain/pain",
	"misc/gibbed",
	"misc/i_pkup",
	"misc/w_pkup",
	"*land",
	"misc/teleport",
	"grunt/sight",
	"grunt/sight",
	"grunt/sight",
	"imp/sight",
	"imp/sight",
	"demon/sight",
	"caco/sight",
	"baron/sight",
	"cyber/sight",
	"spider/sight",
	"baby/sight",
	"knight/sight",
	"vile/sight",
	"fatso/sight",
	"pain/sight",
	"skull/melee",
	"demon/melee",
	"skeleton/melee",
	"vile/start",
	"imp/melee",
	"skeleton/swing",
	"*death",
	"*xdeath",
	"grunt/death",
	"grunt/death",
	"grunt/death",
	"imp/death",
	"imp/death",
	"demon/death",
	"caco/death",
	"misc/unused",
	"baron/death",
	"cyber/death",
	"spider/death",
	"baby/death",
	"vile/death",
	"knight/death",
	"pain/death",
	"skeleton/death",
	"grunt/active",
	"imp/active",
	"demon/active",
	"baby/active",
	"baby/walk",
	"vile/active",
	"*grunt",
	"world/barrelx",
	"*fist",
	"cyber/hoof",
	"spider/walk",
	"weapons/chngun",
	"misc/chat2",
	"doors/dr2_open",
	"doors/dr2_clos",
	"misc/spawn",
	"vile/firecrkl",
	"vile/firestrt",
	"misc/p_pkup",
	"brain/spit",
	"brain/cube",
	"brain/sight",
	"brain/pain",
	"brain/death",
	"fatso/attack",
	"fatso/death",
	"wolfss/sight",
	"wolfss/death",
	"keen/pain",
	"keen/death",
	"skeleton/active",
	"skeleton/sight",
	"skeleton/attack",
	"misc/chat",
	"dog/sight",
	"dog/attack",
	"dog/active",
	"dog/death",
	"dog/pain"
]
ZDOOMNAMES=[
    "OFFSET", #Exists to offset index to start at 1
	"DoomPlayer",
	"ZombieMan",
	"ShotgunGuy",
	"Archvile",
	"ArchvileFire",
	"Revenant",
	"RevenantTracer",
	"RevenantTracerSmoke",
	"Fatso",
	"FatShot",
	"ChaingunGuy",
	"DoomImp",
	"Demon",
	"Spectre",
	"Cacodemon",
	"BaronOfHell",
	"BaronBall",
	"HellKnight",
	"LostSoul",
	"SpiderMastermind",
	"Arachnotron",
	"Cyberdemon",
	"PainElemental",
	"WolfensteinSS",
	"CommanderKeen",
	"BossBrain",
	"BossEye",
	"BossTarget",
	"SpawnShot",
	"SpawnFire",
	"ExplosiveBarrel",
	"DoomImpBall",
	"CacodemonBall",
	"Rocket",
	"PlasmaBall",
	"BFGBall",
	"ArachnotronPlasma",
	"BulletPuff",
	"Blood",
	"TeleportFog",
	"ItemFog",
	"TeleportDest",
	"BFGExtra",
	"GreenArmor",
	"BlueArmor",
	"HealthBonus",
	"ArmorBonus",
	"BlueCard",
	"RedCard",
	"YellowCard",
	"YellowSkull",
	"RedSkull",
	"BlueSkull",
	"Stimpack",
	"Medikit",
	"Soulsphere",
	"InvulnerabilitySphere",
	"Berserk",
	"BlurSphere",
	"RadSuit",
	"Allmap",
	"Infrared",
	"Megasphere",
	"Clip",
	"ClipBox",
	"RocketAmmo",
	"RocketBox",
	"Cell",
	"CellPack",
	"Shell",
	"ShellBox",
	"Backpack",
	"BFG9000",
	"Chaingun",
	"Chainsaw",
	"RocketLauncher",
	"PlasmaRifle",
	"Shotgun",
	"SuperShotgun",
	"TechLamp",
	"TechLamp2",
	"Column",
	"TallGreenColumn",
	"ShortGreenColumn",
	"TallRedColumn",
	"ShortRedColumn",
	"SkullColumn",
	"HeartColumn",
	"EvilEye",
	"FloatingSkull",
	"TorchTree",
	"BlueTorch",
	"GreenTorch",
	"RedTorch",
	"ShortBlueTorch",
	"ShortGreenTorch",
	"ShortRedTorch",
	"Stalagtite",
	"TechPillar",
	"Candlestick",
	"Candelabra",
	"BloodyTwitch",
	"Meat2",
	"Meat3",
	"Meat4",
	"Meat5",
	"NonsolidMeat2",
	"NonsolidMeat4",
	"NonsolidMeat3",
	"NonsolidMeat5",
	"NonsolidTwitch",
	"DeadCacodemon",
	"DeadMarine",
	"DeadZombieMan",
	"DeadDemon",
	"DeadLostSoul",
	"DeadDoomImp",
	"DeadShotgunGuy",
	"GibbedMarine",
	"GibbedMarineExtra",
	"HeadsOnAStick",
	"Gibs",
	"HeadOnAStick",
	"HeadCandles",
	"DeadStick",
	"LiveStick",
	"BigTree",
	"BurningBarrel",
	"HangNoGuts",
	"HangBNoBrain",
	"HangTLookingDown",
	"HangTSkull",
	"HangTLookingUp",
	"HangTNoBrain",
	"ColonGibs",
	"SmallBloodPool",
	"BrainStem",
# Boom additional actors:
	"PointPusher",
	"PointPuller",
# MBF additional actors:
	"MBFHelperDog",
	"PlasmaBall1",
	"PlasmaBall2",
	"EvilSceptre",
	"UnholyBible",
#Actors added since Fist/Pistol can be changed despite not being things

]
ZDOOMTHINGSTATES=[
    "Spawn",
    "See",
    "Pain",
    "Melee",
    "Missile",
    "Death",
    "XDeath",
    "Raise",
    "Select",
    "Deselect",
    "Ready",
    "Fire",
    "Flash"
]

WEAPONIDS = [
78, #shotgun 2
74, #chaingun 3
76, #rocket 4
77, #plasma 5
73, #bfg 6
75, #chainsaw 7
79, #ssg 8
    ]
#20:20 21.05.2025
ZDOOMAMMONAMES =[
    "Clip",
    "Shell",
    "Cell",
    "RocketAmmo",
    "" #infinite
]
#Name of sprites in ZDoom
ZDOOMSPRITENAMES=[
	"TROO","SHTG","PUNG","PISG","PISF","SHTF","SHT2","CHGG","CHGF","MISG",
	"MISF","SAWG","PLSG","PLSF","BFGG","BFGF","BLUD","PUFF","BAL1","BAL2",
	"PLSS","PLSE","MISL","BFS1","BFE1","BFE2","TFOG","IFOG","PLAY","POSS",
	"SPOS","VILE","FIRE","FATB","FBXP","SKEL","MANF","FATT","CPOS","SARG",
	"HEAD","BAL7","BOSS","BOS2","SKUL","SPID","BSPI","APLS","APBX","CYBR",
	"PAIN","SSWV","KEEN","BBRN","BOSF","ARM1","ARM2","BAR1","BEXP","FCAN",
	"BON1","BON2","BKEY","RKEY","YKEY","BSKU","RSKU","YSKU","STIM","MEDI",
	"SOUL","PINV","PSTR","PINS","MEGA","SUIT","PMAP","PVIS","CLIP","AMMO",
	"ROCK","BROK","CELL","CELP","SHEL","SBOX","BPAK","BFUG","MGUN","CSAW",
	"LAUN","PLAS","SHOT","SGN2","COLU","SMT2","GOR1","POL2","POL5","POL4",
	"POL3","POL1","POL6","GOR2","GOR3","GOR4","GOR5","SMIT","COL1","COL2",
	"COL3","COL4","CAND","CBRA","COL6","TRE1","TRE2","ELEC","CEYE","FSKU",
	"COL5","TBLU","TGRN","TRED","SMBT","SMGT","SMRT","HDB1","HDB2","HDB3",
	"HDB4","HDB5","HDB6","POB1","POB2","BRS1","TLMP","TLP2",
	"TNT1","DOGS","PLS1","PLS2","BON3","BON4","BLD2"
]
#length of this^ is 145, the bld2 index is 144
#SP00 is 145 in dehacked
#lenZDSPRN
def zdoomspritenames(x):
    if x not in sprAliases.keys():
        if x < len(ZDOOMSPRITENAMES):
            return ZDOOMSPRITENAMES[x]
        else:
            y = x - len(ZDOOMSPRITENAMES)
            return 'SP{:02d}'.format(y)
    else:
        return sprAliases.get(x)
PAIRS = [
[0,0],
[1,9],
[2,1],
[3,10],
[4,17],
[5,6],
[6,18],
[7,11],
[8,7],
[9,19],
[10,12],
[11,13],
[12,14],
[13,15],
[14,20],
[15,2],
[16,3],
[17,4],
[18,8],
[19,5],
[20,21],
[21,22],
[23,16]
]
THING_FIELD_MAP = {
'index': 'Thing',
'doomednum': 'ID #',
'spawnstate': 'Initial frame',
'spawnhealth': 'Hit points',
'seestate': 'First moving frame',
'seesound': 'Alert sound',
'reactiontime': 'Reaction time',
'attacksound': 'Attack sound',
'painstate': 'Injury frame',
'painchance': 'Pain chance',
'painsound': 'Pain sound',
'meleestate': 'Close attack frame',
'missilestate': 'Far attack frame',
'deathstate': 'Death frame',
'xdeathstate': 'Exploding frame',
'deathsound': 'Death sound',
'speed': 'Speed',
'radius': 'Width',
'height': 'Height',
'mass': 'Mass',
'damage': 'Missile damage',
'activesound': 'Action sound',
'flags': 'Bits',
'flags2': 'Bits2',
'raisestate': 'Respawn frame',
'droppeditem': 'Dropped item',
'infighting_group': 'Infighting group',
'projectile_group': 'Projectile group',
'splash_group': 'Splash group',
'flags21': 'MBF21 Bits',
'ripsound': 'Rip sound',
'altspeed': 'Fast speed',
'meleerange': 'Melee range',
'bloodcolor': 'Blood color'
    }

STATE_FIELD_MAP = {
    'index': 'Frame',
    'sprite': "Sprite number",
    'frame': "Sprite subnumber",
    'tics': "Duration",
    'nextstate': "Next frame",
    'misc1': "Unknown 1",
    'misc2': "Unknown 2",
    'flags': "MBF21 Bits"
}

WEAPON_FIELD_MAP = {
'index': 'Weapon',
'ammo': 'Ammo type',
'upstate': 'Deselect frame',
'downstate': 'Select frame',
'readystate': 'Bobbing frame',
'atkstate': 'Shooting frame',
'flashstate': 'Firing frame',
'ammopershot': 'Ammo per shot',
'flags': 'MBF21 Bits'
    }
@dataclass
class ourbase_t:
    index: int = 0
    def __getitem__(self, index):
        return getattr(self, fields(self)[index].name)

    def __setitem__(self, index, value):
        field_name = fields(self)[index].name
        setattr(self, field_name, value)
    def __len__(self):
        return len(fields(self))
@dataclass
class state_t(ourbase_t):
    sprite: int = 138 #tnt1a0
    frame: int = 0
    tics: int = -1
    action: str = ''
    nextstate: int = 0
    misc1: int = 0
    misc2: int = 0
    args: list = None
    flags: int = 0
    isloop: int = 0
    def __post_init__(self):
        if self.args is None:
            self.args = [0] * 8


'''    
@dataclass
class thing_t(ourbase_t):
    doomednum: int = 0
    spawnstate: int = 0
    spawnhealth: int = 0
    seestate: int = 0
    seesound: int = 0
    reactiontime: int = 0
    attacksound: int = 0
    painstate: int = 0
    painchance: int = 0
    painsound: int = 0
    meleestate: int = 0
    missilestate: int = 0
    deathstate: int = 0
    xdeathstate: int = 0
    deathsound: int = 0
    speed: int = 0
    radius: int = 0
    height: int = 0
    mass: int = 0
    damage: int = 0
    activesound: int = 0
    flags: int = 0
    flags2: int = 0
    raisestate: int = 0
    droppeditem: int = 0
    infighting_group: int = 0
    projectile_group: int = 0
    splash_group: int = 0
    flags21: int = 0
    ripsound: int = 0
    altspeed: int = 0
    meleerange: int = 0
    bloodcolor: int = 0
'''
@dataclass
class thing_t(ourbase_t):
    doomednum: int = -1
    spawnstate: int = 0
    spawnhealth: int = 1000
    seestate: int = 0
    seesound: int = 0
    reactiontime: int = 8
    attacksound: int = 0
    painstate: int = 0
    painchance: int = 0
    painsound: int = 0
    meleestate: int = 0
    missilestate: int = 0
    deathstate: int = 0
    xdeathstate: int = 0
    deathsound: int = 0
    speed: int = 0
    radius: int = 16
    height: int = 16
    mass: int = 100
    damage: int = 0
    activesound: int = 0
    flags: int = 0
    flags2: int = 0
    raisestate: int = 0
    droppeditem: int = 0
    infighting_group: int = 0
    projectile_group: int = 0
    splash_group: int = 0
    flags21: int = 0
    ripsound: int = 0
    altspeed: int = 0
    meleerange: int = 0
    bloodcolor: int = 0
@dataclass
class weapon_t(ourbase_t):
    ammo: int = 0
    upstate: int = 0
    downstate: int = 0
    readystate: int = 0
    atkstate: int = 0
    flashstate: int = 0
    ammopershot: int = 0
    flags: int = 0

@dataclass
class actor_t(thing_t):
    spawnloop: list = None
    seeloop: list = None
    painloop: list = None
    meleeloop: list = None
    missileloop: list = None
    deathloop: list = None
    xdeathloop: list = None
    raiseloop: list = None

    def __post_init__(self):
        if self.spawnloop is None:
            self.spawnloop = []
        if self.seeloop is None:
            self.seeloop = []
        if self.painloop is None:
            self.painloop = []
        if self.meleeloop is None:
            self.meleeloop = []
        if self.missileloop is None:
            self.missileloop = []
        if self.deathloop is None:
            self.deathloop = []
        if self.xdeathloop is None:
            self.xdeathloop = []
        if self.raiseloop is None:
            self.raiseloop = []
        #if self.rndloops is None:
        #    self.rndloops = []


#act=actor_t()
#act.walkloop = "piska"
#print(act.walkloop)
    
#21:55 15.05.2025
#21:00 17.05.2025
jumpEnters = []
jumpOuts = []
jumppoints = []

@dataclass
class jumppoint_t():
    enter: int=0
    out: int=0

#23:22 20.05.2025
usedLabels = []
@dataclass
class label_t():
    index: int=0
    what: int=0


#ammo, up, down, ready, atk, flash, ammopershot, idunno, flags

WEAPONTABLE = [
[4,4,3,2,5,0,0,1,0,56],
[0,12,11,10,13,0,17,1,0,16],
[1,20,19,18,21,0,30,1,0,0],
[0,51,50,49,52,0,55,1,0,0],
[3,59,58,57,60,0,63,1,0,4],
[2,76,75,74,77,0,79,1,0,0],
[2,83,82,81,84,0,88,40,0,4],
[4,70,69,67,71,0,0,1,0,41],
[1,34,33,32,35,0,47,2,0,0]
]

WEAPONNAMES = [
'Fist',
'Pistol'
'Shotgun',
"Chaingun",
"RocketLauncher",
"PlasmaRifle",
"BFG9000",
"Chainsaw",
"SuperShotgun"
]

def extract_number(line):
    digits = ''
    for char in line:
        if char.isdigit():
            digits += char
        elif digits:
            break  # если начало не-цифры после цифр — значит число закончилось
    if digits:
        return int(digits)
    else:
        return None
    
def extract_after_eq(line):
    return extract_number(line.split('=')[1])

def make_get_int(data):
    def get_int(key, default=0):
        value = data.get(key, str(default)).strip()
        try:
            return int(value)
        except ValueError:
            print(f"Ошибка при чтении [{key}]: '{value}' — не число")
            return default
    return get_int

def block_header_try(line):
    if line.startswith('Thing'):
        return thing_t
    elif line.startswith('Frame'):
        return state_t
    elif line.startswith('Weapon'):
        return weapon_t
    else:
        return 0


def deh_read_blocks(lines):
    blockstream=''
    blocks = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i].strip()
        block_type = block_header_try(line)

        if block_type:  # Начало нового блока
            start_index = i
            j = i + 1

            # Ищем конец текущего блока
            while j < n:
                next_line = lines[j].strip()
                if not next_line:
                    # Пустая строка — конец блока
                    break
                if block_header_try(next_line):  # Новый заголовок — конец блока
                    break
                j += 1

            end_index = j
            blocks.append((start_index, end_index+1, block_type))
            blockstream += f'{start_index} {end_index} {lines[start_index]} {lines[end_index]}\n'
            i = j+1  # Переходим к следующему блоку или концу
        else:
            i += 1

    print('deh blocks count', len(blocks))
    #print(blockstream)
    return blocks
state_kwargsstream=''            
def parse_blocks(lines, blocks):
    parsedcount = 0
    for block in blocks:
        blockstart = block[0]
        blockend = block[1]
        blocktype2 = block[2]
        lineslice = lines[blockstart:blockend]
        parse_block(lineslice,blocktype2)
        parsedcount+=1
    print('parsed blocks',parsedcount)
    #print(state_kwargsstream)

kwargi=50       
def parse_block(lines, blocktype = thing_t):
    global st,tt,wt,kwargi,state_kwargsstream
    FIELD_DICT = {
    thing_t: THING_FIELD_MAP,
    state_t: STATE_FIELD_MAP,
    weapon_t: WEAPON_FIELD_MAP
        }
    tablenum = -1
    TABLE_LIST = [st,tt,wt]
    FIELD_MAP = FIELD_DICT[blocktype]
    data = {}

    if blocktype == state_t:
        tablenum = 0
    elif blocktype == thing_t:
        tablenum = 1
    elif blocktype == weapon_t:
        tablenum = 2
    table = TABLE_LIST[tablenum]
    
    for line in lines:
        if not line: #or '=' not in line:
            continue
        line = line.strip()
        if '=' in line:
            key, value = map(str.strip, line.split('=', 1))
        else:
            parts = line.split(' ')
            key = parts[0].strip()
            value = parts[1].strip()
            #key, value = map(str.strip, line.split(' ', 1))
            
        data[key] = value
    get_int = make_get_int(data)
    state_kwargs = {}

    # Заполняем основные поля через маппинг
    for field_name, config_key in FIELD_MAP.items():
        if config_key in data:
            #print('field_name, config_key',field_name, config_key)
            state_kwargs[field_name] = get_int(config_key)

    # Заполняем args
    if blocktype == state_t:
        state_kwargs['args'] = [get_int(f"Args{i + 1}") for i in range(8)]
    
    index3 = state_kwargs.get('index', 0)
    
    # Создаем копию прототипа по индексу
    broy = copy.deepcopy(table[index3])
    state_kwargsstream+=str(state_kwargs.items())+'\n'
    # Обновляем только те поля, что пришли из конфигурации
    for field_name, value in state_kwargs.items():
        setattr(broy, field_name, value)

    # Сохраняем изменённый объект обратно в таблицу
    table[index3] = broy

    if kwargi>0 and field_name == 'tics':
        print(field_name, value)
        kwargi-=1
    
    #return (blocktype(**state_kwargs))
    #maybe update st,tt,wt? 14:47 10.05.2025
    
    return 0

ttsize,stsize,wtsize=0,0,0
def tsizeeval(filelines):
    global ttsize,stsize,wtsize
    inSprAliases = False
    inSfxAliases = False
    for line in filelines:
        val = extract_number(line)
        if 'Frame ' in line:
            stptr = val
            if val>stsize:
                stsize=val
        elif 'Thing ' in line:
            ttptr = val
            if val>ttsize:
                ttsize=val
        elif 'Weapon ' in line:
            wtptr = val
            if val>wtsize:
                wtsize=val
        elif '[SOUNDS]' in line:
            inSfxAliases = True
            
        elif '[SPRITES]' in line:
            inSprAliases = True
            
        elif inSfxAliases:
            if line.strip():
                linesp = line.split('=')
                try:
                    keya = int(linesp[0].strip())
                    valaa = linesp[1].strip()
                    sfxAliases[keya]='ds'+valaa
                except Exception:
                    inSfxAliases = False
                    
        elif inSprAliases:
            if line.strip():
                linesp = line.split('=')
                try:
                    keya = int(linesp[0].strip())
                    valaa = linesp[1].strip()
                    sprAliases[keya]=valaa
                except Exception:
                    inSprAliases = False
                
                
                
    stsize+=1
    ttsize+=1
    wtsize+=1
#19:39 25.05.2025 desultory bug fix (when dehacked has less stuff than basetables)
    
    stsize = max(1076, stsize)
    ttsize = max(147, ttsize)
    wtsize = max(9, ttsize)
    
def initbasetables():
    fnum = 0
    for file_name in files:
    # Читаем исходный файл
        with open(wha+file_name, 'r', encoding='utf-8') as basefile:
            lptr = 0
            if fnum==0:
                while True:
                    line = basefile.readline()
                    if not line:
                        break
                    
                    ls = line.split()
                    st[lptr].index = lptr
                    st[lptr].sprite=int(ls[0])
                    st[lptr].frame=int(ls[1])+ (32768 if int(ls[2]) else 0)
                    st[lptr].nextstate=int(ls[3])
                    st[lptr].tics=int(ls[4])
                    st[lptr].action=ls[5]
                    lptr+=1
            elif fnum==1:
                while True:
                    line = basefile.readline()
                    if not line:
                        break
                    n = [int(x) for x in line.split()]
                    #if field order or count in thing_t are changed, this screws up!
                    for a,b in PAIRS:
                        tt[lptr][a+1]=n[b]
                    tt[lptr].index = lptr
                    lptr+=1         
        fnum+=1
    
    for v in range(len(WEAPONTABLE)):
        w = WEAPONTABLE[v]
        cw = weapon_t()
        cw.index = v
        cw.ammo=w[0]
        cw.upstate=w[1]
        cw.downstate=w[2]
        cw.readystate=w[3]
        cw.atkstate=w[4]
        cw.flashstate=w[6]
        cw.ammopershot=w[7]
        cw.flags=w[9]
        wt.append(cw)

#17:20 20.05.2025 eats state_t
def doAddFlags(flags,flags21,mode=1):
    dafStream = ''


    fsl = flags_to_list_of_strings(curactor.flags,flags)
    fsl21 = flags_to_list_of_strings(curactor.flags21,flags21,MBF21FLAGS)
    
    sprwrtn = True
    for fsl_list in (fsl, fsl21):
        for entry in fsl_list:
            if not sprwrtn:
                dafStream+='TNT1 A 0 '
                sprwrtn = True
            dafStream+=f'A_ChangeFlag("{entry}",{mode})\n'
            sprwrtn = False
    return dafStream
        
#18:19 24.05.2025    
def doJumpIfFlags(flags,flags21,label):
    jifStream = ''
    xarr1, varr1 = flags_for_checks(curactor.flags,flags)
    xarr21, varr21 = flags_for_checks(curactor.flags21,flags21,MBF21FLAGS)
    xarr = xarr1+xarr21
    varr = varr1+varr21

    xlen = len(xarr)
    vlen = len(varr)
    l = xlen + 2 * vlen - 1

    counter = 0
    sprwrtn = True
    for flagname in xarr:
        if not sprwrtn:
            jifStream+='TNT1 A 0 '
            sprwrtn = True
        jifStream+=f'A_CheckFlag("{flagname}",{l-counter})\n'
        counter+=1
        sprwrtn = False
        
    counter = 2    
    for flagname in varr[:-1]:
        if not sprwrtn:
            jifStream+='TNT1 A 0 '
            sprwrtn = True
        jifStream+=(
            f'A_CheckFlag("{flagname}",{l-counter})\n'+
            f'TNT1 A 0 A_Jump(255,{2*vlen-counter})\n'
            )
        counter+=2
        sprwrtn = False

    if varr:
        flagname = varr[-1]
        if not sprwrtn:
            jifStream+='TNT1 A 0 '
            sprwrtn = True
        sprwrtn = False
        jifStream+=(
            f'A_CheckFlag("{flagname}","{label}")\n'
            )    

    return jifStream
    

    
    
    
    
    
def doAction(state):
    action = state.action 
    misc1 = state.misc1
    misc2 = state.misc2
    args = copy.deepcopy(state.args)
    expr = ''
    if action == 'NULL':
        return ''
    #
    # MBF21 BEGIN
    #
    elif action == 'SpawnObject':
        for i in range(1,8):
            args[i]=int32tofixed(args[i])
        expr = (
            f'A_SpawnItemEx("{getActorName(args[0])}",{args[2]},{args[3]},{args[4]},'
            f'{args[5]},{args[6]},{args[7]},{args[1]})'
            )
    elif action == 'MonsterProjectile':
        for i in range(1,5):
            args[i]=int32tofixed(args[i])
        expr = (
            f'A_CustomMissile("{getActorName(args[0])}",{32.0-args[4]},{args[3]},{args[1]},'
            f'0,{args[2]})'
            )
    elif action == 'MonsterBulletAttack':
        for i in range(0,1):
            args[i]=int32tofixed(args[i])
        for i, val in enumerate([3, 5]):
            if args[i+3] == 0:
                args[i+4] = val
        damageexpr = f'{args[3]}*random[mbf21](1,{args[4]})'
        expr = (
            f'A_CustomBulletAttack({args[0]},{args[1]},{args[2]},{damageexpr})'
            )
    elif action == 'MonsterMeleeAttack':
        for i, val in enumerate([3, 8]):
            if args[i] == 0:
                args[i] = val
        damageexpr = f'{args[0]}*random[mbf21](1,{args[1]})'
        soundexpr = getSoundName(args[2])
        expr = (
            f'A_CustomMeleeAttack({damageexpr},"{soundexpr}")'
            )
    elif action == 'NoiseAlert':
        expr = (
            f'A_AlertMonsters(0,AMF_EMITFROMTARGET)'
            )
    elif action == 'HealChase':
        expr = (
            f'A_VileChase'
            )
    elif action == 'FindTracer':
        dist = args[1] or 128
        expr = (
            f'A_SeekerMissile(0,0,SMF_LOOK,50,{dist})'
            )
    elif action == 'ClearTracer':
        expr = f'A_RearrangePointers(AAPTR_DEFAULT,AAPTR_DEFAULT,AAPTR_NULL)'
        
    elif action == 'SeekTracer':
        threshold = int32tofixed(args[0])
        turnmax = int32tofixed(args[1])
        expr = f'A_SeekerMissile({threshold},{turnmax},SMF_PRECISE)'
    elif action == 'RadiusDamage':
        damag = args[0]
        distn = int32tofixed(args[1])
        expr = f'A_Explode({damag},{distn})'
    #
    # FLAG STUFF
    #

    elif action == 'AddFlags':
        expr = doAddFlags(args[0],args[1])
    elif action == 'RemoveFlags':
        expr = doAddFlags(args[0],args[1],0)
    elif action == 'JumpIfFlagsSet':
        labl = labelDict.get(args[0],0)
        expr = doJumpIfFlags(args[0],args[1],labl)
    
    #    
    # 5 JUMPS BEGIN
    #
    elif action == 'JumpIfHealthBelow':
        helth = args[1]
        labl = labelDict.get(args[0],0)
        expr = f'A_JumpIfHealthLower({helth},"{labl}")'
    elif action == 'JumpIfTargetInSight':
        labl = labelDict.get(args[0],0)
        fov = int32tofixed(args[1])
        expr = f'A_JumpIfTargetInLOS("{labl}",{fov})'
    elif action == 'JumpIfTargetCloser':
        labl = labelDict.get(args[0],0)
        dist = int32tofixed(args[1])
        expr = f'A_JumpIfCloser({dist},"{labl}")' 
    elif action == 'JumpIfTracerInSight':
        labl = labelDict.get(args[0],0)
        fov = int32tofixed(args[1])
        expr = f'A_JumpIfTargetInLOS("{labl}",{fov},JLOSF_CHECKTRACER)'
    elif action == 'JumpIfTracerCloser':
        labl = labelDict.get(args[0],0)
        dist = int32tofixed(args[1])
        expr = f'A_JumpIfTracerCloser({dist},"{labl}")'
    #
    # 5 JUMPS END
    #

    #
    # WEPEN BEGIN
    #
    elif action == 'WeaponProjectile':
        typ = getActorName(args[0])
        angle = int32tofixed(args[1])
        pitch = int32tofixed(args[2])
        xyoffs = int32tofixed(args[3])
        zoffs = int32tofixed(args[4])
        expr = f'A_FireCustomMissile("{typ}",{angle},0,{xyoffs},{zoffs})'
        
    elif action == 'WeaponBulletAttack':
        spreadxy = int32tofixed(args[0])
        spreadz = int32tofixed(args[1])
        numbullets = args[2] or 1
        base = args[3] or 5
        dice = args[4] or 3
        damageexpr = f'{base}*random[mbf21](1,{dice})'
        expr = f'A_FireBullets({spreadxy},{spreadz},{numbullets},{damageexpr})'

    elif action == 'WeaponMeleeAttack':
        
        base = args[0]
        dice = args[1]
        bers = int32tofixed(args[2]) or 1.0
        sound = getSoundName(args[3])
        rangee = int32tofixed(args[4])

        if bers != 1.0:
            si = state.index
            beatsprseq = (
f'{zdoomspritenames(state.sprite)} '
f'{BUKVATABLE(state.frame & 0x7FFF)} '
                )
            if (state.frame & 32768):
                beatsprseq += "Bright "
            
            damageexpr1 = f'{base}*random[mbf21](1,{dice})'
            damageexpr2 = f'{bers*base}*random[mbf21](1,{dice})'
            expr = (
f'TNT1 A 0 A_JumpIfInventory("PowerStrength", 1, "Berserked{si}")\n'
f'Normal{si}:\n'
f'{beatsprseq} A_CustomPunch({damageexpr1}, TRUE)\n'
f'Goto FireEnd{si}\n'
f'Berserked{si}:\n'
f'{beatsprseq} A_CustomPunch({damageexpr2}, TRUE)\n'
f'FireEnd{si}:\n'
)
    elif action == 'WeaponAlert':
        expr = 'A_AlertMonsters'
    elif action == 'WeaponJump':
        labl = labelDict.get(args[0],0)
        chance = args[1]
        expr = f'A_Jump({chance},"{labl}")'
    elif action == 'ConsumeAmmo':
        #howmuch = args[0]
        howmuch = 0 if curwepnammouse != 0 else args[0]
            
        if howmuch == 0: #if zero, use wepen's ammopershot
            #howmuch = curwepnammouse
            return ''
            
        #howmuch = curwepnammotype
        try:
            typ = ZDOOMAMMONAMES[curwepnammotype]
        except Exception:
            typ = 'Clip'
        expr = f'A_TakeInventory("{typ}",{howmuch},TIF_NOTAKEINFINITE)'
    elif action == 'CheckAmmo':
        labl = labelDict.get(args[0],0)
        expr = f'A_JumpIfNoAmmo("{labl}")'
        
#23:57 21.05.2025 name flash is a mischoice. ZDoom wiki says.
    elif action == 'RefireTo':
        labl = labelDict.get(args[0],"Fire")
        expr = f'A_Refire("{labl}")'
        
    elif action == 'GunFlashTo':
        labl = labelDict.get(args[0],"Flash")
        expr = f'A_GunFlash("{labl}")'
    elif action == 'WeaponSound':
        sound = getSoundName(args[0])
        attn = 'ATTN_NONE' if misc2!=0 else 'ATTN_NORM'
        #expr = f'A_StartSound("{sound}", CHAN_WEAPON, 0, 1.0, {attn})'
        expr = f'A_PlaySound("{sound}",CHAN_WEAPON,1.0,FALSE,{attn})'
        
    #
    # WEPEN END
    #    


    
    #
    # MBF BEGIN
    #
    elif action == 'RandomJump':
        labl = labelDict.get(misc1,0)
        chance = misc2
        expr = f'A_Jump({chance},"{labl}")'
    elif action == 'Mushroom': #todo: missile damage dehardcode
        vrange = int32tofixed(misc1)
        hrange = int32tofixed(misc2)
        expr = f'A_Mushroom("FatShot", 3, MSF_DontHurt, {vrange}, {hrange})'
    elif action == 'Spawn':
        who = getActorName(misc1)
        zoffs = int32tofixed(misc2)
        expr = f'A_SpawnItem("{who}", 0.0, {zoffs})'
    elif action == 'Turn':
        #angle = int32tofixed(misc1)
        angle = misc1
        expr = f'A_Turn({angle})'
    elif action == 'Face':
        #angle = int32tofixed(misc1)
        angle = misc1
        expr = f'A_Face({angle})'
    elif action == 'Scratch':
        sound = getSoundName(misc2)
        expr = f'A_CustomMeleeAttack({misc1},"{sound}")'
    elif action == 'PlaySound':
        sound = getSoundName(misc1)
        attn = 'ATTN_NONE' if misc2!=0 else 'ATTN_NORM'
        expr = f'A_PlaySound("{sound}",CHAN_BODY,1.0,FALSE,{attn})'
    elif action == 'LineEffect':
        boomspec = misc1
        tag = misc2
        expr = f'A_LineEffect({boomspec},{tag})'
    elif action == 'NailBomb':
        expr = f'A_Explode(-1,-1,XF_HURTSOURCE,0,0,30)'
    #
    # MBF END
    #
        
    else:
        return f'A_{action}'
        # В самом конце функции
    if expr is None:
        raise ValueError(f"Неожиданное состояние: action={action}, expr=None")
    return expr
    
def getLabelName(index, actor):
    pass    
#21:56 15.05.2025 todo: adapt to JUMPS
#23:34 15.05.2025 oops, was watching youtube, like
#19:38 17.05.2025 gonna make a list of funcs with branching
#

JUMPACTIONS = ['HealChase', 'JumpIfHealthBelow', 'JumpIfTargetInSight', '',
               'JumpIfTargetCloser', 'JumpIfTracerInSight', 'JumpIfTracerCloser',
               'JumpIfFlagsSet', 'WeaponJump', 'CheckAmmo', 'RefireTo', 'GunFlashTo']
healchaseOuts = []



def deh_read_frames(lines):
    for line in lines:
        if line.startswith('FRAME'):
            parts = line.split()
            frameIndex = int(parts[1])
            frameAction = parts[3]
            st[frameIndex].action = frameAction
            if st[frameIndex].args[0] or st[frameIndex].misc1:
                if frameAction in JUMPACTIONS:
                    jumppoints.append(jumppoint_t(frameIndex, st[frameIndex].args[0]))
                    if frameAction == 'HealChase':
                        healchaseOuts.append(st[frameIndex].args[0])
                elif frameAction == 'RandomJump':
                    jumppoints.append(jumppoint_t(frameIndex, st[frameIndex].misc1))
                    

def compnmod():
    modtracker = []
    TPAIRS = [[st,st0],[tt,tt0],[wt,wt0]]
    pairnum = 0
    
    for pair in TPAIRS:
        lentable = len(pair[0])
        structlen = len(pair[0][0])
        print(lentable,structlen)
        for structnum in range(lentable):
            for fieldnum in range(structlen):
                if pair[0][structnum][fieldnum]!=pair[1][structnum][fieldnum]:
                    what = pair[0][structnum][fieldnum]
                    modtracker.append([pairnum,structnum,fieldnum,what])
        pairnum+=1
    return modtracker

decactors=[]
emptyguy = actor_t()
decactorsindexes=[]

def compThings():
    global vivod
    thingcount = len(tt)
    fieldcount = len(tt[0])
    #for i,thing in enumerate(tt):
    #   workactor.index = thing.index
    for ti in range(thingcount):
        if ti in decactorsindexes:
            continue
#1. Check fields of thing_t, if yes, write to workactor
        workactor = actor_t()
        workactor.index = tt[ti].index
        for fi in range(fieldcount):
            if tt[ti][fi]!=tt0[ti][fi]:
                workactor[fi]=tt[ti][fi]
#2. Check loops
        ourstateflags=0

        spawnloop=getLoop(tt[ti].spawnstate,st)
        seeloop=getLoop(tt[ti].seestate,st)
        painloop=getLoop(tt[ti].painstate,st)
        meleeloop=getLoop(tt[ti].meleestate,st)
        missileloop=getLoop(tt[ti].missilestate,st)
        deathloop=getLoop(tt[ti].deathstate,st)
        xdeathloop=getLoop(tt[ti].xdeathstate,st)
        raiseloop=getLoop(tt[ti].raisestate,st)


        #if spawnloop!=getLoop(tt0[ti].spawn)
        
        if spawnloop!=getLoop(tt0[ti].spawnstate,st0): workactor.spawnloop=spawnloop
        if seeloop!=getLoop(tt0[ti].seestate,st0): workactor.seeloop=seeloop
        if painloop!=getLoop(tt0[ti].painstate,st0): workactor.painloop=painloop
        if meleeloop!=getLoop(tt0[ti].meleestate,st0): workactor.meleeloop=meleeloop
        if missileloop!=getLoop(tt0[ti].missilestate,st0): workactor.missileloop=missileloop
        if deathloop!=getLoop(tt0[ti].deathstate,st0): workactor.deathloop=deathloop
        if xdeathloop!=getLoop(tt0[ti].xdeathstate,st0): workactor.xdeathloop=xdeathloop
        if raiseloop!=getLoop(tt0[ti].raisestate,st0): workactor.raiseloop=raiseloop
        #if workactor.
        #vivod+=f'{workactor.spawnloop}\n'

#3. Check if our actor is not empty.
        if workactor != emptyguy:
            decactors.append(workactor)
            decactorsindexes.append(ti)
#4. Check if actor has random access states
        

def isInSet(value, array):
    try:
        return array.index(value)
    except ValueError:
        return -1
    
def is_same_actions(s1, s2):
    return (
        s1.sprite == s2.sprite and
        s1.frame & 32768 == s2.frame & 32768 and         # или hasattr(s1, 'Lit') and ...
        s1.tics == s2.tics and
        s1.action == s2.action and
        s1.misc1 == s2.misc1 and     # Param1
        s1.misc2 == s2.misc2 and        # Param2
        s1.flags == s2.flags and
        s1.args == s2.args #22:06 17.05.2025
    )
#23:39 19.05.2025
def get_corresponding_number(num,list1,list2):
    if num in list1:
        index = list1.index(num)
        return list2[index]
    else:
        return None
    
def decorateStates(actor):
    global curactor, vivod
    
    notHasHealState = True
    
    statesStream = ''
    
    protoStateLoops = [
    actor.spawnloop,
    actor.seeloop,
    actor.painloop,
    actor.meleeloop,
    actor.missileloop,
    actor.deathloop,
    actor.xdeathloop,
    actor.raiseloop
    ]

    tta=tt[actor.index]
    curactor = copy.deepcopy(tta)
    
    protoloopFrames = [
    tta.spawnstate,
    tta.seestate,
    tta.painstate,
    tta.meleestate,
    tta.missilestate,
    tta.deathstate,
    tta.xdeathstate,
    tta.raisestate
    ]
    #vivod+=str(protoloopFrames)
    #print(protoloopFrames)
    StateLoops = copy.deepcopy(protoStateLoops)
    loopFrames = copy.deepcopy(protoloopFrames)
    
    specialLoopFrames = []
    #visitedRandomJumps = {}
    
    #branching of loops
    
    tempFrames = []
    tempStateLoops = []
    #listedRandomJumps = {}
    for i in jumpEnters:
        if any(i in sublist for sublist in StateLoops):
            j = get_corresponding_number(i,jumpEnters,jumpOuts)
            if j not in tempFrames and j not in loopFrames:
                tempRandomLoop = getLoop(j, st)
                #cc+=1
                if tempRandomLoop:
                    #cc+=1
                    #statesStream += f'{j} ugabuga\n'
                    
                    tempFrames.append(j)
                    tempStateLoops.append(tempRandomLoop)
    
    loopFrames += tempFrames
    StateLoops += tempStateLoops
    
    #statesStream +=f'{loopFrames} {StateLoops}'
    for i in range(len(StateLoops)):

        if not StateLoops[i]:
            continue
        
        if i < 8:
            labelDict[loopFrames[i]]=ZDOOMTHINGSTATES[i]
        elif notHasHealState and (loopFrames[i] in healchaseOuts):
            labelDict[loopFrames[i]]='Heal'
            #notHasHealState = False
        else:
            labelDict[loopFrames[i]]=f'RndLabel_{loopFrames[i]}'    
                
    #creation of special loop starts           
    for i in range(len(StateLoops)):
        loop = StateLoops[i]
        if not loop:
            continue   
        last_frame = st[loop[-1]].index
        if (last_frame != 0
            and last_frame not in loopFrames
            and last_frame not in specialLoopFrames):
            specialLoopFrames.append(last_frame)
            labelDict[last_frame]=f'State_{last_frame}'
    
    statesStream += '\tStates\n\t{\n'

    
    #DECORATE WRITING CYCLES START
    for i in range(len(StateLoops)):
        if not StateLoops[i]:
            continue
        
        if i < 8:
            statesStream+=(f"\t{ZDOOMTHINGSTATES[i]}:\n")
        elif notHasHealState and (loopFrames[i] in healchaseOuts):
            statesStream+=(f"\tHeal:\n")
            notHasHealState = False
        else:
            statesStream+=(f"\tRndLabel_{loopFrames[i]}:\n")
        loop_size = len(StateLoops[i])-1
        


        #Создание стейтлупа
        j = 0

        while j < loop_size: 
            state_values = st[StateLoops[i][j]]

            # Если это особая метка — создаём её
            if j>0:
                if StateLoops[i][j] in loopFrames:
                # or StateLoops[i][j] in specialLoopFrames:
                    break
                
            if StateLoops[i][j] in specialLoopFrames:
                statesStream+=(f"\tState_{StateLoops[i][j]}:\n")
                # Пишем спрайт и подкадр
            if state_values.action != 'WeaponMeleeAttack':
                line = f"\t\t{zdoomspritenames(state_values.sprite)} {BUKVATABLE(state_values.frame & 0x7FFF)}"
                #line = f"{i} {j} {state_values.index} {state_values.nextstate}\t\t{zdoomspritenames(state_values.sprite)} {BUKVATABLE(state_values.frame & 0x7FFF)}"
                # Сливаем подкадры с одинаковыми действиями
                while ( 
                    j+1 < loop_size and
                     is_same_actions(st[StateLoops[i][j]], st[st[StateLoops[i][j]].nextstate])
                    and st[StateLoops[i][j]].nextstate not in loopFrames
                    and st[StateLoops[i][j]].nextstate not in specialLoopFrames
                ):

                    frame_number = st[st[StateLoops[i][j]].nextstate].frame & 0x7FFF
                    line += BUKVATABLE(frame_number)
                    j += 1
                    if j+1 >= loop_size:
                        break
                
                # Длительность и флаг "Bright"
                line += f" {state_values.tics}"

                #bright_flag =
                if (state_values.frame & 32768):
                    line += " Bright"
                frame_number = state_values.frame & 0x7FFF  # безопасное извлечение номера подкадра
                

                # Действие
            if state_values.action:
                line += ' '+f'{doAction(state_values)}'

            statesStream+=(line + "\n")
            j += 1

        # Последнее состояние: stop или goto

        # После while цикла
        
        try:
            last_state = st[StateLoops[i][j]].index
        except IndexError:
            last_state = 0
            print('IndexError',i,j)
            
        #last_state = StateLoops[i][j]

        standard_state = isInSet(last_state, loopFrames)
        special_state = isInSet(last_state, specialLoopFrames)

        if last_state == 0:
            statesStream+=("\t\tstop\n")
        elif standard_state != -1:
            if i == standard_state:
                statesStream+=(f"\t\tloop\n")
            else:
                if standard_state<8:
                    statesStream+=(f"\t\tgoto {ZDOOMTHINGSTATES[standard_state]}\n")
                elif loopFrames[standard_state] in healchaseOuts:
                    statesStream+=(f"\t\tgoto Heal\n")
                else:
                    statesStream+=(f"\t\tgoto RndLabel_{loopFrames[standard_state]}\n")
        elif special_state != -1:
            statesStream+=(f"\t\tgoto State_{last_state}\n")
    #DECORATE WRITING CYCLES END
    
    #if actor.index==155:
    #    print(StateLoops)
    statesStream+=("\t}\n")
    return statesStream


WPNUM2ANUM = {
2:78,
3:74,
4:76,
5:77,
6:73,
7:75,
8:79
    }
    
def decorateWepenStates(wepennum):

    global curwepnammotype, curwepnammouse
    
    notHasHealState = True
    
    statesStream = ''
    actorid = WPNUM2ANUM.get(wepennum,-1)
    wn = wt[wepennum]
    curwepnammotype = wn.ammo
    curwepnammouse = wn.ammopershot
    wepenstates = [
    wn.upstate,
    wn.downstate,
    wn.readystate,
    wn.atkstate,
    wn.flashstate
    ]
#add wepens loops 21:32 22.05.2025

    newWeaponStateLoops = [
    getLoop(wn.upstate, st), 
    getLoop(wn.downstate, st),
    getLoop(wn.readystate, st),
    getLoop(wn.atkstate, st),
    getLoop(wn.flashstate, st)
        ]
    #print(newWeaponStateLoops)
    oldWeaponStateLoops = [
getLoop(wn.upstate, st0), 
getLoop(wn.downstate, st0),
getLoop(wn.readystate, st0),
getLoop(wn.atkstate, st0),
getLoop(wn.flashstate, st0)
        ]
    
    modWeaponStateLoops =[]
    for ka in range(0,5):
        if newWeaponStateLoops[ka]!=oldWeaponStateLoops[ka]:
            modWeaponStateLoops.append(newWeaponStateLoops[ka])
        else:
            modWeaponStateLoops.append([])
            
    if actorid != -1:
        actor=decactors[actorid]
        tta = tt[actorid]
        protoStateLoops = [
        actor.spawnloop,
        actor.seeloop,
        actor.painloop,
        actor.meleeloop,
        actor.missileloop,
        actor.deathloop,
        actor.xdeathloop,
        actor.raiseloop
        ]+modWeaponStateLoops

        protoloopFrames = [
        tta.spawnstate,
        tta.seestate,
        tta.painstate,
        tta.meleestate,
        tta.missilestate,
        tta.deathstate,
        tta.xdeathstate,
        tta.raisestate
        ]+wepenstates
    else:
        protoStateLoops = [
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        [],
        ]+modWeaponStateLoops
        protoloopFrames = [
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        ]+wepenstates
    
    StateLoops = copy.deepcopy(protoStateLoops)
    loopFrames = copy.deepcopy(protoloopFrames)
    
    specialLoopFrames = []
    
    #branching of loops
    
    tempFrames = []
    tempStateLoops = []
    #listedRandomJumps = {}
    for i in jumpEnters:
        if any(i in sublist for sublist in StateLoops):
            j = get_corresponding_number(i,jumpEnters,jumpOuts)
            if j not in tempFrames and j not in loopFrames:
                tempRandomLoop = getLoop(j, st)
                #cc+=1
                if tempRandomLoop:
                    #cc+=1
                    #statesStream += f'{j} ugabuga\n'
                    
                    tempFrames.append(j)
                    tempStateLoops.append(tempRandomLoop)
    
    loopFrames += tempFrames
    StateLoops += tempStateLoops
    
    #statesStream +=f'{loopFrames} {StateLoops}'
    for i in range(len(StateLoops)):

        if not StateLoops[i]:
            continue
        
        if i < 8+5:
            labelDict[loopFrames[i]]=ZDOOMTHINGSTATES[i]
        elif notHasHealState and (loopFrames[i] in healchaseOuts):
            labelDict[loopFrames[i]]='Heal'
            #notHasHealState = False
        else:
            labelDict[loopFrames[i]]=f'RndLabel_{loopFrames[i]}'    
                
    #creation of special loop starts           
    for i in range(len(StateLoops)):
        loop = StateLoops[i]
        if not loop:
            continue   
        last_frame = st[loop[-1]].index
        if (last_frame != 0
            and last_frame not in loopFrames
            and last_frame not in specialLoopFrames):
            specialLoopFrames.append(last_frame)
            labelDict[last_frame]=f'State_{last_frame}'
    
    statesStream += '\tStates\n\t{\n'

    
    #DECORATE WRITING CYCLES START
    for i in range(len(StateLoops)):
        if not StateLoops[i]:
            continue
        
        if i < 8+5:
            statesStream+=(f"\t{ZDOOMTHINGSTATES[i]}:\n")
        elif notHasHealState and (loopFrames[i] in healchaseOuts):
            statesStream+=(f"\tHeal:\n")
            notHasHealState = False
        else:
            statesStream+=(f"\tRndLabel_{loopFrames[i]}:\n")
        loop_size = len(StateLoops[i])-1
        


        #Создание стейтлупа
        j = 0

        while j < loop_size: 
            state_values = st[StateLoops[i][j]]

            # Если это особая метка — создаём её
            if j>0:
                if StateLoops[i][j] in loopFrames:
                    break
                
            if StateLoops[i][j] in specialLoopFrames:
                statesStream+=(f"\tState_{StateLoops[i][j]}:\n")
                # Пишем спрайт и подкадр
            if state_values.action != 'WeaponMeleeAttack':
                #line = f"{i} {j} {state_values.index} {state_values.nextstate}\t\t{zdoomspritenames(state_values.sprite)} {BUKVATABLE(state_values.frame & 0x7FFF)}"
                line = f"\t\t{zdoomspritenames(state_values.sprite)} {BUKVATABLE(state_values.frame & 0x7FFF)}"

                # Сливаем подкадры с одинаковыми действиями
                while ( 
                    j+1 < loop_size and
                     is_same_actions(st[StateLoops[i][j]], st[st[StateLoops[i][j]].nextstate])
                    and st[StateLoops[i][j]].nextstate not in loopFrames
                    and st[StateLoops[i][j]].nextstate not in specialLoopFrames
                ):

                    frame_number = st[st[StateLoops[i][j]].nextstate].frame & 0x7FFF
                    line += BUKVATABLE(frame_number)
                    j += 1
                    if j+1 >= loop_size:
                        break
                
                # Длительность и флаг "Bright"
                line += f" {state_values.tics}"

                #bright_flag =
                if (state_values.frame & 32768):
                    line += " Bright"
                frame_number = state_values.frame & 0x7FFF  # безопасное извлечение номера подкадра
                

                # Действие
            if state_values.action:
                line += ' '+doAction(state_values)

            statesStream+=(line + "\n")
            j += 1

        # Последнее состояние: stop или goto

        # После while цикла
        
        try:
            last_state = st[StateLoops[i][j]].index
        except IndexError:
            last_state = 0
            print('IndexError',i,j)
            
        #last_state = StateLoops[i][j]

        standard_state = isInSet(last_state, loopFrames)
        special_state = isInSet(last_state, specialLoopFrames)

        if last_state == 0:
            statesStream+=("\t\tstop\n")
        elif standard_state != -1:
            if i == standard_state:
                statesStream+=(f"\t\tloop\n")
            else:
                if standard_state<8+5:
                    statesStream+=(f"\t\tgoto {ZDOOMTHINGSTATES[standard_state]}\n")
                elif loopFrames[standard_state] in healchaseOuts:
                    statesStream+=(f"\t\tgoto Heal\n")
                else:
                    statesStream+=(f"\t\tgoto RndLabel_{loopFrames[standard_state]}\n")
        elif special_state != -1:
            statesStream+=(f"\t\tgoto State_{last_state}\n")
    #DECORATE WRITING CYCLES END
    
    #if actor.index==155:
    #    print(StateLoops)
    statesStream+=("\t}\n")
    return statesStream    
def getProperties(actor):
    return [
        actor.doomednum,
        actor.spawnhealth,
        actor.speed,
        actor.radius,
        actor.height,
        actor.damage,
        actor.reactiontime,
        actor.painchance,
        actor.mass,
        #actor.droppeditem
        ]
def getSounds(actor):
    return [
        actor.seesound,
        actor.attacksound,
        actor.painsound,
        actor.deathsound,
        actor.activesound
        ]

NUM2PROPERTIES = {
0: 'ID',
1: 'Health',
2: 'Speed',
3: 'Radius',
4: 'Height',
5: 'Damage',
6: 'ReactionTime',
7: 'PainChance',
8: 'Mass',
#9: 'DropItem'
}

NUM2SOUNDS = {
0: 'See',
1: 'Attack',
2: 'Pain',
3: 'Death',
4: 'Active'
}

NUM2WEPENPROPERTIES = {
0: 'Alert',
1: 'Attack',
2: 'Pain',
3: 'Death',
4: 'Active'
}

def decorateActor(actor, iswepen = 0):
    
    daStream = ''
    actorold = tt0[actor.index]
    actornew =  tt[actor.index]
    #if actorold == actornew:
    #    return ''
    actorName = getActorName(actor.index)
    #actorednum = '' if actornew.doomednum==actorold.doomednum else f' {actor.doomednum}'
    actorednum = '' if actor.doomednum==-1 else f' {actor.doomednum}'
    if actor.index>145:
        actorinh = ''
        prefix = ''
    else:
        prefix = 'DH_'
        actorinh = (
' : '+actorName+
' replaces '+actorName
            )
    #Actor header

    actorRow = ('Actor '+prefix+actorName+
                actorinh+
                actorednum+
                #f' {actor.doomednum}'+
                '\n\t{\n')
    
    #flags
    flagStream = (
        actorRow+
        get_flags_diff(actorold.flags, actornew.flags)+
        get_flags_diff(actorold.flags21, actornew.flags21,MBF21FLAGS)
        )
    if flagStream:
       daStream+= flagStream+'\n'
       
    #properties

    nap = getProperties(actornew)
    oap = getProperties(actorold)
    #print(nap,oap) #debug
    for i, p in enumerate(nap):
        if i == 0:
            continue
        if nap[i]!=oap[i]:
            #p2 = p // 65536 if i >= 3 and i <= 4 else p
            p2 = p // 65536 if (
                (i>=3 and i<=4)
                or (i==2 and (actornew.flags & 0x00010000))
                ) else p
            
            daStream += NUM2PROPERTIES.get(i,-1)+f' {p2}\n'

    ditem = actornew.droppeditem or actorold.droppeditem
    if ditem:
        daStream += f'DropItem "{getActorName(ditem)}"\n'
        
    #sounds

    nas = getSounds(actornew)
    oas = getSounds(actorold)

    for i, sfx in enumerate(nas):
        if nas[i]!=oas[i]:
            daStream += NUM2SOUNDS.get(i,-1)+f'Sound "{getSoundName(sfx)}"\n'    

    if iswepen:
        wepenum = WEAPONIDS.index(actor.index) + 2
        daStream += wepenHeader(wepenum)
        
    return daStream
def getWepenProperties(wepens):
    return [
    wepens.ammo,
    wepens.ammopershot,
    wepens.flags
        ]
'''
NOTHRUST 	0x001 	Doesn't thrust things
SILENT 	0x002 	Weapon is silent
NOAUTOFIRE 	0x004 	Weapon won't autofire when swapped to
FLEEMELEE 	0x008 	Monsters consider it a melee weapon
AUTOSWITCHFROM 	0x010 	Can be switched away from when ammo is picked up
NOAUTOSWITCHTO 	0x020 	Cannot be switched to when ammo is picked up
'''
WEPENFLAGS = {
    #0x00000001: "SPECIAL",
    0x00000002: "WEAPON.NOALERT",
    0x00000004: "WEAPON.NOAUTOFIRE",
    0x00000008: "WEAPON.MELEEWEAPON",
    0x00000010: "WEAPON.WIMPY_WEAPON",
    #0x00000020: "WEAPON.NOAUTOSWITCHTO"
}
def wepenHeader(wepenum):
    whStream = ''
    newwepen =  wt[wepenum]
    oldwepen = wt0[wepenum]
#ammo, up, down, ready, atk, flash, ammopershot, idunno, flags

#Wepen header
    if wepenum<2:
        actorName = 'Pistol' if wepenum else 'Fist'
        actorinh = (
    ' : '+actorName+
    ' replaces '+actorName
                ) 
        actorRow = ('Actor DH_'+actorName+
                    actorinh+
                    '\n\t{\n')
        whStream += actorRow
    
    nwp = getWepenProperties(newwepen)
    owp = getWepenProperties(oldwepen)


    if newwepen.ammo!=oldwepen.ammo:
        try:
            typ = ZDOOMAMMONAMES[newwepen.ammo]
        except Exception:
            typ = 'Clip'  
        whStream+=f'Weapon.AmmoType "{typ}"\n'
    
    if newwepen.ammopershot!=oldwepen.ammopershot:
        ammouse = newwepen.ammopershot
        whStream+=f'Weapon.AmmoUse {ammouse}\n'
    #Weapon.KickBack
    
    '''
    flagdiff = newwepen.flags^oldwepen.flags   
    if flagdiff:
    '''
    wfdiff = get_flags_diff(oldwepen.flags,newwepen.flags,WEPENFLAGS)
    if wfdiff:
        whStream+=wfdiff+'\n'

    if newwepen.flags & 1:
        whStream+='Weapon.KickBack 0\n'
        
    return whStream
    
    
    
    
    
    
    

def forDecActors():
    global vivod
    for actor in decactors:
        if actor.index not in WEAPONIDS:
            vivod+=decFullActor(actor)
        else:
            vivod+=decFullWepen(actor)
    for i9 in range(0,2):
        vivod+=decFullOtherWepen(i9)
        
            
        
def forDecWepens():
    for i9 in range(0,9):
        print(decorateWepenStates(i9))
        
def decFullOtherWepen(i9):
    bits = 3
    temp1 = decorateWepenStates(i9)
    if temp1 == '\tStates\n\t{\n\t}\n':
        #bits &= ~0b001
        bits -= 1

    temp2 = wepenHeader(i9)
    aftern = temp2.find('\n')
    temp2l2 = temp2[aftern+1:]
    if temp2l2 == '\t{\n\n':
        #bits &= ~0b010
        bits -= 2

    if bits:
        if bits & 1:
            return temp2+temp1+'}\n'
        else:
            return temp2+'}\n'
    return ''

def decFullWepen(actor):
    bits = 3
    i9 = WEAPONIDS.index(actor.index) + 2
    
    temp1 = decorateWepenStates(i9)
    if temp1 == '\tStates\n\t{\n\t}\n':
        bits -= 1

    temp2 = decorateActor(actor, 1)
    aftern = temp2.find('\n')
    temp2l2 = temp2[aftern+1:]
    if temp2l2 and not temp1 == '\t{\n\n':
        bits -= 2

    if bits:
        if bits & 1:
            return temp2+temp1+'}\n'
        else:
            return temp2+'}\n'
    return ''

def decFullActor(actor):
    bits = 3
    temp1 = decorateStates(actor)
    if temp1 == '\tStates\n\t{\n\t}\n':
        bits -= 1
        
    temp2 = decorateActor(actor)
    aftern = temp2.find('\n')
    temp2l2 = temp2[aftern+1:]
    if temp2l2 == '\t{\n\n':
        bits -= 2

    if bits:
        if bits & 1:
            return temp2+temp1+'}\n'
        else:
            return temp2+'}\n'
    return ''
    

    
        
            
            
            
        
        
        

thingTracker, frameTracker, weaponTracker = list,list,list
#modtracker: [class, index, field, what]
def compareThings():
    
    TPAIRS = [[tt,tt0],[st,st0],[wt,wt0]]
    TRACKERS = [thingTracker, frameTracker, weaponTracker]
    
    for pairnum, pair in enumerate(TPAIRS):
        lentable = len(pair[0])
        structlen = len(pair[0][0])
        print(lentable,structlen)
        for structnum in range(lentable):
            for fieldnum in range(structlen):
                if pair[0][structnum][fieldnum]!=pair[1][structnum][fieldnum]:
                    what = pair[0][structnum][fieldnum]
                    thingtracker.append([pairnum,structnum,fieldnum,what])
    return TRACKERS


state_loopstream=''
def getLoop(state_value, state_array):
    #в decorateWrite.h плохая функция. Она присобачивает лупы перед переходом в эти лупы. То есть делает дубликаты.
    #оно не ломает декорейт, но просто так жирнее получается. 18:23 13.05.2025
    global state_loopstream
    state_loop = []
    complete = False
    current_state = state_value

    while not complete:
        state_loop.append(current_state)
        current_state = state_array[current_state].nextstate

        # Проверяем, является ли текущее состояние концом (повтор или 0)
        for prev_state in state_loop:
            if current_state == prev_state or current_state == 0:
                # Добавляем финальное состояние и завершаем
                state_loop.append(current_state)
                complete = True
                break
    state_loopstream+=f'{state_loop}\n'
    return state_loop

def detect_inner_cycle(numbers):
    # Создаем словарь, где ключи - числа, а значения - индексы
    indices = {}
    done = False
    for i, num in enumerate(numbers):
        # Если число уже встречалось, значит мы нашли цикл
        if num in indices:
            # Возвращаем срез списка до индекса повторяющегося числа + 1
            temp = numbers[:indices[num] + 1]
            done = True
        # Добавляем число и его индекс в словарь
        indices[num] = i
    
    # Если цикл не найден, возвращаем весь список
    if not done or len(temp)==1:
        return numbers
    return temp
  
def CHECKFRAMES():
    for frame in st:
        if frame.tics>10:
            print(frame.index,frame.tics,'wtf!')
def SHOWTICS():
    debil=0
    framevivod=''
    for frame in st:
        framevivod+=str(frame.tics)+' '
        debil+=1
        if debil>30:
            debil=0
            framevivod+='\n'
    print(framevivod)    
        
#def main(args):


#21:17 10.05.2025 UTC+3 Description of steps.
#1. Open the dehacked

with open(patient, 'r', encoding='utf-8') as deh:
    deh_lines = deh.read().splitlines()
    
#2. Get sizes to initialise base tables
tsizeeval(deh_lines)

st = [copy.deepcopy(state_t()) for _ in range(stsize)]
tt = [copy.deepcopy(thing_t()) for _ in range(ttsize)]
wt = []

for i7, stat in enumerate(st):
    stat.nextstate = i7

initbasetables()
#SHOWTICS()
#CHECKFRAMES()


#3. Create copies to override with dehacked parsing
st0 = copy.deepcopy(st)
tt0 = copy.deepcopy(tt)
wt0 = copy.deepcopy(wt)

#3.5 Add +NOBLOCKMONST to those who fly? 17:59 04.06.2025

#4. Get blocks, parse blocks, get frame actions.

blocks = deh_read_blocks(deh_lines)
parse_blocks(deh_lines, blocks)
deh_read_frames(deh_lines)
jumpEnters = [point.enter for point in jumppoints]
jumpOuts = [point.out for point in jumppoints]


#6. Parse states to find if they lead to modified ones?

compThings()
forDecActors()
#forDecWepens()

#print(jumppoints)
#print(jumpEnters)
#print(jumpOuts)
#print(labelDict)

#print(cc)
'''
for decactor in decactors:
    vivod+=str(decactor.index)+'\n'
print(vivod, len(decactors))
'''
#print(decactors)
#print(state_loopstream)
#20:14 11.05.2025
#version 52 lol
for key,value in sfxAliases.items():
    
    if key>=500:
        key2 = key - 500
        vivod+='dehextra/sound'+str(key2)+' '+str(value)+'\n'
print(vivod)
#if __name__ == "__main__":
#	main(argv[1:])

