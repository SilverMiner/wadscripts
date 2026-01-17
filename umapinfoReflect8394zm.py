from sys import argv
from dataclasses import dataclass, fields, field
import typing
from typing import Optional, List, Tuple
from enum import IntEnum
import copy, os

#0:36 11.01.2026 todo:
#na karte 22 v nt2f juzajetsa boomovskij ekszon
#nado i takije umet chendlit

#PATIENT = "H:/Games/Doom/UMAPINFO300lnmas.txt"
PATIENT = "H:/Games/Doom/UMAPINFO (3)admorte.txt"
um2miWarnings = ''
# глобальный буфер, в который будет складываться весь вывод
vivod = []
#clusterset = set()
clusterdict = {}
interdict = {}

lvlnexts = []
lvlsecrets = []

def extract_digits(text):
    """Оставляет только цифры от строки из букв и цифр"""
    return int(''.join(char for char in text if char.isdigit()))

def increment_string_suffix(text):
    """
    Делит строку на буквенную часть и числовой суффикс,
    увеличивает число на 1 и объединяет обратно.
    """
    # Ищем индекс, с которого начинаются цифры с конца строки
    i = len(text)
    while i > 0 and text[i-1].isdigit():
        i -= 1
    
    # Разделяем строку
    left_part = text[:i]  # буквенная часть
    right_part = text[i:]  # числовая часть
    
    # Если числовой части нет, добавляем "1"
    if right_part == "":
        return left_part + "1"
    
    # Преобразуем правую часть в число, увеличиваем на 1
    # и сохраняем с тем же количеством нулей в начале (если были)
    num = int(right_part)
    new_num = num + 1
    
    # Сохраняем ведущие нули
    if right_part.startswith('0'):
        # Вычисляем новую длину с учетом ведущих нулей
        new_right_part = str(new_num).zfill(len(right_part))
        # Если число стало длиннее, обрезаем ведущие нули
        if len(new_right_part) > len(right_part):
            new_right_part = str(new_num)
    else:
        new_right_part = str(new_num)
    
    return left_part + new_right_part

def make_counter(start: int = 0):
    current = start

    def _next() -> int:
        nonlocal current
        current += 1
        return current

    return _next

def print2(*args, sep=' ', end='\n', file=None, flush=False):
    """
    Похож на встроенный print, но вместо непосредственного вывода
    собирает строку в глобальный список `vivod`.
    """
    # Формируем строку так же, как делает обычный print
    output = sep.join(str(a) for a in args) + end
    # Добавляем её в буфер
    vivod.append(output)
@dataclass
class ourbase_t:
    index: int = 0
    name: str = ""
    
    def __getitem__(self, index):
        return getattr(self, fields(self)[index].name)

    def __setitem__(self, index, value):
        field_name = fields(self)[index].name
        setattr(self, field_name, value)
        
    def __len__(self):
        return len(fields(self))
@dataclass
class cluster_t(ourbase_t):
    flat: str = "FLOOR4_8"
    music: str = ""
    enter: str = ""
    exit: str = ""

@dataclass
class ending_t(ourbase_t):
    textscreen: cluster_t() = None
    endkok: str = ""

    #13:30 10.01.2026
    #jesli endkok ne '$CAST' ne '$BUNNY' i ne '!', to ne linkujem
    #a prosto Image{Background='<endpic>'}
    
@dataclass
class level_t(ourbase_t):
    levelname: str = ""
    author: str = ""
    label: str = ""
    levelpic: str = ""
    next: str = ""
    nextsecret: str = ""
    skytexture: str = ""
    music: str = ""
    exitpic: str = ""
    enterpic: str = ""
    partime: int = 0
    endkok: str = ""
    nointermission: Optional[bool] = None
    #intertext: Optional[str] = None #str = ""
    #intertextsecret: Optional[str] = None
    intertext:str = ""
    intertextsecret:str = ""
    interbackdrop: str = ""
    intermusic: str = ""
    episode: List[Tuple[str, str, str]] = field(default_factory=list)
    bossaction: List[Tuple[str, int, int]] = field(default_factory=list)
    #19:58 09.01.2026 cluster
    cluster: int = 0

    #23:09 10.01.2026
    translator: str = ""

    _parsed_fields: set = field(default_factory=set, init=False, compare=False, repr=False)

    def set_field_value(self, field_name, value):
        """Устанавливает значение поля и отмечает его как измененное"""
        setattr(self, field_name, value)
        self._parsed_fields.add(field_name)

    def add_bossaction(self, actor, special, tag):
        """Добавляет действие босса к уровню"""
        self.set_field_value('bossaction', self.bossaction + [(actor, special, tag)])

UM2MIDICT = {
    'levelpic':'titlepatch',
    'nextsecret':'secret',
    'skytexture':'skybox'
    }    

#doClusters 20:21 10.01.2026
def isFlat(x):
    
    return True
def doClusters():
    #flat/pic, music, entertext/exittext
    for clusternum, cluster in clusterdict.items():  # FIXED: Added .items()
        print2(f'cluster {clusternum} {{')
        
        if isFlat(cluster.flat):
            print2(f'flat = {cluster.flat}')
        else:
            print2(f'pic = {cluster.flat}')

        if cluster.music:
            print2(f'music = {cluster.music}')
            
        if cluster.enter:
            print2(f'entertext = "{cluster.enter}"')
            
        if cluster.exit:
            print2(f'exittext = "{cluster.exit}"')


        
        print2('}')  # FIXED: Moved closing brace to its own line after all properties
        
def doInters():
    for internum, inter in interdict.items():
        #print2(f'Intermission {internum, inter}')
        print2(f'Intermission vauinter_{internum}{{')
        if inter.textscreen:
            it = inter.textscreen
            print2('Textscreen {')
            if it.flat:
                print2(f'Background = "{it.flat}", 1')
            if it.music:
                print2(f'Music = "{it.music}"')
            kok2 = it.exit or it.enter
            if kok2:
                print2(f'Text = "{kok2}"')
            print2('}')
        if inter.endkok == '$BUNNY':
            print2('Link = Inter_Bunny')
        elif inter.endkok == '$CAST':
            print2('Link = Inter_Cast')
        elif inter.endkok == '!':
            print2('Link = Inter_Pic3')
        elif inter.endkok:
            print2(f'Image {{ Background = {inter.endkok} }}')
        print2('}') 
        
        
        
#0:49 11.01.2026    
def is_boom_generalized(special_num):
    """
    Проверяет, является ли номер спешла BOOM generalized linedef.
    """
    return special_num >= 0x2F80  # GenCrusherBase

