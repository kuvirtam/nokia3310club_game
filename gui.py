import pygame as pg
from sys import exit

_KEYS = {
	# цифры
	48: "0",
	49: "1",
	50: "2",
	51: "3",
	52: "4",
	53: "5",
	54: "6",
	55: "7",
	56: "8",
	57: "9",
	# буквы
	97: "a",
	98: "b",
	99: "c",
	100: "d",
	101: "e",
	102: "f",
	103: "g",
	104: "h",
	105: "i",
	106: "j",
	107: "k",
	108: "l",
	109: "m",
	110: "n",
	111: "o",
	112: "p",
	113: "q",
	114: "r",
	115: "s",
	116: "t",
	117: "u",
	118: "v",
	119: "w",
	120: "x",
	121: "y",
	122: "z",
	# остальные
	13: "Enter",
	27: "Esc",
	32: "Space",
	8: "Backspace",
	9: "Tab",
	1073741906: "Up",
	1073741905: "Down",
	1073741904: "Left",
	1073741903: "Right",
	45: "-",
	61: "+",}

class Scene:

	def __init__(self, title, size, fps, bg=(0,0,0), icon_path=False):
		self.title = title
		self.size = size
		self.fps = fps
		self.bg = bg

		pg.init() 
		self.screen = pg.display.set_mode(self.size) 
		pg.display.set_caption(self.title) 
		self.screen.fill(self.bg) 
		self.clock = pg.time.Clock()

		if icon_path:
			pg.display.set_icon(pg.image.load(icon_path))

	def close(self):
		pg.display.quit()
		pg.quit()
		exit()

	def start(self):
		self.screen.fill(self.bg)
		for event in pg.event.get():
			if event.type == pg.QUIT: self.close()
			elif event.type == pg.KEYDOWN:
				try: return _KEYS[event.key]
				except: return False
		return False

	def update(self, fps=0):
		self.clock.tick(self.fps)
		self.fps = fps if fps else self.fps
		pg.display.update()

	def drawBox(self, xy, size, color, bd=0, border=0):
		pg.draw.rect(self.screen, color, [xy[0]+bd, xy[1]+bd, size[0]-2*bd, size[1]-2*bd], border)

	def drawLine(self, poses, color, fill=False, close=False):
		if fill: pg.draw.polygon(self.screen, color, poses)
		else: pg.draw.lines(self.screen, color, close, poses)

	def drawDot(self, pos, r, color):
		pg.draw.circle(self.screen, color, pos, r)


	def playBG(self, path, volume=1, loop=1, fade=1000):
		pg.mixer.music.load(path)
		pg.mixer.music.play(loop, 0, fade)
		pg.mixer.music.set_volume(volume)

	def stopBG(self):
		pg.mixer.music.stop()