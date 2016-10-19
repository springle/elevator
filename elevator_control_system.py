class ElevatorControlSystem():
	def __init__(self, number_of_floors, number_of_elevators):
		self.elevators = [Elevator(i) for i in range(number_of_elevators)]
		self.number_of_floors = number_of_floors
		self.pending_requests = []

	def status(self):
		# returns the status of all elevators in the system (id, floor #, goal floor #)
		return [(e.id, e.current_floor_number, e.goal_floor_number) for e in self.elevators]

	def update(self, elevator_id, floor_number, goal_floor_number):
		# updates the state of an elevator in the system
		e = self.elevators[elevator_id]
		e.current_floor_number = floor_number
		e.goal_floor_number = goal_floor_number

	def pickup(self, floor_number, direction):
		# submits a pickup request to the system
		pass

	def step(self):
		# moves through one interval in the simulation
		for e in self.elevators:
			e.step()
		return self.status()

class Elevator():
	def __init__(self, elevator_id):
		# new elevators are installed on the first floor
		self.id = elevator_id
		self.current_floor_number = 0
		self.goal_floor_number = 0

	def get_direction(self):
		# returns 1 moving up, -1 if moving down, 0 if still
		distance = self.goal_floor_number - self.current_floor_number
		return distance if distance == 0 else distance // abs(distance)

	def step(self):
		self.current_floor_number += self.get_direction()