def translate_boom_generalized_to_hexen(special_num, tag=0, flags=0):
#def decode_boom_generalized(special_num, tag=0, flags=0):
    """
    Декодирует BOOM generalized linedef в Hexen-формат.
    Возвращает словарь с результатом или None, если не generalized.
    """
    # Определяем диапазоны (в десятичной системе!)
    GEN_CRUSHER_BASE = 0x2F80    # 12160
    GEN_STAIRS_BASE = 0x3000     # 12288  
    GEN_LIFT_BASE = 0x3400       # 13312
    GEN_LOCKED_BASE = 0x3800     # 14336
    GEN_DOOR_BASE = 0x3C00       # 15360
    GEN_CEILING_BASE = 0x4000    # 16384
    GEN_FLOOR_BASE = 0x6000      # 24576
    
    # Проверяем, является ли generalized
    if special_num < GEN_CRUSHER_BASE:
        return None  # Не generalized linedef
    
    result = {
        'special': 0,
        'args': [0, 0, 0, 0, 0],
        'flags': flags & 0x01FF,  # Очищаем activation flags
        'tag_used': False
    }
    
    # Определяем триггерный тип
    trigger_type = special_num & 0x0007
    
    # Устанавливаем флаги активации (как в C-коде)
    if trigger_type in [0, 1]:  # WalkOnce (0), WalkMany (1)
        result['flags'] |= 0x0000  # ML_ACTIVATECROSS
        if trigger_type == 1:  # WalkMany
            result['flags'] |= 0x0200  # ML_REPEATABLE
    elif trigger_type in [2, 3]:  # SwitchOnce (2), SwitchMany (3)
        if special_num & 0x0200:  # ML_PASSUSEORG из C-кода
            result['flags'] |= 0x1800  # ML_ACTIVATEUSETHROUGH
        else:
            result['flags'] |= 0x0400  # ML_ACTIVATEUSE
        if trigger_type == 3:  # SwitchMany
            result['flags'] |= 0x0200  # ML_REPEATABLE
    elif trigger_type in [4, 5]:  # PushOnce (4), PushMany (5)
        result['flags'] |= 0x1000  # ML_ACTIVATEPUSH
        if trigger_type == 5:  # PushMany
            result['flags'] |= 0x0200  # ML_REPEATABLE
    elif trigger_type in [6, 7]:  # GunOnce (6), GunMany (7)
        result['flags'] |= 0x0C00  # ML_ACTIVATEPROJECTILEHIT
        if trigger_type == 7:  # GunMany
            result['flags'] |= 0x0200  # ML_REPEATABLE
    
    # Для push-триггеров тег не используется (как в C-коде)
    if trigger_type in [4, 5]:  # Push triggers
        result['args'][0] = 0
    else:
        result['args'][0] = tag
        result['tag_used'] = True
    
    # Определяем конкретный тип по диапазонам
    if special_num <= GEN_CRUSHER_BASE:
        # Generalized crusher (tag, dnspeed, upspeed, silent, damage)
        result['special'] = LineSpecial.Generic_Crusher.value
        
        if special_num & 0x0020:
            result['flags'] |= 0x2000  # ML_MONSTERSCANACTIVATE
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 8  # C_SLOW
        elif speed_bits == 1:
            speed = 16  # C_NORMAL
        elif speed_bits == 2:
            speed = 32  # C_FAST
        else:
            speed = 64  # C_TURBO
        
        result['args'][1] = speed  # down speed
        result['args'][2] = speed  # up speed
        result['args'][3] = (special_num & 0x0040) >> 6  # silent flag
        result['args'][4] = 10  # damage
        
    elif special_num <= GEN_STAIRS_BASE:
        # Generalized stairs (tag, speed, step, dir/igntxt, reset)
        result['special'] = LineSpecial.Generic_Stairs.value
        
        if special_num & 0x0020:
            result['flags'] |= 0x2000  # ML_MONSTERSCANACTIVATE
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 2  # S_SLOW
        elif speed_bits == 1:
            speed = 4  # S_NORMAL
        elif speed_bits == 2:
            speed = 16  # S_FAST
        else:
            speed = 32  # S_TURBO
        
        # Высота ступени
        step_bits = (special_num & 0x00C0) >> 6
        if step_bits == 0:
            step = 4
        elif step_bits == 1:
            step = 8
        elif step_bits == 2:
            step = 16
        else:
            step = 24
        
        result['args'][1] = speed
        result['args'][2] = step
        result['args'][3] = (special_num & 0x0300) >> 8  # direction/ignore texture
        result['args'][4] = 0  # reset
        
    elif special_num <= GEN_LIFT_BASE:
        # Generalized lift (tag, speed, delay, target, height)
        result['special'] = LineSpecial.Generic_Lift.value
        
        if special_num & 0x0020:
            result['flags'] |= 0x2000  # ML_MONSTERSCANACTIVATE
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 16  # P_SLOW*2
        elif speed_bits == 1:
            speed = 32  # P_NORMAL*2
        elif speed_bits == 2:
            speed = 64  # P_FAST*2
        else:
            speed = 128  # P_TURBO*2
        
        # Задержка
        delay_bits = (special_num & 0x00C0) >> 6
        if delay_bits == 0:
            delay = 8
        elif delay_bits == 1:
            delay = 24
        elif delay_bits == 2:
            delay = 40
        else:
            delay = 80
        
        result['args'][1] = speed
        result['args'][2] = delay
        result['args'][3] = ((special_num & 0x0300) >> 8) + 1  # target
        result['args'][4] = 0  # height
        
    elif special_num <= GEN_LOCKED_BASE:
        # Generalized locked door (tag, speed, kind, delay, lock)
        result['special'] = LineSpecial.Generic_Door.value
        
        if special_num & 0x0080:
            result['flags'] |= 0x2000  # ML_MONSTERSCANACTIVATE
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 16  # D_SLOW
        elif speed_bits == 1:
            speed = 32  # D_NORMAL
        elif speed_bits == 2:
            speed = 64  # D_FAST
        else:
            speed = 128  # D_TURBO
        
        result['args'][1] = speed
        result['args'][2] = (special_num & 0x0020) >> 5  # kind
        result['args'][3] = 0  # delay
        
        # Тип ключа (как в C-коде)
        lock_bits = (special_num & 0x01C0) >> 6
        if lock_bits == 0:
            key = 100  # AnyKey
        elif lock_bits == 7:
            key = 101  # AllKeys
        else:
            key = lock_bits
        
        # Флаг карты/черепа
        if special_num & 0x0200:
            key |= 128  # CardIsSkull
        
        result['args'][4] = key
        
    elif special_num <= GEN_DOOR_BASE:
        # Generalized door (tag, speed, kind, delay, lock)
        result['special'] = LineSpecial.Generic_Door.value
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 16  # D_SLOW
        elif speed_bits == 1:
            speed = 32  # D_NORMAL
        elif speed_bits == 2:
            speed = 64  # D_FAST
        else:
            speed = 128  # D_TURBO
        
        result['args'][1] = speed
        result['args'][2] = (special_num & 0x0060) >> 5  # kind
        
        # Задержка
        delay_bits = (special_num & 0x0300) >> 8
        if delay_bits == 0:
            delay = 8
        elif delay_bits == 1:
            delay = 32
        elif delay_bits == 2:
            delay = 72
        else:
            delay = 240
        
        result['args'][3] = delay
        result['args'][4] = 0  # no lock
        
    elif special_num <= GEN_CEILING_BASE:
        # Generalized ceiling (tag, speed, height, target, change/model/direct/crush)
        result['special'] = LineSpecial.Generic_Ceiling.value
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 8  # F_SLOW
        elif speed_bits == 1:
            speed = 16  # F_NORMAL
        elif speed_bits == 2:
            speed = 32  # F_FAST
        else:
            speed = 64  # F_TURBO
        
        # Цель (target)
        target = ((special_num & 0x0380) >> 7) + 1
        
        if target >= 7:
            height = 24 + (target - 7) * 8
            target = 0
        else:
            height = 0
        
        # Флаги изменения/модели/направления
        change_flags = ((special_num & 0x0C00) >> 10) | \
                      ((special_num & 0x0060) >> 3) | \
                      ((special_num & 0x1000) >> 8)
        
        result['args'][1] = speed
        result['args'][2] = height
        result['args'][3] = target
        result['args'][4] = change_flags
        
    else:  # special_num <= GEN_FLOOR_BASE (но фактически всё что >= 0x6000)
        # Generalized floor (tag, speed, height, target, change/model/direct/crush)
        result['special'] = LineSpecial.Generic_Floor.value
        
        # Скорость
        speed_bits = (special_num & 0x0018) >> 3
        if speed_bits == 0:
            speed = 8  # F_SLOW
        elif speed_bits == 1:
            speed = 16  # F_NORMAL
        elif speed_bits == 2:
            speed = 32  # F_FAST
        else:
            speed = 64  # F_TURBO
        
        # Цель (target)
        target = ((special_num & 0x0380) >> 7) + 1
        
        if target >= 7:
            height = 24 + (target - 7) * 8
            target = 0
        else:
            height = 0
        
        # Флаги изменения/модели/направления
        change_flags = ((special_num & 0x0C00) >> 10) | \
                      ((special_num & 0x0060) >> 3) | \
                      ((special_num & 0x1000) >> 8)
        
        result['args'][1] = speed
        result['args'][2] = height
        result['args'][3] = target
        result['args'][4] = change_flags
    
    return result

