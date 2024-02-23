import json
import gui
from random import choice as rch
from random import shuffle as rsh
from random import randint as rnd

# -----------------------------------------

# открытие json и забор данных
def jsOpen(path):
	with open(path, "r", encoding="utf-8") as file:
		data = json.load(file)
	return data
# сохранение данных в json
def jsSave(path, data):
	with open(path, "w", encoding="utf-8") as file:
		json.dump(data, file, ensure_ascii=False)

# нормализация индекса
def n(i, size=False):
	if isinstance(size, int):
		while True:
			if size == 0: return 0
			elif i >= size: i -= size; continue
			elif i < 0: i += size; continue
			else: return i
	else:
		if i > 0: return 1
		elif i < 0: return -1
		else: return 0

# генерация таблицы
def arr(size, el=0):
	res = []
	i = 0
	while i < size[0]:
		res.append([])
		ii = 0
		while ii < size[1]:
			res[i].append(el)
			ii += 1
		i += 1
	return res

# разделение строки на таблицу
def split(arr, n):
	res = []
	t = ""
	for el in arr:
		t += el
		if len(t) == n:
			res.append(t)
			t = ""
	return res

# -----------------------------------------

# GUI = [size, pix, pallette=[0, 1]]
JSON = jsOpen("src.json")
GUI = JSON["display"]
GUI["pallette"] = JSON["pallette"][GUI["pallette"]]
GL = JSON["gamelimit"]

FONT = jsOpen("font.json")
SPR = jsOpen("sprites.json")
ART = jsOpen("arts.json")

SCENARY = jsOpen("langs/{}.json".format(GUI["lang"]))

display = gui.Scene(
	"NOKIA 3310 Club", 
	[GUI["size"][0]*GUI["pix"], GUI["size"][1]*GUI["pix"]], 
	GUI["fps"], 
	GUI["pallette"][0],
	"icon.png")

# -----------------------------------------

class Canvas:
	def __init__(self, display, size):
		self.display = display
		self.size = size
		self.canvas = arr(GUI["size"])

	def draw(self):
		for ix in range(GUI["size"][0]):
			for iy in range(GUI["size"][1]):
				clr = GUI["pallette"][1] if self.canvas[ix][iy] else GUI["pallette"][0]
				self.display.drawBox(
					[ix*GUI["pix"], iy*GUI["pix"]],
					[GUI["pix"], GUI["pix"]],
					clr, GUI["border"])

	def clear(self):
		self.canvas = arr(GUI["size"])

	def addBox(self, pos, size, full=True):
		for ix in range(pos[0], pos[0]+size[0]):
			for iy in range(pos[1], pos[1]+size[1]):
				if not full and (ix not in [pos[0], pos[0]+size[0]-1]) and (iy not in [pos[1], pos[1]+size[1]-1]):
					self.canvas[ix][iy] = 0
				else:
					self.canvas[ix][iy] = 1

	def addSym(self, pos, sym):
		sym = split(FONT[sym], 3)
		for ix in range(3):
			for iy in range(4):
				self.canvas[pos[0]+ix][pos[1]+iy] = int(sym[iy][ix])

	def addText(self, pos, text):
		text = text.lower()
		shift = 0
		for i in range(len(text)):
			if i >= 20: shift = 1
			if i >= 40: break
			rx = pos[0] + 4*i - shift*20*4
			ry = pos[1] + shift*5
			self.addSym([rx, ry], text[i])

	def addSprite(self, typ, pos, path):
		if typ == "spr":
			try: spr = SPR[path[0]][path[1]]
			except: spr = SPR["test"][path[1]]
		elif typ == "art":
			try: spr = ART[path]
			except: spr = ART["void"]

		for ix in range(len(spr[0])):
			for iy in range(len(spr)):
				self.canvas[pos[0]+ix][pos[1]+iy] = int(spr[iy][ix])

def drawSlide(canvas, slide):

	if slide[0] == "mode":
		return ["mode", slide[1]]

	elif slide[0] == "snd":
		return ["snd", slide[1]]

	elif slide[0] == "txt":
		canvas.addSprite("spr", [24,0], [slide[1], slide[2]])
		canvas.addBox([0, 29], [4*(len(slide[1])+1), 8], False)
		canvas.addText([2, 31], slide[1])
		canvas.addBox([0, 36], [84, 12], False)
		canvas.addText([2, 38], slide[3])

	elif slide[0] == "art":
		canvas.addSprite("art", [0, 0], slide[1])
		canvas.addText([2, 38], slide[2])

	elif slide[0] == "chg":
		canvas.addText([2, 1], "[Down] -1 [Up] +1")
		canvas.addText([2, 38], slide[2])


