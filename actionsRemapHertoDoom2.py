#!/usr/bin/env python3

#21:25 08.03.2025 SilverMiner convert Heretic maps to MBF
#15:45 16.03.2025 add 3 modes

from sys import argv
from omg import *
from omg.mapedit import *
import math

def make_adder(collection, struct_type):
	def adder(**kwargs):
		result = len(collection)
		collection.append(struct_type(**kwargs))
		return result
	return adder

xmin = ymin = 32767
xmax = ymax = -32768

action_map = {
	7: 12618,
	8: 12616,
	10: 13392,
	49: 167,
	88: 13393,
	99: 85,
	100: 15641,
	105: 124,
	106: 12680,
	107: 12682
}
action_maplr = {
	99: 48,
	100: 105,
	105: 124,
	106: 100,
	107: 127
}

angle_map = {
	0: 0,
	1: 16384,
	2: -16384,
	3: -32768
}

thing_map = {
5: 3001,
6: 84,
7: 16,
10: 2007,
12: 2048,
13: 2046,
15: 3005,
16: 2046,
17: 60,
18: 2008,
19: 2049,
20: 2047,
21: 17,
9: 16,
22: 2010,
23: 2046,
24: 61,
25: 62,
26: 63,
27: 55,
28: 59,
29: 36,
30: 2001,
31: 2019,
32: 2013,
33: 2045,
34: 2010,
35: 2026,
36: 2001,
37: 25,
38: 25,
39: 59,
40: 60,
41: 14011,
42: 14012,
43: 2035,
44: 2035,
45: 3001,
46: 3001,
47: 44,
48: 24,
49: 24,
50: 34,
51: 63,
52: 79,
53: 2002,
54: 2007,
55: 2048,
56: 2008,
64: 3001,
65: 69,
66: 3001,
68: 3002,
69: 58,
73: 38,
74: 80,
75: 2024,
76: 35,
79: 40,
80: 39,
81: 2011,
82: 2012,
83: 2019,
84: 2022,
85: 2018,
86: 2023,
87: 26,
90: 3002,
94: 77,
95: 73,
96: 75,
1200: 14001,
1201: 14002,
1202: 14003,
1203: 14004,
1204: 14005,
1205: 14006,
1206: 14007,
1207: 14008,
1208: 14009,
1209: 14010,
2001: 82,
70: 69,
92: 3003,
2002: 2006,
}
mode_map = {
	'-mbf': 0,
	'-br2': 1,
	'-lr': 2,
}
#def sefs15(s,ed):

def sefs2039(s,ed,parm253):
	global xmin, ymin, xmax, ymax, unique_tag,add_sector,add_sidedef,add_linedef,add_vertex,add_thing,mode
	se = s.type
	s.type = 768
	foundExisting = False
	useSectorTag = False
	#anyOrtho = False
	if s.tag != 0:
		useSectorTag = True
	tline = -1
	
	if parm253 == 253:
		controlLineLen = 2**(se%5+4)
		controlLineDir = (se-20)//5
	elif parm253 == 224:
		controlLineLen = 2**((se-40)%3+4)
		controlLineDir = (se-40)//3
	elif parm253 == 223:
		controlLineLen = 171 # 108
		controlLineDir = 0
	
	controlLineAng = angle_map.get(controlLineDir, controlLineDir)
	for seg in ed.segs:
		if seg.angle == controlLineAng:
			tline = ed.linedefs[seg.line]
			if tline.action !=0 or tline.tag != 0:
				continue
			tva = ed.vertexes[tline.vx_a]
			tvb = ed.vertexes[tline.vx_b]
			check = abs(tvb.x - tva.x)+abs(tvb.y - tva.y)
			if check == controlLineLen:
				foundExisting = True
				print('exists', check)
			else:
				print(check)
			break
	if foundExisting:
		tline.action = parm253
		if useSectorTag:
			tline.tag = s.tag
		else:
			tline.tag = unique_tag
			s.tag = unique_tag
			unique_tag += 1
	else:
		#for ld in ed.linedefs:
		if controlLineDir == 0 or controlLineDir == 3:
			v1 = add_vertex(x=xmax+16, y=ymax+16)
			v2 = add_vertex(x=xmax+16+controlLineLen,y=ymax+16)
			if controlLineDir == 3:
				v1,v2=v2,v1
			xmax += 32 + controlLineLen
		else:
			v1 = add_vertex(x=xmax+16, y=ymax+16)
			v2 = add_vertex(x=xmax+16, y=ymax+16+controlLineLen)
			if controlLineDir == 2:
				v1,v2=v2,v1
			ymax += 32 + controlLineLen
		if useSectorTag:
			newtag = s.tag
		else:
			newtag = unique_tag
			s.tag = unique_tag
			unique_tag +=1
		newline = add_linedef(vx_a=v1, vx_b=v2, flags=1, action = parm253, tag = newtag)


