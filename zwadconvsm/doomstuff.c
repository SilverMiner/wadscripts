//
// The code in this file was adapted from DOOM's r_main.c and p_setup.c.
// Here's the appropriate header info:
//
// Copyright (C) 1993-1996 by id Software, Inc.
//
// This source is available for distribution and/or modification
// only under the terms of the DOOM Source Code License as
// published by id Software. All rights reserved.
//
// The source is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// FITNESS FOR A PARTICULAR PURPOSE. See the DOOM Source Code License
// for more details.
#include "zwadconv.h"


//
// R_PointOnSide
// Traverse BSP (sub) tree, check point against partition plane.
// Returns side 0 (front) or 1 (back).
//
static int PointOnSide (WORD x, WORD y, mapnode_t *node)
{
	WORD dx, dy;
	double left, right;
		
	if (!node->dx)
	{
		if (x <= node->x)
			return node->dy > 0;
		
		return node->dy < 0;
	}
	if (!node->dy)
	{
		if (y <= node->y)
			return node->dx < 0;
		
		return node->dx > 0;
	}
		
	dx = (x - node->x);
	dy = (y - node->y);
		
	// Try to quickly decide by looking at sign bits.
	if ( (node->dy ^ node->dx ^ dx ^ dy)&0x8000 )
	{
		if	( (node->dy ^ dx) & 0x8000 )
		{
			// (left is negative)
			return 1;
		}
		return 0;
	}

	left = ((float)(node->dy) / 65536.0) * (float)dx;
	right = (float)dy * ((float)(node->dx) / 65536.0);

	return (right < left) ? 0 : 1;
}

//
// R_PointInSector
//
mapsector_t *PointInSector (WORD x, WORD y)
{
	mapnode_t* 	node;
	int 		side;
	int 		nodenum;

	// single subsector is a special case
	if (!numnodes)								
		return &sectors[subsectors->numsegs];
				
	nodenum = numnodes - 1;

	while (! (nodenum & NF_SUBSECTOR) )
	{
		node = &nodes[nodenum];
		side = PointOnSide (x, y, node);
		nodenum = node->children[side];
	}
		
	return &sectors[subsectors[nodenum & ~NF_SUBSECTOR].numsegs];
}

void GroupLines (void)
{
	mapsubsector_t *ss = subsectors;
	int i;

	// look up sector number for each subsector
	// Store the sector index in ss->numsegs, since we don't use it.
	for (i = 0; i < numsubsectors; i++, ss++) {
		mapseg_t *seg = &segs[ss->firstseg];
		maplinedef2_t *line = &lines[seg->linedef];
		mapsidedef_t *side = &sides[line->sidenum[seg->side]];

		ss->numsegs = side->sector;
	}
}