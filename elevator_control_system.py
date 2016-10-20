import heapq

class ElevatorControlSystem():
	def __init__(self, number_of_floors, number_of_elevators):
		if number_of_elevators <= 0:
			raise AssertionError("Your building must have at least one elevator.")
		if number_of_floors <= 0:
			raise AssertionError("Your building must have at least one floor.")
		self.elevators = [Elevator(i) for i in range(number_of_elevators)]
		self.number_of_floors = number_of_floors
		self.pending_requests = []

	def status(self):
		# returns the status of all elevators in the system (id, floor #, goal floor #)
		return [(e.id, e.current_floor, e.up_queue, e.down_queue, e.direction) for e in self.elevators]

	def describe(self):
		for e in self.elevators:
			print(e)

	def update(self, elevator_id, floor_number):
		# updates the state of an elevator in the system, adding a floor to its queue
		e = self.elevators[elevator_id]
		e.add_to_queue(floor_number)

	def pickup(self, floor_number, direction):
		# submits a pickup request to the system
		best_elevator = self.elevators[0]
		best_distance = self.number_of_floors * 2
		for e in self.elevators:
			distance = abs(e.current_floor - floor_number)

			# penalize elevator scores based on direction
			if (e.direction > 0 and floor_number < e.current_floor) or (e.direction > 0 and direction < 0):
				highest_stop = heapq.nlargest(1, e.up_queue)[0]
				distance += 2 * highest_stop
			elif (e.direction < 0 and floor_number > e.current_floor) or (e.direction < 0 and direction > 0):
				lowest_stop = heapq.nsmallest((1, e.down_queue))[0]
				distance += 2 * lowest_stop

			if distance < best_distance:
				best_elevator = e
				best_distance = distance
		best_elevator.add_to_queue(floor_number)

	def step(self):
		# moves through one interval in the simulation
		for e in self.elevators:
			e.step()

class Elevator():
	def __init__(self, elevator_id):
		self.id = elevator_id
		self.current_floor = 0
		self.direction = 0 # 1 for moving up, -1 for moving down, 0 for stationary
		self.up_queue = [] # heap
		self.down_queue = [] # heap

	def step(self):
		self.current_floor += self.direction
		self.drop_off()
		self.update_direction()

	def drop_off(self):
		if self.up_queue and self.current_floor == self.up_queue[0]:
			heapq.heappop(self.up_queue)
			print("Elevator " + str(self.id) + " stopping on floor " + str(self.current_floor))
		elif self.down_queue and self.current_floor == abs(self.down_queue[0]):
			heapq.heappop(self.down_queue)
			print("Elevator " + str(self.id) + " stopping on floor " + str(self.current_floor))

	def update_direction(self):
		if self.direction > 0 and not self.up_queue:
			self.direction = -1 if self.down_queue else 0
		if self.direction < 0 and not self.down_queue:
			self.direction = 1 if self.up_queue else 0

	def add_to_queue(self, floor_number, direction=0):
		if floor_number == self.current_floor:
			print("Elevator " + str(self.id) + " stopping on floor " + str(floor_number))
		elif floor_number > self.current_floor:
			if floor_number not in self.up_queue:
				heapq.heappush(self.up_queue, floor_number)
			if not self.direction:
				self.direction = 1
		else:
			if floor_number not in self.down_queue:
				heapq.heappush(self.down_queue, -floor_number)
			if not self.direction:
				self.direction = -1

	def __str__(self):
		return "Elevator " + str(self.id) \
							+ " is on floor " \
							+ str(self.current_floor) \
							+ " going in direction " \
							+ str(self.direction) \
							+ " with up_queue " \
							+ str(self.up_queue) \
							+ " and down_queue " \
							+ str(self.down_queue) \
							+ "."
