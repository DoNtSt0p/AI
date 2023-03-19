import lib
import file_system
from random import randint, uniform

try:
	from pygame import *
except:
	lib.install("pygame")
	from pygame import *
icon = Surface((90, 90), SRCALPHA)
icon.set_colorkey((255,0,255))
icon.fill((255,0,255))
for i in range(45, 0, -4):
	c = 255 - i / 45 * 127
	draw.circle(icon, (0, c, 0), (45, 45), i, 1)

try:
	source = [list(map(float, i.split())) for i in open("storage/p1/source.txt")]
except FileNotFoundError as error:
	log_file = open("log.txt", "a")
	print("fail opening 'storage/p1/source.txt', start generating...", file = log_file)
	file_system.python_run("generate.pyw")
	try:
		source = [list(map(float, i.split())) for i in open("storage/p1/source.txt")]
	except:
		log_file = open("log.txt", "a")
		print("fail opening 'storage/p1/source.txt' again", file = log_file)
		exit()

def display_info():
	inf = display.Info()
	return inf.current_w, inf.current_h

def dis_init(pos = None, size = (0, 0), farame = False):
	global dis, dx, dy
	if pos != None:
		lib.set_window_pos(pos[0], pos[1])
	if farame:
		dis = display.set_mode(size, RESIZABLE)
	else:
		dis = display.set_mode(size, NOFRAME)
	dx, dy = dis.get_size()
	display.set_icon(icon)
	display.set_caption("AI draw")
clock = time.Clock()

init()
inf = display.Info()
ix, iy = inf.current_w, inf.current_h
im = min(ix, iy)
dis = display.set_mode((im * 0.8, im * 0.8), NOFRAME)
dx, dy = dis.get_size()
center = Vector2(dx / 2, dy / 2)
display.set_caption("AI draw")
clock = time.Clock()

surf = Surface((100, 100))
pos = center.copy()
scale = min(dx, dy) - 10
zoom = 1

stat = Surface((1000,100))
stat.fill((0,0,0))

font_size = 32
font.init()
FONT = font.Font(None, font_size)

pause = False
pause_learn = False

file_name = "0"
def update_surf():
	global file_name, surf
	File = image.load("storage/p1/" + file_name + ".png")
	surf.blit(File, (0, 0))
update_surf()

border = lib.get_border(dx, dy)
border_color = (127,127,127)
backgroun_color = (31,31,31)
info_color = (255,255,255)

def update_other():
	global dx, dy, center, border
	dx, dy = dis.get_size()
	center = Vector2(dx / 2, dy / 2)
	border = lib.get_border(dx, dy)

pause_text = FONT.render("scroll pause", True, (255,255,255))
pause_learn_text = FONT.render("learn pause", True, (255,255,255))
def draw_info():
	source_info = source[int(file_name)]
	info_text = f"{file_name}.png (100 x 100) error: {(source_info[0] - ai_result_x):0.4f}"
	info_render = FONT.render(info_text, True, info_color)
	info_render = transform.scale(info_render, (info_render.get_size()[0] * zoom, info_render.get_size()[1] * zoom))
	info_render_pos = info_render.get_rect(bottomleft=(pos - Vector2(info_render.get_size()) / 2 + Vector2(0, - scale / 2 * zoom)))
	dis.blit(info_render, info_render_pos)
	if pause:
		dis.blit(pause_text, (10,10))
	if pause_learn:
		dis.blit(pause_learn_text, (10,30))

brain = lib.neuron()
def use_brain(hide=False):
	global ai_result_x, ai_result_y, ai_result_pos_x, ai_result_pos_y
	ai_result_x = brain.use(surf)
	ai_result_pos_x = scale / 2 + scale / 2 * ai_result_x
	#ai_result_y = brain.use( transform.rotate(surf, 90) )
	#ai_result_pos_y = scale / 2 + scale / 2 * ai_result_y
	if not hide:
		error_x = abs(source[int(file_name)][0] - ai_result_x)
		#error_y = abs(source[int(file_name)][1] - ai_result_y)
		if int(file_name) % 10 == 0:
			stat.scroll(1, 0)
			if file_name == '0':
				draw.line(stat, (31,31,31), (0, 0), (0, 99))
			else:
				draw.line(stat, (0,0,0), (0, 0), (0, 99))
			draw.line(stat, (255,0,0), (0, 49), (0, 49 - error_x * 50))
		#draw.line(stat, (0,63,255), (0, 50), (0, 50 + error_y * 50))
use_brain()

