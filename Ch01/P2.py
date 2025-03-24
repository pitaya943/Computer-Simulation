import sys
import math
import random
#############################################
# Problem 2: M/M/1/K Queue with Blocking
#############################################
class MM1QueueBlocking:
    def __init__(self, arrival_rate, service_rate, capacity, num_arrivals_required):
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.mean_interarrival = 1.0 / arrival_rate
        self.mean_service = 1.0 / service_rate
        self.capacity = capacity
        self.num_arrivals_required = num_arrivals_required

        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0

        self.total_arrivals = 0
        self.num_blocked = 0

        self.time_next_event = [0.0, 0.0, 1.0e+30]
        self.num_events = 2

    def expon(self, mean):
        return -mean * math.log(random.random())

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = 0
        self.num_in_q = 0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.time_last_event = 0.0
        self.total_arrivals = 0
        self.num_blocked = 0

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
        self.total_arrivals += 1
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        current_system_size = 1 if self.server_status == 1 else 0
        current_system_size += self.num_in_q

        if current_system_size >= self.capacity:
            self.num_blocked += 1
            return 0
        else:
            if self.server_status == 1:
                self.num_in_q += 1
            else:
                self.server_status = 1
                self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[2] = 1.0e+30
        else:
            self.num_in_q -= 1
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def run(self):
        self.initialize()
        while self.total_arrivals < self.num_arrivals_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive()
            elif self.next_event_type == 2:
                self.depart()

        blocking_prob = self.num_blocked / self.total_arrivals
        return blocking_prob