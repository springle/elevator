import unittest
from elevator_control_system import ElevatorControlSystem

class TestElevatorControlSystem(unittest.TestCase):
	def test_init(self):
		"""
		Make sure ElevatorControlSystem correctly initializes with 16 elevators and 16 floors.
		"""
		ecs = ElevatorControlSystem(16, 16)
		self.assertEqual(ecs.status(), [(0, 0, [], [], 0), \
											 (1, 0, [], [], 0), \
											 (2, 0, [], [], 0), \
											 (3, 0, [], [], 0), \
											 (4, 0, [], [], 0), \
											 (5, 0, [], [], 0), \
											 (6, 0, [], [], 0), \
											 (7, 0, [], [], 0), \
											 (8, 0, [], [], 0), \
											 (9, 0, [], [], 0), \
											 (10, 0, [], [], 0), \
											 (11, 0, [], [], 0), \
											 (12, 0, [], [], 0), \
											 (13, 0, [], [], 0), \
											 (14, 0, [], [], 0), \
											 (15, 0, [], [], 0)])

	def test_update_order(self):
		"""
		Make sure several requests are handled correctly by the up_queue.
		Note that this simulation is impractical because the pickup algorithm
			would have distributed people more evenly among the elevators; however,
			it is useful to make sure a single elevator orders several requests
			in the correct order.
		"""
		ecs = ElevatorControlSystem(16, 16)
		ecs.update(0, 5)
		ecs.update(0, 4)
		ecs.update(0, 2)
		ecs.update(0, 8)
		self.assertEqual(ecs.status(), [(0, 0, [2, 5, 4, 8], [], 1), \
										(1, 0, [], [], 0), \
										(2, 0, [], [], 0), \
										(3, 0, [], [], 0), \
										(4, 0, [], [], 0), \
										(5, 0, [], [], 0), \
										(6, 0, [], [], 0), \
										(7, 0, [], [], 0), \
										(8, 0, [], [], 0), \
										(9, 0, [], [], 0), \
										(10, 0, [], [], 0), \
										(11, 0, [], [], 0), \
										(12, 0, [], [], 0), \
										(13, 0, [], [], 0), \
										(14, 0, [], [], 0), \
										(15, 0, [], [], 0)])

	def test_duplicates(self):
		"""
		Make sure no extra effort is wasted on a duplicate request.
		"""
		ecs = ElevatorControlSystem(16, 16)
		ecs.update(1, 5)
		ecs.update(1, 5)
		self.assertEqual(ecs.status(), [(0, 0, [], [], 0), \
										(1, 0, [5], [], 1), \
										(2, 0, [], [], 0), \
										(3, 0, [], [], 0), \
										(4, 0, [], [], 0), \
										(5, 0, [], [], 0), \
										(6, 0, [], [], 0), \
										(7, 0, [], [], 0), \
										(8, 0, [], [], 0), \
										(9, 0, [], [], 0), \
										(10, 0, [], [], 0), \
										(11, 0, [], [], 0), \
										(12, 0, [], [], 0), \
										(13, 0, [], [], 0), \
										(14, 0, [], [], 0), \
										(15, 0, [], [], 0)])

	def test_pickup(self):
		"""
		Make sure the system correctly distributes a set of pickup requests.
		Given the requests below, we check to make sure:
			(1) The system correctly penalizes based on elevator direction
			(2) The individual elevators order requests correctly
			(3) Duplicate requests are consolidated
		"""
		ecs = ElevatorControlSystem(16,16)
		ecs.pickup(5, 1)
		ecs.pickup(5, -1)
		ecs.pickup(4, 1)
		ecs.pickup(5, 1)
		ecs.pickup(6, -1)
		ecs.pickup(4, -1)
		self.assertEqual(ecs.status(), [(0, 0, [4,5], [], 1), \
										(1, 0, [5], [], 1), \
										(2, 0, [6], [], 1), \
										(3, 0, [4], [], 1), \
										(4, 0, [], [], 0), \
										(5, 0, [], [], 0), \
										(6, 0, [], [], 0), \
										(7, 0, [], [], 0), \
										(8, 0, [], [], 0), \
										(9, 0, [], [], 0), \
										(10, 0, [], [], 0), \
										(11, 0, [], [], 0), \
										(12, 0, [], [], 0), \
										(13, 0, [], [], 0), \
										(14, 0, [], [], 0), \
										(15, 0, [], [], 0)])

	def test_step(self):
		"""
		Make sure the simulation actually runs and that elevators drop people off as expected.
		Given the requests below, we check to make sure:
			(1) Each elevator should move 4 floors, since they are all heading up.
			(2) All requests below or on floor 4 should be completed.
			(3) Elevators with now empty queues should have direction 0.
		"""
		ecs = ElevatorControlSystem(16,16)
		ecs.pickup(2, 1)
		ecs.pickup(5, -1)
		ecs.pickup(4, 1)
		ecs.pickup(2, 1)
		ecs.pickup(6, -1)
		ecs.pickup(4, -1)
		ecs.step()
		ecs.step()
		ecs.step()
		ecs.step()
		self.assertEqual(ecs.status(), [(0, 4, [], [], 0), \
										(1, 4, [5], [], 1), \
										(2, 4, [6], [], 1), \
										(3, 4, [], [], 0), \
										(4, 0, [], [], 0), \
										(5, 0, [], [], 0), \
										(6, 0, [], [], 0), \
										(7, 0, [], [], 0), \
										(8, 0, [], [], 0), \
										(9, 0, [], [], 0), \
										(10, 0, [], [], 0), \
										(11, 0, [], [], 0), \
										(12, 0, [], [], 0), \
										(13, 0, [], [], 0), \
										(14, 0, [], [], 0), \
										(15, 0, [], [], 0)])

	def test_turnaround(self):
		"""
		Make sure that the system correctly prioritizes between up_queue and down_queue.
		Given the instructions below, we expect Elevator 0 to complete all of its
			requests within the 6 steps. This is considered optimal given the order
			and timing of the requests. We also expect the elevator to finish on
			floor 2, because it should respect the order of the requests when possible.
		"""
		ecs = ElevatorControlSystem(16,16)
		ecs.pickup(4,1)
		ecs.step()
		ecs.step()
		ecs.step()
		ecs.update(0,2)
		ecs.step()
		ecs.step()
		ecs.step()
		self.assertEqual(ecs.status(), [(0, 2, [], [], 0), \
										(1, 0, [], [], 0), \
										(2, 0, [], [], 0), \
										(3, 0, [], [], 0), \
										(4, 0, [], [], 0), \
										(5, 0, [], [], 0), \
										(6, 0, [], [], 0), \
										(7, 0, [], [], 0), \
										(8, 0, [], [], 0), \
										(9, 0, [], [], 0), \
										(10, 0, [], [], 0), \
										(11, 0, [], [], 0), \
										(12, 0, [], [], 0), \
										(13, 0, [], [], 0), \
										(14, 0, [], [], 0), \
										(15, 0, [], [], 0)])

if __name__ == '__main__':
	unittest.main()
