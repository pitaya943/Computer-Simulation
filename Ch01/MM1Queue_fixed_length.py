# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1obvoFs3K9tbTkSdjeVTfsoI1rY1OAP4g

Github for Computer Simulation's DEMO is located at
    https://github.com/pitaya943/Computer-Simulation2025/tree/main
"""

import sys
import math
import random

class MM1Queue:
    def __init__(self, mean_interarrival, mean_service, time_end):
        # Initialize parameters
        self.mean_interarrival = mean_interarrival
        self.mean_service = mean_service
        self.time_end = time_end

        # Simulation control variables
        self.sim_time = 0.0
        self.num_custs_delayed = 0
        self.num_in_q = 0
        self.server_status = 0  # 0 = IDLE, 1 = BUSY
        self.q_limit = 100
        self.num_events = 3

        # Statistical accumulators
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.total_of_delays = 0.0
        self.time_last_event = 0.0

        # Event lists
        self.time_arrival = [0.0] * (self.q_limit + 1)
        self.time_next_event = [0.0, 0.0, 1.0e+30, self.time_end]

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

        # First arrival event
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)
        # Since no customers are present, the departure event is eliminated from consideration.
        self.time_next_event[2] = 1.0e+30
        # The end simulation event (type 3) is scheduled for time time_end
        self.time_next_event[3] = self.time_end

    def timing(self):
        # Find the event is closest from now
        min_time_next_event = min(self.time_next_event[1:self.num_events + 1])

        # Check next event is ARRIVE or DEPARTURE
        # 1 = ARRIVE, 2 = DEPARTURE, 3 = END_SIMULATION_EVENT
        self.next_event_type = self.time_next_event.index(min_time_next_event)

        # Event list is EMPTY
        if self.next_event_type == 0:
            print(f'\nEvent list EMPTY at time {self.sim_time}')
            sys.exit(1)

        self.sim_time = min_time_next_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)

        # Check to see whether the server is BUSY
        if self.server_status == 1:
            # Add 1 to the number in queue
            self.num_in_q += 1

            # Check to see whether the number in queue is full
            if self.num_in_q > self.q_limit:
                print('\nOverflow of the array time_arrival at')
                print(f'time {self.sim_time}')
                sys.exit(2)

            # Add the event to WAITING QUEUE
            self.time_arrival[self.num_in_q] = self.sim_time

        else:
            # Set delay = 0 for this customer
            delay = 0.0
            # Compute statistics
            self.total_of_delays += delay
            # Add 1 to the number of customers delayed
            self.num_custs_delayed += 1
            # Make the server BUSY
            self.server_status = 1
            # Schedule a DEPARTURE event for this customer
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

    def depart(self):
        # Check to see whether the WAITING QUEUE is EMPTY
        if self.num_in_q == 0:
            # Make the server IDLE
            self.server_status = 0
            self.time_next_event[2] = 1.0e+30

        else:
            # Substract 1 from the number in queue
            self.num_in_q -= 1
            # Compute delay of customer entering service
            delay = self.sim_time - self.time_arrival[1]
            # Compute statistics
            self.total_of_delays += delay
            # Add i to the number of customers delayed
            self.num_custs_delayed += 1
            # Schedule a DEPARTURE event for this customer
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_service)

            # Move each customer in queue (if any) up one place
            for i in range(1, self.num_in_q + 1):
                self.time_arrival[i] = self.time_arrival[i + 1]
                self.time_arrival[i + 1] = 0.0
            if self.num_in_q == 0:
                self.time_arrival[1] = 0.0

    def update_time_avg_stats(self):
        time_since_last_event = self.sim_time - self.time_last_event
        self.time_last_event = self.sim_time
        self.area_num_in_q += self.num_in_q * time_since_last_event
        self.area_server_status += self.server_status * time_since_last_event

    def report(self):
        print('\n\n------------------------------------------\n')
        print(f'Average delay in queue {(self.total_of_delays / self.num_custs_delayed):11.3f} minutes')
        print(f'Average number in queue {(self.area_num_in_q / self.sim_time):10.3f}')
        print(f'Server utilization {(self.area_server_status / self.sim_time):15.3f}')
        print(f'Number of delays completed {self.num_custs_delayed:7d}')
        print('\n------------------------------------------\n')

    def run_simulation(self):
        self.initialize()
        print(f'Initialization time: {self.sim_time}')
        print(f'Server status: {self.server_status}')
        print(f'Number in queue: {self.num_in_q}')
        print(f'Times of arrival: {self.time_arrival}')
        print(f'Time of last event: {self.time_last_event}')
        print(f'Clock: {self.time_last_event}')
        print(f'Event list: {self.time_next_event[1:]}')
        print(f'Number delayed: {self.num_custs_delayed}')
        print(f'Total delay: {self.total_of_delays}')
        print(f'Area under Q(t): {self.area_num_in_q}')
        print(f'Area under B(t): {self.area_server_status}\n')

        while True:
            self.timing()
            self.update_time_avg_stats()

            if self.next_event_type == 1:
                self.arrive()
                print(f'Arrival time: {self.sim_time}')
                print(f'Server status: {self.server_status}')
                print(f'Number in queue: {self.num_in_q}')
                print(f'Times of arrival: {self.time_arrival[1:]}')
                print(f'Time of last event: {self.time_last_event}')
                print(f'Clock: {self.time_last_event}')
                print(f'Event list: {self.time_next_event[1:]}')
                print(f'Number delayed: {self.num_custs_delayed}')
                print(f'Total delay: {self.total_of_delays}')
                print(f'Area under Q(t): {self.area_num_in_q}')
                print(f'Area under B(t): {self.area_server_status}\n')

            elif self.next_event_type == 2:
                self.depart()
                print(f'Departure time: {self.sim_time}')
                print(f'Server status: {self.server_status}')
                print(f'Number in queue: {self.num_in_q}')
                print(f'Times of arrival: {self.time_arrival[1:]}')
                print(f'Time of last event: {self.time_last_event}')
                print(f'Clock: {self.time_last_event}')
                print(f'Event list: {self.time_next_event[1:]}')
                print(f'Number delayed: {self.num_custs_delayed}')
                print(f'Total delay: {self.total_of_delays}')
                print(f'Area under Q(t): {self.area_num_in_q}')
                print(f'Area under B(t): {self.area_server_status}\n')

            elif self.next_event_type == 3:
                self.report()
                break

            else:
                print('next_event_type ERROR!', file=self.outfile)

def main():
        # Input three parameters here !!!
        mean_interarrival, mean_service, time_end = 1.000, 0.500, 480
        print('------------------------------------------\n')
        print('// Single-Server Queueing System with fixed run//\n')
        print(f'Mean interarrival time{mean_interarrival:11.3f} minutes')
        print(f'Mean service time{mean_service:16.3f} minutes')
        print(f'Length of the simulation{time_end:9.3f} minutes\n')
        print('------------------------------------------\n')

        # Create and run the simulation
        mm1_queue = MM1Queue(mean_interarrival, mean_service, time_end)
        mm1_queue.run_simulation()

main()
