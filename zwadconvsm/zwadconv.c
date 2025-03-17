#include "zwadconv.h"

/* To be considered a map, each map label *must* be
 * followed by the following lumps in this order
 */
char MapLumps[10][8] = {
	"THINGS",
	"LINEDEFS",
	"SIDEDEFS",
	"VERTEXES",
	"SEGS",
	"SSECTORS",
	"NODES",
	"SECTORS",
	"REJECT",
	"BLOCKMAP"
};

/* An empty behavior lump containing no scripts or strings */
UBYTE NullBehavior[16] = "ACS\0\x8\0\0\0\0\0\0\0\0\0\0\0";

/* Behavior generated on the fly if sectors tag 666 or 667
 * are referenced by a linedef. Also used if lineids get
 * mapped to special lines. (4k ought to be plenty.)
 */
ULONG FlyBehavior[1024];
ULONG FlySize, FlyScript;
ULONG ScriptStarts[255];

FILE *logfile;

UBYTE SectorTags[65536];
UBYTE RefCount[65536/8];
UBYTE UsedTags[256/8];

UBYTE LineIDMaps[65536];
UWORD ReverseLineIDMaps[256];

BOOL SomeProblems = FALSE;

BOOL UsedLineIDs;

mapsector_t *sectors;
mapthing2_t *things;
maplinedef2_t *lines;
mapnode_t *nodes;
mapseg_t *segs;
mapsidedef_t *sides;
mapsubsector_t *subsectors;
int numthings, numlines, numsectors, numnodes, numsegs, numsubsectors, numsides;



void put (const char *fmt, ...)
{
	va_list argptr;

	va_start (argptr, fmt);
	vprintf (fmt, argptr);
	vfprintf (logfile, fmt, argptr);
	va_end (argptr);
}

void err (const char *fmt, ...)
{
	va_list argptr;

	va_start (argptr, fmt);
	vfprintf (stderr, fmt, argptr);
	vfprintf (logfile, fmt, argptr);
	va_end (argptr);
}

void *safemalloc (size_t bytes)
{
	void *mem = malloc (bytes);

	if (!mem) {
		err ("Failed allocating %d bytes!\n", bytes);
		exit (20);
	}
	return mem;
}

void saferead (FILE *in, size_t bytes, void *dest)
{
	size_t read = fread (dest, 1, bytes, in);
	
	if (read != bytes) {
		err ("Failed reading %d bytes (got %d)!\n", bytes, read);
		exit (20);
	}
}

void safewrite (FILE *out, size_t bytes, void *src)
{
	size_t wrote = fwrite (src, 1, bytes, out);

	if (wrote != bytes) {
		err ("Failed writing %d bytes (only wrote %d)!\n", bytes, wrote);
		exit (20);
	}
}

void safeseek (FILE *f, long offset)
{
	if (fseek (f, offset, SEEK_SET)) {
		err ("Failed trying to fseek to %d\n", offset);
		exit (20);
	}
}

void *readlump (FILE *f, const dir_t *directory, int lump)
{
	void *space = safemalloc (directory[lump].size);

	safeseek (f, directory[lump].pos);
	saferead (f, directory[lump].size, space);
	return space;
}

void copylump (FILE *in, FILE *out, const dir_t *directory, int lump)
{
	void *lumpdata;
	
	if (directory[lump].size) {
		lumpdata = readlump (in, directory, lump);
		safewrite (out, directory[lump].size, lumpdata);
		free (lumpdata);
	}
}

void makeentry (dir_t *dir, const char *name, ULONG pos, ULONG size)
{
	dir->pos = pos;
	dir->size = size;
	strncpy (dir->name, name, 8);
}

void copyentry (dir_t *to, const dir_t *from, ULONG newpos)
{
	to->pos = newpos;
	to->size = from->size;
	strncpy (to->name, from->name, 8);
}

void copylump2 (FILE *in, FILE *out, const dir_t *src, dir_t *dest,
				int lump, int newlump, ULONG *newpos)
{
	copylump (in, out, src, lump);
	copyentry (&dest[newlump], &src[lump], *newpos);
	*newpos += src[lump].size;
}

