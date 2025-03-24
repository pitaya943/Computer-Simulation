import sys
import math
import random
#############################################
# Problem 3: M/M/1 Queue with Two Input Classes
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

# 模擬具有兩個到達類別（Class I 與 Class II）的單一服務器排隊系統
# 使用共用一個隊列，但記錄每位顧客的到達時間與類別，並依據類別決定服務時間
class MM1QueueTwoClasses:
    def __init__(self, arrival_rate1, arrival_rate2, service_rate1, service_rate2, num_delays_required):
        self.arrival_rate1 = arrival_rate1   # Class I 到達率
        self.arrival_rate2 = arrival_rate2   # Class II 到達率
        self.mean_interarrival1 = 1.0 / arrival_rate1
        self.mean_interarrival2 = 1.0 / arrival_rate2
        
        # 服務率根據客戶類別而定
        self.service_rate1 = service_rate1   # Class I
        self.service_rate2 = service_rate2   # Class II
        
        self.num_delays_required = num_delays_required

        self.sim_time = 0.0
        self.server_status = 0  # 0 idle, 1 busy
        self.queue = LinkedListQueue()  # 儲存 (arrival_time, class_type)
        self.num_in_q = 0
        
        self.time_last_event = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        
        # 分別統計兩類客戶的延遲
        self.total_delay_class1 = 0.0
        self.total_delay_class2 = 0.0
        self.num_delayed_class1 = 0
        self.num_delayed_class2 = 0
        
        # 事件列表：1 = Class I 到達，2 = Class II 到達，3 = 離開事件
        self.time_next_event = [0.0, 0.0, 0.0, 1.0e+30]
        self.num_events = 3

    def expon(self, mean):
        return -mean * math.log(random.random())

    def initialize(self):
        self.sim_time = 0.0
        self.server_status = 0
        self.queue = LinkedListQueue()
        self.num_in_q = 0
        self.time_last_event = 0.0
        self.area_num_in_q = 0.0
        self.area_server_status = 0.0
        self.total_delay_class1 = 0.0
        self.total_delay_class2 = 0.0
        self.num_delayed_class1 = 0
        self.num_delayed_class2 = 0
        
        # 安排第一個到達事件（兩個類別各自獨立）
        self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival1)
        self.time_next_event[2] = self.sim_time + self.expon(self.mean_interarrival2)
        self.time_next_event[3] = 1.0e+30

    def timing(self):
        # 找到三個事件中最早發生的那一個
        min_time_next_event = min(self.time_next_event[1:4])
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

    def arrive_class(self, class_type):
        # 根據類別安排下一次到達
        if class_type == 1:
            self.time_next_event[1] = self.sim_time + self.expon(self.mean_interarrival1)
        else:
            self.time_next_event[2] = self.sim_time + self.expon(self.mean_interarrival2)
        # 到達事件：如果服務器忙碌，則加入隊列；否則立即服務
        if self.server_status == 1:
            self.num_in_q += 1
            self.queue.enqueue((self.sim_time, class_type))
        else:
            delay = 0.0
            if class_type == 1:
                self.total_delay_class1 += delay
                self.num_delayed_class1 += 1
            else:
                self.total_delay_class2 += delay
                self.num_delayed_class2 += 1
            self.server_status = 1
            # 離開事件的服務時間取決於客戶類型
            if class_type == 1:
                service_time = self.expon(1.0 / self.service_rate1)
            else:
                service_time = self.expon(1.0 / self.service_rate2)
            self.time_next_event[3] = self.sim_time + service_time

    def depart(self):
        if self.num_in_q == 0:
            self.server_status = 0
            self.time_next_event[3] = 1.0e+30
        else:
            self.num_in_q -= 1
            arrival_time, class_type = self.queue.dequeue()
            delay = self.sim_time - arrival_time
            if class_type == 1:
                self.total_delay_class1 += delay
                self.num_delayed_class1 += 1
            else:
                self.total_delay_class2 += delay
                self.num_delayed_class2 += 1
            # 根據該客戶類型安排下一個離開事件
            if class_type == 1:
                service_time = self.expon(1.0 / self.service_rate1)
            else:
                service_time = self.expon(1.0 / self.service_rate2)
            self.time_next_event[3] = self.sim_time + service_time

    def run(self):
        self.initialize()
        # 以總完成顧客數達到 num_delays_required 為停止準則
        while (self.num_delayed_class1 + self.num_delayed_class2) < self.num_delays_required:
            self.timing()
            self.update_time_avg_stats()
            if self.next_event_type == 1:
                self.arrive_class(1)
            elif self.next_event_type == 2:
                self.arrive_class(2)
            elif self.next_event_type == 3:
                self.depart()
        avg_delay_class1 = self.total_delay_class1 / self.num_delayed_class1 if self.num_delayed_class1 > 0 else 0
        avg_delay_class2 = self.total_delay_class2 / self.num_delayed_class2 if self.num_delayed_class2 > 0 else 0
        return avg_delay_class1, avg_delay_class2