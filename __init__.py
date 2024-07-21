import os
import sys
import time
import pygame
import numpy as np

Ecosystem_size = (1000, 1000)
Grid_size = 20

Color = [
	[(44,58,44)],
	[(223,174,220), (223,174,174), (223,174,206), (223,174,191)],
	[(118,164,213), (118,135,213), (137,118,213), (161,118,213)],
	[(135,185,49), (67,185,49), (49,185,85), (49,185,133)],
	[(155,42,42), (105,51,22), (0, 0, 0), (0, 0, 0)],
]

Ecosystem_img = []

Creatures = []

for _ in range(10000): Creatures.append([200, 0, 1, 1, 
										[0, 0], 
										[np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 
										200, 
										Color[0][0], 1])
	
for _ in range(2000): 
	tribe = np.random.randint(0, 2)
	Creatures.append([500, np.random.normal(1.0,1.5), 
					2, 
					tribe, 
					[0, 0], 
					[np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 
					300, 
					Color[1][tribe], 1])
	
for _ in range(2000): 
	tribe = np.random.randint(0, 2)
	Creatures.append([500, np.random.normal(1.0,1.5), 
					3, 
					tribe, 
					[0, 0], 
					[np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 
					400, 
					Color[3][tribe], 1])
	
for _ in range(100): 
	tribe = 0#np.random.randint(0, 1)
	Creatures.append([500, np.random.normal(0.5,1.0), 
					4, 
					tribe, 
					[0, 0], 
					[np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 
					500, 
					Color[4][tribe], 1])


'''
0 총 에너지량
1 속도

2 영양단계
3 종 값

4 그리드 상의 위치
5 위치_
6 현제 에너지량

7 색상

8 노화

각 영양단계당 에너지 충분 개체, 에너지 부족 개체
'''
screen = pygame.display.set_mode(Ecosystem_size)
scroll = 1
clock = pygame.time.Clock()
mouse_pos = (0, 0)

while True:
	#clock.tick(10)

	screen.fill((0, 0, 0))
	screen_ = pygame.PixelArray(screen)
	
	for _ in range(60): Creatures.append([200, 0, 1, 1, 
										[0, 0], 
										[np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 
										200, 
										Color[0][0], 1])

	Ecosystem_img = [[0 for _ in range(Ecosystem_size[0])] for _ in range(Ecosystem_size[1])]
	Grid = [[[[[], []] for _ in range(4)] for _ in range(int(Ecosystem_size[0]/Grid_size))]for _ in range(int(Ecosystem_size[1]/Grid_size))]

	for Creature in Creatures:
		Creature[4] = [int(Creature[5][0]/Grid_size), int(Creature[5][1]/Grid_size)]
		for x in [-1, 0, 1]: 
			for y in [-1, 0, 1]:
				try:
					Grid[int(Creature[5][0]/Grid_size)+x][int(Creature[5][1]/Grid_size)+y][Creature[2]-1][int(np.around(Creature[6]/Creature[0]))].append(Creature)
				except: pass
	# start = time.time()
	# print("time :", time.time() - start)

	for Creature in Creatures:
		if Creature[2] != 1: 
			Grid_index = Grid[Creature[4][0]][Creature[4][1]]

			Grid_ = Grid_index[Creature[2]-2][0] + Grid_index[Creature[2]-2][1]

			if Creature[6] > Creature[0]/2: Grid_ += Grid_index[Creature[2]-1][1]

			try: Grid_ += Grid_index[Creature[2]][0] + Grid_index[Creature[2]][1]
			except IndexError: pass

			if Creature in Grid_:
				Grid_.remove(Creature)

			if Grid_ != []:
				X_list = [i[5][0] for i in Grid_]
				Y_list = [i[5][1] for i in Grid_]
				
				target_Creature = Grid_[np.argmin(np.power(np.add(X_list, -Creature[5][0]), 2)
												+ np.power(np.add(Y_list, -Creature[5][1]), 2))]

				target_length = (target_Creature[5][0] -Creature[5][0])**2 + (target_Creature[5][1] -Creature[5][1])**2
				target_angle = np.atan2(target_Creature[5][0] -Creature[5][0], target_Creature[5][1] -Creature[5][1]) 
				
				ntrition_stages_v = target_Creature[2] - Creature[2]
				if ntrition_stages_v == -1:
					if target_length < Creature[1]: 
						if target_Creature in Creatures:
							Creatures.remove(target_Creature)
							Creature[6] += target_Creature[6]*0.9
							if Creature[6] > Creature[0]: Creature[6] = Creature[0]
					else:
						Creature[5][0] += np.sin(target_angle) * Creature[1] * Creature[8]
						Creature[5][1] += np.cos(target_angle) * Creature[1] * Creature[8]
						
				elif ntrition_stages_v == 1:
					Creature[5][0] += np.sin(target_angle) * -Creature[1] * Creature[8]
					Creature[5][1] += np.cos(target_angle) * -Creature[1] * Creature[8]
				else:
					if Creature[3] == target_Creature[3]:
						if target_length < Creature[1]: 
							Creature[6] /= 2
							target_Creature[6] /= 2
							Creature[5][0] -= 1
							ENG = np.random.choice([Creature[0], target_Creature[0]])
							SPEED = np.random.choice([Creature[1], target_Creature[1]])

							Creatures.append(
								[np.random.choice([ENG, ENG+np.random.randint(-30, 30)], p=[0.75,0.25]), 
								np.random.choice([SPEED, SPEED+np.random.normal(0, 0.01)], p=[0.75,0.25]), 
								Creature[2], Creature[3], [0, 0], 
								[Creature[5][0], Creature[5][1]-1], 
								Creature[6]+target_Creature[6], Creature[7], 1])
						else:
							Creature[5][0] += np.sin(target_angle) * Creature[1] * Creature[8]
							Creature[5][1] += np.cos(target_angle) * Creature[1] * Creature[8]
					else:
						Creature[5][0] += np.sin(target_angle) * -Creature[1] * Creature[8]
						Creature[5][1] += np.cos(target_angle) * -Creature[1] * Creature[8]
			else:
				Creature[5][0] += np.sin(np.random.normal(0, 3.14)) * Creature[1] * Creature[8]
				Creature[5][1] += np.cos(np.random.randint(0, 3.14)) * Creature[1] * Creature[8]

			Creature[5][0] %= Ecosystem_size[0]-1
			Creature[5][1] %= Ecosystem_size[1]-1

		#Ecosystem_img[int(Creature[5][0])][int(Creature[5][1])] = Creature[2]
		screen_[int(Creature[5][0]), int(Creature[5][1])] = Creature[7]
		
		if Creature[6] < 0: Creatures.remove(Creature)
		Creature[6] -= Creature[1]**2
		Creature[8] *= 0.99
		
	# os.system('cls')
	# #print(target_length)

	# for y in Ecosystem_img:
	# 	for x in y: 
	# 		if x == 0: print(' ',end=' ')
	# 		else: print(x,end=' ')
	# 	print()
	pygame.PixelArray.close(screen_)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 5:
				if scroll > 1:
					scroll *= 0.8
					mouse_pos = (-(pygame.mouse.get_pos()[0]-mouse_pos[0])*(scroll-1)/(scroll/0.8), -(pygame.mouse.get_pos()[1]-mouse_pos[1])*(scroll-1)/(scroll/0.8))
			elif event.button == 4:
				if scroll < 5:
					scroll *= 1.2
					mouse_pos = (-(pygame.mouse.get_pos()[0]-mouse_pos[0])*(scroll-1)/(scroll/1.2), -(pygame.mouse.get_pos()[1]-mouse_pos[1])*(scroll-1)/(scroll/1.2))

		if event.type == pygame.MOUSEMOTION:
			if event.buttons[0] == 1:
				mouse_pos = (mouse_pos[0]+event.rel[0], mouse_pos[1]+event.rel[1])
			
	zoomedScreen = pygame.transform.rotozoom(screen, 0, scroll)
	screen.fill((0, 0, 0))
	screen.blit(zoomedScreen, mouse_pos)

	pygame.display.update()
	