void putlump (FILE *out, void *data, ULONG size,
			  char *name, dir_t *dir, int lump, ULONG *pos)
{
	safewrite (out, size, data);
	dir[lump].pos = *pos;
	dir[lump].size = size;
	strncpy (dir[lump].name, name, 8);
	*pos += size;
}

/****** Begin actual program code ******/

BOOL IsMap (const dir_t *dir, ULONG dirsize, ULONG lump)
{
	int i;
	char name[9];

	if (lump + 10 >= dirsize)
		return FALSE;

	for (i = 1; i <= 10; i++) {
		if (strnicmp (dir[lump+i].name, MapLumps[i-1], 8))
			return FALSE;
	}

	strncpy (name, dir[lump].name, 8);
	name[8] = 0;

	// If the map already has a BEHAVIOR lump, pretend it isn't a map.
	if (lump + 11 < dirsize)
		if (strnicmp (dir[lump+11].name, "BEHAVIOR", 8) == 0) {
			put ("\n%s already has a BEHAVIOR lump.\n", name);
			return FALSE;
		}

	put ("\nConverting %s\n", name);

	return TRUE;
}

UWORD freetag (UWORD tag)
{
	if (tag < 256 && ((UsedTags[tag/8] & (1 << (tag & 7))) == 0)) {
		return tag;
	} else {
		int i;

		if (tag == 666 || tag == 667)
			put ("WARNING! ");

		for (i = 128; i < 256; i++) {
			if ((UsedTags[i/8] & (1 << (i&7)))== 0) {
				put ("Tag %d remapped to %d\n", tag, i);
				return i;
			}
		}
		for (i = 127; i >= 0; i--) {
			if ((UsedTags[i/8] & (1 << (i&7))) == 0) {
				put ("Tag %d remapped to %d\n", tag, i);
				return i;
			}
		}
	}
	put ("FIX THIS: Could not remap tag %d (using 0)!\n", tag);
	SomeProblems = TRUE;
	return 0;
}


UBYTE maptag (UWORD tag)
{
	if (tag == 0) {
		return 0;
	} else if (SectorTags[tag] == 0) {
		// Try to find a good tag for this one (preferably the same)
		int newtag = freetag (tag);

		SectorTags[tag] = newtag;
		UsedTags[newtag/8] |= 1 << (newtag & 7);
	}

	return SectorTags[tag];
}

UWORD freelineid (UWORD id)
{
	if (id < 256 && !ReverseLineIDMaps[id]) {
		return id;
	} else {
		int i;

		for (i = 0; i < 255; i++)
			if (ReverseLineIDMaps[i] == 0) {
				put ("LineID %d remapped to %d\n", id, i);
				return i;
			}
	}
	put ("FIXTHIS: Could not remap lineid %d (using 0)!\n", id);
	SomeProblems = TRUE;
	return 0;
}


UBYTE maplineid (UWORD id)
{
	if (id == 0) {
		return 0;
	} else if (LineIDMaps[id] == 0) {
		// Try to find a good lineid for this one (preferably the same)
		int newid = freelineid (id);

		LineIDMaps[id] = newid;
		ReverseLineIDMaps[newid] = id;
	}

	return LineIDMaps[id];
}


