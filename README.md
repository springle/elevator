# Elevator Coding Challenge

**[Update 1] I added unit tests which can be run with `python3 elevator_control_system_tests.py`.**

**[Update 2] I added a main function with a simulation that continuously makes random requests to the system and prints the status. 
To try this simulation, run `python3 elevator_control_system.py`. Since there is now a main function, interactive mode is less
pretty for the instructions below. For something cleaner, just open up a shell with `python3` and import the system
with `from elevator_control_system import ElevatorControlSystem`.**

## How to Use the Interface

I chose to implement the Elevator Control System in Python. The easiest way to start using it is to clone this repository, then start an interactive Python shell: `python3 -i elevator_control_system.py`.

The main interface is the `ElevatorControlSystem` class, which has a number of useful methods. Create an instance of this class with however many floors and elevators you prefer: `ecs = ElevatorControlSystem(20, 16)` (for 20 floors and 16 elevators)

Run `ecs.status()` for a machine-readable description of the system's status. Its output will be in the form `[(<elevator id>, <current floor>, <up_queue>, <down_queue>, <direction>), ...]`.

Run `ecs.describe()` for a human-readable description of the system's status.

Use the pickup method to submit a request to the system. For example, `ecs.pickup(10, -1)` will submit a request on floor 10 going down.

After submitting a few requests, try using the step method to walk through the simulation. Run `ecs.step()` to move one interval through the simulation. Check the status/description between intervals to see the system working.

## Goals

Design and implement an elevator control system in Python that handles arbirtrary elevators and floors. The interface should:

1. Allow a user to query the state of the elevators
2. Allow an elevator to update its state in the system
3. Allow a user to submit a pickup request
4. Include a time-stepping simulation
5. Optimize ordering of stops in elevator queue
6. Pick the best elevator to handle each new pickup request

## Design Decisions

The most interesting part of this problem was deciding how to handle queued elevator requests. To make my decision regarding which data structures and algorithms to use here, I made a few observations:

1. Once an elevator is moving in a direction with a goal, it is never benificial (to the collective interests of the persons on the elevator) to change directions until it completes that goal. Basically, if an elevator is moving up, it should complete all of its up-queued requests before turning around and handling the down-queued ones.
2. If an elevator is moving in a direction with a goal, but it can complete another goal on its way, this other goal should be completed on the way. For example, consider an elevator that is on floor 6 and headed up to floor 9. If someone requests a dropoff at floor 8, then this elevator should stop at floor 8 before continuing on to floor 9.

Given these considerations, it seemed natural to create two heaps to represent each elevator's queue. A min-heap to represent the elevator's "up-queue", and a max-heap to represent the elevator's "down-queue". An elevator would start out stationary, and start moving in the direction of its first request. It will then continue in that direction, adding all new requests to the appropriate heap as they come in. Once the heap in the current direciton is empty, the elevator will switch directions (or stop if both heaps are empty).

The two-heap implementation is a significant improvmenet on FCFS, because it drastically reduces the amount of time each person needs to spend on an elevator. The maximum amount of time an elevator can take to serve all of its current requests is now reduced to 2k (where k is the number of floors). With FCFS, this maximum time can grow arbitrarily with the number of reqeusts.

Another important part of the elevator control system is deciding which elevator should handle a given request. The approach I took involves calculating a heuristic distance for each elevator, then choosing the optimal one from the system's list. The raw distance from the requested floor to the elevator is a good starting point, but it is also important to take into account both the elevators direction and the requests direction. If these directions are opposite, or if the elevator already passed the requested floor in the given direction, the heuristic distance needs to be increased by a factor of 2 * the elevator's distance to the end of its current queue (the amount of time it will take for the elevator to finish moving in its current direction, and then come back to its current location).

There are a lot of moving pieces in this problem, so there are several places where I would want to improve my implementation given more time. I tried to focus on choosing the best data strutures and algorithms to solve the interesting problems optimally, and I also made sure to spend enough time building a system that would actually function correctly in the simulation. My next steps would be to increase validation of inputs and to add testing to catch potential errors in my implementation and ensure it's behaving as expected.

Please don't hesitate to contact me if you have any questions about my submission or in general! I really enjoyed working on this problem, and I look forward to discussion my implementation and getting feedback.
