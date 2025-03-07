import sys
import math
import random

class MM1Queue:
    def __init__(self, arrival_rate, service_rate, num_delays_required):
        self.service_rate = service_rate
        self.arrival_rate = arrival_rate
        self.mean_interarrival = 1 / self.arrival_rate
        self.mean_service = 1 / self.service_rate
        self.num_delays_required = num_delays_required

        self.sim_time = 0.0
        self.num_custs_delayed = 0
        self.num_in_q = 0
        self.server_status = 0
        self.q_limit = 100
        self.num_events = 2

        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.total_of_delays = 0.0
        self.time_last_event = 0.0

        self.time_arrival = [0.0] * (self.q_limit + 1)
        self.time_next_event = [0.0, 0.0, 1.0e+30]

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
        min_time_next_event = min(self.time_next_event[1:self.num_events + 1])
        self.next_event_type = self.time_next_event.index(min_time_next_event)

        if self.next_event_type == 0:
            print(f'\nEvent list EMPTY at time {self.sim_time}')
            sys.exit(1)

        self.sim_time = min_time_next_event

    def arrive(self):
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival)

        if self.server_status == 1:
            self.num_in_q += 1

            if self.num_in_q > self.q_limit:
                print('\nOverflow of the array time_arrival at')
                print(f'time {self.sim_time}')
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
        with open('outfile.txt', 'a', encoding='utf-8') as outfile:
            outfile.write('------------------------------------------\n')
            outfile.write('// Single-Server Queueing System //\n')
            outfile.write(f'Arrival rate {self.arrival_rate:21.1f}\n')
            outfile.write(f'Mean interarrival time {self.mean_interarrival:11.3f} minutes\n')
            outfile.write(f'Service rate {self.service_rate:21.1f}\n')
            outfile.write(f'Mean service time {self.mean_service:16.3f} minutes\n')
            outfile.write(f'Number of customers {self.num_delays_required:14d}\n')
            outfile.write('------------------------------------------\n')
            outfile.write(f'Mean system delays {(self.total_of_delays / self.num_custs_delayed):15.3f} minutes\n')
            outfile.write(f'Mean system lengths {(self.area_num_in_q / self.sim_time):14.3f}\n')
            outfile.write(f'Server utilization {(self.area_server_status / self.sim_time):15.3f}\n')
            outfile.write(f'Time simulation ended {self.sim_time:12.3f} minutes\n')
            outfile.write('------------------------------------------\n\n')

    def run_simulation(self):
        self.initialize()

        while self.num_custs_delayed < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()

            if self.next_event_type == 1:
                self.arrive()

            elif self.next_event_type == 2:
                self.depart()

            else:
                print('next_event_type ERROR!', file=self.outfile)

        self.report()

def main():
        service_rate = 1.2
        arrival_rate_1 = 0.2
        arrival_rate_2 = 0.4
        arrival_rate_3 = 0.6
        arrival_rate_4 = 0.8

        mm1_queue_1 = MM1Queue(arrival_rate=arrival_rate_1, service_rate=service_rate, num_delays_required=1000)
        mm1_queue_2 = MM1Queue(arrival_rate=arrival_rate_2, service_rate=service_rate, num_delays_required=1000)
        mm1_queue_3 = MM1Queue(arrival_rate=arrival_rate_3, service_rate=service_rate, num_delays_required=1000)
        mm1_queue_4 = MM1Queue(arrival_rate=arrival_rate_4, service_rate=service_rate, num_delays_required=1000)

        with open('outfile.txt', 'w', encoding='utf-8') as outfile:
            outfile.write('')

        mm1_queue_1.run_simulation()
        mm1_queue_2.run_simulation()
        mm1_queue_3.run_simulation()
        mm1_queue_4.run_simulation()

if __name__ == "__main__":
    main()