#21:51 07.01.2026
#x это будет короче это как его мммм блять аааа ну вощем
#x это bossaction: чудик, экшон думовский, тэг.
#А мне надо specialaction. А это чё аааа надо вспомнить короче.
#21:59 07.01.2026 итак нахуй хмммм да.
#22:02 Ну вот примеры:
#specialaction = Deh_Actor_153, Door_Open, 34, 64
#specialaction = Fatso, Floor_LowerToLowest, 25, 8
#вощем надо куда-то xlat запихнуть.
# Определение типов специальных эффектов как в оригинальном коде
class LineSpecial(IntEnum):
    Polyobj_StartLine = 1
    Polyobj_RotateLeft = 2
    Polyobj_RotateRight = 3
    Polyobj_Move = 4
    Polyobj_ExplicitLine = 5
    Polyobj_MoveTimes8 = 6
    Polyobj_DoorSwing = 7
    Polyobj_DoorSlide = 8
    Line_Horizon = 9
    Door_Close = 10
    Door_Open = 11
    Door_Raise = 12
    Door_LockedRaise = 13
    Autosave = 15
    Transfer_WallLight = 16
    Floor_LowerByValue = 20
    Floor_LowerToLowest = 21
    Floor_LowerToNearest = 22
    Floor_RaiseByValue = 23
    Floor_RaiseToHighest = 24
    Floor_RaiseToNearest = 25
    Stairs_BuildDown = 26
    Stairs_BuildUp = 27
    Floor_RaiseAndCrush = 28
    Pillar_Build = 29
    Pillar_Open = 30
    Stairs_BuildDownSync = 31
    Stairs_BuildUpSync = 32
    Floor_RaiseByValueTimes8 = 35
    Floor_LowerByValueTimes8 = 36
    Ceiling_LowerByValue = 40
    Ceiling_RaiseByValue = 41
    Ceiling_CrushAndRaise = 42
    Ceiling_LowerAndCrush = 43
    Ceiling_CrushStop = 44
    Ceiling_CrushRaiseAndStay = 45
    Floor_CrushStop = 46
    Sector_CopyScroller = 58
    Plat_PerpetualRaise = 60
    Plat_Stop = 61
    Plat_DownWaitUpStay = 62
    Plat_DownByValue = 63
    Plat_UpWaitDownStay = 64
    Plat_UpByValue = 65
    Floor_LowerInstant = 66
    Floor_RaiseInstant = 67
    Floor_MoveToValueTimes8 = 68
    Ceiling_MoveToValueTimes8 = 69
    Teleport = 70
    Teleport_NoFog = 71
    ThrustThing = 72
    DamageThing = 73
    Teleport_NewMap = 74
    Teleport_EndGame = 75
    ACS_Execute = 80
    ACS_Suspend = 81
    ACS_Terminate = 82
    ACS_LockedExecute = 83
    Polyobj_OR_RotateLeft = 90
    Polyobj_OR_RotateRight = 91
    Polyobj_OR_Move = 92
    Polyobj_OR_MoveTimes8 = 93
    Pillar_BuildAndCrush = 94
    FloorAndCeiling_LowerByValue = 95
    FloorAndCeiling_RaiseByValue = 96
    Scroll_Texture_Left = 100
    Scroll_Texture_Right = 101
    Scroll_Texture_Up = 102
    Scroll_Texture_Down = 103
    Light_ForceLightning = 109
    Light_RaiseByValue = 110
    Light_LowerByValue = 111
    Light_ChangeToValue = 112
    Light_Fade = 113
    Light_Glow = 114
    Light_Flicker = 115
    Light_Strobe = 116
    Radius_Quake = 120
    Line_SetIdentification = 121
    UsePuzzleItem = 129
    Thing_Activate = 130
    Thing_Deactivate = 131
    Thing_Remove = 132
    Thing_Destroy = 133
    Thing_Projectile = 134
    Thing_Spawn = 135
    Thing_ProjectileGravity = 136
    Thing_SpawnNoFog = 137
    Floor_Waggle = 138
    Sector_ChangeSound = 140
    FS_Execute = 158
    Sector_Set3DFloor = 160
    Plane_Align = 181
    Line_Mirror = 182
    Static_Init = 190
    SetPlayerProperty = 191
    Ceiling_LowerToHighestFloor = 192
    Ceiling_LowerInstant = 193
    Ceiling_RaiseInstant = 194
    Ceiling_CrushRaiseAndStayA = 195
    Ceiling_CrushAndRaiseA = 196
    Ceiling_CrushAndRaiseSilentA = 197
    Ceiling_RaiseByValueTimes8 = 198
    Ceiling_LowerByValueTimes8 = 199
    Generic_Floor = 200
    Generic_Ceiling = 201
    Generic_Door = 202
    Generic_Lift = 203
    Generic_Stairs = 204
    Generic_Crusher = 205
    Plat_DownWaitUpStayLip = 206
    Plat_PerpetualRaiseLip = 207
    TranslucentLine = 208
    Transfer_Heights = 209
    Transfer_FloorLight = 210
    Transfer_CeilingLight = 211
    Sector_SetColor = 212
    Sector_SetFade = 213
    Sector_SetDamage = 214
    Teleport_Line = 215
    Sector_SetGravity = 216
    Stairs_BuildUpDoom = 217
    Sector_SetWind = 218
    Sector_SetFriction = 219
    Sector_SetCurrent = 220
    Scroll_Texture_Both = 221
    Scroll_Texture_Model = 222
    Scroll_Floor = 223
    Scroll_Ceiling = 224
    Scroll_Texture_Offsets = 225
    ACS_ExecuteAlways = 226
    PointPush_SetForce = 227
    Plat_RaiseAndStayTx0 = 228
    Thing_SetGoal = 229
    Plat_UpByValueStayTx = 230
    Plat_ToggleCeiling = 231
    Light_StrobeDoom = 232
    Light_MinNeighbor = 233
    Light_MaxNeighbor = 234
    Floor_TransferTrigger = 235
    Floor_TransferNumeric = 236
    ChangeCamera = 237
    Floor_RaiseToLowestCeiling = 238
    Floor_RaiseByValueTxTy = 239
    Floor_RaiseByTexture = 240
    Floor_LowerToLowestTxTy = 241
    Floor_LowerToHighest = 242
    Exit_Normal = 243
    Exit_Secret = 244
    Elevator_RaiseToNearest = 245
    Elevator_MoveToFloor = 246
    Elevator_LowerToNearest = 247
    HealThing = 248
    Door_CloseWaitOpen = 249
    Floor_Donut = 250
    FloorAndCeiling_LowerRaise = 251
    Ceiling_RaiseToNearest = 252
    Ceiling_LowerToLowest = 253
    Ceiling_LowerToFloor = 254
    Ceiling_CrushRaiseAndStaySilA = 255

#1:00 11.01.2026
    # Функция для получения имени по номеру
def get_line_special_name(number: int) -> str:
    try:
        return LineSpecial(number).name
    except ValueError:
        return f"Unknown line special: {number}"

# Определение флагов активации
class ActivationFlags:
    WALK = 0x01
    USE = 0x02
    SHOOT = 0x04
    MONST = 0x08
    MONWALK = 0x10
    REP = 0x20

# Константы скорости
C_SLOW = 8
C_NORMAL = 16
C_FAST = 32
C_TURBO = 64
CEILWAIT = 150
F_SLOW = 8
F_NORMAL = 16
F_FAST = 32
F_TURBO = 64
D_SLOW = 16
D_NORMAL = 32
D_FAST = 64
D_TURBO = 128
VDOORWAIT = 150
S_SLOW = 2
S_NORMAL = 4
S_FAST = 16
S_TURBO = 32
P_SLOW = 8
P_NORMAL = 16
P_FAST = 32
P_TURBO = 64
PLATWAIT = 105
ELEVATORSPEED = 32
DORATE = 4
SCROLL_UNIT = 64

# Специальные значения для замены
TAG = 123
LINETAG = 124

# Klucziki
NoKey = 0
RCard = 1
BCard = 2
YCard = 3
RSkull = 4
BSkull = 5
YSkull = 6

AnyKey = 100
AllKeys = 101
CardIsSkull = 128

Init_Gravity = 0,
Init_Color = 1,
Init_Damage = 2,
Init_TransferSky = 255

class TranslatedSpecial:
    """Класс для хранения переведенного специального эффекта"""
    def __init__(self, flags: int, newspecial: int, numparms: int, args: typing.List[int]):
        self.flags = flags
        self.newspecial = newspecial
        self.numparms = numparms
        self.args = args
    
    def __repr__(self):
        return f"TranslatedSpecial(flags={self.flags:#x}, newspecial={self.newspecial}, args={self.args})"


# Таблица перевода специальных эффектов (извлечена из C кода)
SpecialTranslation = [
# 0
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 1
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [0, D_SLOW, VDOORWAIT]),
# 2
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_Open, 2, [TAG, D_SLOW]),
# 3
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_Close, 2, [TAG, D_SLOW]),
# 4
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Door_Raise, 3, [TAG, D_SLOW, VDOORWAIT]),
# 5
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseToLowestCeiling, 2, [TAG, F_SLOW]),
# 6
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_NORMAL, C_NORMAL, 10]),
# 7
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Stairs_BuildUpDoom, 3, [TAG, S_SLOW, 8]),
# 8
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Stairs_BuildUpDoom, 3, [TAG, S_SLOW, 8]),
# 9
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_Donut, 3, [TAG, DORATE, DORATE]),
# 10
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_FAST, PLATWAIT, 0]),
# 11
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Exit_Normal, 1, [0]),
# 12
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Light_MaxNeighbor, 1, [TAG]),
# 13
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 255]),
# 14
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 4]),
# 15
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 3]),
# 16
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_CloseWaitOpen, 3, [TAG, D_SLOW, 240]),
# 17
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Light_StrobeDoom, 3, [TAG, 5, 35]),
# 18
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_SLOW]),
# 19
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_SLOW, 128]),
# 20
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_RaiseAndStayTx0, 2, [TAG, P_SLOW/2]),
# 21
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_DownWaitUpStayLip, 3, [TAG, P_FAST, PLATWAIT]),
# 22
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_RaiseAndStayTx0, 2, [TAG, P_SLOW/2]),
# 23
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_LowerToLowest, 2, [TAG, F_SLOW]),
# 24
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.Floor_RaiseToLowestCeiling, 2, [TAG, F_SLOW]),
# 25
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 26
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_SLOW, VDOORWAIT, BCard | CardIsSkull]),
# 27
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_SLOW, VDOORWAIT, YCard | CardIsSkull]),
# 28
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_SLOW, VDOORWAIT, RCard | CardIsSkull]),
# 29
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Raise, 3, [TAG, D_SLOW, VDOORWAIT]),
# 30
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseByTexture, 2, [TAG, F_SLOW]),
# 31
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Open, 2, [0, D_SLOW]),
# 32
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST,
                     LineSpecial.Door_LockedRaise, 4, [0, D_SLOW, 0, BCard | CardIsSkull]),
# 33
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST,
                     LineSpecial.Door_LockedRaise, 4, [0, D_SLOW, 0, RCard | CardIsSkull]),
# 34
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST,
                     LineSpecial.Door_LockedRaise, 4, [0, D_SLOW, 0, YCard | CardIsSkull]),
# 35
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 35]),
# 36
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_FAST, 136]),
# 37
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_LowerToLowestTxTy, 2, [TAG, F_SLOW]),
# 38
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_LowerToLowest, 2, [TAG, F_SLOW]),
# 39
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Teleport, 1, [TAG]),
# 40
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Generic_Ceiling, 5, [TAG, C_SLOW, 0, 1, 8]),
# 41
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_LowerToFloor, 2, [TAG, C_SLOW]),
# 42
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Close, 2, [TAG, D_SLOW]),
# 43
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToFloor, 2, [TAG, C_SLOW]),
# 44
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_LowerAndCrush, 3, [TAG, C_SLOW, 0]),
# 45
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_SLOW, 128]),
# 46
    TranslatedSpecial(ActivationFlags.SHOOT | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Door_Open, 2, [TAG, D_SLOW]),
