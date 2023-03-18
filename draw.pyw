import lib
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

file_name = "0"
def update_surf():
	global file_name, surf
	File = image.load("storage/p1/" + file_name + ".png")
	surf.blit(File, (0, 0))
update_surf()

border = lib.get_border(dx, dy)
border_color = (127,127,127)
backgroun_color = (31,31,31)

brain = lib.neuron()
ai_result = brain.use(surf)
ai_result_pos = scale / 2 + scale / 2 * ai_result



loop = True
while loop:
	dis.fill(backgroun_color)
	draw.lines(dis, border_color, True, border)
	q = transform.scale(surf, (scale * zoom, scale * zoom))
	dis.blit(q, pos - Vector2(q.get_size()) / 2)
	draw.line(dis, (255,127,127), pos - Vector2(q.get_size()) / 2 + Vector2(ai_result_pos * zoom, 0),
		pos - Vector2(q.get_size()) / 2 + Vector2(ai_result_pos * zoom, scale * zoom))
	display.update()
	pressed_keys = key.get_pressed()
	pressed_mouse = mouse.get_pressed(3)
	mouse_pos = mouse.get_pos()
	for e in event.get():
		if e.type == WINDOWCLOSE:
			loop = False
		elif e.type == KEYDOWN:
			if e.key == K_ESCAPE:
				loop = False
			elif pressed_keys[K_LCTRL] or pressed_keys[K_RCTRL]:
				if e.key == K_LEFT:
					if display.get_init(): display.quit()
					display.init(); inf = display.Info(); ix, iy = inf.current_w, inf.current_h
					dis_init((0, 0), (ix // 2, iy))
					border = lib.get_border(dx, dy)
				elif e.key == K_RIGHT:
					if display.get_init(): display.quit()
					display.init(); inf = display.Info(); ix, iy = inf.current_w, inf.current_h
					dis_init((ix // 2, 0), (ix // 2, iy))
					border = lib.get_border(dx, dy)
				elif e.key == K_UP:
					if display.get_init(): display.quit()
					display.init(); inf = display.Info(); ix, iy = inf.current_w, inf.current_h
					dis_init((0, 0), (ix, iy))
					border = lib.get_border(dx, dy)
				elif e.key == K_DOWN:
					if display.get_init(): display.quit()
					display.init(); inf = display.Info(); ix, iy = inf.current_w, inf.current_h
					im = min(ix, iy)
					dis_init((ix // 2 - im * 0.4, iy // 2 - im * 0.4), (im * 0.8, im * 0.8), True)
					border = lib.get_border(dx, dy)
			elif pressed_keys[K_LSHIFT] or pressed_keys[K_RSHIFT]:
				if e.key == K_LEFT:
					file_name = str( (int(file_name) + 999) % 1000 )
					update_surf()
					ai_result = brain.use(surf)
					ai_result_pos = scale / 2 + scale / 2 * ai_result
				elif e.key == K_RIGHT:
					file_name = str( (int(file_name) + 1) % 1000 )
					update_surf()
					ai_result = brain.use(surf)
					ai_result_pos = scale / 2 + scale / 2 * ai_result
		elif e.type == MOUSEMOTION:
			if pressed_mouse[0]:
				pos += Vector2(e.rel)
		elif e.type == MOUSEWHEEL:
			if e.y == 1 and zoom < 10:
				zoom += 0.1
				pos += ((pos - center) - (mouse_pos - center)) * 0.1 / zoom
			elif e.y == -1 and zoom > 0.2:
				zoom -= 0.1
				pos -= ((pos - center) - (mouse_pos - center)) * 0.1 / zoom
		elif e.type == WINDOWFOCUSLOST:
			border_color = (63,63,63)
			backgroun_color = (23,23,23)
		elif e.type == WINDOWFOCUSGAINED:
			border_color = (127,127,127)
			backgroun_color = (31,31,31)
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 2:
				pos = center.copy()
				zoom = 1
	clock.tick(60)

display.quit()
