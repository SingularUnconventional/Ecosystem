import os
import sys
import time
import pygame
import numpy as np

Ecosystem_size = (100, 100)
Grid_size = 10

Ecosystem_img = []

Grid = [[[] for _ in range(int(Ecosystem_size[0]/Grid_size))]for _ in range(int(Ecosystem_size[1]/Grid_size))]

Creatures = []
Creatures = [
	[10, 0, 1, 0, [0, 0], 2, 3, 10],
	[10, 0, 1, 0, [0, 0], 9, 3, 10],
	[10, 0, 2, 0, [0, 0], 12, 10, 10],
	[10, 0, 2, 0, [0, 0], 30, 30, 10],
]

'''
0 총 에너지량
1 속도

2 영양단계
3 종 값

4 그리드 상의 위치
5 위치_X
6 위치_Y
7 현제 에너지량
'''
clock = pygame.time.Clock()
while True:
	#clock.tick(32)
	input()
	Ecosystem_img = [[0 for _ in range(Ecosystem_size[0])] for _ in range(Ecosystem_size[1])]
	Grid = [[None for _ in range(int(Ecosystem_size[0]/Grid_size))]for _ in range(int(Ecosystem_size[1]/Grid_size))]
	# start = time.time()
	# print("time :", time.time() - start)

	for Creature in Creatures:
		Grid_ = []
		for x in [-1, 0, 1]: 
			for y in [-1, 0, 1]: 
				if Grid[Creature[4][0]+x][Creature[4][1]+y]: Grid_ += [Grid[Creature[4][0]+x][Creature[4][1]+y]]
		target_length
		try:
			X_list = [i[5] for i in Grid_]
			Y_list = [i[6] for i in Grid_]
		
			target_Creature = Grid_[np.argmin(np.power(np.add(X_list, -Creature[5]), 2)
											+ np.power(np.add(Y_list, -Creature[6]), 2))]

			target_length = (target_Creature[5] -Creature[5])**2 + (target_Creature[6] -Creature[6])**2
			target_angle = np.atan2(target_Creature[5] -Creature[5], (target_Creature[6] -Creature[6])) 
			
			ntrition_stages_v = target_Creature[2] - Creature[2]
			if ntrition_stages_v < 0:
				Creature[5] = np.cos(target_angle) * Creature[1]
				Creature[6] = np.sin(target_angle) * Creature[1]
			if ntrition_stages_v > 0:
				Creature[5] = np.cos(target_angle) * Creature[1] *(-1)
				Creature[6] = np.sin(target_angle) * Creature[1] *(-1)
			else:
				if target_Creature[0] > (Creature[0]/2):
					Creature[5] = np.cos(target_angle) * Creature[1]
					Creature[6] = np.sin(target_angle) * Creature[1]
				else:
					Creature[5] = np.cos(target_angle) * Creature[1] *(-1)
					Creature[6] = np.sin(target_angle) * Creature[1] *(-1)
		except ValueError: pass

		Ecosystem_img[int(Creature[5])][int(Creature[6])] = Creature[2]
		Grid[int(Creature[5]/Grid_size)][int(Creature[6]/Grid_size)] = Creature
		
		
	os.system('cls')
	print(target_length)
	for y in Ecosystem_img:
		for x in y: print(x,end=' ')
		print()