import sys
import math
import random
#############################################
# Problem 1: M/M/1 Queue Simulation
#############################################
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedListQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1

    def dequeue(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return data

    def __len__(self):
        return self.size

# Array for M/M/1
class MM1QueueArray:
    def __init__(self, arrival_rate, service_rate, num_delays_required):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.mean_interarrival = 1.0 / arrival_rate
        self.mean_service = 1.0 / service_rate
        self.num_delays_required = num_delays_required

        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.num_custs_delayed = 0       

        self.q_limit = 100
        self.time_arrival = [0.0] * (self.q_limit + 1)

        self.time_next_event = [0.0, 0.0, 1.0e+30]
        self.num_events = 2

    def expon(self, mean):
        return -mean * math.log(random.random())

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_last_event = 0.0

        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        self.time_next_event[2] = 1.0e+30

    def timing(self):
        min_time_next_event = min(self.time_next_event[1:self.num_events+1])
        self.next_event_type = self.time_next_event.index(min_time_next_event)
        if self.next_event_type == 0:
            print(f"Event list empty at time {self.sim_time}")
            sys.exit(1)
        self.sim_time = min_time_next_event

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time
        self.area_num_in_q += self.num_in_q * time_since_last_event
        self.area_server_status += self.server_status * time_since_last_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        if self.server_status == 1:
            self.num_in_q += 1
            if self.num_in_q > self.q_limit:
                print("Overflow of time_arrival array at time", self.sim_time)
                sys.exit(2)
            self.time_arrival[self.num_in_q] = self.sim_time
        else:
            delay = 0.0
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.server_status = 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[2] = 1.0e+30
        else:
            self.num_in_q -= 1
            delay = self.sim_time - self.time_arrival[1]
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)
            
            for i in range(1, self.num_in_q + 1):
                self.time_arrival[i] = self.time_arrival[i+1]

    def run(self):
        self.initialize()
        while self.num_custs_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()
        avg_delay = self.total_of_delays / self.num_custs_delayed
        avg_num_in_q = self.area_num_in_q / self.sim_time
        return avg_delay, avg_num_in_q

# LinkedList for M/M/1
class MM1QueueLinked:
    def __init__(self, arrival_rate, service_rate, num_delays_required):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.mean_interarrival = 1.0 / arrival_rate
        self.mean_service = 1.0 / service_rate
        self.num_delays_required = num_delays_required

        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.num_custs_delayed = 0

        self.queue = LinkedListQueue()

        self.time_next_event = [0.0, 0.0, 1.0e+30]
        self.num_events = 2

    def expon(self, mean):
        return -mean * math.log(random.random())

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.num_custs_delayed = 0
        self.total_of_delays = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_last_event = 0.0
        self.queue = LinkedListQueue()

        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        self.time_next_event[2] = 1.0e+30

    def timing(self):
        min_time_next_event = min(self.time_next_event[1:self.num_events+1])
        self.next_event_type = self.time_next_event.index(min_time_next_event)
        if self.next_event_type == 0:
            print("Event list empty at time", self.sim_time)
            sys.exit(1)
        self.sim_time = min_time_next_event

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time
        self.area_num_in_q += self.num_in_q * time_since_last_event
        self.area_server_status += self.server_status * time_since_last_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        if self.server_status == 1:
            self.num_in_q += 1
            self.queue.enqueue(self.sim_time)
        else:
            delay = 0.0
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.server_status = 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[2] = 1.0e+30
        else:
            self.num_in_q -= 1
            arrival_time = self.queue.dequeue()
            delay = self.sim_time - arrival_time
            self.total_of_delays += delay
            self.num_custs_delayed += 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def run(self):
        self.initialize()
        while self.num_custs_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()
        avg_delay = self.total_of_delays / self.num_custs_delayed
        avg_num_in_q = self.area_num_in_q / self.sim_time
        return avg_delay, avg_num_in_q