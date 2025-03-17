// xlat.h: Translate old linedefs to new linedefs
//		   Pulled from the ZDoom source itself

typedef enum
{
	Init_Gravity,
	Init_Color,
	Init_Damage,
	Init_TransferSky = 255
} inittype_t;
typedef enum
{
	NoKey,
	RCard,
	BCard,
	YCard,
	RSkull,
	BSkull,
	YSkull,

	AnyKey = 100,
	AllKeys = 101,

	CardIsSkull = 128
} keytype_t;

// Speeds for ceilings/crushers (x/8 units per tic)
//	(Hexen crushers go up at half the speed that they go down)
#define C_SLOW			8
#define C_NORMAL		16
#define C_FAST			32
#define C_TURBO			64

#define CEILWAIT		150

// Speeds for floors (x/8 units per tic)
#define F_SLOW			8
#define F_NORMAL		16
#define F_FAST			32
#define F_TURBO			64

// Speeds for doors (x/8 units per tic)
#define D_SLOW			16
#define D_NORMAL		32
#define D_FAST			64
#define D_TURBO			128

#define VDOORWAIT		150

// Speeds for stairs (x/8 units per tic)
#define S_SLOW			2
#define S_NORMAL		4
#define S_FAST			16
#define S_TURBO			32

// Speeds for plats (Hexen plats stop 8 units above the floor)
#define P_SLOW			8
#define P_NORMAL		16
#define P_FAST			32
#define P_TURBO			64

#define PLATWAIT		105

#define ELEVATORSPEED	32

// Speeds for donut slime and pillar (x/8 units per tic)
#define DORATE			4

// Texture scrollers operate at a rate of x/64 units per tic.
#define SCROLL_UNIT		64


//Define masks, shifts, for fields in generalized linedef types
// (from BOOM's p_psec.h file)

#define GenFloorBase			0x6000
#define GenCeilingBase			0x4000
#define GenDoorBase				0x3c00
#define GenLockedBase			0x3800
#define GenLiftBase				0x3400
#define GenStairsBase			0x3000
#define GenCrusherBase			0x2F80

#define ZDoomStaticInits		333
#define NUM_STATIC_INITS		3

// define names for the TriggerType field of the general linedefs

typedef enum
{
	WalkOnce,
	WalkMany,
	SwitchOnce,
	SwitchMany,
	GunOnce,
	GunMany,
	PushOnce,
	PushMany,
} triggertype_e;

// Line special translation structure
typedef struct {
	UBYTE	flags;
	UBYTE	newspecial;
	UBYTE	numparms;
	UBYTE	args[5];
} xlat_t;

#define TAG	123		// Special value that gets replaced with the line tag
#define LINETAG 124	// Special value that gets replaced with the line id (tag)

#define WALK	(ML_ACTIVATECROSS>>8)
#define USE		(ML_ACTIVATEUSE>>8)
#define SHOOT	(ML_ACTIVATEPROJECTILEHIT>>8)
#define MONST	(ML_MONSTERSCANACTIVATE>>8)
#define MONWALK (ML_ACTIVATEMONSTERCROSS>>8)
#define REP		(ML_REPEATABLE>>8)

