from sys import argv
from dataclasses import dataclass, fields, field
import typing
from typing import Optional, List, Tuple
from enum import IntEnum
import copy, os

PATIENT = "H:/Games/Doom/UMAPINFO300lnmas.txt"

# глобальный буфер, в который будет складываться весь вывод
vivod = []

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
class guga2_t(ourbase_t):
    a: str = ""
    b: str = ""
    c: str = ""

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
    intertext: str = ""
    intertextsecret: str = ""
    interbackdrop: str = ""
    intermusic: str = ""
    episode: List[Tuple[str, str, str]] = field(default_factory=list)
    bossaction: List[Tuple[str, int, int]] = field(default_factory=list)

    _parsed_fields: set = field(default_factory=set, init=False, compare=False, repr=False)

    def set_field_value(self, field_name, value):
        """Устанавливает значение поля и отмечает его как измененное"""
        setattr(self, field_name, value)
        self._parsed_fields.add(field_name)

UM2MIDICT = {
    'levelpic':'titlepatch',
    'nextsecret':'secret',
    'skytexture':'skybox'
    }    

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

def simple_translate_doom_to_hexen(doom_special: int, doom_tag: int = 0) -> str:
    """
    Упрощенная версия - только строковый вывод.
    """
    if doom_special < 0 or doom_special >= len(SpecialTranslation):
        return f"ERROR, {doom_tag}, 0, 0, 0, 0"
    
    translation = SpecialTranslation[doom_special]
    
    # Подготавливаем аргументы
    args = [0] * 5
    
    for i in range(min(translation.numparms, 5)):
        if translation.args[i] == TAG:
            args[i] = doom_tag
        elif translation.args[i] == LINETAG:
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

    
    

def parse_levels_robust(filename):
    """Парсер для блоков MAP с поддержкой многострочных значений"""
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
            
            #print2(f"Начало блока MAP: {map_name}")
            
            # Создаем объект уровня
            level = level_t(index=len(level_dict), name=map_name)
            
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
                            if key.startswith('end'):
                                if key == 'endpic':
                                    level.set_field_value('endkok', value)
                                elif key == 'endcast':
                                    level.set_field_value('endkok', '$CAST')
                                elif key == 'endbunny':
                                    level.set_field_value('endkok', '$BUNNY')
                                else:
                                    level.set_field_value('endkok', '!')
                            
                            # Проверяем, начинается ли значение с кавычки
                            elif value.startswith('"') and key != 'episode' and key != 'bossaction':
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
                                            #print2(episode_tuple) #14:05 04.01.2026 was for debug
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

            #Постобработка уровня
            if level.nextsecret == "" and level.next:
                level.nextsecret = level.next
            elif level.next == "" and level.nextsecret:
                level.next = level.nextsecret
                
            
            # Добавляем уровень в словарь
            level_dict[map_name] = level
        else:
            i += 1
    
    #print2(f"//Найдено блоков: {len(level_dict)}")
    return level_dict

def parse_file_robust(filename):
    """Более надежный парсер для произвольных блоков"""
    level_dict = parse_levels_robust(filename)
    
    if level_dict:
        return level_dict
    
    return {}
def reflect_umapinfo(level_dict):

        
        # Выводим результат
        if level_dict:
            #print2(f"\nНайдено уровней: {len(level_dict)}")
            for map_name, level in level_dict.items():
                print2(f"\nmap {map_name}")
                print2("{")
                
                # Выводим только те поля, которые были найдены при парсинге
                excluded_fields = {'index', 'name', '_parsed_fields'}
                
                # Получаем все поля dataclass
                for field_info in fields(level_t):
                    field_name = field_info.name
                    
                    if field_name in excluded_fields:
                        continue
                        
                    value = getattr(level, field_name)
                    
                    # Пропускаем пустые значения
                    if value is None or value == "" or value == []:
                        continue
                    
                    # Обработка episode (список кортежей)

                    if field_name == 'episode' and value:
                        if isinstance(value, list):
                            for episode_item in value:
                                if isinstance(episode_item, (list, tuple)) and len(episode_item) >= 3:
                                    print2(f'    episode = "{episode_item[0]}", "{episode_item[1]}", "{episode_item[2]}"')
                                else:
                                    print2(f'    # Ошибка: некорректный формат episode: {episode_item}')
                        else:
                            # Если по какой-то причине это не список, попробуем вывести как есть
                            print2(f'    episode = {value}')
                    # Обработка bossaction (список кортежей)
                    elif field_name == 'bossaction' and value:
                        for action in value:
                            if isinstance(action, (list, tuple)) and len(action) >= 3:
                                print2(f'    bossaction = "{action[0]}", "{action[1]}", {action[2]}')
                    # Числовые значения
                    elif isinstance(value, int):
                        print2(f'    {field_name} = {value}')
                    # Логические значения
                    elif isinstance(value, bool):
                        print2(f'    {field_name} = {str(value).lower()}')
                    # Опциональные логические значения
                    elif field_name in ['endgame', 'nointermission'] and value is not None:
                        print2(f'    {field_name} = {str(value).lower()}')
                    # Строковые значения
                    elif isinstance(value, str):
                        # Для intertext выводим как многострочное значение
                        if field_name == 'intertext' and '\n' in value:
                            print2(f'    {field_name} = "{value}"')
                        else:
                            print2(f'    {field_name} = "{value}"')
                
                print2("}")
        else:
            print2("Блоки map не найдены в файле")
            