# 47
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.Plat_RaiseAndStayTx0, 2, [TAG, P_SLOW/2]),
# 48
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Left, 1, [SCROLL_UNIT]),
# 49
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 50
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Close, 2, [TAG, D_SLOW]),
# 51
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Exit_Secret, 1, [0]),
# 52
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Exit_Normal, 1, [0]),
# 53
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_PerpetualRaiseLip, 4, [TAG, P_SLOW, PLATWAIT, 0]),
# 54
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_Stop, 1, [TAG]),
# 55
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseAndCrush, 3, [TAG, F_SLOW, 10]),
# 56
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseAndCrush, 3, [TAG, F_SLOW, 10]),
# 57
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_CrushStop, 1, [TAG]),
# 58
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 24]),
# 59
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseByValueTxTy, 3, [TAG, F_SLOW, 24]),
# 60
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToLowest, 2, [TAG, F_SLOW]),
# 61
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Open, 2, [TAG, D_SLOW]),
# 62
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_FAST, PLATWAIT, 0]),
# 63
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [TAG, D_SLOW, VDOORWAIT]),
# 64
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToLowestCeiling, 2, [TAG, F_SLOW]),
# 65
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseAndCrush, 3, [TAG, F_SLOW, 10]),
# 66
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 3]),
# 67
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 4]),
# 68
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_RaiseAndStayTx0, 2, [TAG, P_SLOW/2]),
# 69
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_SLOW]),
# 70
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_FAST, 136]),
# 71
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_FAST, 136]),
# 72
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerAndCrush, 3, [TAG, C_SLOW, 0]),
# 73
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 74
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushStop, 1, [TAG]),
# 75
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Close, 2, [TAG, D_SLOW]),
# 76
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_CloseWaitOpen, 3, [TAG, D_SLOW, 240]),
# 77
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_NORMAL, C_NORMAL, 10]),
# 78
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_TransferNumeric, 1, [TAG]),
# 79
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 35]),
# 80
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Light_MaxNeighbor, 1, [TAG]),
# 81
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 255]),
# 82
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToLowest, 2, [TAG, F_SLOW]),
# 83
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_SLOW, 128]),
# 84
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToLowestTxTy, 2, [TAG, F_SLOW]),
# 85
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Right, 1, [SCROLL_UNIT]),
# 86
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Open, 2, [TAG, D_SLOW]),
# 87
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_PerpetualRaiseLip, 4, [TAG, P_SLOW, PLATWAIT, 0]),
# 88
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_FAST, PLATWAIT, 0]),
# 89
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_Stop, 1, [TAG]),
# 90
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [TAG, D_SLOW, VDOORWAIT]),
# 91
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToLowestCeiling, 2, [TAG, F_SLOW]),
# 92
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 24]),
# 93
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValueTxTy, 3, [TAG, F_SLOW, 24]),
# 94
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseAndCrush, 3, [TAG, F_SLOW, 10]),
# 95
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_RaiseAndStayTx0, 2, [TAG, P_SLOW/2]),
# 96
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByTexture, 2, [TAG, F_SLOW]),
# 97
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport, 1, [TAG]),
# 98
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_FAST, 136]),
# 99
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, BCard | CardIsSkull]),
# 100
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_TURBO, 16, 0, 0]),
# 101
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseToLowestCeiling, 2, [TAG, F_SLOW]),
# 102
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_LowerToHighest, 3, [TAG, F_SLOW, 128]),
# 103
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Open, 2, [TAG, D_SLOW]),
# 104
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Light_MinNeighbor, 1, [TAG]),
# 105
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [TAG, D_FAST, VDOORWAIT]),
# 106
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Open, 2, [TAG, D_FAST]),
# 107
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Door_Close, 2, [TAG, D_FAST]),
# 108
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_Raise, 3, [TAG, D_FAST, VDOORWAIT]),
# 109
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_Open, 2, [TAG, D_FAST]),
# 110
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Door_Close, 2, [TAG, D_FAST]),
# 111
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Raise, 3, [TAG, D_FAST, VDOORWAIT]),
# 112
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Open, 2, [TAG, D_FAST]),
# 113
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Close, 2, [TAG, D_FAST]),
# 114
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [TAG, D_FAST, VDOORWAIT]),
# 115
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Open, 2, [TAG, D_FAST]),
# 116
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Close, 2, [TAG, D_FAST]),
# 117
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_Raise, 3, [0, D_FAST, VDOORWAIT]),
# 118
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_Open, 2, [0, D_FAST]),
# 119
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_SLOW]),
# 120
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_TURBO, PLATWAIT, 0]),
# 121
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_TURBO, PLATWAIT, 0]),
# 122
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_TURBO, PLATWAIT, 0]),
# 123
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_DownWaitUpStayLip, 4, [TAG, P_TURBO, PLATWAIT, 0]),
# 124
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Exit_Secret, 1, [0]),
# 125
    TranslatedSpecial(ActivationFlags.MONWALK,
                     LineSpecial.Teleport, 1, [TAG]),
# 126
    TranslatedSpecial(ActivationFlags.MONWALK | ActivationFlags.REP,
                     LineSpecial.Teleport, 1, [TAG]),
# 127
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_TURBO, 16, 0, 0]),
# 128
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_SLOW]),
# 129
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_FAST]),
# 130
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_FAST]),
# 131
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_FAST]),
# 132
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseToNearest, 2, [TAG, F_FAST]),
# 133
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, BCard | CardIsSkull]),
# 134
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, RCard | CardIsSkull]),
# 135
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, RCard | CardIsSkull]),
# 136
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, YCard | CardIsSkull]),
# 137
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_LockedRaise, 4, [TAG, D_FAST, 0, YCard | CardIsSkull]),
# 138
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 255]),
# 139
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 35]),
# 140
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseByValueTimes8, 3, [TAG, F_SLOW, 64]),
# 141
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_CrushAndRaiseSilentA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 142
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseByValueTimes8, 3, [TAG, F_SLOW, 64]),
# 143
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 3]),
# 144
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 4]),
# 145
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_LowerToFloor, 2, [TAG, C_SLOW]),
# 146
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_Donut, 3, [TAG, DORATE, DORATE]),
# 147
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValueTimes8, 3, [TAG, F_SLOW, 64]),
# 148
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 3]),
# 149
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_UpByValueStayTx, 3, [TAG, P_SLOW/2, 4]),
# 150
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseSilentA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 151
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.FloorAndCeiling_LowerRaise, 3, [TAG, F_SLOW, C_SLOW]),
# 152
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToFloor, 2, [TAG, C_SLOW]),
# 153
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_TransferTrigger, 1, [TAG]),
# 154
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_TransferTrigger, 1, [TAG]),
# 155
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_Donut, 3, [TAG, DORATE, DORATE]),
# 156
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Light_StrobeDoom, 3, [TAG, 5, 35]),
# 157
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Light_MinNeighbor, 1, [TAG]),
# 158
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseByTexture, 2, [TAG, F_SLOW]),
# 159
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_LowerToLowestTxTy, 2, [TAG, F_SLOW]),
# 160
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseByValueTxTy, 3, [TAG, F_SLOW, 24]),
# 161
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 24]),
# 162
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_PerpetualRaiseLip, 4, [TAG, P_SLOW, PLATWAIT, 0]),
# 163
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Plat_Stop, 1, [TAG]),
# 164
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_NORMAL, C_NORMAL, 10]),
# 165
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_CrushAndRaiseSilentA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 166
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.FloorAndCeiling_LowerRaise, 3, [TAG, F_SLOW, C_SLOW]),
# 167
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_LowerAndCrush, 3, [TAG, C_SLOW, 0]),
# 168
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_CrushStop, 1, [TAG]),
# 169
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Light_MaxNeighbor, 1, [TAG]),
# 170
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 35]),
# 171
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Light_ChangeToValue, 2, [TAG, 255]),
# 172
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Light_StrobeDoom, 3, [TAG, 5, 35]),
# 173
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Light_MinNeighbor, 1, [TAG]),
# 174
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST,
                     LineSpecial.Teleport, 1, [TAG]),
# 175
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Door_CloseWaitOpen, 3, [TAG, F_SLOW, 240]),
# 176
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByTexture, 2, [TAG, F_SLOW]),
# 177
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToLowestTxTy, 2, [TAG, F_SLOW]),
# 178
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValueTimes8, 3, [TAG, F_SLOW, 64]),
# 179
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValueTxTy, 3, [TAG, F_SLOW, 24]),
# 180
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 24]),
# 181
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_PerpetualRaiseLip, 4, [TAG, P_SLOW, PLATWAIT, 0]),
# 182
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_Stop, 1, [TAG]),
# 183
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_NORMAL, C_NORMAL, 10]),
# 184
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 185
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushAndRaiseSilentA, 4, [TAG, C_SLOW, C_SLOW, 10]),
# 186
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.FloorAndCeiling_LowerRaise, 3, [TAG, F_SLOW, C_SLOW]),
# 187
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerAndCrush, 3, [TAG, C_SLOW, 0]),
# 188
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_CrushStop, 1, [TAG]),
# 189
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_TransferTrigger, 1, [TAG]),
# 190
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_TransferTrigger, 1, [TAG]),
# 191
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_Donut, 3, [TAG, DORATE, DORATE]),
# 192
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Light_MaxNeighbor, 1, [TAG]),
# 193
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Light_StrobeDoom, 3, [TAG, 5, 35]),
# 194
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Light_MinNeighbor, 1, [TAG]),
# 195
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport, 1, [TAG]),
# 196
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Door_CloseWaitOpen, 3, [TAG, D_SLOW, 240]),
# 197
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.Exit_Normal, 1, [0]),
# 198
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.Exit_Secret, 1, [0]),
# 199
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_LowerToLowest, 2, [TAG, C_SLOW]),
# 200
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Ceiling_LowerToHighestFloor, 2, [TAG, C_SLOW]),
# 201
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToLowest, 2, [TAG, C_SLOW]),
# 202
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToHighestFloor, 2, [TAG, C_SLOW]),
# 203
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_LowerToLowest, 2, [TAG, C_SLOW]),
# 204
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Ceiling_LowerToHighestFloor, 2, [TAG, C_SLOW]),
# 205
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToLowest, 2, [TAG, C_SLOW]),
# 206
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Ceiling_LowerToHighestFloor, 2, [TAG, C_SLOW]),
# 207
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 208
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 209
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 210
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 211
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Plat_ToggleCeiling, 1, [TAG]),
# 212
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Plat_ToggleCeiling, 1, [TAG]),
# 213
    TranslatedSpecial(0,
                     LineSpecial.Transfer_FloorLight, 1, [TAG]),