// Returns TRUE if a 666 or 667 tag was referenced, and there
// were no free scripts.
BOOL TranslateLineDef (maplinedef2_t *ld, const maplinedef_t *mld)
{
	BOOL res = FALSE;
	WORD special = mld->special;
	WORD flags = mld->flags;
	int i;
	UBYTE nspecial;
	UWORD args[5];
	UWORD tag;
	BOOL usedtag = FALSE;
	int numparms = 0;
	BOOL passthrough;
	//BOOL 3dmidtex;

	ld->v1 = mld->v1;
	ld->v2 = mld->v2;
	ld->sidenum[0] = mld->sidenum[0];
	ld->sidenum[1] = mld->sidenum[1];
	
	passthrough = (flags & ML_PASSUSEORG);
	//3dmidtex = (flags & ML_3DMIDTEX);

	flags = flags & 0x01ff;	// Ignore flags unknown to DOOM

	if (special <= NUM_SPECIALS) {
		// This is a regular special; translate thru LUT
		flags = flags | (SpecialTranslation[special].flags << 8);
		if (passthrough && (flags & ML_ACTIVATIONMASK) == ML_ACTIVATEUSE) {
			flags &= ~ML_ACTIVATIONMASK;
			flags |= ML_ACTIVATEUSETHROUGH;
		}
		nspecial = SpecialTranslation[special].newspecial;
		numparms = SpecialTranslation[special].numparms;
		for (i = 0; i < 5; i++) {
			if (SpecialTranslation[special].args[i] == TAG) {
				usedtag = TRUE;
				if (mld->tag != 666 && mld->tag != 667)
					tag = maptag (mld->tag);
				else
					tag = mld->tag;
				args[i] = tag;
			} else if (SpecialTranslation[special].args[i] == LINETAG) {
				UsedLineIDs = TRUE;
				tag = maplineid (mld->tag);
				args[i] = tag;
			} else {
				args[i] = SpecialTranslation[special].args[i];
			}
		}
	} else if (special <= GenCrusherBase) {
		if (special >= ZDoomStaticInits && special < ZDoomStaticInits + NUM_STATIC_INITS) {
			// A ZDoom Static_Init special
			nspecial = Static_Init;
			usedtag = TRUE;
			if (mld->tag != 666 && mld->tag != 667)
				tag = maptag (mld->tag);
			else
				tag = mld->tag;
			args[0] = tag;
			args[1] = special - ZDoomStaticInits;
		} else {
			// This is an unknown special. Just zero it.
			nspecial = 0;
			memset (args, 0, sizeof(args));
			flags &= ~ML_ACTIVATIONMASK;
		}
	} else {
		// Anything else is a BOOM generalized linedef type
		if (mld->tag != 666 && mld->tag != 667)
			tag = maptag (mld->tag);
		else
			tag = mld->tag;

		switch (special & 0x0007) {
			case WalkMany:
				flags |= ML_REPEATABLE;
			case WalkOnce:
				flags |= ML_ACTIVATECROSS;
				break;

			case SwitchMany:
			case PushMany:
				flags |= ML_REPEATABLE;
			case SwitchOnce:
			case PushOnce:
				if (passthrough)
					flags |= ML_ACTIVATEUSETHROUGH;
				else
					flags |= ML_ACTIVATEUSE;
				break;

			case GunMany:
				flags |= ML_REPEATABLE;
			case GunOnce:
				flags |= ML_ACTIVATEPROJECTILEHIT;
				break;
		}

		// We treat push triggers like switch triggers with zero tags.
		if ((special & 0x0007) == PushMany ||
			(special & 0x0007) == PushOnce)
			args[0] = 0;
		else {
			args[0] = tag;
			usedtag = TRUE;
		}

		if (special <= GenStairsBase) {
			// Generalized crusher (tag, dnspeed, upspeed, silent, damage)
			nspecial = Generic_Crusher;
			if (special & 0x0020)
				flags |= ML_MONSTERSCANACTIVATE;
			switch (special & 0x0018) {
				case 0x0000:	args[1] = C_SLOW;	break;
				case 0x0008:	args[1] = C_NORMAL;	break;
				case 0x0010:	args[1] = C_FAST;	break;
				case 0x0018:	args[1] = C_TURBO;	break;
			}
			args[2] = args[1];
			args[3] = (special & 0x0040) >> 6;
			args[4] = 10;
			numparms = 5;
		} else if (special <= GenLiftBase) {
			// Generalized stairs (tag, speed, step, dir/igntxt, reset)
			nspecial = Generic_Stairs;
			if (special & 0x0020)
				flags |= ML_MONSTERSCANACTIVATE;
			switch (special & 0x0018) {
				case 0x0000:	args[1] = S_SLOW;	break;
				case 0x0008:	args[1] = S_NORMAL;	break;
				case 0x0010:	args[1] = S_FAST;	break;
				case 0x0018:	args[1] = S_TURBO;	break;
			}
			switch (special & 0x00c0) {
				case 0x0000:	args[2] = 4;		break;
				case 0x0040:	args[2] = 8;		break;
				case 0x0080:	args[2] = 16;		break;
				case 0x00c0:	args[2] = 24;		break;
			}
			args[3] = (special & 0x0300) >> 8;
			args[4] = 0;
			numparms = 5;
		} else if (special <= GenLockedBase) {
			// Generalized lift (tag, speed, delay, target, height)
			nspecial = Generic_Lift;
			if (special & 0x0020)
				flags |= ML_MONSTERSCANACTIVATE;
			switch (special & 0x0018) {
				case 0x0000:	args[1] = P_SLOW*2;		break;
				case 0x0008:	args[1] = P_NORMAL*2;	break;
				case 0x0010:	args[1] = P_FAST*2;		break;
				case 0x0018:	args[1] = P_TURBO*2;	break;
			}
			switch (special & 0x00c0) {
				case 0x0000:	args[2] = 8;		break;
				case 0x0040:	args[2] = 24;		break;
				case 0x0080:	args[2] = 40;		break;
				case 0x00c0:	args[2] = 80;		break;
			}
			args[3] = ((special & 0x0300) >> 8) + 1;
			args[4] = 0;
			numparms = 5;
		} else if (special <= GenDoorBase) {
			// Generalized locked door (tag, speed, kind, delay, lock)
			nspecial = Generic_Door;
			if (special & 0x0080)
				flags |= ML_MONSTERSCANACTIVATE;
			switch (special & 0x0018) {
				case 0x0000:	args[1] = D_SLOW;	break;
				case 0x0008:	args[1] = D_NORMAL;	break;
				case 0x0010:	args[1] = D_FAST;	break;
				case 0x0018:	args[1] = D_TURBO;	break;
			}
			args[2] = (special & 0x0020) >> 5;
			args[3] = 0;
			args[4] = (special & 0x01c0) >> 6;
			if (args[4] == 0)
				args[4] = AnyKey;
			else if (args[4] == 7)
				args[4] = AllKeys;
			args[4] |= (special & 0x0200) >> 2;
			numparms = 5;
		} else if (special <= GenCeilingBase) {
			// Generalized door (tag, speed, kind, delay, lock)
			nspecial = Generic_Door;
			switch (special & 0x0018) {
				case 0x0000:	args[1] = D_SLOW;	break;
				case 0x0008:	args[1] = D_NORMAL;	break;
				case 0x0010:	args[1] = D_FAST;	break;
				case 0x0018:	args[1] = D_TURBO;	break;
			}
			args[2] = (special & 0x0060) >> 5;
			switch (special & 0x0300) {
				case 0x0000:	args[3] = 8;		break;
				case 0x0100:	args[3] = 32;		break;
				case 0x0200:	args[3] = 72;		break;
				case 0x0300:	args[3] = 240;		break;
			}
			args[4] = 0;
			numparms = 5;
		} else {
			// Generalized ceiling (tag, speed, height, target, change/model/direct/crush)
			// Generalized floor (tag, speed, height, target, change/model/direct/crush)
			if (special <= GenFloorBase)
				nspecial = Generic_Ceiling;
			else
				nspecial = Generic_Floor;
			
			switch (special & 0x0018) {
				case 0x0000:	args[1] = F_SLOW;	break;
				case 0x0008:	args[1] = F_NORMAL;	break;
				case 0x0010:	args[1] = F_FAST;	break;
				case 0x0018:	args[1] = F_TURBO;	break;
			}
			args[3] = ((special & 0x0380) >> 7) + 1;
			if (args[3] >= 7) {
				args[2] = 24 + (args[3] - 7) * 8;
				args[3] = 0;
			} else {
				args[2] = 0;
			}
			args[4] = ((special & 0x0c00) >> 10) |
					  ((special & 0x0060) >> 3) |
					  ((special & 0x1000) >> 8);
			numparms = 5;
		}
	}

	ld->flags = flags;

	if (usedtag && (tag == 666 || tag == 667) && numparms) {
		// Sector tags 666 and 667 are special cases:
		// We need to preserve them, so we construct a script for them.
		// If the special takes no parameters, though, we don't need to
		// bother, since the tag isn't actually used by it in that case.
		if (FlyScript >= 255) {
			res = TRUE;
		} else {
			ScriptStarts[FlyScript++] = FlySize * 4;
			FlyBehavior[FlySize++] = PCD_LSPEC1DIRECT + numparms - 1;
			FlyBehavior[FlySize++] = nspecial;
			for (i = 0; i < numparms; i++)
				FlyBehavior[FlySize++] = args[i];
			FlyBehavior[FlySize++] = PCD_TERMINATE;

			ld->special = ACS_ExecuteAlways;
			ld->args[0] = FlyScript;
			ld->args[1] = ld->args[2] = ld->args[3] = ld->args[4] = 0;

			return FALSE;
		}
	}

	ld->special = nspecial;
	for (i = 0; i < 5; i++)
		ld->args[i] = (UBYTE)args[i];
	return res;
}


