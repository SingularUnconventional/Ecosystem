import os
import sys
import time
import pygame
import numpy as np

Ecosystem_size = (30, 30)
Grid_size = 5

Ecosystem_img = []

Grid = [[[] for _ in range(int(Ecosystem_size[0]/Grid_size))]for _ in range(int(Ecosystem_size[1]/Grid_size))]

Creatures = []

Creatures = [[1000, np.random.randint(1,3), np.random.randint(2, 5), 0, [0, 0], [np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 1000] for _ in range(10)]

'''
0 총 에너지량
1 속도

2 영양단계
3 종 값

4 그리드 상의 위치
5 위치_
6 현제 에너지량
'''
image_bg = pygame.image.load('./image.png')
print(list(image_bg))

clock = pygame.time.Clock()
while True:
	Creatures.append([500, 0, 1, 1, [0, 0], [np.random.randint(Ecosystem_size[0]), np.random.randint(Ecosystem_size[1])], 500])

	#clock.tick(32)
	input()
	Ecosystem_img = [[0 for _ in range(Ecosystem_size[0])] for _ in range(Ecosystem_size[1])]
	Grid = [[[] for _ in range(int(Ecosystem_size[0]/Grid_size))]for _ in range(int(Ecosystem_size[1]/Grid_size))]

	for Creature in Creatures:
		Creature[4] = [int(Creature[5][0]/Grid_size), int(Creature[5][1]/Grid_size)]
		for x in [-1, 0, 1]: 
			for y in [-1, 0, 1]:
				try:
					Grid[int(Creature[5][0]/Grid_size)+x][int(Creature[5][1]/Grid_size)+y].append(Creature)
				except: pass
	# start = time.time()
	# print("time :", time.time() - start)

	for Creature in Creatures:
		Grid_ = Grid[Creature[4][0]][Creature[4][1]]
		try:
			Grid_.remove(Creature)

			X_list = [i[5][0] for i in Grid_]
			Y_list = [i[5][1] for i in Grid_]
			
			target_Creature = Grid_[np.argmin(np.power(np.add(X_list, -Creature[5][0]), 2)
											+ np.power(np.add(Y_list, -Creature[5][1]), 2))]

			target_length = (target_Creature[5][0] -Creature[5][0])**2 + (target_Creature[5][1] -Creature[5][1])**2
			target_angle = np.atan2(target_Creature[5][0] -Creature[5][0], target_Creature[5][1] -Creature[5][1]) 
			
			ntrition_stages_v = target_Creature[2] - Creature[2]
			if ntrition_stages_v == -1:
				if target_length < Creature[1]: 
					Creature[6] += target_Creature[6]*0.9
					if Creature[6] > Creature[0]: Creature[6] = Creature[0]

					Creatures.remove(target_Creature)
				else:
					Creature[5][0] += np.cos(target_angle) * Creature[1]
					Creature[5][1] += np.sin(target_angle) * Creature[1]
			if ntrition_stages_v == 1:
				Creature[5][0] += np.cos(target_angle) * Creature[1] *(-1)
				Creature[5][1] += np.sin(target_angle) * Creature[1] *(-1)
			else:
				if Creature[3] == target_Creature[3] and Creature[6] > Creature[0]/2 and target_Creature[6] > Creature[0]/2:
					if target_length < Creature[1]: 
						Creature[6] /= 2
						target_Creature[6] /= 2
						Creatures.append([1000, np.random.randint(1,3), Creature[2], Creature[3], [0, 0], [Creature[5][0]+0.1, Creature[5][1]+0.1], Creature[6]+target_Creature[6]])
					else:
						Creature[5][0] += np.cos(target_angle) * Creature[1]
						Creature[5][1] += np.sin(target_angle) * Creature[1]
				else:
					Creature[5][0] += np.cos(target_angle) * Creature[1] *(-1)
					Creature[5][1] += np.sin(target_angle) * Creature[1] *(-1)
		except ValueError:print(Creature)

		Creature[5][0] %= Ecosystem_size[0]-1
		Creature[5][1] %= Ecosystem_size[1]-1
		Ecosystem_img[int(Creature[5][0])][int(Creature[5][1])] = Creature[2]
		
		if Creature[6] < 0: Creatures.remove(Creature)
		Creature[6] -= Creature[1]
		
	#os.system('cls')
	#print(target_length)


	# for y in Ecosystem_img:
	# 	for x in y: 
	# 		if x == 0: print(' ',end=' ')
	# 		else: print(x,end=' ')
	# 	print()
	clock.tick(64)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
	