# 214
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Ceiling, 5, [TAG, 6, 0, 0, 0]),
# 215
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 6, 0, 0, 0]),
# 216
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 6, 1, 0, 0]),
# 217
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 6, 2, 0, 0]),
# 218
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Model, 2, [LINETAG, 2]),
# 219
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_LowerToNearest, 2, [TAG, F_SLOW]),
# 220
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToNearest, 2, [TAG, F_SLOW]),
# 221
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_LowerToNearest, 2, [TAG, F_SLOW]),
# 222
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_LowerToNearest, 2, [TAG, F_SLOW]),
# 223
    TranslatedSpecial(0,
                     LineSpecial.Sector_SetFriction, 2, [TAG, 0]),
# 224
    TranslatedSpecial(0,
                     LineSpecial.Sector_SetWind, 4, [TAG, 0, 0, 1]),
# 225
    TranslatedSpecial(0,
                     LineSpecial.Sector_SetCurrent, 4, [TAG, 0, 0, 1]),
# 226
    TranslatedSpecial(0,
                     LineSpecial.PointPush_SetForce, 4, [TAG, 0, 0, 1]),
# 227
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Elevator_RaiseToNearest, 2, [TAG, ELEVATORSPEED]),
# 228
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Elevator_RaiseToNearest, 2, [TAG, ELEVATORSPEED]),
# 229
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Elevator_RaiseToNearest, 2, [TAG, ELEVATORSPEED]),
# 230
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Elevator_RaiseToNearest, 2, [TAG, ELEVATORSPEED]),
# 231
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Elevator_LowerToNearest, 2, [TAG, ELEVATORSPEED]),
# 232
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Elevator_LowerToNearest, 2, [TAG, ELEVATORSPEED]),
# 233
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Elevator_LowerToNearest, 2, [TAG, ELEVATORSPEED]),
# 234
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Elevator_LowerToNearest, 2, [TAG, ELEVATORSPEED]),
# 235
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Elevator_MoveToFloor, 2, [TAG, ELEVATORSPEED]),
# 236
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Elevator_MoveToFloor, 2, [TAG, ELEVATORSPEED]),
# 237
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Elevator_MoveToFloor, 2, [TAG, ELEVATORSPEED]),
# 238
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Elevator_MoveToFloor, 2, [TAG, ELEVATORSPEED]),
# 239
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_TransferNumeric, 1, [TAG]),
# 240
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_TransferNumeric, 1, [TAG]),
# 241
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_TransferNumeric, 1, [TAG]),
# 242
    TranslatedSpecial(0,
                     LineSpecial.Transfer_Heights, 1, [TAG]),
# 243
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 0]),
# 244
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 0]),
# 245
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Ceiling, 5, [TAG, 5, 0, 0, 0]),
# 246
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 5, 0, 0, 0]),
# 247
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 5, 1, 0, 0]),
# 248
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 5, 2, 0, 0]),
# 249
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Model, 2, [LINETAG, 1]),
# 250
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Ceiling, 5, [TAG, 4, 0, 0, 0]),
# 251
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 4, 0, 0, 0]),
# 252
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 4, 1, 0, 0]),
# 253
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Floor, 5, [TAG, 4, 2, 0, 0]),
# 254
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Model, 2, [LINETAG, 0]),
# 256
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_SLOW, 8, 0, 0]),
# 257
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_TURBO, 16, 0, 0]),
# 258
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_SLOW, 8, 0, 0]),
# 259
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Stairs_BuildUpDoom, 5, [TAG, S_TURBO, 16, 0, 0]),
# 260
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 2, [LINETAG, 128]),
# 261
    TranslatedSpecial(0,
                     LineSpecial.Transfer_CeilingLight, 1, [TAG]),
# 262
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.MONST,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 1]),
# 263
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP | ActivationFlags.MONST,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 1]),
# 264
    TranslatedSpecial(ActivationFlags.MONWALK,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 1]),
# 265
    TranslatedSpecial(ActivationFlags.MONWALK | ActivationFlags.REP,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 1]),
# 266
    TranslatedSpecial(ActivationFlags.MONWALK,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 0]),
# 267
    TranslatedSpecial(ActivationFlags.MONWALK | ActivationFlags.REP,
                     LineSpecial.Teleport_Line, 3, [TAG, TAG, 0]),
# 268
    TranslatedSpecial(ActivationFlags.MONWALK,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 269
    TranslatedSpecial(ActivationFlags.MONWALK | ActivationFlags.REP,
                     LineSpecial.Teleport_NoFog, 1, [TAG]),
# 270
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 271
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 3, [TAG, Init_TransferSky, 0]),
# 272
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 3, [TAG, Init_TransferSky, 1]),
# 273
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.FS_Execute, 2, [TAG, 1]),
# 274
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 275
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.FS_Execute, 2, [TAG, 1]),
# 276
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 277
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 278
    TranslatedSpecial(ActivationFlags.SHOOT | ActivationFlags.REP,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 279
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.FS_Execute, 1, [TAG]),
# 280
    TranslatedSpecial(0,
                     LineSpecial.Transfer_Heights, 2, [TAG, 12]),
# 281
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 0, 255]),
# 282
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 2, [TAG, 1]),
# 283
    TranslatedSpecial(0,
                     LineSpecial.Transfer_WallLight, 2, [TAG, 1]),
# 284
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 3, [LINETAG, 128, 0]),
# 285
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 3, [LINETAG, 192, 0]),
# 286
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 3, [LINETAG, 48, 0]),
# 287
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 3, [LINETAG, 128, 1]),
# 288
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 3, [LINETAG, 255, 0]),
# 289
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 1, 255]),
# 290
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST | ActivationFlags.REP,
                     LineSpecial.Polyobj_StartLine, 4, [TAG, 0, 1, 0]),
# 291
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST | ActivationFlags.REP,
                     LineSpecial.Polyobj_DoorSwing, 4, [TAG, P_FAST, P_TURBO, D_TURBO]),
# 292
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.MONST | ActivationFlags.REP,
                     LineSpecial.Polyobj_DoorSwing, 4, [TAG, -P_FAST, P_TURBO, D_TURBO]),
# 293
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.ACS_Execute, 4, [27, 0, TAG, 1]),
# 294
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 295
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 296
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 297
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 298
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 299
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 300
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 1, 127]),
# 301
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 127]),
# 302
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 3, 6, 127]),
# 303
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 2, [TAG, 3]),
# 304
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 255]),
# 305
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 3, [TAG, 3, 2]),
# 306
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 2, [TAG, 1]),
# 307
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 308
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 309
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 310
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 311
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 312
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 313
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 314
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 315
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 316
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 317
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 318
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 319
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 320
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 321
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 322
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 323
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 324
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 325
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 326
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 327
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 328
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 329
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 330
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 331
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 332
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 2, [TAG, 4]),
# 333
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 2, [TAG, Init_Gravity]),
# 334
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 2, [TAG, Init_Color]),
# 335
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 2, [TAG, Init_Damage]),
# 336
    TranslatedSpecial(0,
                     LineSpecial.Line_Mirror, 1, []),
# 337
    TranslatedSpecial(0,
                     LineSpecial.Line_Horizon, 1, []),
# 338
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_Waggle, 5, [TAG, 24, 32, 0, 0]),
# 339
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_Waggle, 5, [TAG, 12, 32, 0, 0]),
# 340
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [1, 0]),
# 341
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [0, 1]),
# 342
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [1, 1]),
# 343
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [2, 0]),
# 344
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [0, 2]),
# 345
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [2, 2]),
# 346
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [2, 1]),
# 347
    TranslatedSpecial(0,
                     LineSpecial.Plane_Align, 2, [1, 2]),
# 348
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Autosave, 1, []),
# 349
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Autosave, 1, []),
# 350
    TranslatedSpecial(0,
                     LineSpecial.Transfer_Heights, 2, [TAG, 2]),
# 351
    TranslatedSpecial(0,
                     LineSpecial.Transfer_Heights, 2, [TAG, 6]),
# 352
    TranslatedSpecial(0,
                     LineSpecial.Sector_CopyScroller, 2, [TAG, 1]),
# 353
    TranslatedSpecial(0,
                     LineSpecial.Sector_CopyScroller, 2, [TAG, 2]),
# 354
    TranslatedSpecial(0,
                     LineSpecial.Sector_CopyScroller, 2, [TAG, 6]),
# 355
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 356
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 357
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 358
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 359
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 360
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 361
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 362
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 363
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 364
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 365
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 366
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 367
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 368
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 369
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 370
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 371
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 372
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 373
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 374
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 375
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 376
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 377
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 378
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 379
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 3, [TAG, 3, 1]),
# 380
    TranslatedSpecial(0,
                     LineSpecial.Static_Init, 3, [TAG, 3, 0]),