static const xlat_t SpecialTranslation[] = {
/*   0 */ { 0, 0, 0, TAG },
/*   1 */ { USE|MONST|REP,	Door_Raise,					 3, { 0, D_SLOW, VDOORWAIT } },
/*   2 */ { WALK,			Door_Open,					 2, { TAG, D_SLOW } },
/*   3 */ { WALK,			Door_Close,					 2, { TAG, D_SLOW } },
/*   4 */ { WALK|MONST,		Door_Raise,					 3, { TAG, D_SLOW, VDOORWAIT } },
/*   5 */ { WALK,			Floor_RaiseToLowestCeiling,	 2, { TAG, F_SLOW } },
/*	 6 */ { WALK,			Ceiling_CrushAndRaiseA,		 4, { TAG, C_NORMAL, C_NORMAL, 10 } },
/*   7 */ { USE,			Stairs_BuildUpDoom,			 3, { TAG, S_SLOW, 8 } },
/*   8 */ { WALK,			Stairs_BuildUpDoom,			 3, { TAG, S_SLOW, 8 } },
/*	 9 */ { USE,			Floor_Donut,				 3, { TAG, DORATE, DORATE } },
/*  10 */ { WALK|MONST,		Plat_DownWaitUpStayLip,		 4, { TAG, P_FAST, PLATWAIT, 0 } },
/*  11 */ { USE,			Exit_Normal,				 1, { 0 } },
/*  12 */ { WALK,			Light_MaxNeighbor,			 1, { TAG } },
/*  13 */ { WALK,			Light_ChangeToValue,		 2, { TAG, 255 } },
/*  14 */ { USE,			Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 4 } },
/*  15 */ { USE,			Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 3 } },
/*  16 */ { WALK,			Door_CloseWaitOpen,			 3, { TAG, D_SLOW, 240 } },
/*  17 */ { WALK,			Light_StrobeDoom,			 3, { TAG, 5, 35 } },
/*  18 */ { USE,			Floor_RaiseToNearest,		 2, { TAG, F_SLOW } },
/*  19 */ { WALK,			Floor_LowerToHighest,		 3, { TAG, F_SLOW, 128 } },
/*  20 */ { USE,			Plat_RaiseAndStayTx0,		 2, { TAG, P_SLOW/2 } },
/*  21 */ { USE,			Plat_DownWaitUpStayLip,		 3, { TAG, P_FAST, PLATWAIT } },
/*  22 */ { WALK,			Plat_RaiseAndStayTx0,		 2, { TAG, P_SLOW/2 } },
/*  23 */ { USE,			Floor_LowerToLowest,		 2, { TAG, F_SLOW } },
/*  24 */ { SHOOT,			Floor_RaiseToLowestCeiling,  2, { TAG, F_SLOW } },
/*  25 */ { WALK,			Ceiling_CrushAndRaiseA,		 4, { TAG, C_SLOW, C_SLOW, 10 } },
/*  26 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_SLOW, VDOORWAIT, BCard | CardIsSkull } },
/*  27 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_SLOW, VDOORWAIT, YCard | CardIsSkull } },
/*  28 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_SLOW, VDOORWAIT, RCard | CardIsSkull } },
/*  29 */ { USE,			Door_Raise,					 3, { TAG, D_SLOW, VDOORWAIT } },
/*  30 */ { WALK,			Floor_RaiseByTexture,		 2, { TAG, F_SLOW } },
/*  31 */ { USE,			Door_Open,					 2, { 0, D_SLOW } },
/*  32 */ { USE|MONST,		Door_LockedRaise,			 4, { 0, D_SLOW, 0, BCard | CardIsSkull } },
/*  33 */ { USE|MONST,		Door_LockedRaise,			 4, { 0, D_SLOW, 0, RCard | CardIsSkull } },
/*  34 */ { USE|MONST,		Door_LockedRaise,			 4, { 0, D_SLOW, 0, YCard | CardIsSkull } },
/*  35 */ { WALK,			Light_ChangeToValue,		 2, { TAG, 35 } },
/*  36 */ { WALK,			Floor_LowerToHighest,		 3, { TAG, F_FAST, 136 } },
/*  37 */ { WALK,			Floor_LowerToLowestTxTy,	 2, { TAG, F_SLOW } },
/*  38 */ { WALK,			Floor_LowerToLowest,		 2, { TAG, F_SLOW } },
/*  39 */ { WALK|MONST,		Teleport,					 1, { TAG } },
/*  40 */ { WALK,			Generic_Ceiling,			 5, { TAG, C_SLOW, 0, 1, 8 } },
/*  41 */ { USE,			Ceiling_LowerToFloor,		 2, { TAG, C_SLOW } },
/*  42 */ { USE|REP,		Door_Close,					 2, { TAG, D_SLOW } },
/*  43 */ { USE|REP,		Ceiling_LowerToFloor,		 2, { TAG, C_SLOW } },
/*  44 */ { WALK,			Ceiling_LowerAndCrush,		 3, { TAG, C_SLOW, 0 } },
/*  45 */ { USE|REP,		Floor_LowerToHighest,		 3, { TAG, F_SLOW, 128 } },
/*  46 */ { SHOOT|REP|MONST,Door_Open,					 2, { TAG, D_SLOW } },
/*  47 */ { SHOOT,			Plat_RaiseAndStayTx0,		 2, { TAG, P_SLOW/2 } },
/*  48 */ { 0,				Scroll_Texture_Left,		 1, { SCROLL_UNIT } },
/*  49 */ { USE,			Ceiling_CrushAndRaiseA,		 4, { TAG, C_SLOW, C_SLOW, 10 } },
/*  50 */ { USE,			Door_Close,					 2, { TAG, D_SLOW } },
/*  51 */ { USE,			Exit_Secret,				 1, { 0 } },
/*  52 */ { WALK,			Exit_Normal,				 1, { 0 } },
/*  53 */ { WALK,			Plat_PerpetualRaiseLip,		 4, { TAG, P_SLOW, PLATWAIT, 0 } },
/*  54 */ { WALK,			Plat_Stop,					 1, { TAG } },
/*  55 */ { USE,			Floor_RaiseAndCrush,		 3, { TAG, F_SLOW, 10 } },
/*  56 */ { WALK,			Floor_RaiseAndCrush,		 3, { TAG, F_SLOW, 10 } },
/*  57 */ { WALK,			Ceiling_CrushStop,			 1, { TAG } },
/*  58 */ { WALK,			Floor_RaiseByValue,			 3, { TAG, F_SLOW, 24 } },
/*  59 */ { WALK,			Floor_RaiseByValueTxTy,		 3, { TAG, F_SLOW, 24 } },
/*  60 */ { USE|REP,		Floor_LowerToLowest,		 2, { TAG, F_SLOW } },
/*  61 */ { USE|REP,		Door_Open,					 2, { TAG, D_SLOW } },
/*  62 */ { USE|REP,		Plat_DownWaitUpStayLip,		 4, { TAG, P_FAST, PLATWAIT, 0 } },
/*  63 */ { USE|REP,		Door_Raise,					 3, { TAG, D_SLOW, VDOORWAIT } },
/*  64 */ { USE|REP,		Floor_RaiseToLowestCeiling,	 2, { TAG, F_SLOW } },
/*  65 */ { USE|REP,		Floor_RaiseAndCrush,		 3, { TAG, F_SLOW, 10 } },
/*  66 */ { USE|REP,		Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 3 } },
/*  67 */ { USE|REP,		Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 4 } },
/*  68 */ { USE|REP,		Plat_RaiseAndStayTx0,		 2, { TAG, P_SLOW/2 } },
/*  69 */ { USE|REP,		Floor_RaiseToNearest,		 2, { TAG, F_SLOW } },
/*  70 */ { USE|REP,		Floor_LowerToHighest,		 3, { TAG, F_FAST, 136 } },
/*  71 */ { USE,			Floor_LowerToHighest,		 3, { TAG, F_FAST, 136 } },
/*  72 */ { WALK|REP,		Ceiling_LowerAndCrush,		 3, { TAG, C_SLOW, 0 } },
/*  73 */ { WALK|REP,		Ceiling_CrushAndRaiseA,		 4, { TAG, C_SLOW, C_SLOW, 10 } },
/*  74 */ { WALK|REP,		Ceiling_CrushStop,			 1, { TAG } },
/*  75 */ { WALK|REP,		Door_Close,					 2, { TAG, D_SLOW } },
/*  76 */ { WALK|REP,		Door_CloseWaitOpen,			 3, { TAG, D_SLOW, 240 } },
/*  77 */ { WALK|REP,		Ceiling_CrushAndRaiseA,		 4, { TAG, C_NORMAL, C_NORMAL, 10 } },
/*  78 */ { USE|REP,		Floor_TransferNumeric,		 1, { TAG } },			// <- BOOM special
/*  79 */ { WALK|REP,		Light_ChangeToValue,		 2, { TAG, 35 } },
/*  80 */ { WALK|REP,		Light_MaxNeighbor,			 1, { TAG } },
/*  81 */ { WALK|REP,		Light_ChangeToValue,		 2, { TAG, 255 } },
/*  82 */ { WALK|REP,		Floor_LowerToLowest,		 2, { TAG, F_SLOW } },
/*  83 */ { WALK|REP,		Floor_LowerToHighest,		 3, { TAG, F_SLOW, 128 } },
/*  84 */ { WALK|REP,		Floor_LowerToLowestTxTy,	 2, { TAG, F_SLOW } },
/*  85 */ { 0,				Scroll_Texture_Right,		 1, { SCROLL_UNIT } }, // <- BOOM special
/*  86 */ { WALK|REP,		Door_Open,					 2, { TAG, D_SLOW } },
/*  87 */ { WALK|REP,		Plat_PerpetualRaiseLip,		 4, { TAG, P_SLOW, PLATWAIT, 0 } },
/*  88 */ { WALK|REP|MONST, Plat_DownWaitUpStayLip,		 4, { TAG, P_FAST, PLATWAIT, 0 } },
/*  89 */ { WALK|REP,		Plat_Stop,					 1, { TAG } },
/*  90 */ { WALK|REP,		Door_Raise,					 3, { TAG, D_SLOW, VDOORWAIT } },
/*  91 */ { WALK|REP,		Floor_RaiseToLowestCeiling,	 2, { TAG, F_SLOW } },
/*  92 */ { WALK|REP,		Floor_RaiseByValue,			 3, { TAG, F_SLOW, 24 } },
/*  93 */ { WALK|REP,		Floor_RaiseByValueTxTy,		 3, { TAG, F_SLOW, 24 } },
/*  94 */ { WALK|REP,		Floor_RaiseAndCrush,		 3, { TAG, F_SLOW, 10 } },
/*  95 */ { WALK|REP,		Plat_RaiseAndStayTx0,		 2, { TAG, P_SLOW/2 } },
/*  96 */ { WALK|REP,		Floor_RaiseByTexture,		 2, { TAG, F_SLOW } },
/*  97 */ { WALK|REP|MONST, Teleport,					 1, { TAG } },
/*  98 */ { WALK|REP,		Floor_LowerToHighest,		 3, { TAG, F_FAST, 136 } },
/*  99 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_FAST, 0, BCard | CardIsSkull } },
/* 100 */ { WALK,			Stairs_BuildUpDoom,			 5, { TAG, S_TURBO, 16, 0, 0 } },
/* 101 */ { USE,			Floor_RaiseToLowestCeiling,	 2, { TAG, F_SLOW } },
/* 102 */ { USE,			Floor_LowerToHighest,		 3, { TAG, F_SLOW, 128 } },
/* 103 */ { USE,			Door_Open,					 2, { TAG, D_SLOW } },
/* 104 */ { WALK,			Light_MinNeighbor,			 1, { TAG } },
/* 105 */ { WALK|REP,		Door_Raise,					 3, { TAG, D_FAST, VDOORWAIT } },
/* 106 */ { WALK|REP,		Door_Open,					 2, { TAG, D_FAST } },
/* 107 */ { WALK|REP,		Door_Close,					 2, { TAG, D_FAST } },
/* 108 */ { WALK,			Door_Raise,					 3, { TAG, D_FAST, VDOORWAIT } },
/* 109 */ { WALK,			Door_Open,					 2, { TAG, D_FAST } },
/* 110 */ { WALK,			Door_Close,					 2, { TAG, D_FAST } },
/* 111 */ { USE,			Door_Raise,					 3, { TAG, D_FAST, VDOORWAIT } },
/* 112 */ { USE,			Door_Open,					 2, { TAG, D_FAST } },
/* 113 */ { USE,			Door_Close,					 2, { TAG, D_FAST } },
/* 114 */ { USE|REP,		Door_Raise,					 3, { TAG, D_FAST, VDOORWAIT } },
/* 115 */ { USE|REP,		Door_Open,					 2, { TAG, D_FAST } },
/* 116 */ { USE|REP,		Door_Close,					 2, { TAG, D_FAST } },
/* 117 */ { USE|REP,		Door_Raise,					 3, { 0, D_FAST, VDOORWAIT } },
/* 118 */ { USE,			Door_Open,					 2, { 0, D_FAST } },
/* 119 */ { WALK,			Floor_RaiseToNearest,		 2, { TAG, F_SLOW } },
/* 120 */ { WALK|REP,		Plat_DownWaitUpStayLip,		 4, { TAG, P_TURBO, PLATWAIT, 0 } },
/* 121 */ { WALK,			Plat_DownWaitUpStayLip,		 4, { TAG, P_TURBO, PLATWAIT, 0 } },
/* 122 */ { USE,			Plat_DownWaitUpStayLip,		 4, { TAG, P_TURBO, PLATWAIT, 0 } },
/* 123 */ { USE|REP,		Plat_DownWaitUpStayLip,		 4, { TAG, P_TURBO, PLATWAIT, 0 } },
/* 124 */ { WALK,			Exit_Secret,				 1, { 0 } },
/* 125 */ { MONWALK,		Teleport,					 1, { TAG } },
/* 126 */ { MONWALK|REP,	Teleport,					 1, { TAG } },
/* 127 */ { USE,			Stairs_BuildUpDoom,			 5, { TAG, S_TURBO, 16, 0, 0 } },
/* 128 */ { WALK|REP,		Floor_RaiseToNearest,		 2, { TAG, F_SLOW } },
/* 129 */ { WALK|REP,		Floor_RaiseToNearest,		 2, { TAG, F_FAST } },
/* 130 */ { WALK,			Floor_RaiseToNearest,		 2, { TAG, F_FAST } },
/* 131 */ { USE,			Floor_RaiseToNearest,		 2, { TAG, F_FAST } },
/* 132 */ { USE|REP,		Floor_RaiseToNearest,		 2, { TAG, F_FAST } },
/* 133 */ { USE,			Door_LockedRaise,			 4, { TAG, D_FAST, 0, BCard | CardIsSkull } },
/* 134 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_FAST, 0, RCard | CardIsSkull } },
/* 135 */ { USE,			Door_LockedRaise,			 4, { TAG, D_FAST, 0, RCard | CardIsSkull } },
/* 136 */ { USE|REP,		Door_LockedRaise,			 4, { TAG, D_FAST, 0, YCard | CardIsSkull } },
/* 137 */ { USE,			Door_LockedRaise,			 4, { TAG, D_FAST, 0, YCard | CardIsSkull } },
/* 138 */ { USE|REP,		Light_ChangeToValue,		 2, { TAG, 255 } },
/* 139 */ { USE|REP,		Light_ChangeToValue,		 2, { TAG, 35 } },
/* 140 */ { USE,			Floor_RaiseByValueTimes8,	 3, { TAG, F_SLOW, 64 } },
/* 141 */ { WALK,			Ceiling_CrushAndRaiseSilentA,4, { TAG, C_SLOW, C_SLOW, 10 } },

