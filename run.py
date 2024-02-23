from engine import *

canvas = Canvas(display, GUI["size"])

devmode = False

scenarys = ["intro", "day0", "day1", "day2", "day3", "end_alone", "end_garem", "end_aurora", "end_eva", "end_sophia", "ending"]
mode = "intro"
slide = 0
gamevalue = 0

gamescores = {"pingpong": 0, "taggame": 0, "snakegame": 0}
changes = {"pingpong": 0, "taggame": 0, "snakegame": 0}

run = 1
while run:
	canvas.clear()
	key = display.start()
	# ---------------------

	if key:
		if key == "Esc": run = 0
		elif key == "d": devmode = False if devmode else True
		elif key in ["0", "1", "2", "3", "4", "5", "6", "7", "8","9"] and devmode:
			if key == "0": pass
			elif key == "1": 
				slide = 0
				mode = "end_alone"
			elif key == "2": 
				slide = 0
				mode = "end_aurora"
			elif key == "3": 
				slide = 0
				mode = "end_eva"
			elif key == "4": 
				slide = 0
				mode = "end_sophia"
			elif key == "5": 
				slide = 0
				mode = "end_garem"
			elif key == "6": 
				gamescores["pingpong"] = 1
				changes["pingpong"] = 1
			elif key == "7":
				gamescores["taggame"] = 1
				changes["taggame"] = 1
			elif key == "8":
				gamescores["snakegame"] = 1
				changes["snakegame"] = 1
			elif key == "9": pass

		if mode in scenarys:
			if key in ["Left", "Right"] and not SCENARY[mode][slide][0] == "chg":
				if key == "Right" and slide+1 < len(SCENARY[mode]): slide += 1
				elif key == "Left" and slide > 0: slide -= 1
			elif key in ["Up", "Down"] and SCENARY[mode][slide][0] == "chg":
				if key == "Up": changes[SCENARY[mode][slide][1]] = 1
				elif key == "Down": changes[SCENARY[mode][slide][1]] = 0
				slide += 1

		if mode == "pingpong":
			if key == "Up" and gamevalue > 0: gamevalue -= 1
			elif key == "Down" and gamevalue < 3: gamevalue += 1

	# ---------------------

	if mode in scenarys:
		switch = drawSlide(canvas, SCENARY[mode][slide])
		if switch:
			if switch[0] == "mode": 
				mode = switch[1]
				slide = 0
			elif switch[0] == "snd":
				if switch[1] == "":
					display.stopBG()
					slide += 1
				else:
					display.stopBG()
					display.playBG("snd/{}.mp3".format(switch[1]), GUI["volume"], -1)
					slide += 1

	elif mode == "switch":
		girls = {
			"eva": gamescores["pingpong"]+changes["pingpong"],
			"sophia": gamescores["taggame"]+changes["taggame"],
			"aurora": gamescores["snakegame"]+changes["snakegame"],
		}
		if girls["eva"] == 2 and girls["sophia"] < 2 and girls["aurora"] < 2: mode = "end_eva"
		elif girls["sophia"] == 2 and girls["eva"] < 2 and girls["aurora"] < 2: mode = "end_sophia"
		elif girls["aurora"] == 2 and girls["sophia"] < 2 and girls["eva"] < 2: mode = "end_eva"
		elif girls["eva"] < 2 and girls["sophia"] < 2 and girls["aurora"] < 2: mode = "end_alone"
		else: mode = "end_garem"

	elif mode == "end":
		run = 0

	elif mode == "pingpong":
		score = play(canvas, "pingpong", gamevalue)
		if score:
			if score == "end":
				gamescores["pingpong"] = 1 if gamescores["pingpong"] >= GL["pingpong"] else 0
				slide = 0
				mode = "day1"
			else: gamescores["pingpong"] += score

	elif mode == "taggame":
		score = play(canvas, "taggame", key)
		if score:
			gamescores["taggame"] = 1 if score > 0 and score < GL["taggame"] else 0
			slide = 0
			mode = "day2"

	elif mode == "snakegame":
		score = play(canvas, "snakegame", key)
		if score:
			if score == "end":
				gamescores["snakegame"] = 1 if gamescores["snakegame"] >= GL["snakegame"] else 0
				slide = 0
				mode = "day3"
			else:
				gamescores["snakegame"] += score

	# ---------------------
	canvas.draw()
	display.update(GUI["fps"])