// Set the TID of all teleport destinations to match the tag
// of their containing sectors.
void TranslateTeleportThings (void)
{
	int i;
	mapthing2_t *thing;

	for (i = 0, thing = things; i < numthings; i++, thing++)
		if (thing->type == T_DESTINATION)
			thing->thingid = PointInSector (thing->x, thing->y)->tag;
}


void ConvertSectors (mapsector_t *sectors, int numsectors)
{
	mapsector_t *sector;
	int i;

	for (i = 0, sector = sectors; i < numsectors; i++, sector++)
	{
		if (SectorTags[sector->tag])
			sector->tag = SectorTags[sector->tag];
		else if ((RefCount[sector->tag/8] & (1 << (sector->tag & 7))) == 0 &&
				 sector->tag && sector->tag != 666 && sector->tag != 667) {
				put ("Sector tag %d is unreferenced\n", sector->tag);
				RefCount[sector->tag/8] |= 1 << (sector->tag & 7);
		}
		if (sector->special)
			sector->special =
				(sector->special == 9) ? SECRET_MASK :
				(sector->special == 20) ? 196 :
				((sector->special & 0xfe0) << 3) |
				((sector->special & 0x01f) + (((sector->special & 0x1f) < 21) ? 64 : -20));
	}
}

maplinedef2_t *ConvertLines (const maplinedef_t *lines, int numlines)
{
	int i;
	maplinedef2_t *newlines;

	newlines = safemalloc (sizeof(*newlines) * numlines);

	for (i = 0; i < numlines; i++) {
		if (TranslateLineDef (newlines + i, lines + i)) {
			put ("Linedef %d referenced sector tag %d, but there were no free scripts.\n",
				 i, lines[i].tag);
			SomeProblems = TRUE;
		}
		if ((newlines[i].flags & ML_ACTIVATIONMASK) == ML_ACTIVATEPROJECTILEHIT) 
			;
			// This warning isn't necessary anymore, because when a projectile
			// encounters a line, it always acts as if it hit it, even if it
			// only crosses over it. This is because Hexen does it that way.
			//put ("Linedef %d has activation G%c. Assuming projectile hit.\n",
			//	 i, (newlines[i].flags & ML_REPEATABLE) ? 'R' : '1');
	}

	return newlines;
}

