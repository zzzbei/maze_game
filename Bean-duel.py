'''
Function:
	吃豆豆小游戏
'''
import os
import sys
import pygame
import Levels


'''定义一些必要的参数'''
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (153, 0, 0)
GREY=(153,153,153)
YELLOW = (204, 153, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 102, 204)
# os.path.join:连接两个或更多的路径名组件;os.getcwd():在Python中可以使用os.getcwd()函数获得当前的路径。
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
ashanPATH = os.path.join(os.getcwd(), 'resources/images/ashan.png')
qiqiPATH = os.path.join(os.getcwd(), 'resources/images/qiqi.png')
panghuPATH = os.path.join(os.getcwd(), 'resources/images/panghu.png')
qingqingPATH = os.path.join(os.getcwd(), 'resources/images/qingqing.png')


'''开始某一关游戏'''
def startLevelGame(level, screen, font):
	# clock=pygame.time.Clock()来定义时钟，调用CPU的时间
	clock = pygame.time.Clock()
	SCORE = 0
	# 设置关卡中的各个元素，如食物、精灵等的颜色之类的
	wall_sprites = level.setupWalls(BLUE)
	gate_sprites = level.setupGate(YELLOW)
	hero_sprites, ghost_sprites = level.setupPlayers(HEROPATH, [ashanPATH, qiqiPATH, panghuPATH, qingqingPATH])
	food_sprites = level.setupFood(YELLOW, WHITE)
	is_clearance = False
	while True:
		# pygame中通过pygame.event.get()获得用户当前所做动作的时间列表，用户可以在同一时间做很多事情
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit(-1)		# sys.exit(-1):有错误退出
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:		# pygame.K_LEFT:左键
					for hero in hero_sprites:
						hero.changeSpeed([-1, 0])		# “-1”表示沿x轴向左一步
						hero.is_move = True
				elif event.key == pygame.K_RIGHT:	 # pygame.K_RIGHT:右键
					for hero in hero_sprites:
						hero.changeSpeed([1, 0])		# ”1“表示沿x轴向右一步
						hero.is_move = True
				elif event.key == pygame.K_UP:		# pygame.K_UP:上键
					for hero in hero_sprites:
						hero.changeSpeed([0, -1])		# ”-1“表示沿y轴向上一步
						hero.is_move = True
				elif event.key == pygame.K_DOWN:	 # pygame.K_DOWN:下键
					for hero in hero_sprites:
						hero.changeSpeed([0, 1])		# ”1“表示沿y轴向下一步
						hero.is_move = True
			if event.type == pygame.KEYUP:
				if (event.key == pygame.K_LEFT) or (event.key == pygame.K_RIGHT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN):
					hero.is_move = False
		screen.fill(BLACK)			# 游戏界面背景色为黑色,若是原本未定义BLACK的RGB，则直接写成screen.fill((0,0,0))亦可
		for hero in hero_sprites:
			hero.update(wall_sprites, gate_sprites)
		hero_sprites.draw(screen)
		for hero in hero_sprites:
			# pygame.sprite.spritecollide()这个函数的第一个参数就是单个精灵-吃豆精灵，第二个参数是精灵组-食物豆，第三个参数是一个bool值，
			# 最后这个参数起了很大的作用。当为True的时候，会删除组中所有冲突的精灵，False的时候不会删除冲突的精灵
			# 此处为True，即发生碰撞，因此这个碰撞检测机制被触动，所以会将发生冲突的精灵即“食物豆”删除掉以实现“豆”被吃掉的效果。
			food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
		# SCORE:分数通过对被吃掉的都的长度进行累加从而实现
		SCORE += len(food_eaten)
		wall_sprites.draw(screen)
		gate_sprites.draw(screen)
		food_sprites.draw(screen)
		for ghost in ghost_sprites:
			if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0:2])
				ghost.tracks_loc[1] += 1
			else:
				if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
					ghost.tracks_loc[0] += 1
				elif ghost.role_name == 'ashan':
					ghost.tracks_loc[0] = 2
				else:
					ghost.tracks_loc[0] = 0
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
				ghost.tracks_loc[1] = 0
			if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
				ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
			else:
				if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
					loc0 = ghost.tracks_loc[0] + 1
				elif ghost.role_name == 'qiqi':
					loc0 = 2
				else:
					loc0 = 0
				ghost.changeSpeed(ghost.tracks[loc0][0: 2])
			ghost.update(wall_sprites, None)
		ghost_sprites.draw(screen)
		score_text = font.render("Score: %s" % SCORE, True, RED)
		screen.blit(score_text, [10, 10])
		if len(food_sprites) == 0:
			is_clearance = True
			break
		if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
			is_clearance = False
			break
		pygame.display.flip()
		clock.tick(10)
	return is_clearance


'''显示文字'''
def showText(screen, font, is_clearance, flag=False):
	clock = pygame.time.Clock()
	msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
	positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
	surface = pygame.Surface((400, 200))
	surface.set_alpha(10)
	surface.fill((128, 128, 128))
	screen.blit(surface, (100, 200))
	texts = [font.render(msg, True,GREY),
			 font.render('Press ENTER to continue or play again.', True, GREY),
			 font.render('Press ESCAPE to quit.', True, GREY)]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if is_clearance:
						if not flag:
							return
						else:
							main(initialize())
					else:
						main(initialize())
				elif event.key == pygame.K_ESCAPE:
					sys.exit()
					pygame.quit()
		for idx, (text, position) in enumerate(zip(texts, positions)):
			screen.blit(text, position)
		pygame.display.flip()
		clock.tick(10)


'''初始化'''
def initialize():
	pygame.init()
	icon_image = pygame.image.load(ICONPATH)
	pygame.display.set_icon(icon_image)
	screen = pygame.display.set_mode([606, 606])
	pygame.display.set_caption('吃豆精灵--19网络工程1班吴家欣--Linux期末大作业')
	return screen


'''主函数'''
def main(screen):
	pygame.mixer.init()			# 初始化混音器模块
	pygame.mixer.music.load(BGMPATH)
	pygame.mixer.music.play(-1, 0.0)
	pygame.font.init()
	font_small = pygame.font.Font(FONTPATH, 18)
	font_big = pygame.font.Font(FONTPATH, 24)
	for num_level in range(1, Levels.NUMLEVELS+1):
		if num_level == 1:
			level = Levels.Level1()
			is_clearance = startLevelGame(level, screen, font_small)
			if num_level == Levels.NUMLEVELS:
				showText(screen, font_big, is_clearance, True)
			else:
				showText(screen, font_big, is_clearance)
	

'''test'''
if __name__ == '__main__':
	main(initialize())