# pingpong
xy = [30, 30]
t = [rch([-1, 1]), rch([-1, 1])]

# taggame
table = arr([4,4])
table_win = arr([4,4])
rlist = list("abcdefghijklmno ")
rlist_win = list("abcdefghijklmno ")
rsh(rlist)
i = 0
spacexy = [0, 0]
for ix in range(4):
	for iy in range(4):
		table[ix][iy] = rlist[i]
		table_win[ix][iy] = rlist_win[i]
		if rlist[i] == " ": spacexy = [ix, iy]
		i += 1
tagscore = 0

#snakegame
snake = [5, 5]
global snake_dir, walls, apple
snake_dir = "Right"
walls = []
apple = [7, 7]

def play(canvas, game, value):
	if game == "pingpong":

		canvas.addBox([78, 12*value], [6, 12], 1)

		xy[0] += t[0]
		xy[1] += t[1]

		if xy[0] >= 78: return "end"

		canvas.addBox(xy, [6,6], 1)
		canvas.addBox([0, xy[1]], [6, 6], 1)

		if xy[1] <= 0 or xy[1] >= 42: t[1] *= -1
		if xy[0] <= 6: t[0] *= -1
		if xy[0] >= 72 and xy[1] in range((value*12)-5, (value*12)+11):
			t[0] *= -1
			t[0] = t[0] + 1 if t[0] > 0 else t[0] - 1
			return 1

	elif game == "taggame":

		canvas.addText([0,1], "[space]")
		canvas.addText([0,6], "to lose")

		for ix in range(4):
			for iy in range(4):
				canvas.addBox([36+ix*12, iy*12], [12, 12], 0)
				canvas.addSym([36+ix*12+4, iy*12+4], table[ix][iy])

		try:
			if value == "Up":
				tt = table[spacexy[0]][spacexy[1]+1]
				table[spacexy[0]][spacexy[1]] = tt
				table[spacexy[0]][spacexy[1]+1] = " "
				spacexy[1] += 1
				tagscore += 1
			elif value == "Down":
				tt = table[spacexy[0]][spacexy[1]-1]
				table[spacexy[0]][spacexy[1]] = tt
				table[spacexy[0]][spacexy[1]-1] = " "
				spacexy[1] -= 1
				tagscore += 1
			elif value == "Left":
				tt = table[spacexy[0]+1][spacexy[1]]
				table[spacexy[0]][spacexy[1]] = tt
				table[spacexy[0]+1][spacexy[1]] = " "
				spacexy[0] += 1
				tagscore += 1
			elif value == "Right":
				tt = table[spacexy[0]-1][spacexy[1]]
				table[spacexy[0]][spacexy[1]] = tt
				table[spacexy[0]-1][spacexy[1]] = " "
				spacexy[0] -= 1
				tagscore += 1
		except: pass

		if value == "Space": return -1
		if table == table_win: return tagscore

	elif game == "snakegame":

		global snake_dir, walls, apple

		if snake_dir == "Up": snake[1] -= 2
		elif snake_dir == "Down": snake[1] += 2
		elif snake_dir == "Left": snake[0] -= 2
		elif snake_dir == "Right": snake[0] += 2
		
		if value in ["Up", "Down", "Left", "Right"]:
			snake_dir = value

		if snake[0] <= 1 or snake[0] >= 41 or snake[1] <= 1 or snake[1] >= 23: return "end"
		if snake in walls: return "end"

		if snake in [apple, [apple[0]+1, apple[1]], [apple[0], apple[1]+1], [apple[0]+1, apple[1]+1]]:
			walls.append(apple)
			while 1:
				apple = [rnd(3,39), rnd(3,21)]
				if apple not in walls: break
			return 1

		canvas.addBox([0,0], [84,48], 0)
		canvas.addBox([snake[0]*2, snake[1]*2], [2, 2], 1)
		canvas.addBox([apple[0]*2, apple[1]*2], [4, 4], 0)
		for wall in walls:
			canvas.addBox([wall[0]*2, wall[1]*2], [2, 2], 1)