mapthing2_t *ConvertThings (const mapthing_t *things, int numthings)
{
	int i;
	mapthing2_t *newthings, *post;
	const mapthing_t *pre;
	UWORD flags;

	newthings = safemalloc (sizeof(*newthings) * numthings);

	for (i = 0, pre = things, post = newthings;
		 i < numthings;
		 i++, pre++, post++) {
		memset (post, 0, sizeof(*post));

		// translate the spawn flags to Hexen format.
		flags = pre->options;
		post->flags = (UWORD)((flags & 0xf) | 0x7e0);
		if (flags & BTF_NOTSINGLE)			post->flags &= ~MTF_SINGLE;
		if (flags & BTF_NOTDEATHMATCH)		post->flags &= ~MTF_DEATHMATCH;
		if (flags & BTF_NOTCOOPERATIVE)		post->flags &= ~MTF_COOPERATIVE;
		
		if (flags & BTF_FRIENDLY)	post->flags |= MTF_FRIENDLY;

		post->x = pre->x;
		post->y = pre->y;
		post->angle = pre->angle;
		post->type = pre->type;
	}
	return newthings;
}

int ProcessFile (FILE *in, FILE *out)
{
	char magic[4];
	ULONG dirsize, dirstart;
	ULONG newdirstart;
	dir_t *directory, *newdir;
	ULONG lump, newlump, newpos;

	memcpy (FlyBehavior, NullBehavior, 4);

	saferead (in, 4, magic);

	if (strncmp (magic, "IWAD", 4) && strncmp (magic, "PWAD", 4)) {
		err ("Source file must be a WAD.\n");
	}

	saferead (in, 4, &dirsize);
	saferead (in, 4, &dirstart);

	put ("WAD directory starts at 0x%X and has %d entries\n", dirstart, dirsize);

	directory = safemalloc (dirsize * sizeof(dir_t));
	newdir = safemalloc (((dirsize / 10) + dirsize) * sizeof(dir_t));

	safeseek (in, dirstart);
	saferead (in, dirsize * sizeof(dir_t), directory);

	safewrite (out, 4, magic);
	safewrite (out, 4, &dirsize);		// Corrected later
	safewrite (out, 4, &dirstart);		// Ditto

	newpos = 4 * 3;

	for (lump = newlump = 0; lump < dirsize; lump++, newlump++) {
		if (IsMap (directory, dirsize, lump)) {
			mapthing_t *fromthings;
			maplinedef_t *fromlines;

			// Copy map label
			copylump2 (in, out, directory, newdir, lump, newlump, &newpos);
			// Read things
			fromthings = readlump (in, directory, lump+1);
			numthings = directory[lump+1].size / sizeof(mapthing_t);
			// Read linedefs
			fromlines = readlump (in, directory, lump+2);
			numlines = directory[lump+2].size / sizeof(maplinedef_t);
			// Read sidedefs
			sides = readlump (in, directory, lump+3);
			numsides = directory[lump+3].size / sizeof(mapsidedef_t);
			// Read segs
			segs = readlump (in, directory, lump+5);
			numsegs = directory[lump+5].size / sizeof(mapseg_t);
			// Read subsectors
			subsectors = readlump (in, directory, lump+6);
			numsubsectors = directory[lump+6].size / sizeof(mapsubsector_t);
			// Read nodes
			nodes = readlump (in, directory, lump+7);
			numnodes = directory[lump+7].size / sizeof(mapnode_t);
			// Read sectors
			sectors = readlump (in, directory, lump+8);
			numsectors = directory[lump+8].size / sizeof(mapsector_t);

			// Do the conversion
			memset (SectorTags, 0, sizeof(SectorTags));
			memset (UsedTags, 0, sizeof(UsedTags));
			memset (RefCount, 0, sizeof(RefCount));
			UsedLineIDs = FALSE;
			FlySize = 2;
			FlyScript = 0;

			lines = ConvertLines (fromlines, numlines);
			ConvertSectors (sectors, numsectors);
			things = ConvertThings (fromthings, numthings);
			free (fromthings);
			GroupLines();
			TranslateTeleportThings ();


			if (UsedLineIDs) {
				// Make sure that everything that could be referenced by a
				// line id is. We also need an open script to set the lines
				// up if we can't just give them a special that sets their id.
				int i;
				maplinedef_t *line;
				maplinedef2_t *to;
				BOOL gotscript = FALSE;

				put ("Setting LineIDs\n");
				for (i = 0, line = fromlines, to = lines; i < numlines; i++, line++, to++) {
					if (LineIDMaps[line->tag]) {
						if (to->special != Teleport_Line &&
							to->special != TranslucentLine &&
							to->special != Scroll_Texture_Model) {
							if (line->special == 0) {
								// Set this line to Line_SetIdentification
								to->special = Line_SetIdentification;
								to->args[0] = LineIDMaps[line->tag];
							} else {
								// This line does something special! Gak!
								put ("FIX THIS: Linedef %d (might) need id %d but already has a special.\n",
									 i, LineIDMaps[line->tag]);
								SomeProblems = TRUE;
							}
						}
					}
				}
			}
			free (fromlines);

			// Write things
			putlump (out, things, numthings * sizeof(mapthing2_t),
					 MapLumps[0], newdir, newlump+1, &newpos);
			// Write linedefs
			putlump (out, lines, numlines * sizeof(maplinedef2_t),
					 MapLumps[1], newdir, newlump+2, &newpos);
			// Write sidedefs
			putlump (out, sides, numsides * sizeof(mapsidedef_t),
					 MapLumps[2], newdir, newlump+3, &newpos);
			// Copy vertexes
			copylump2 (in, out, directory, newdir, lump+4, newlump+4, &newpos);
			// Write segs
			putlump (out, segs, numsegs * sizeof(mapseg_t),
					 MapLumps[4], newdir, newlump+5, &newpos);
			// Copy ssectors (we obliterated numsegs, so we can't use the copy in memory)
			free (subsectors);
			copylump2 (in, out, directory, newdir, lump+6, newlump+6, &newpos);
			// Write nodes
			putlump (out, nodes, numnodes * sizeof(mapnode_t),
					 MapLumps[6], newdir, newlump+7, &newpos);
			// Write sectors
			putlump (out, sectors, numsectors * sizeof(mapsector_t),
					 MapLumps[7], newdir, newlump+8, &newpos);
			// Copy reject
			copylump2 (in, out, directory, newdir, lump+9, newlump+9, &newpos);
			// Copy blockmap
			copylump2 (in, out, directory, newdir, lump+10, newlump+10, &newpos);
			// Write behavior
			if (FlyScript) {
				// We generated a behavior lump
				ULONG i;

				FlyBehavior[1] = FlySize * 4;
				FlyBehavior[FlySize++] = FlyScript;
				for (i = 0; i < FlyScript; i++, FlySize += 3) {
					FlyBehavior[FlySize+0] = i + 1;
					FlyBehavior[FlySize+1] = ScriptStarts[i];
					FlyBehavior[FlySize+2] = 0;
				}
				FlyBehavior[FlySize++] = 0;		// 0 strings
				putlump (out, FlyBehavior, FlySize * 4,
						 "BEHAVIOR", newdir, newlump+11, &newpos);
				put ("%d script%s created\n", FlyScript, FlyScript > 1 ? "s" : "");
			} else {
				// The empty behavior lump will suffice
				putlump (out, NullBehavior, sizeof(NullBehavior),
						 "BEHAVIOR", newdir, newlump+11, &newpos);
			}

			free (sectors);
			free (nodes);
			free (segs);
			free (sides);
			free (lines);
			free (things);

			lump += 10;
			newlump += 11;
		} else {
			copylump2 (in, out, directory, newdir, lump, newlump, &newpos);
			if ((lump & 63) == 0)
				put (".");
		}
	}

	newdirstart = ftell (out);

	safewrite (out, newlump * sizeof(dir_t), newdir);
	safeseek (out, 4);
	safewrite (out, 4, &newlump);
	safewrite (out, 4, &newdirstart);

	free (newdir);
	free (directory);

	put ("\nNew wad has %d entries\n", newlump);

	return 0;
}