/****** The following are all new to BOOM ******/

/* 142 */ { WALK,			Floor_RaiseByValueTimes8,	 3, { TAG, F_SLOW, 64 } },
/* 143 */ { WALK,			Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 3 } },
/* 144 */ { WALK,			Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 4 } },
/* 145 */ { WALK,			Ceiling_LowerToFloor,		 2, { TAG, C_SLOW } },
/* 146 */ { WALK,			Floor_Donut,				 3, { TAG, DORATE, DORATE } },
/* 147 */ { WALK|REP,		Floor_RaiseByValueTimes8,	 3, { TAG, F_SLOW, 64 } },
/* 148 */ { WALK|REP,		Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 3 } },
/* 149 */ { WALK|REP,		Plat_UpByValueStayTx,		 3, { TAG, P_SLOW/2, 4 } },
/* 150 */ { WALK|REP,		Ceiling_CrushAndRaiseSilentA,4, { TAG, C_SLOW, C_SLOW, 10 } },
/* 151 */ { WALK|REP,		FloorAndCeiling_LowerRaise,	 3, { TAG, F_SLOW, C_SLOW } },
/* 152 */ { WALK|REP,		Ceiling_LowerToFloor,		 2, { TAG, C_SLOW } },
/* 153 */ { WALK,			Floor_TransferTrigger,		 1, { TAG } },
/* 154 */ { WALK|REP,		Floor_TransferTrigger,		 1, { TAG } },
/* 155 */ { WALK|REP,		Floor_Donut,				 3, { TAG, DORATE, DORATE } },
/* 156 */ { WALK|REP,		Light_StrobeDoom,			 3, { TAG, 5, 35 } },
/* 157 */ { WALK|REP,		Light_MinNeighbor,			 1, { TAG } },
/* 158 */ { USE,			Floor_RaiseByTexture,		 2, { TAG, F_SLOW } },
/* 159 */ { USE,			Floor_LowerToLowestTxTy,	 2, { TAG, F_SLOW } },
/* 160 */ { USE,			Floor_RaiseByValueTxTy,		 3, { TAG, F_SLOW, 24 } },
/* 161 */ { USE,			Floor_RaiseByValue,			 3, { TAG, F_SLOW, 24 } },
/* 162 */ { USE,			Plat_PerpetualRaiseLip,		 4, { TAG, P_SLOW, PLATWAIT, 0 } },
/* 163 */ { USE,			Plat_Stop,					 1, { TAG } },
/* 164 */ { USE,			Ceiling_CrushAndRaiseA,		 4, { TAG, C_NORMAL, C_NORMAL, 10 } },
/* 165 */ { USE,			Ceiling_CrushAndRaiseSilentA,4, { TAG, C_SLOW, C_SLOW, 10 } },
/* 166 */ { USE,			FloorAndCeiling_LowerRaise,	 3, { TAG, F_SLOW, C_SLOW } },
/* 167 */ { USE,			Ceiling_LowerAndCrush,		 3, { TAG, C_SLOW, 0 } },
/* 168 */ { USE,			Ceiling_CrushStop,			 1, { TAG } },
/* 169 */ { USE,			Light_MaxNeighbor,			 1, { TAG } },
/* 170 */ { USE,			Light_ChangeToValue,		 2, { TAG, 35 } },
/* 171 */ { USE,			Light_ChangeToValue,		 2, { TAG, 255 } },
/* 172 */ { USE,			Light_StrobeDoom,			 3, { TAG, 5, 35 } },
/* 173 */ { USE,			Light_MinNeighbor,			 1, { TAG } },
/* 174 */ { USE|MONST,		Teleport,					 1, { TAG } },
/* 175 */ { USE,			Door_CloseWaitOpen,			 3, { TAG, F_SLOW, 240 } },
/* 176 */ { USE|REP,		Floor_RaiseByTexture,		 2, { TAG, F_SLOW } },
/* 177 */ { USE|REP,		Floor_LowerToLowestTxTy,	 2, { TAG, F_SLOW } },
/* 178 */ { USE|REP,		Floor_RaiseByValueTimes8,	 3, { TAG, F_SLOW, 64 } },
/* 179 */ { USE|REP,		Floor_RaiseByValueTxTy,		 3, { TAG, F_SLOW, 24 } },
/* 180 */ { USE|REP,		Floor_RaiseByValue,			 3, { TAG, F_SLOW, 24 } },
/* 181 */ { USE|REP,		Plat_PerpetualRaiseLip,		 4, { TAG, P_SLOW, PLATWAIT, 0 } },
/* 182 */ { USE|REP,		Plat_Stop,					 1, { TAG } },
/* 183 */ { USE|REP,		Ceiling_CrushAndRaiseA,		 4, { TAG, C_NORMAL, C_NORMAL, 10 } },
/* 184 */ { USE|REP,		Ceiling_CrushAndRaiseA,		 4, { TAG, C_SLOW, C_SLOW, 10 } },
/* 185 */ { USE|REP,		Ceiling_CrushAndRaiseSilentA,4, { TAG, C_SLOW, C_SLOW, 10 } },
/* 186 */ { USE|REP,		FloorAndCeiling_LowerRaise,	 3, { TAG, F_SLOW, C_SLOW } },
/* 187 */ { USE|REP,		Ceiling_LowerAndCrush,		 3, { TAG, C_SLOW, 0 } },
/* 188 */ { USE|REP,		Ceiling_CrushStop,			 1, { TAG } },
/* 189 */ { USE,			Floor_TransferTrigger,		 1, { TAG } },
/* 190 */ { USE|REP,		Floor_TransferTrigger,		 1, { TAG } },
/* 191 */ { USE|REP,		Floor_Donut,				 3, { TAG, DORATE, DORATE } },
/* 192 */ { USE|REP,		Light_MaxNeighbor,			 1, { TAG } },
/* 193 */ { USE|REP,		Light_StrobeDoom,			 3, { TAG, 5, 35 } },
/* 194 */ { USE|REP,		Light_MinNeighbor,			 1, { TAG } },
/* 195 */ { USE|REP|MONST,	Teleport,					 1, { TAG } },
/* 196 */ { USE|REP,		Door_CloseWaitOpen,			 3, { TAG, D_SLOW, 240 } },
/* 197 */ { SHOOT,			Exit_Normal,				 1, { 0 } },
/* 198 */ { SHOOT,			Exit_Secret,				 1, { 0 } },
/* 199 */ { WALK,			Ceiling_LowerToLowest,		 2, { TAG, C_SLOW } },
/* 200 */ { WALK,			Ceiling_LowerToHighestFloor, 2, { TAG, C_SLOW } },
/* 201 */ { WALK|REP,		Ceiling_LowerToLowest,		 2, { TAG, C_SLOW } },
/* 202 */ { WALK|REP,		Ceiling_LowerToHighestFloor, 2, { TAG, C_SLOW } },
/* 203 */ { USE,			Ceiling_LowerToLowest,		 2, { TAG, C_SLOW } },
/* 204 */ { USE,			Ceiling_LowerToHighestFloor, 2, { TAG, C_SLOW } },
/* 205 */ { USE|REP,		Ceiling_LowerToLowest,		 2, { TAG, C_SLOW } },
/* 206 */ { USE|REP,		Ceiling_LowerToHighestFloor, 2, { TAG, C_SLOW } },
/* 207 */ { WALK|MONST,		Teleport_NoFog,				 1, { TAG } },
/* 208 */ { WALK|REP|MONST,	Teleport_NoFog,				 1, { TAG } },
/* 209 */ { USE|MONST,		Teleport_NoFog,				 1, { TAG } },
/* 210 */ { USE|REP|MONST,	Teleport_NoFog,				 1, { TAG } },
/* 211 */ { USE|REP,		Plat_ToggleCeiling,			 1, { TAG } },
/* 212 */ { WALK|REP,		Plat_ToggleCeiling,			 1, { TAG } },
/* 213 */ { 0,				Transfer_FloorLight,		 1, { TAG } },
/* 214 */ { 0,				Scroll_Ceiling,				 5, { TAG, 6, 0, 0, 0 } },
/* 215 */ { 0,				Scroll_Floor,				 5, { TAG, 6, 0, 0, 0 } },
/* 216 */ { 0,				Scroll_Floor,				 5, { TAG, 6, 1, 0, 0 } },
/* 217 */ { 0,				Scroll_Floor,				 5, { TAG, 6, 2, 0, 0 } },
/* 218 */ { 0,				Scroll_Texture_Model,		 2, { LINETAG, 2 } },
/* 219 */ { WALK,			Floor_LowerToNearest,		 2, { TAG, F_SLOW } },
/* 220 */ { WALK|REP,		Floor_LowerToNearest,		 2, { TAG, F_SLOW } },
/* 221 */ { USE,			Floor_LowerToNearest,		 2, { TAG, F_SLOW } },
/* 222 */ { USE|REP,		Floor_LowerToNearest,		 2, { TAG, F_SLOW } },
/* 223 */ { 0,				Sector_SetFriction,			 2, { TAG, 0 } },
/* 224 */ { 0,				Sector_SetWind,				 4, { TAG, 0, 0, 1 } },
/* 225 */ { 0,				Sector_SetCurrent,			 4, { TAG, 0, 0, 1 } },
/* 226 */ { 0,				PointPush_SetForce,			 4, { TAG, 0, 0, 1 } },
/* 227 */ { WALK,			Elevator_RaiseToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 228 */ { WALK|REP,		Elevator_RaiseToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 229 */ { USE,			Elevator_RaiseToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 230 */ { USE|REP,		Elevator_RaiseToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 231 */ { WALK,			Elevator_LowerToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 232 */ { WALK|REP,		Elevator_LowerToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 233 */ { USE,			Elevator_LowerToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 234 */ { USE|REP,		Elevator_LowerToNearest,	 2, { TAG, ELEVATORSPEED } },
/* 235 */ { WALK,			Elevator_MoveToFloor,		 2, { TAG, ELEVATORSPEED } },
/* 236 */ { WALK|REP,		Elevator_MoveToFloor,		 2, { TAG, ELEVATORSPEED } },
/* 237 */ { USE,			Elevator_MoveToFloor,		 2, { TAG, ELEVATORSPEED } },
/* 238 */ { USE|REP,		Elevator_MoveToFloor,		 2, { TAG, ELEVATORSPEED } },
/* 239 */ { WALK,			Floor_TransferNumeric,		 1, { TAG } },
/* 240 */ { WALK|REP,		Floor_TransferNumeric,		 1, { TAG } },
/* 241 */ { USE,			Floor_TransferNumeric,		 1, { TAG } },
/* 242 */ { 0,				Transfer_Heights,			 1, { TAG } },
/* 243 */ { WALK|MONST,		Teleport_Line,				 3, { TAG, TAG, 0 } },
/* 244 */ { WALK|REP|MONST,	Teleport_Line,				 3, { TAG, TAG, 0 } },
/* 245 */ { 0,				Scroll_Ceiling,				 5, { TAG, 5, 0, 0, 0 } },
/* 246 */ { 0,				Scroll_Floor,				 5, { TAG, 5, 0, 0, 0 } },
/* 247 */ { 0,				Scroll_Floor,				 5, { TAG, 5, 1, 0, 0 } },
/* 248 */ { 0,				Scroll_Floor,				 5, { TAG, 5, 2, 0, 0 } },
/* 249 */ { 0,				Scroll_Texture_Model,		 2, { LINETAG, 1 } },
/* 250 */ { 0,				Scroll_Ceiling,				 5, { TAG, 4, 0, 0, 0 } },
/* 251 */ { 0,				Scroll_Floor,				 5, { TAG, 4, 0, 0, 0 } },
/* 252 */ { 0,				Scroll_Floor,				 5, { TAG, 4, 1, 0, 0 } },
/* 253 */ { 0,				Scroll_Floor,				 5, { TAG, 4, 2, 0, 0 } },
/* 254 */ { 0,				Scroll_Texture_Model,		 2, { LINETAG, 0 } },
/* 255 */ { 0,				Scroll_Texture_Offsets,		 0, },
/* 256 */ { WALK|REP,		Stairs_BuildUpDoom,			 5, { TAG, S_SLOW, 8, 0, 0 } },
/* 257 */ { WALK|REP,		Stairs_BuildUpDoom,			 5, { TAG, S_TURBO, 16, 0, 0 } },
/* 258 */ { USE|REP,		Stairs_BuildUpDoom,			 5, { TAG, S_SLOW, 8, 0, 0 } },
/* 259 */ { USE|REP,		Stairs_BuildUpDoom,			 5, { TAG, S_TURBO, 16, 0, 0 } },
/* 260 */ { 0,				TranslucentLine,			 2, { LINETAG, 128 } },
/* 261 */ { 0,				Transfer_CeilingLight,		 1, { TAG } },
/* 262 */ { WALK|MONST,		Teleport_Line,				 3, { TAG, TAG, 1 } },
/* 263 */ { WALK|REP|MONST,	Teleport_Line,				 3, { TAG, TAG, 1 } },
/* 264 */ { MONWALK,		Teleport_Line,				 3, { TAG, TAG, 1 } },
/* 265 */ { MONWALK|REP,	Teleport_Line,				 3, { TAG, TAG, 1 } },
/* 266 */ { MONWALK,		Teleport_Line,				 3, { TAG, TAG, 0 } },
/* 267 */ { MONWALK|REP,	Teleport_Line,				 3, { TAG, TAG, 0 } },
/* 268 */ { MONWALK,		Teleport_NoFog,				 1, { TAG } },
/* 269 */ { MONWALK|REP,	Teleport_NoFog,				 1, { TAG } },
/*270 */{ WALK|REP,		FS_Execute, 1, {TAG}},
/*271 */{ 0,		Static_Init , 3, {TAG, Init_TransferSky, 0}},
/*272 */{ 0,		Static_Init , 3, {TAG, Init_TransferSky, 1}},
/*273 */{ WALK|REP,		FS_Execute, 2, {TAG, 1}},
/*274 */{ WALK,		FS_Execute, 1, {TAG}},
/*275 */{ WALK,		FS_Execute, 2, {TAG, 1}},
/*276 */{ USE|REP,		FS_Execute, 1, {TAG}},
/*277 */{ USE,		FS_Execute, 1, {TAG}},
/*278 */{ SHOOT|REP,	FS_Execute, 1, {TAG}},
/*279 */{ SHOOT,		FS_Execute, 1, {TAG}},
/*280 */{ 0,		Transfer_Heights , 2, {TAG, 12}},
/*281 */{ 0,		Sector_Set3DFloor, 4, {TAG, 1, 0, 255}},
/*282 */{ 0,		Static_Init, 2, {TAG, 1}},
/*283 */{ 0,Transfer_WallLight, 2, {TAG,1}},
/*284 */{ 0,		TranslucentLine , 3, {LINETAG, 128, 0}},
/*285 */{ 0,		TranslucentLine , 3, {LINETAG, 192, 0}},
/*286 */{ 0,		TranslucentLine , 3, {LINETAG,  48, 0}},
/*287 */{ 0,		TranslucentLine , 3, {LINETAG, 128, 1}},
/*288 */{ 0,    		TranslucentLine, 3, {LINETAG, 255, 0}},
/*289 */{ 0,     		Sector_Set3DFloor, 4, {TAG, 1, 1, 255}},
/*290 */{ USE|MONST|REP,Polyobj_StartLine, 4, {TAG,0,1,0}},
/*291 */{ USE|MONST|REP,Polyobj_DoorSwing , 4, {TAG,P_FAST,P_TURBO,D_TURBO}},
/*292 */{ USE|MONST|REP,Polyobj_DoorSwing , 4, {TAG,-P_FAST,P_TURBO,D_TURBO}},
/*293 */{ USE|REP, ACS_Execute, 4, {27,0,TAG,1}},
/*294*/{ 0, 0, 0, TAG },
/*295*/{ 0, 0, 0, TAG },
/*296*/{ 0, 0, 0, TAG },
/*297*/{ 0, 0, 0, TAG },
/*298*/{ 0, 0, 0, TAG },
/*299*/{ 0, 0, 0, TAG },
/*300 */{ 0,     		Sector_Set3DFloor, 4, {TAG, 1, 1, 127}},
/*301 */{ 0,     		Sector_Set3DFloor, 4, {TAG, 2, 2, 127}},
/*302 */{ 0,     		Sector_Set3DFloor, 4, {TAG, 3, 6, 127}},
/*303 */{ 0,     		Sector_Set3DFloor, 2, {TAG, 3}},
/*304 */{ 0,     		Sector_Set3DFloor, 4, {TAG, 2, 2, 255}},
/*305 */{ 0,     		Sector_Set3DFloor, 3, {TAG, 3, 2}},
/*306 */{ 0,     		Sector_Set3DFloor, 2, {TAG, 1}},
/*307*/{ 0, 0, 0, TAG },
/*308*/{ 0, 0, 0, TAG },
/*309*/{ 0, 0, 0, TAG },
/*310*/{ 0, 0, 0, TAG },
/*311*/{ 0, 0, 0, TAG },
/*312*/{ 0, 0, 0, TAG },
/*313*/{ 0, 0, 0, TAG },
/*314*/{ 0, 0, 0, TAG },
/*315*/{ 0, 0, 0, TAG },
/*316*/{ 0, 0, 0, TAG },
/*317*/{ 0, 0, 0, TAG },
/*318*/{ 0, 0, 0, TAG },
/*319*/{ 0, 0, 0, TAG },
/*320*/{ 0, 0, 0, TAG },
/*321*/{ 0, 0, 0, TAG },
/*322*/{ 0, 0, 0, TAG },
/*323*/{ 0, 0, 0, TAG },
/*324*/{ 0, 0, 0, TAG },
/*325*/{ 0, 0, 0, TAG },
/*326*/{ 0, 0, 0, TAG },
/*327*/{ 0, 0, 0, TAG },
/*328*/{ 0, 0, 0, TAG },
/*329*/{ 0, 0, 0, TAG },
/*330*/{ 0, 0, 0, TAG },
/*331*/{ 0, 0, 0, TAG },
/*332 */{ 0,		Sector_Set3DFloor, 2, {TAG, 4}},
/*333 */{ 0,		Static_Init , 2, {TAG, Init_Gravity}},
/*334 */{ 0,		Static_Init , 2, {TAG, Init_Color}},
/*335 */{ 0,		Static_Init , 2, {TAG, Init_Damage}},
/*336 */{ 0,		Line_Mirror , 1, {}},
/*337 */{ 0,		Line_Horizon , 1, {}},
/*338 */{ WALK,		Floor_Waggle , 5, {TAG, 24, 32, 0, 0}},
/*339 */{ WALK,		Floor_Waggle , 5, {TAG, 12, 32, 0, 0}},
/*340 */{ 0,		Plane_Align , 2, {1, 0}},	// Slope front floor
/*341 */{ 0,		Plane_Align , 2, {0, 1}},	// Slope front ceiling
/*342 */{ 0,		Plane_Align , 2, {1, 1}},	// Slope front floor and ceiling
/*343 */{ 0,		Plane_Align , 2, {2, 0}},	// Slope back floor
/*344 */{ 0,		Plane_Align , 2, {0, 2}},	// Slope back ceiling
/*345 */{ 0,		Plane_Align , 2, {2, 2}},	// Slope back floor and ceiling
/*346 */{ 0,		Plane_Align , 2, {2, 1}},	// Slope b.f. and f.c.
/*347 */{ 0,		Plane_Align , 2, {1, 2}},	// Slope f.f. and b.c.
/*348 */{ WALK,		Autosave , 1, {}},
/*349 */{ USE,		Autosave , 1, {}},
/*350 */{ 0,		Transfer_Heights , 2, {TAG, 2}},	// Just fake the floor
/*351 */{ 0,		Transfer_Heights , 2, {TAG, 6}},	// Just fake the floor and clip it too
/*352 */{ 0,		Sector_CopyScroller, 2, {TAG, 1}},	// copy ceiling scroller
/*353 */{ 0,		Sector_CopyScroller, 2, {TAG, 2}},	// copy floor scroller
/*354 */{ 0,		Sector_CopyScroller, 2, {TAG, 6}},	// copy carrying floor scroller
/*355*/{ 0, 0, 0, TAG },
/*356*/{ 0, 0, 0, TAG },
/*357*/{ 0, 0, 0, TAG },
/*358*/{ 0, 0, 0, TAG },
/*359*/{ 0, 0, 0, TAG },
/*360*/{ 0, 0, 0, TAG },
/*361*/{ 0, 0, 0, TAG },
/*362*/{ 0, 0, 0, TAG },
/*363*/{ 0, 0, 0, TAG },
/*364*/{ 0, 0, 0, TAG },
/*365*/{ 0, 0, 0, TAG },
/*366*/{ 0, 0, 0, TAG },
/*367*/{ 0, 0, 0, TAG },
/*368*/{ 0, 0, 0, TAG },
/*369*/{ 0, 0, 0, TAG },
/*370*/{ 0, 0, 0, TAG },
/*371*/{ 0, 0, 0, TAG },
/*372*/{ 0, 0, 0, TAG },
/*373*/{ 0, 0, 0, TAG },
/*374*/{ 0, 0, 0, TAG },
/*375*/{ 0, 0, 0, TAG },
/*376*/{ 0, 0, 0, TAG },
/*377*/{ 0, 0, 0, TAG },
/*378*/{ 0, 0, 0, TAG },
/*379 */{ 0,Static_Init, 3, {TAG,3,1}}, //ceil
/*380 */{ 0,Static_Init, 3, {TAG,3,0}}, //floor
/*381*/{ 0, 0, 0, TAG },
/*382*/{ 0, 0, 0, TAG },
/*383*/{ 0, 0, 0, TAG },
/*384*/{ 0, 0, 0, TAG },
/*385*/{ 0, 0, 0, TAG },
/*386*/{ 0, 0, 0, TAG },
/*387*/{ 0, 0, 0, TAG },
/*388*/{ 0, 0, 0, TAG },
/*389*/{ 0, 0, 0, TAG },
/*390*/{ 0, 0, 0, TAG },
/*391*/{ 0, 0, 0, TAG },
/*392*/{ 0, 0, 0, TAG },
/*393*/{ 0, 0, 0, TAG },
/*394*/{ 0, 0, 0, TAG },
/*395*/{ 0, 0, 0, TAG },
/*396*/{ 0, 0, 0, TAG },
/*397*/{ 0, 0, 0, TAG },
/*398*/{ 0, 0, 0, TAG },
/*399*/{ 0, 0, 0, TAG },
/*400 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 0, 255}},
/*401 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 16, 255}},
/*402 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 32, 255}},
/*403 */{ 0,     Sector_Set3DFloor, 4, {TAG, 2, 2, 255}},
/*404 */{ 0,     Sector_Set3DFloor, 4, {TAG, 2, 2, 204}},
/*405 */{ 0,     Sector_Set3DFloor, 4, {TAG, 2, 2, 153}},
/*406 */{ 0,     Sector_Set3DFloor, 4, {TAG, 2, 2, 102}},
/*407 */{ 0,     Sector_Set3DFloor, 4, {TAG, 2, 2, 51}},
/*408 */{ 0,     Sector_Set3DFloor, 3, {TAG, 2, 2}},
/*409*/{ 0, 0, 0, TAG },
/*410*/{ 0, 0, 0, TAG },
/*411*/{ 0, 0, 0, TAG },
/*412*/{ 0, 0, 0, TAG },
/*413 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 8, 255}},
/*414 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 8, 204}},
/*415 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 8, 153}},
/*416 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 8, 102}},
/*417 */{ 0,     Sector_Set3DFloor, 4, {TAG, 1, 8, 51}},
/*409 */{ 0,		TranslucentLine , 2, {LINETAG, 204}},	// 80% translucent
/*410 */{ 0,		TranslucentLine , 2, {LINETAG, 153}},	// 60% translucent
/*411 */{ 0,		TranslucentLine , 2, {LINETAG, 101}},	// 40% translucent
/*412 */{ 0,		TranslucentLine , 2, {LINETAG, 50}},	// 20% translucent
/*413*/{ 0, 0, 0, TAG },
/*414*/{ 0, 0, 0, TAG },
/*415*/{ 0, 0, 0, TAG },
/*416*/{ 0, 0, 0, TAG },
/*417*/{ 0, 0, 0, TAG },
/*418*/{ 0, 0, 0, TAG },
/*419*/{ 0, 0, 0, TAG },
/*420*/{ 0, 0, 0, TAG },
/*421*/{ 0, 0, 0, TAG },
/*422 */{ 0,		Scroll_Texture_Right , 1, {SCROLL_UNIT}},
/*423 */{ 0,		Scroll_Texture_Up , 1, {SCROLL_UNIT}},
/*424 */{ 0,		Scroll_Texture_Down , 1, {SCROLL_UNIT}},
/*425 */{ 0,		Scroll_Texture_Both , 5, {0, SCROLL_UNIT, 0, 0, SCROLL_UNIT}},
/*426 */{ 0,		Scroll_Texture_Both , 5, {0, SCROLL_UNIT, 0, SCROLL_UNIT, 0}},
/*427 */{ 0,		Scroll_Texture_Both , 5, {0, 0, SCROLL_UNIT, 0, SCROLL_UNIT}},
/*428 */{ 0,		Scroll_Texture_Both , 5, {0, 0, SCROLL_UNIT, SCROLL_UNIT, 0}},
/*429*/{ 0, 0, 0, TAG },
/*430*/{ 0, 0, 0, TAG },
/*431*/{ 0, 0, 0, TAG },
/*432*/{ 0, 0, 0, TAG },
/*433*/{ 0, 0, 0, TAG },
/*434 */{ USE,		Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}},
/*435 */{ USE|REP,		Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}},
/*436 */{ WALK,		Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}},
/*437 */{ WALK|REP,		Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}},
/*438 */{ SHOOT,		Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}},
/*439 */{ SHOOT|REP,	Floor_RaiseByValue , 3, {TAG, F_SLOW, 2}}
};
#define NUM_SPECIALS 439

