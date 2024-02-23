from engine import *

pix = 15
size = [84, 36]

display = gui.Scene("jsArt", [pix*size[0], pix*size[1]], 30)

canvas = arr(size, 0)

run = 1
while run:
	key = display.start()
	# ---------------------

	if isinstance(key, str):
		if key == "Esc": run = 0
		elif key == "Space": 
			lines = arr2lines(canvas)
			for line in lines: print("\"{}\",".format(line))
			print()
	elif isinstance(key, tuple):
		mx = int(key[0]/pix)
		my = int(key[1]/pix)
		canvas[mx][my] = 0 if canvas[mx][my] else 1

	# ---------------------

	draw(display, canvas, pix)

	# ---------------------
	display.update()