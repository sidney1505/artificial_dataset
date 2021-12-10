import random
import pygame

class Generator:
	def __init__(self):
		self.colors = ['red','blue','yellow']
		self.shapes = ['circle','triangle','square']
		self.sizes = ['small','medium','big']
		self.x_positions = [0,1,2]
		self.y_positions = [0,1,2]

	def generate_sample(self):
		num_shapes = random.randint(0, len(self.x_positions) * len(self.y_positions))
		shapes = []
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
			shapes.append({'color' : color, 'shape' : shape, 'size' : size, 'x_positions' : x_positions, 'y_positions' : y_positions})
		img = self.visualize_shapes(shapes)
		labels = self.calculate_lables(shapes)
		return shapes, img, labels

	def visualize_shapes(self, shapes):
		background_color = (255,255,255)
		(width,height) = (16 * len(self.x_positions), 16 * len(self.y_positions))
		screen = pygame.display.set_mode((width, height))
		screen.fill(background_colour)
		for shape in shapes:
			if shape['shape'] == 'circle':
				pygame.draw.circle()
			elif shape['shape'] == 'rect':
				pygame.draw.rect()
			elif shape['shape'] == 'triangle':
				pygame.draw.polygon()
		return img

	def calculate_labels(self, shapes):
		return labels
