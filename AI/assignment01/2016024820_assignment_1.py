import random
import copy

MAX_TRY = 50

class chess_map:
	def __init__(self,n):
		self.n = int(n)

	# 랜덤한 포지션 리턴
	def get_random_position(self):
		random_position = []
		for i in range(self.n):
			random_position.append(random.randrange(1,self.n+1))
		return random_position

	# 주어진 퀸의 위치에 대한 heuristic 리턴.
	def cal_heuristic(self, position):
		chess_map = [[0 for col in range(self.n)] for row in range(self.n)]
		for i in range (self.n):
			x = position[i] - 1
			y = i
			chess_map[x][i] = 1

		#왼쪽 col부터 하나씩 서치.
		h = 0
		for x in range (self.n):
			for y in range (self.n):
				if chess_map[y][x] != 1:
					continue
				#현재 col의 체스가 오른쪽으로 이동 할 때 잡을 수 있는 말의 수
				i = x
				while True:
					i+=1
					if i >= self.n:
						break
					if chess_map[y][i] == 1:
						h+=1;

				#현재 col의 체스가 오른쪽 대각선 위로 이동 할 때 잡을 수 있는 말의 수
				i = x
				j = y
				while True:
					i -= 1
					j += 1
					if i < 0 or j >= self.n:
						break
					if chess_map[j][i] == 1:
						h+=1;

				#현재 col의 체스가 오른쪽 대각선 아래로 이동 할 때 잡을 수 있는 말의 수
				i = x
				j = y 
				while True:
					i += 1
					j += 1
					if i >= self.n or j >= self.n:
						break
					if chess_map[j][i] == 1:
						h+=1;
		return h

	def get_n(self):
		return self.n

def bfs(n):
	print("bfs")
	

def hc(n):
	hc_calculator = chess_map(n)

	for i in range(1,MAX_TRY+1):
		print (i,"번째 TRY")
		# get random position
		position = hc_calculator.get_random_position()

		# 루프
		min = 9999
		min_position = []
		while True:
			current_heuristic = hc_calculator.cal_heuristic(position)
			min = 9999
			min_position = copy.copy(position)

			# 휴리스틱 맵 계산
			tmp_position =[]
			heuristic_map = [[0 for col in range(n)] for row in range(n)]
			for x in range(n):
				tmp_position = copy.copy(position)
				for y in range(n):
					tmp_position[x] = y+1
					weight = hc_calculator.cal_heuristic(tmp_position)
					heuristic_map[y][x] = weight
					if min > weight:
						min = weight
						min_position = copy.copy(tmp_position)

			# Case: 휴리스틱이 최소인 포지션 0이면 리턴
			if min == 0:
				return min_position

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
			right_next += 1
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
		if len(current_positions) == 4:
			return current_positions
	return positions

def is_empty(containers):
	for i in containers:
		if len(i) == 0:
			return True
	return False

def main():
	csp(4)

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