def heretic2mbf(map):
	global xmin, ymin, xmax, ymax, unique_tag,add_sector,add_sidedef,add_linedef,add_vertex,add_thing,mode
	ed = MapEditor(map)
	
	add_sector = make_adder(ed.sectors, omg.Sector)
	add_sidedef = make_adder(ed.sidedefs, omg.Sidedef)
	add_linedef = make_adder(ed.linedefs, omg.Linedef)
	add_vertex = make_adder(ed.vertexes, omg.Vertex)
	add_thing = make_adder(ed.things, omg.Thing)
	
	xmin = ymin = 32767
	xmax = ymax = -32768
	usedtags = {}
	
	for ld in ed.linedefs:
		usedtags[ld.tag] = 1
	for s in ed.sectors:
		usedtags[s.tag] = 1
	sorted_tags = sorted(usedtags.keys())
	unique_tag = sorted_tags[-1] + 1

	for v in ed.vertexes:
		xmin = min(xmin, v.x)
		xmax = max(xmax, v.x)
		ymin = min(ymin, v.y)
		ymax = max(ymax, v.y)
	if mode == 0:
		for s in ed.sectors:
			if s.type == 4:
				s.type = 66
			elif s.type == 15:
				sefs2039(s,ed,223)
			elif s.type >= 20 and s.type <= 39:
				sefs2039(s,ed,253)
			elif s.type >= 40 and s.type <= 51:
				sefs2039(s,ed,224)
	if mode < 2:
		theactionmap = action_map
	else:
		theactionmap = action_maplr
		for s in ed.sectors:
			if s.type == 1:
				s.type = 17
			elif s.type in [4,5]:
				s.type = 7
			elif s.type == 16:
				s.type = 5
			elif s.type in [6,15,*range(21,52)]:
				s.type = 0

	for s in ed.linedefs:
		s.action = theactionmap.get(s.action, s.action)
	
	if mode == 1:
		for t in ed.things:
			num = t.type
			if(num <= 96 and num>=5):
				t.type+=7000
			elif((num >= 2001 and num <= 2005) or num == 2035):
				t.type+=5200
			else:
				continue
	else:
		for t in ed.things:
			t.type = thing_map.get(t.type, t.type)



	return ed.to_lumps()

mode = 0
pattern = "*"

def main(args):
	global pattern,mode
	if (len(args) < 2):
		print ("	Omgifol script: convert Heretic map to MBF\n")
		print ("	Usage:")
		print ("	actionsRemapHer2Doom.py input.wad output.wad [-mbf/-lr/-br2] [pattern]\n")
		print ("	i remember my mus_e1m1 got erased somehow lol")
		print ("	pattern is like E?M4 or MAP*.")
		print ("	-mbf is default mode. -br2 means one for my 4 iwads zdoom mission pack.")
	else:
		print ("Loading %s..." % args[0])
		inwad = WAD()
		outwad = WAD()
		inwad.from_file(args[0])
		
		if (len(args) >= 3):
			for arg in args[2:]:
				if arg in mode_map:
					mode = mode_map.get(arg, 0)
				else:
					pattern = arg
		
		for name in inwad.maps.find(pattern):
			print ("Remapping %s" % name)
			outwad.maps[name] = heretic2mbf(inwad.maps[name])
		print ("Saving %s..." % args[1])
		outwad.to_file(args[1])


if __name__ == "__main__":
	main(argv[1:])
