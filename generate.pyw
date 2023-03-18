import lib
import file_system
import random
try:
	from pygame import *
except:
	lib.install("pygame") # bad code )
	from pygame import *

try:
	source = [map(float, i.split()) for i in open("storage/p1/source.txt")]
except:
	source = []

init()
inf = display.Info()
ix, iy = inf.current_w, inf.current_h
im = min(ix, iy)
dis = display.set_mode((im * 0.8, im * 0.8), NOFRAME)
dx, dy = dis.get_size()
center = Vector2(dx / 2, dy / 2)
display.set_caption("AI generate")
clock = time.Clock()

font_size = 32
font.init()
FONT = font.Font(None, font_size)
def font_update():
	FONT = font.Font(None, int(font_size * zoom))

surf = Surface((100, 100))
pos = center.copy()
scale = min(dx, dy) - 10
zoom = 1

border = [0, 0], [0, dy - 1], [dx - 1, dy - 1], [dx - 1, 0]
border_color = (127,127,127)
backgroun_color = (31,31,31)
info_color = (255,255,255)

def p1():
	FILL_COLOR = random.randint(0, 255)
	surf.fill((FILL_COLOR, FILL_COLOR, FILL_COLOR))
	SIZE = random.randint(10, 25)
	POS = random.randint(SIZE + 1, 100 - SIZE - 1), random.randint(SIZE + 1, 100 - SIZE - 1)
	COLOR = random.randint(0, 255)
	while abs(FILL_COLOR - COLOR) < 64:
		COLOR = random.randint(0, 255)
	draw.rect(surf, (COLOR, COLOR, COLOR), [POS[0] - SIZE, POS[1] - SIZE, SIZE * 2, SIZE * 2])
	return f"{(POS[0] / 50  - 1):0.2f} {(POS[1] / 50 - 1):0.2f} {SIZE / 50}"

file_system.new_dirs("storage/p1")
FILE = open("storage/p1/source.txt", "w")
for i in range(1000):
	print(p1(), file = FILE)
	image.save(surf, "storage/p1/" + str(i) + ".png")
	dis.fill(backgroun_color)
	q = transform.scale(surf, (scale * zoom, scale * zoom))
	dis.blit(q, pos - Vector2(q.get_size()) / 2)
	draw.lines(dis, border_color, True, border)
	display.update()
	event.pump()
FILE.close()
print("finish")

def draw_info():
	source_info = source(int(file_name))
	info_render = FONT.render(f"{file_name}.png (100 x 100) real:{source_info}", True, info_color)
	

loop = True
while loop:
	dis.fill(backgroun_color)
	q = transform.scale(surf, (scale * zoom, scale * zoom))
	dis.blit(q, pos - Vector2(q.get_size()) / 2)
	draw.lines(dis, border_color, True, border)
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
			elif e.key == K_1:
				p1()
		elif e.type == WINDOWFOCUSLOST:
			border_color = (63,63,63)
			backgroun_color = (23,23,23)
		elif e.type == WINDOWFOCUSGAINED:
			border_color = (127,127,127)
			backgroun_color = (31,31,31)
		elif e.type == MOUSEWHEEL:
			if e.y == 1 and zoom < 10:
				zoom += 0.1
				pos += ((pos - center) - (mouse_pos - center)) * 0.1 / zoom
				font_update()
			elif e.y == -1 and zoom > 0.2:
				zoom -= 0.1
				pos -= ((pos - center) - (mouse_pos - center)) * 0.1 / zoom
				font_update()
		elif e.type == MOUSEMOTION:
			if pressed_mouse[0]:
				pos += Vector2(e.rel)
		elif e.type == MOUSEBUTTONDOWN:
			if e.button == 2:
				pos = center.copy()
				zoom = 1
				font_update()
	clock.tick(60)

display.quit()