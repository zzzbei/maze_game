'''
Function:
	定义一些精灵类
'''
import random
import pygame


'''墙类'''
# 在pygame.sprite模块中包含了一个名为Sprite类，它是pygame本身自带的一个精灵。
# 由于这个类的功能比较少，因此我们需要新建一个类对其继承，在sprite类的基础上丰富，以便我们使用。
class Wall(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, **kwargs):
		pygame.sprite.Sprite.__init__(self)
		# pygame.Surface是pygame中用于表示图像的对象
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		# rect = img.get_rect()是将rect对象存储到rect变量中
		self.rect = self.image.get_rect()
		# rect.left与rect.top固定矩形的位置，rect是用于存储矩形坐标的pygame对象
		self.rect.left = x
		self.rect.top = y


'''食物类'''
class Food(pygame.sprite.Sprite):
	def __init__(self, x, y, width, height, color, bg_color, **kwargs):
		pygame.sprite.Sprite.__init__(self)			# init、__init__初始化作用
		self.image = pygame.Surface([width, height])
		# 对图片着色
		self.image.fill(bg_color)
		#  image.set_colorkey:设置图片颜色值
		self.image.set_colorkey(bg_color)
		# pygame.draw.ellipse:根据限定矩形绘制一个椭圆形，ellipse
		pygame.draw.ellipse(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y


'''角色类'''
class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, role_image_path):
		pygame.sprite.Sprite.__init__(self)
		# python split()通过指定分隔符对字符串进行切片，如果参数num有指定值，则仅分隔num个子字符串。
		self.role_name = role_image_path.split('/')[-1].split('.')[0]
		# pygame.image.load(图片),加载图片，convert()转换图片类型
		self.base_image = pygame.image.load(role_image_path).convert()
		# 对当前 Surface 对象进行拷贝，返回的 Surface 对象拥有相同的像素格式、调色板和透明度设置。
		self.image = self.base_image.copy()
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.prev_x = x
		self.prev_y = y
		self.base_speed = [30,30]
		self.speed = [0, 0]
		self.is_move = False
		self.tracks = []
		self.tracks_loc = [0, 0]
	'''改变速度方向'''
	def changeSpeed(self, direction):
		if direction[0] < 0:
			# pygame.transform.flip(img,True,False),img为需要翻转的图像,True为水平翻转的布尔值,False为垂直翻转的布尔值
			# pygame.transform.flip():对图像进行水平和垂直翻转。
			self.image = pygame.transform.flip(self.base_image, True, False)
		elif direction[0] > 0:
			self.image = self.base_image.copy()
		elif direction[1] < 0:
			# pygame.transform.rotate刻度盘翻转
			self.image = pygame.transform.rotate(self.base_image, 90)
		elif direction[1] > 0:
			self.image = pygame.transform.rotate(self.base_image, -90)
		self.speed = [direction[0] * self.base_speed[0], direction[1] * self.base_speed[1]]
		return self.speed
	'''更新角色位置'''
	def update(self, wall_sprites, gate_sprites):
		if not self.is_move:
			return False
		x_prev = self.rect.left
		y_prev = self.rect.top
		self.rect.left += self.speed[0]
		self.rect.top += self.speed[1]
		# pygame.sprite.spritecollide()这个函数的第一个参数就是单个精灵，第二个参数是精灵组-墙，第三个参数是一个bool值，
		# 最后这个参数起了很大的作用。当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
		is_collide = pygame.sprite.spritecollide(self, wall_sprites, False)
		if gate_sprites is not None:
			if not is_collide:
				is_collide = pygame.sprite.spritecollide(self, gate_sprites, False)
		if is_collide:
			self.rect.left = x_prev
			self.rect.top = y_prev
			return False
		return True
	'''生成随机的方向'''
	# random模块在python中起到的是生成随机数的作用
	# random模块中choice()可以从序列中获取一个随机元素，并返回一个（列表，元组或字符串中的）随机项。
	def randomDirection(self):
		return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])
	# return random.choice([[-0.5, 0], [0.5, 0], [0, 0.5], [0, -0.5]])/return random.choice()