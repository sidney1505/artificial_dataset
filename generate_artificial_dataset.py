import random
import pygame

class Generator:
	def __init__(self):
		self.colors = [(255,0,0),(0,255,0),(0,0,255)] # ['red','blue','yellow']
		self.shapes = ['circle','triangle','square']
		self.sizes = [3, 5, 7] # 'small','medium','big'
		self.x_positions = range(5)
		self.y_positions = range(5)

	def generate_sample(self):
		num_shapes = random.randint(0, len(self.x_positions) * len(self.y_positions))
		shapes = []
		shape_grid = []
		for x_posistion in range(self.x_positions):
			shape_grid.append([])
			for y_posistion in range(self.y_positions):
				shape_grid[x_posistion].append([None])
		covered_positions = []
		for shape in range(num_shapes):
			color = self.colors(random.randint(0, len(self.colors)))
			shape = self.shapes(random.randint(0, len(self.shapes)))
			size = self.sizes(random.randint(0, len(self.sizes)))
			while len(covered_positions) != shape + 1:
				x_position = self.x_positions(random.randint(0, len(self.x_positions)))
				y_position = self.y_positions(random.randint(0, len(self.y_positions)))
				if not [x_position, y_position] in covered_positions:
					covered_positions.append([x_position, y_position])
			shapes.append({'color' : color, 'shape' : shape, 'size' : size, 'x_position' : x_position, 'y_position' : y_position})
			shape_grid[x_position][y_position] = [color, shape, size]
		img = self.visualize_shapes(shapes)
		relations = self.calculate_relations(shape_grid)
		return shapes, img, relations

	def visualize_shapes(self, shapes):
		background_color = (255,255,255)
		(width,height) = (16 * len(self.x_positions), 16 * len(self.y_positions))
		screen = pygame.Surface((width, height))
		screen.fill(background_colour)
		for shape in shapes:
			center = (16 * shape['x_position'] + 8, 16 * shape['y_position'] + 8)
			if shape['shape'] == 'circle':
				pygame.draw.circle(screen, shape['color'], center, shape['size'])
			elif shape['shape'] == 'rect':
				pygame.draw.rect(screen, shape['color'], pygame.Rect(center[0] - 0.5 * shape['size'], center[1] - 0.5 * shape['size'], shape['size'], shape['size']))
			elif shape['shape'] == 'triangle':
				pygame.draw.polygon(screen, shape['color'], [
					(center[0] - 0.5 * shape['size'], center[1]),
					(center[0] + 0.5 * shape['size'], center[1] - 0.5 * shape['size']),
					(center[0] + 0.5 * shape['size'], center[1] + 0.5 * shape['size'])
				])
		data = pygame.image.tostring(surf, 'RGB')
		img = Image.fromstring('RGB', (width, height), data)
		return img

	def calculate_relations(self, shape_grid):
		attribute_tuples = []
		for color in self.colors:
			for shape in self.shapes:
				for size in self.sizes:
					attribute_tuples.append([color, shape, size])
		#
		pairs = []
		for idx_outer, attribute_tuple_outer in enumerate(attribute_tuples):
			for idx_inner, attribute_tuple_inner in enumerate(attribute_tuples):
				if idx_inner != idx_outer:
					pairs.append([attribute_tuple_outer, attribute_tuple_inner])
		#
		relation_functional_dict = {}
		def less(pair, shape_grid):
			count_a = 0
			count_b = 0
			for x_position in self.x_positions:
				for y_position in self.y_positions:
					if pair[0] == shape_grid[x_position][y_position]:
						count_a += 1
					if pair[0] == shape_grid[x_position][y_position]:
						count_b += 1
			return count_a < count_b
		relation_functional_dict['less'] = less
		def exists_above(pair, shape_grid):			
			for x_position in self.x_positions[:-1]:
				for y_position in self.y_positions:
					if shape_grid[x_position][y_position] == pair[0] and shape_grid[x_position + 1][y_position] == pair[1]:
						return True
			return False
		relation_functional_dict['exists_above'] = exists_above
		#
		relations = []
		for pair in pairs:
			for relation_type in relation_functional_dict.keys():
				relations.append(relation_type, pair, relation_functional_dict[relation_type](pair, shape_grid))
		return relations
