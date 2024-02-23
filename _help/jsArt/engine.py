import json
import gui

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

def arr2lines(arr):
	lines = []
	for iy in range(len(arr[0])):
		lines.append("")
		for ix in range(len(arr)):
			lines[iy] = "{}{}".format(lines[iy], arr[ix][iy])
	return lines

def draw(display, canvas, pix):
	for ix in range(len(canvas)):
		for iy in range(len(canvas[ix])):
			color = [255,255,255] if canvas[ix][iy] else [50,50,50]
			display.drawBox(
				[ix*pix+1, iy*pix+1],
				[pix-2, pix-2],
				color)