# 381
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 382
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 383
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 384
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 385
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 386
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 387
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 388
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 389
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 390
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 391
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 392
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 393
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 394
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 395
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 396
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 397
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 398
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 399
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 400
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 0, 255]),
# 401
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 16, 255]),
# 402
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 32, 255]),
# 403
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 255]),
# 404
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 204]),
# 405
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 153]),
# 406
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 102]),
# 407
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 2, 2, 51]),
# 408
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 3, [TAG, 2, 2]),
# 409
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 2, [LINETAG, 204]),
# 410
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 2, [LINETAG, 153]),
# 411
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 2, [LINETAG, 101]),
# 412
    TranslatedSpecial(0,
                     LineSpecial.TranslucentLine, 2, [LINETAG, 50]),
# 413
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 8, 255]),
# 414
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 8, 204]),
# 415
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 8, 153]),
# 416
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 8, 102]),
# 417
    TranslatedSpecial(0,
                     LineSpecial.Sector_Set3DFloor, 4, [TAG, 1, 8, 51]),
# 418
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 419
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 420
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 421
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 422
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Right, 1, [SCROLL_UNIT]),
# 423
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Up, 1, [SCROLL_UNIT]),
# 424
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Down, 1, [SCROLL_UNIT]),
# 425
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Both, 5, [0, SCROLL_UNIT, 0, 0, SCROLL_UNIT]),
# 426
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Both, 5, [0, SCROLL_UNIT, 0, SCROLL_UNIT, 0]),
# 427
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Both, 5, [0, 0, SCROLL_UNIT, 0, SCROLL_UNIT]),
# 428
    TranslatedSpecial(0,
                     LineSpecial.Scroll_Texture_Both, 5, [0, 0, SCROLL_UNIT, SCROLL_UNIT, 0]),
# 429
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 430
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 431
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 432
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 433
    TranslatedSpecial(0,
                     0, 0, [TAG]),
# 434
    TranslatedSpecial(ActivationFlags.USE,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2]),
# 435
    TranslatedSpecial(ActivationFlags.USE | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2]),
# 436
    TranslatedSpecial(ActivationFlags.WALK,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2]),
# 437
    TranslatedSpecial(ActivationFlags.WALK | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2]),
# 438
    TranslatedSpecial(ActivationFlags.SHOOT,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2]),
# 439
    TranslatedSpecial(ActivationFlags.SHOOT | ActivationFlags.REP,
                     LineSpecial.Floor_RaiseByValue, 3, [TAG, F_SLOW, 2])
]
def simple_convert_generalized(result_dict):
    """
    Упрощенная конверсия для использования в simple_translate_doom_to_hexen
    """
    # Берем флаги как есть
    flags = 0
    
    # Определяем флаги активации из строковых флагов
    line_flags = result_dict['flags']
    
    # Простая конвертация
    if line_flags & 0x0200:  # REPEATABLE
        flags |= ActivationFlags.REP
    if line_flags & 0x2000:  # MONSTERSCANACTIVATE
        flags |= ActivationFlags.MONST
    
    # Для линий обычно есть WALK флаг, если нет других триггеров
    if not (line_flags & 0x0400) and not (line_flags & 0x0C00) and not (line_flags & 0x1000):
        flags |= ActivationFlags.WALK
    
    newspecial = result_dict['special']
    args = result_dict['args']
    
    # Убираем нули в конце
    numparms = 0
    for i in range(len(args)):
        if args[i] != 0:
            numparms = i + 1
    
    # Если есть реальные аргументы, сохраняем их
    clean_args = args[:numparms] if numparms > 0 else []
    
    return TranslatedSpecial(flags=flags, newspecial=newspecial, 
                            numparms=numparms, args=clean_args)

def simple_translate_doom_to_hexen(doom_special: int, doom_tag: int = 0) -> str:
    """
    Упрощенная версия - только строковый вывод.
    """
    #if not (doom_special >= 0 and doom_special <= len(SpecialTranslation)):
        
    #if (doom_special >=12160 and <= 32767):
    if not (
        (doom_special >= 0 and doom_special <= len(SpecialTranslation))
            or (doom_special >=12160 and doom_special <= 32767)
        ):
        return f"ERROR, {doom_tag}, 0, 0, 0, 0"

    if doom_special >= 0 and doom_special <= len(SpecialTranslation):
        translation = SpecialTranslation[doom_special]
    else:
        translation = translate_boom_generalized_to_hexen(doom_special, doom_tag, 0)
        #print(translation)
        translation = simple_convert_generalized(translation)
    #print(translation)
    
    #print(repr(translation), repr(simple_convert_generalized(translation)))
    # Подготавливаем аргументы
    args = [0] * 5

    #if doom_special >= 0 and doom_special <= len(SpecialTranslation):
    for i in range(min(translation.numparms, 5)):
        if translation.args[i] == TAG and doom_special >= 0 and doom_special <= len(SpecialTranslation):
            args[i] = doom_tag
        elif translation.args[i] == LINETAG and doom_special >= 0 and doom_special <= len(SpecialTranslation):
            args[i] = doom_tag
        else:
            args[i] = translation.args[i]
    
    # Получаем имя
    special_name = "0"
    if translation.newspecial > 0:
        try:
            special_name = LineSpecial(translation.newspecial).name
        except:
            special_name = str(translation.newspecial)
    
    # Формируем строку
    result = [special_name]
    
    # Добавляем только используемые аргументы, остальные нули
    for i in range(5):
        if i < translation.numparms:
            result.append(str(args[i]))
        else:
            result.append("0")
    
    while result and result[-1] == "0":
        result.pop()          # удаляем последний элемент, пока он "0"
    
    return ", ".join(result)

    
    