def reflect_umapinfo2(level_dict):
    def make_counter(start: int = 0):
        current = start

        def _next() -> int:
            nonlocal current
            current += 1
            return current

        return _next
    next_num = make_counter()
    
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
    'partime'
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
            
    # Выводим результат
    if level_dict:
        #print2(f"\nНайдено уровней: {len(level_dict)}")
        for map_name, level in level_dict.items():
            interIndex = next_num()
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
                        #for whatNext in ['next','secret']:
                        whatNext = 'secret' if field_name == 'nextsecret' else 'next'
                        if level.endkok == '$CAST':
                            print2(f'    {whatNext} = EndGameC')
                        elif level.endkok == '$BUNNY':
                            print2(f'    {whatNext} = EndBunny')
                        elif level.endkok == '!':
                            print2(f'    {whatNext} = EndGame1')
                        else:
                            print2(f'    {whatNext} = endsequence, vauinter_{interIndex}')
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
                #{simple_translate_doom_to_hexen(doomspec,doomtag)}
                

                #22:01 06.01.2026
##                специальная обработка
##                касающаяся кластердефов
##                или простых интермиссий
##                
                #18:08 07.01.2026
                #Не может так оказаться что обычный выход ведёт на одну концовку, а необычный - на другую.
                #В Гоззе конечно может быть, но не в старой как 1.9.1 например
                #if level.endkok:
                    #whatNext = 'next' if level.next else ('secret' if level.nextsecret else 'next')
                    #whatNext = 'secret' if not level.next and level.nextsecret else 'next'
                    



                '''
                # Обработка episode (список кортежей)
                if field_name == 'episode' and value:
                    if isinstance(value, list):
                        for episode_item in value:
                            if isinstance(episode_item, (list, tuple)) and len(episode_item) >= 3:
                                print2(f'    episode = "{episode_item[0]}", "{episode_item[1]}", "{episode_item[2]}"')
                            else:
                                print2(f'    # Ошибка: некорректный формат episode: {episode_item}')
                    else:
                        # Если по какой-то причине это не список, попробуем вывести как есть
                        print2(f'    episode = {value}')
                # Обработка bossaction (список кортежей)
                elif field_name == 'bossaction' and value:
                    for action in value:
                        if isinstance(action, (list, tuple)) and len(action) >= 3:
                            print2(f'    bossaction = "{action[0]}", "{action[1]}", {action[2]}')
                # Числовые значения
                elif isinstance(value, int):
                    print2(f'    {field_name} = {value}')
                # Логические значения
                elif isinstance(value, bool):
                    print2(f'    {field_name} = {str(value).lower()}')
                # Опциональные логические значения
                elif field_name in ['endgame', 'nointermission'] and value is not None:
                    print2(f'    {field_name} = {str(value).lower()}')
                # Строковые значения
                elif isinstance(value, str):
                    # Для intertext выводим как многострочное значение
                    if field_name == 'intertext' and '\n' in value:
                        print2(f'    {field_name} = "{value}"')
                    else:
                        print2(f'    {field_name} = "{value}"')
                '''
            print2("}")
    else:
        print2("Блоки map не найдены в файле")            

        
def main():
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
        
    reflect_umapinfo2(level_dict)
    #print(*vivod)
    print(''.join(vivod))
    

if __name__ == "__main__":
    main()
