#cal_heuristic 그냥 position base로 바꾸기 

import random
import copy
from collections import deque

MAX_TRY = 50

# 랜덤한 포지션 리턴
def get_random_position(n):
	random_position = []
	for i in range(n):
		random_position.append(random.randrange(n))
	return random_position

# position에 대한 heuristic 리턴 - 포지션 이용.
def cal_heuristic(n, position):
	h = 0
	for i in range(n):
		y = position[i]
		right_up = y
		right_next = y
		right_down = y
		for j in range(i+1, n):
			right_up += -1
			right_down += 1
			if right_up >= 0 and right_up == position[j]:
				h+=1
			if right_next == position[j]:
				h+=1
			if right_down < n and right_down == position[j]:
				h+=1
	return h

def bfs(n):
	position_queue = deque()
	position = []
	position_queue.append(copy.copy(position))

	while position_queue:
		p = position_queue.popleft()

		#end check
		if len(p) == n and cal_heuristic(n,p) == 0:
			for i in range(n):
				p[i] += 1
			return print(p)

		for i in range (n):
			tmp = copy.copy(p)
			tmp.append(i)
			position_queue.append(copy.copy(tmp))
			
def hc(n):
	position=[]
	for i in range(MAX_TRY):
		# get random position
		position = get_random_position(n)

		# 루프
		min = 9999
		min_position = []
		while True:
			current_heuristic = cal_heuristic(n,position)
			min = 9999
			min_position = copy.copy(position)

			# 휴리스틱 맵 계산
			tmp_position =[]
			for x in range(n):
				tmp_position = copy.copy(position)
				for y in range(n):
					tmp_position[x] = y
					weight = cal_heuristic(n,tmp_position)
					if min > weight:
						min = weight
						min_position = copy.copy(tmp_position)

			# Case: 휴리스틱이 최소인 포지션 0이면 리턴
			if min == 0:
				for i in range(n):
					min_position[i]+=1
				return print(min_position)


			# 만약 현재 휴리스틱이랑 최소 값 휴리스틱이 같다면 Local Optimal. 탈출 
			if current_heuristic == min:
				break;

			# 최소 값으로
			position = copy.copy(min_position)

def csp(n):
	#Phase 01: 
	#각 칼럼당 가능한 변수 초기화 
	legal_variables = []
	for i in range(n):
		legal_variables.append(i)
	col_containers = []
	for i in range(n):
		col_containers.append(copy.copy(legal_variables))
	
	#Phase 02: Forward Checking
	print(forward_check(n,[],col_containers, 0))
	

def forward_check(n, positions, col_containers, i):
	# 끝 도달, no empty, 포지션 리턴 
	if i == n:
		return positions

	# 해당 index의 퀸 위치 선정
	for queen_position in col_containers[i]:
		print("i,queen:",i,queen_position)
		current_positions = copy.copy(positions)
		current_col_containers = copy.deepcopy(col_containers)

		#현재 column의 퀸 위치 선정
		current_positions.append(queen_position+1)
		
		#해당 위치에 따른 불가능한 포지션 삭제
		right_up = queen_position
		right_next = queen_position
		right_down = queen_position
		for j in range(i+1, n):
			right_up += -1
			right_down += 1
			if right_up >= 0 and right_up in current_col_containers[j]:
				current_col_containers[j].remove(right_up)
			if right_next in current_col_containers[j]:
				current_col_containers[j].remove(right_next)
			if right_down < n and right_down in current_col_containers[j]:
				current_col_containers[j].remove(right_down)

		# empty check
		if is_empty(current_col_containers):
			continue
		
		current_positions = forward_check(n, current_positions ,current_col_containers, i+1)
		if len(current_positions) == n:
			return current_positions
	return positions

def is_empty(containers):
	for i in containers:
		if len(i) == 0:
			return True
	return False

def main():
	hc(5)

"""
def main():
	f = open("input.txt",'r')
	lines = f.readlines()
	f.close()

	for query in lines:
		n = query.split()[0]
		search = query.split()[1]

		if search == "bfs":
			bfs(n)
		elif search == "hc":
			hc(n)
		elif search == "csp":
			csp(n)
		else:
			print("error")
"""	

if __name__ == "__main__":
	main()