EPISMAS = []
def parse_levels_robust(filename):
    """Парсер для блоков MAP с поддержкой многострочных значений"""
    global EPISMAS
    clusterkok = make_counter()
    level_dict = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    #print2(f"//Всего строк в файле: {len(lines)}")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ищем начало блока MAP
        if line.upper().startswith('MAP '):
            # Получаем название карты
            parts = line.split()
            if len(parts) >= 2:
                map_name = parts[1].strip('{').strip()
            else:
                map_name = ""

            
            #if map_name=='MAP30':
                
            
            #print2(f"Начало блока MAP: {map_name}")
            
            # Создаем объект уровня
            level = level_t(index=len(level_dict), name=map_name)

            #21:22 10.01.2026
            #Navoraczivajem defolty

            
            if map_name == "MAP06":
                level.intertext = 'lookup, "C1TEXT"'
            elif map_name == "MAP07":
                level.add_bossaction('Fatso', 23, 666)
                level.add_bossaction('Arachnotron', 30, 667)
            elif map_name == "MAP11":
                level.intertext = 'lookup, "C2TEXT"'
            elif map_name == "MAP20":
                level.intertext = 'lookup, "C3TEXT"'
            elif map_name == "MAP30":
                level.intertext = 'lookup, "C4TEXT"'
            elif map_name == "MAP15":
                level.intertextsecret = 'lookup, "C5TEXT"'
            elif map_name == "MAP31":
                level.intertextsecret = 'lookup, "C6TEXT"'

            elif map_name == "E1M1":
                episoda = ('M_EPI1', 'Knee-Deep in the Dead', 'K')
                level.set_field_value('episode', [episoda])
            elif map_name == "E2M1":
                episoda = ('M_EPI2', 'The Shores of Hell', 'T')
                level.set_field_value('episode', [episoda])
            elif map_name == "E3M1":
                episoda = ('M_EPI3', 'Inferno', 'I')
                level.set_field_value('episode', [episoda])
            elif map_name == "E4M1":
                episoda = ('M_EPI4', 'Thy Flesh Consumed', 'T')
                level.set_field_value('episode', [episoda])                
                
            elif map_name == "E1M8":
                level.add_bossaction('BaronOfHell', 23, 666)
            elif map_name == "E2M8":
                level.add_bossaction('Cyberdemon', 11, 666)
            elif map_name == "E3M8":
                level.add_bossaction('SpiderMastermind', 11, 666)

            elif map_name == "E4M6":
                level.add_bossaction('Cyberdemon', 109, 666)                
            elif map_name == "E4M8":
                level.add_bossaction('SpiderMastermind', 23, 666)
            
            # Начинаем читать поля со следующей строки
            i += 1
            
            # Флаг для обработки многострочного значения
            multiline_value = False
            current_field = ""
            accumulated_lines = []
            
            while i < len(lines):
                current_line = lines[i].rstrip('\n')
                stripped_line = current_line.strip()
                
                # Проверяем, не конец ли это блока
                if '}' in stripped_line and not multiline_value:
                    # Если это простая строка с } (не внутри многострочного значения)
                    #print2(f"Конец блока {map_name}")
                    i += 1
                    break
                
                # Если мы в процессе сбора многострочного значения
                if multiline_value:
                    # Проверяем, заканчивается ли значение на этой строке
                    if stripped_line.endswith('"'):
                        # Закрывающая кавычка - конец значения
                        # Убираем последнюю кавычку
                        line_without_end_quote = current_line.rstrip('"')
                        accumulated_lines.append(line_without_end_quote)
                        full_value = '\n'.join(accumulated_lines)
                        
                        # Устанавливаем значение поля
                        if hasattr(level, current_field):
                            level.set_field_value(current_field, full_value)
                        
                        # Сбрасываем флаги
                        multiline_value = False
                        current_field = ""
                        accumulated_lines = []
                    else:
                        # Продолжение многострочного значения
                        accumulated_lines.append(current_line)
                else:
                    # Обычная строка (не многострочное значение)
                    if stripped_line and not stripped_line.startswith('//'):
                        # Проверяем, есть ли присваивание
                        if '=' in stripped_line:
                            # Разделяем на ключ и значение
                            key_part, value_part = stripped_line.split('=', 1)
                            key = key_part.strip().lower()
                            value = value_part.strip()
                            # Обработка специальных полей end*
                            if key.startswith('end'):
                                if key == 'endpic':
                                    level.set_field_value('endkok', value)
                                elif key == 'endcast':
                                    level.set_field_value('endkok', '$CAST')
                                elif key == 'endbunny':
                                    level.set_field_value('endkok', '$BUNNY')
                                else:
                                    level.set_field_value('endkok', '!')
                            
                            # Если значение пустое или его нет в текущей строке
                            elif not value or value == '':
                                # Ищем значение на следующей строке
                                found_value = False
                                j = i + 1
                                while j < len(lines):
                                    next_line = lines[j].rstrip('\n').strip()
                                    # Пропускаем пустые строки и комментарии
                                    if not next_line or next_line.startswith('//'):
                                        j += 1
                                        continue
                                    
                                    # Нашли следующую непустую строку - это значение
                                    value = next_line
                                    found_value = True
                                    i = j  # Переходим к строке со значением
                                    break
                                
                                if not found_value:
                                    # Если так и не нашли значение, оставляем пустым
                                    value = ''
                            
                            # Теперь обрабатываем найденное значение
                            if value.startswith('"') and key != 'episode' and key != 'bossaction':
                                # Если значение заканчивается кавычкой в той же строке
                                if value.endswith('"') and not value.endswith('",'):
                                    # Простое строковое значение
                                    value = value[1:-1]
                                    if hasattr(level, key):
                                        level.set_field_value(key, value)
                                else:
                                    # Начинается многострочное значение
                                    multiline_value = True
                                    current_field = key
                                    # Убираем начальную кавычку
                                    accumulated_lines.append(value[1:])
                            else:
                                # Нестроковое значение
                                # Обработка числовых значений
                                if key == 'partime':
                                    try:
                                        value = int(value)
                                        level.set_field_value(key, value)
                                    except ValueError:
                                        print2(f"//Неверное значение partime: {value}")
                                # Обработка списка episode (БОЛЕЕ ТОЧНАЯ ВЕРСИЯ)
                                elif key == 'episode':
                                    
                                    try:
                                        # Формат: episode = "M_EPI1", "Pick Your Eggnog", "P"
                                        cleaned_value = value.strip()
                                        
                                        # Разделяем строку с учетом кавычек
                                        parts = []
                                        current_part = ""
                                        in_quotes = False
                                        escape_next = False
                                        
                                        # ИЗМЕНЕНИЕ: используем другую переменную для индекса
                                        for char_index, char in enumerate(cleaned_value):
                                            if escape_next:
                                                current_part += char
                                                escape_next = False
                                            elif char == '\\':
                                                escape_next = True
                                            elif char == '"':
                                                in_quotes = not in_quotes
                                                current_part += char
                                            elif char == ',' and not in_quotes:
                                                parts.append(current_part.strip())
                                                current_part = ""
                                            else:
                                                current_part += char
                                        
                                        # Добавляем последнюю часть
                                        if current_part:
                                            parts.append(current_part.strip())
                                        
                                        # Убираем внешние кавычки из каждой части
                                        cleaned_parts = []
                                        for part in parts:
                                            if part.startswith('"') and part.endswith('"'):
                                                part = part[1:-1]
                                            cleaned_parts.append(part)
                                        
                                        # Должно быть 3 части
                                        if len(cleaned_parts) >= 3:
                                            episode_tuple = (cleaned_parts[0], cleaned_parts[1], cleaned_parts[2])
                                            level.set_field_value('episode', [episode_tuple])
                                            combined_tuple = (level.name,) + episode_tuple #10:33 09.01.2026
                                            EPISMAS.append(combined_tuple)  #9:54 09.01.2026
                                            #print2(episode_tuple) #14:05 04.01.2026 was for debug
                                        elif cleaned_parts[0] == 'clear':
                                            level.set_field_value('episode', [])
                                        else:
                                            print2(f"//Предупреждение: episode содержит {len(cleaned_parts)} частей вместо 3: {cleaned_parts}")
                                            
                                    except Exception as e:
                                        print2(f"//Ошибка обработки episode: {e}, значение: {value}")
                                # Обработка списка bossaction
                                elif key == 'bossaction':
                                    try:
                                        # Формат: bossaction = thingtype, linespecial, tag
                                        cleaned_value = value.strip()
                                        
                                        # Разделяем на три части
                                        parts = []
                                        in_quotes = False
                                        current_part = ""
                                        
                                        for char in cleaned_value:
                                            if char == '"':
                                                in_quotes = not in_quotes
                                            elif char == ',' and not in_quotes:
                                                parts.append(current_part.strip())
                                                current_part = ""
                                            else:
                                                current_part += char
                                        
                                        if current_part:
                                            parts.append(current_part.strip())
                                        
                                        # Убираем кавычки из строковых частей
                                        parts = [p.strip('"') if '"' in p else p.strip() for p in parts]
                                        
                                        if len(parts) >= 3:
                                            try:
                                                tag = int(parts[2])
                                                level.set_field_value('bossaction', level.bossaction + [(parts[0], int(parts[1]), tag)])
                                            except ValueError:
                                                print2(f"//Неверный tag в bossaction: {parts[2]}")
                                        elif parts[0] == 'clear':
                                            level.set_field_value('bossaction', [])
                                    except Exception as e:
                                        print2(f"//Ошибка обработки bossaction: {e}, значение: {value}")
                                # Обработка логических полей
                                elif key in ['endbunny', 'endcast', 'endgame', 'nointermission']:
                                    if value.lower() == 'true':
                                        level.set_field_value(key, True)
                                    elif value.lower() == 'false':
                                        level.set_field_value(key, False)
                                    else:
                                        level.set_field_value(key, None)
                                # Обработка других полей
                                elif hasattr(level, key):
                                    level.set_field_value(key, value)

                                
                
                i += 1
                
                # Защита от бесконечного цикла
                if i > len(lines):
                    print2("//Превышен лимит строк. Возможно, ошибка в формате файла.")
                    break
            '''
            #Постобработка уровня
            #mock_count = 0 #+1 i will give for each intertext
            #mock = level.intertext + level.intertextsecret
            #mock_count = !!level.intertext + !!level.intertextsecret
                
            #mock = level.intertext or level.intertextsecret
            #exit_count = sum(bool(x) for x in [level.intertext, level.intertextsecret])
            #19:52 09.01.2026
            #0 - net textov, 1 - tolko intertext, 2 - tolko secrettext, 3 - oba texta
            if muga:
                #newcluster = 
                if exita == 0 and level.endkok: #endgame razrulivajem
                    pass
                elif exita == 1: #jest odin normal exit
                    level.cluster = clusterkok()
                    clusterset.add(level.cluster)
            '''
            #10:32 10.01.2026
            if not level.next:
                level.next = increment_string_suffix(map_name)
            #13:19 10.01.2026
            #if not level.nextsecret:
            #    level.nextsecret = level.next
            '''
            interkok = [level.intertext, level.intertextsecret]
            interptr = -1 #-1 n
            
            for i in interkok:
                if interkok[i]:
                    interptr = i
                    break
            '''
            
            muga = int(bool(level.intertext)) + 2 * int(bool(level.intertextsecret))
            #exita = int(bool(level.next)) + 2 * int(bool(level.nextsecret))

            for fielda in ['label', 'intertext', 'intertextsecret']:
                val = getattr(level, fielda)
                if val == 'clear':
                    setattr(level, fielda, '')
            #22:12 10.01.2026      
            if not level.nextsecret:
                level.intertextsecret = ''
                
                

#12:30 10.01.2026 BIASED_PRECISION_ROUTINE
            #biased_exit_count = 1 if level.next == level.nextsecret else 2
            has_secret_exit = level.nextsecret and level.next != level.nextsecret
            biased_exit_count = 2 if has_secret_exit else 1

            
            '''
            if muga&1 or muga&2:
                if level.endkok:
                    next = endsequence, vauinterXY
                    #level.next =
                if level.next == level.nextsecret:
                    level.cluster = clusterkok()
                    clusterset.add(level.cluster)
                else:
            '''
            
            #level.cluster = clusterkok()
            #clustertemp = clusterkok()
            clustertemp = extract_digits(map_name)
            
            if biased_exit_count == 1 and \
            not level.endkok and \
            (level.intertext
            or level.intertextsecret):
            #and not level.intertextsecret:
                #doExitText

                newcluster = clusterdict.get(clustertemp, cluster_t())
                newcluster.flat = level.interbackdrop or 'FLOOR4_8'
                newcluster.exit = level.intertext or level.intertextsecret
                if level.intermusic:
                    newcluster.music = level.intermusic

                clusterdict[clustertemp] = newcluster
                level.cluster = clustertemp

            elif biased_exit_count == 1 and level.endkok:
                level.next = f'endsequence, vauinter_{clustertemp}'

                textscreen = interdict.get(clustertemp, cluster_t())
                textscreen.flat = level.interbackdrop or 'FLOOR4_8'
                textscreen.exit = level.intertext

                newinter = ending_t()
                newinter.textscreen = textscreen
                newinter.endkok = level.endkok
                interdict[clustertemp] = newinter
            #10:34 12.01.2026
            #tryEnterText
            #elif biased_exit_count == 2 and not level.endkok:
            #    level
                
            

            # Добавляем уровень в словарь
            level_dict[map_name] = level
        else:
            i += 1
    
    #print2(f"//Найдено блоков: {len(level_dict)}")
    #print(level_dict)
    return level_dict