def learn():
	source_info = source[int(file_name)]
	use_brain(True)
	last_error = (ai_result_x - source_info[0]) ** 2# + (ai_result_y - source_info[1]) ** 2
	x1 = randint(0,9)
	y1 = randint(0,9)
	if randint(0,1):
		x2 = randint(0,9)
		y2 = randint(0,9)
		_recover = float(brain.array[0][x1][y1][x2][y2]) + 0.0000000001
		brain.array[0][x1][y1][x2][y2] = lib.clamp(brain.array[0][x1][y1][x2][y2] + uniform(-0.1, 0.1), -1, 1)
		use_brain(True)
		new_error = (ai_result_x - source_info[0]) ** 2# + (ai_result_y - source_info[1]) ** 2
		if new_error > last_error:
			brain.array[0][x1][y1][x2][y2] = _recover
	else:
		_recover = float(brain.array[1][x1][y1]) + 0.0000000001
		brain.array[1][x1][y1] = lib.clamp(brain.array[1][x1][y1] + uniform(-0.1, 0.1), -1, 1)
		use_brain(True)
		new_error = (ai_result_x - source_info[0]) ** 2# + (ai_result_y - source_info[1]) ** 2
		if new_error > last_error:
			brain.array[1][x1][y1] = _recover

loop = True
while loop:
	dis.fill(backgroun_color)
	draw.lines(dis, border_color, False, border)
	q = transform.scale(surf, (scale * zoom, scale * zoom))
	dis.blit(q, pos - Vector2(q.get_size()) / 2)
	s = transform.scale(stat, (scale * zoom, scale * zoom))
	dis.blit(s, pos - Vector2(s.get_size()) / 2 + Vector2(scale + 10, 0) * zoom)
	
	draw.line(dis, (255,0,0), pos - Vector2(q.get_size()) / 2 + Vector2(ai_result_pos_x * zoom, 0),
		pos - Vector2(q.get_size()) / 2 + Vector2(ai_result_pos_x * zoom, scale * zoom))
	#draw.line(dis, (0,62,255), pos - Vector2(q.get_size()) / 2 + Vector2(0, ai_result_pos_y * zoom),
	#	pos - Vector2(q.get_size()) / 2 + Vector2(scale * zoom, ai_result_pos_y * zoom))
	
	draw_info()
	display.update()
	pressed_keys = key.get_pressed()
	pressed_mouse = mouse.get_pressed(3)
	mouse_pos = mouse.get_pos()

	if not pause:
		file_name = str( (int(file_name) + 1) % 1000 )
		update_surf()
	if not pause_learn:
		learn()
		use_brain()

	for e in event.get():
		if e.type == WINDOWCLOSE:
			loop = False
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				loop = False
			elif pressed_keys[K_LCTRL] or pressed_keys[K_RCTRL]:
				if e.key == K_LEFT:
					if display.get_init(): display.quit()
					display.init()
					ix, iy = display_info()
					dis_init((0, 0), (ix // 2, iy))
					update_other()
				elif e.key == K_RIGHT:
					if display.get_init(): display.quit()
					display.init()
					ix, iy = display_info()
					dis_init((ix // 2, 0), (ix // 2, iy))
					update_other()
				elif e.key == K_UP:
					if display.get_init(): display.quit()
					display.init()
					ix, iy = display_info()
					dis_init((0, 0), (ix, iy))
					update_other()
				elif e.key == K_DOWN:
					if display.get_init(): display.quit()
					display.init()
					ix, iy = display_info()
					im = min(ix, iy)
					dis_init((ix // 2 - im * 0.4, iy // 2 - im * 0.4), (im * 0.8, im * 0.8), True)
					update_other()
			elif pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
				if e.key == K_LEFT:
					file_name = str( (int(file_name) + 999) % 1000 )
					update_surf()
					use_brain()
				elif e.key == K_RIGHT:
					file_name = str( (int(file_name) + 1) % 1000 )
					update_surf()
					use_brain()
			elif e.key == K_p:
				pause = not pause
			elif e.key == K_l:
				pause_learn = not pause_learn
			elif e.key == K_SPACE:
				if pause or pause_learn:
					pause = False
					pause_learn = False
				else:
					pause = True
					pause_learn = True
		elif e.type == MOUSEMOTION:
			if pressed_mouse[0]:
				pos += Vector2(e.rel)
		elif e.type == MOUSEWHEEL:
			if e.y == 1 and zoom < 2:
				add = zoom * 0.1
				pos += ((pos - center) - (mouse_pos - center)) * add / zoom
				zoom *= 1.1
			elif e.y == -1 and zoom > 0.2:
				add = zoom * 0.1
				pos -= ((pos - center) - (mouse_pos - center)) * add / zoom
				zoom *= 0.9
		elif e.type == WINDOWFOCUSLOST:
			border_color = (63,63,63)
			backgroun_color = (23,23,23)
		elif e.type == WINDOWFOCUSGAINED:
			border_color = (127,127,127)
			backgroun_color = (31,31,31)
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 2:
				if pressed_keys[K_LCTRL] or pressed_keys[K_RCTRL]:
					pos = center - Vector2(scale + 10, 0)
				else:
					pos = center.copy()
				zoom = 1
		elif e.type == WINDOWRESIZED:
			update_other()
	clock.tick(60)

display.quit()
