import os
from random import randint, uniform

default_path = "C:/A/storage/"

def install(lib_name):
	os.system(f"pip --quiet install {lib_name}")

def set_window_pos(x, y):
	os.environ['SDL_VIDEO_WINDOW_POS'] = '%i, %i' % (x, y)

def get_border(dx, dy):
	return [0, 0], [0, dy - 1], [dx - 1, dy - 1], [dx - 1, 0]

def name(i):
	return i.__class__.__name__

e = 2.71828
def activate(value, size = 4):
	return - 2 / (1 + e ** (size * value)) + 1

def clamp(value, min_v, max_v):
	return min(max_v, max(min_v, value))

class list2d:
	"""list2d((width, height), value) -> list2d
> width: int
> height: int
> value: int or str or float or list2d (or another objects whith .copy() function)"""
	def __init__(self, size, value):
		self.size = size
		self.width = self.size[0]
		self.height = self.size[1]
		if name(value) in ('int', 'str', 'float'):
			self.list = [[value for y in range(self.height)] for x in range(self.width)]
		else:
			self.list = [[value.copy() for y in range(self.height)] for x in range(self.width)]
	def __setitem__(self, index, value):
		try:
			self.list[index[1]][index[0]] = value
		except TypeError as error:
			error.add_note(f"\texcepted 'tuple:(int,int)' or 'list:[int,int]', example:\n\t> list2d[x, y] = value")
			raise
	def __getitem__(self, index):
		return self.list[index]
	def __iter__(self):
		return iter(self.list)
	def __repr__(self):
		ml = 0
		for x in self:
			for y in x:
				ml = max(ml, len(repr(y)))
		ml = ml // 2 * 2
		res = ''
		for x in self:
			for y in x:
				res += repr(y).center(ml, ' ') + " "
			res = res + "\n"# * (ml // 4 + 1)
		return res[:-1]
	def copy(self):
		res = list2d(self.size, 0)
		res.list = self.list.copy()
		return res

class neuron:
	def __init__(self):
		self.random()
	def random(self, value = 0.5):
		self.array = [list2d((10,10), list2d((10,10), 0)), list2d((10,10), 0)]
		for x1 in range(10):
			for y1 in range(10):
				for x2 in range(10):
					for y2 in range(10):
						self.array[0][x1][y2][x2][y2] = uniform(-value, value)
				self.array[1][x1][y1] = uniform(-value, value)
	def use(self, SURF):
		res = 0
		for x1 in range(10):
			for y1 in range(10):
				val = 0
				for x2 in range(10):
					for y2 in range(10):
						val += self.array[0][x1][y1][x2][y2] * (SURF.get_at((x1 * 10 + x2, y1 * 10 + y2)).r) / 255
				res += self.array[1][x1][y1] * activate(val / 100, 4)
		return activate(res)
	def copy(self):
		res = neuron()
		res.array = self.array.copy()
		return res