def parse_file_robust(filename):
    """Более надежный парсер для произвольных блоков"""
    level_dict = parse_levels_robust(filename)
    
    if level_dict:
        return level_dict
    
    return {}

def skokoEnters(levelstr, level_dict):
    lvlnexts.clear()
    lvlsecrets.clear()
    
    #print2(f"\n=== DEBUG skokoEnters для {levelstr} ===")
    
    for lvlname, level in level_dict.items():
        if level.next == levelstr:
            #print2(f"  Найдено через level.next: {lvlname}, intertext: '{level.intertext}'")
            lvlnexts.append(level)
        if level.nextsecret == levelstr:
            #print2(f"  Найдено через level.nextsecret: {lvlname}, intertextsecret: '{level.intertextsecret}'")
            lvlsecrets.append(level)
    
    uniqueInterTexts = set()
    
    for sok in lvlnexts:
        if sok.intertext:
            #print2(f"  Добавляю intertext из {sok.name}: '{sok.intertext}'")
            uniqueInterTexts.add(sok.intertext)
            
    for sok in lvlsecrets:
        if sok.intertextsecret:
            #print2(f"  Добавляю intertextsecret из {sok.name}: '{sok.intertextsecret}'")
            uniqueInterTexts.add(sok.intertextsecret)
    
    #print2(f"  Уникальных текстов: {len(uniqueInterTexts)}")
    #print2(f"  === КОНЕЦ DEBUG ===\n")
    
    return len(uniqueInterTexts)

def skokoEnters2(levelstr, level_dict):
    #levelnext = level_dict.get(levelstr)
    
    for lvlname, level in level_dict.items():
        if level.next == levelstr:
            lvlnexts.append(level)
        if level.nextsecret == levelstr:
            lvlsecrets.append(level)
    #lvlallnexts = lvlnexts+lvlsecrets
    uniqueInterTexts = set()
    for sok in lvlnexts:
        uniqueInterTexts.add(sok.intertext)
    for sok in lvlsecrets:
        uniqueInterTexts.add(sok.intertextsecret)

    if len(uniqueInterTexts) > 1:
        print(uniqueInterTexts)
    return len(uniqueInterTexts)
    
    

def reflect_umapinfo2(level_dict):
    global EPISMAS, um2miWarnings
    next_num = make_counter()

    #10:43 12.01.2026
    #prodolzit razborki s textami
    
    
    
    #11:36 06.01.2026
    #случай когда достаточно менять только название или можно не менять
    BLUSET={
    'author',
    'label',
    'levelpic',
    'next',
    'nextsecret',
    'skytexture',
    'music',
    'exitpic',
    'enterpic',
    'partime',
    'cluster'
    }

    BLUDICT={
    'levelpic':'titlepatch',
    'nextsecret':'secret',
    'skytexture':'skybox',
    'partime':'par'
    }

    #11:46 06.01.2026 интермиссии и кластердефы
    #по сути можно startswith('end') заюзать
    YELSET={
    'endgame',
    'endpic',
    'endbunny',
    'endcast'
    }
    
    #11:50 06.01.2026
    VIOSET={
    'intertext',
    'intertextsecret',
    'interbackdrop',
    'intermusic'
    }

    #11:50 06.01.2026
    #and special handling of nointermission, episode and bossaction words

    # Выводим только те поля, которые были найдены при парсинге
    excluded_fields = {
        'index',
        'name',
        '_parsed_fields',
        #'endkok'#18:41 07.01.2026
        }

    #9:51 09.01.2026
    #Разборка с эпизодами
    #episode eto pic, name, key 10:10 09.01.2026
    
    if EPISMAS:
        print2(f"clearepisodes")
        #for pic, name, key in EPISMAS:
        #    print2(f'')





      
    # Выводим результат
    if level_dict:
        #print2(f"\nНайдено уровней: {len(level_dict)}")
        for map_name, level in level_dict.items():
            interIndex = next_num()
            
            
            #10:47 12.01.2026 2 exita tryEntertext
            has_secret_exit = level.nextsecret and level.next != level.nextsecret
            biased_exit_count = 2 if has_secret_exit else 1
            if biased_exit_count == 2 and not level.endkok:
                #clustertemp = extract_digits(map_name)
                if level.intertext:
                    #skokoVchodov = skokoEnters(level.next, level_dict)
                    uniqueEnters = skokoEnters(level.next, level_dict)
                    
                    if uniqueEnters == 1:
                        clustertemp = extract_digits(level.next)
                        #if not clustertemp in clusterdict.keys():
                        newcluster = clusterdict.get(clustertemp, cluster_t())    
                        levelnext = level_dict.get(level.next)
                        
                        newcluster.flat = level.interbackdrop or newcluster.flat or 'FLOOR4_8'
                        newcluster.enter = level.intertext
                        newcluster.music = level.intermusic or newcluster.music
                        clusterdict[clustertemp] = newcluster
                        levelnext.cluster = clustertemp
                    else:
                        um2miWarnings += f'level {level.next} has {uniqueEnters} enters with unique texts\n'
                        #print(uniqueEnters)
                        
                if level.intertextsecret:
                    uniqueEnters = skokoEnters(level.nextsecret, level_dict)
                    
                    if uniqueEnters == 1:
                        clustertemp = extract_digits(level.nextsecret)
                        newcluster = clusterdict.get(clustertemp, cluster_t())
                        levelnextsecret = level_dict.get(level.nextsecret)
                        
                        newcluster.flat = level.interbackdrop or newcluster.flat or 'FLOOR4_8'
                        newcluster.enter = level.intertextsecret
                        newcluster.music = level.intermusic or newcluster.music
                        clusterdict[clustertemp] = newcluster
                        levelnextsecret.cluster = clustertemp                      
                    else:
                        um2miWarnings += f'secret level {level.nextsecret} has {uniqueEnters} enters with unique texts\n'
                        #print(uniqueEnters)




            

            if level.episode:
                #print(repr(level.episode))
                picname, name, key = level.episode[0]
                print2(f'episode {map_name}\n{{\n\tname = "{name}"\n\tpicname = "{picname}"\n\tkey = "{key}"\n}}')
            
            print2(f'\nmap {map_name} "{level.levelname}"')
            print2("{")
            
            # Получаем все поля dataclass
            for field_info in fields(level_t):
                field_name = field_info.name
                
                if field_name in excluded_fields:
                    continue
                    
                value = getattr(level, field_name)
                
                # Пропускаем пустые значения
                #if value is None or value == "" or value == []:
                if not value:
                    continue

                #Обработка разных полей 

                #21:59 06.01.2026
##                синий сет в экселе
##                случай когда достаточно
##                менять только название
##                или можно не менять

                if field_name in BLUSET:
                    if level.endkok and field_name in ['next','nextsecret']:
                        field_name2 = BLUDICT.get(field_name,field_name)
                        print2(f'    {field_name2} = {value}')
                    else:
                        if not value:
                            continue
                        field_name2 = BLUDICT.get(field_name,field_name)
                        if isinstance(value, str):
                            print2(f'    {field_name2} = "{value}"')
                        elif isinstance(value, int):
                            print2(f'    {field_name2} = {value}')
                        elif isinstance(value, bool):
                            print2(f'    {field_name2} = {str(value).lower()}')
                #22:51 07.01.2026
                if field_name == 'bossaction':
                    for massiv in level.bossaction:
                        monstr, doomspec, doomtag = massiv
                        print2(f'    specialaction = {monstr}, {simple_translate_doom_to_hexen(doomspec,doomtag)}')
                
            print2("}")
    else:
        print2("Блоки map не найдены в файле")
    doClusters()
    doInters()

        
def main():
    global EPISMAS, um2miWarnings
    if len(argv) < 2:
        if os.path.exists(PATIENT):
            filename = PATIENT
        else:
            print2("Использование: python umapinfoReflect26.py <имя_файла>")
            return
    else:
        filename = argv[1]
        
    try:
        level_dict = parse_file_robust(filename)
        
    except FileNotFoundError:
        print2(f"Ошибка: Файл '{filename}' не найден")
        
    except Exception as e:
        print2(f"Ошибка при обработке файла: {e}")
        import traceback
        traceback.print_exc()
    print2('defaultmap\n{\ntranslator = dehsupp\n')
    print2('''compat_corpsegibs = 0
	compat_noblockfriends = 1
	compat_limitpain = 0
	compat_mbfmonstermove = 1
	compat_crossdropoff = 0
	compat_dropoff = 0
	compat_invisibility = 0
	compat_minotaur = 0
	compat_notossdrops = 1 //15:51 08.12.2025
	compat_dehhealth = 0
	compat_mushroom = 1
	compat_useblocking = 0
	compat_anybossdeath = 0
	compat_nodoorlight = 0
	compat_light = 0
	compat_shorttex = 0
	compat_stairs = 0
	compat_floormove = 0
	compat_boomscroll = 1
	compat_badangles = 0
	compat_ravenscroll = 0
	compat_trace = 1
	compat_missileclip = 1
	compat_polyobj = 0
	compat_maskedmidtex = 1
	compat_spritesort = 0
	compat_silent_instant_floors = 0
	compat_sectorsounds = 0
	compat_soundtarget = 1
}
	''')
    reflect_umapinfo2(level_dict)
    #print(*vivod)
    print(''.join(vivod))
    print(um2miWarnings)
    

if __name__ == "__main__":
    main()