int main (int argc, char **argv)
{
	FILE *in, *out;
	int res = 20;

	if (argc < 3) {
		printf ("Usage: zdwadconv <source.wad> <output.wad>\n\n"
				"This program converts every map in the source.wad into the\n"
				"enhanced format supported by ZDoom. This is essentially what\n"
				"the game does when it loads a normal Doom map. However, ZDoom\n"
				"is free to use certain tricks which this program can't, so it\n"
				"is possible that some maps will not convert successfully.\n"
				"The file convlog.txt will contain a copy of every message\n"
				"printed to the screen during the conversion and should be\n"
				"checked if something went wring.\n");
		return 0;
	}

	if (!stricmp (argv[1], argv[2])) {
		fprintf (stderr, "Source and destination files must have different names.\n");
		return 10;
	}

	if (logfile = fopen ("convlog.txt", "w")) {
		if (in = fopen (argv[1], "rb")) {
			if (out = fopen (argv[2], "wb")) {
				res = ProcessFile (in, out);
				fclose (out);
				if (SomeProblems)
					fprintf (stderr, "\nThe conversion was not entirely successful. You should review convlog.txt\n"
									 "and make any necessary changes to the wad so that it works properly.\n");
			} else {
				err ("Could not open %s\n", argv[2]);
			}
			fclose (in);
		} else {
			err ("Could not open %s\n", argv[1]);
		}
		fclose (logfile);
	} else {
		fprintf (stderr, "Could not open convlog.txt\n");
	}

	return res;
}