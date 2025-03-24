import random
import P1, P2, P3
#############################################
# Main function to run all problems
#############################################
def main():
    # For fixed result of simulations
    random.seed(123)

    #############################################
    # Problem 1: M/M/1 Queue Simulation
    #############################################
    print("\n\nProblem 1: M/M/1 Queuing System (Array and Linked List Versions)")
    arrival_rates = [0.2, 0.4, 0.6, 0.8]
    service_rate = 1.2
    num_delays = 1000

    print("# Using Array Version:")
    print("Arrival Rate\tMean Delay (min)\tMean Queue Length")
    for lam in arrival_rates:
        sim_array = P1.MM1QueueArray(arrival_rate=lam, service_rate=service_rate, num_delays_required=num_delays)
        avg_delay, avg_q = sim_array.run()
        print(f"{lam:.1f}\t\t{avg_delay:.3f}\t\t\t{avg_q:.3f}")

    print("\n# Using Linked List Version:")
    print("Arrival Rate\tMean Delay (min)\tMean Queue Length")
    for lam in arrival_rates:
        sim_linked = P1.MM1QueueLinked(arrival_rate=lam, service_rate=service_rate, num_delays_required=num_delays)
        avg_delay, avg_q = sim_linked.run()
        print(f"{lam:.1f}\t\t{avg_delay:.3f}\t\t\t{avg_q:.3f}")



    #############################################
    # Problem 2: M/M/1/K Queue with Blocking
    #############################################
    print("\nProblem 2: M/M/1/K Queue with Blocking")
    # For ρ = λ/µ = 0.9 with µ = 1.2, we have λ = 1.08
    service_rate_block = 1.2
    arrival_rate_block = 1.08
    capacities = [5, 7, 9, 11]
    num_arrivals_required = 10000

    print("Capacity (K)\tBlocking Probability")
    for K in capacities:
        sim_block = P2.MM1QueueBlocking(arrival_rate=arrival_rate_block, service_rate=service_rate_block, capacity=K, num_arrivals_required=num_arrivals_required)
        blocking_prob = sim_block.run()
        print(f"{K}\t\t{blocking_prob:.3f}")



    #############################################
    # Problem 3: M/M/1 Queue with Two Input Classes
    #############################################
    print("\nProblem 3: M/M/1 Queue with Two Input Classes")
    arrival_rate_class1 = 0.4
    arrival_rate_class2 = 0.5
    num_delays_two = 1000

    # Case 1: Both classes have service rate 1.2
    service_rate_class1_case1 = 1.2
    service_rate_class2_case1 = 1.2
    sim_two_case1 = P3.MM1QueueTwoClasses(arrival_rate_class1, arrival_rate_class2,
                                        service_rate_class1_case1, service_rate_class2_case1,
                                        num_delays_two)
    avg_delay1_case1, avg_delay2_case1 = sim_two_case1.run()

    # Case 2: Service rates: class I: 1.2, class II: 1.6
    service_rate_class1_case2 = 1.2
    service_rate_class2_case2 = 1.6
    sim_two_case2 = P3.MM1QueueTwoClasses(arrival_rate_class1, arrival_rate_class2,
                                        service_rate_class1_case2, service_rate_class2_case2,
                                        num_delays_two)
    avg_delay1_case2, avg_delay2_case2 = sim_two_case2.run()

    print("# Case 1 (µ1 = 1.2, µ2 = 1.2):")
    print("Class\t\tMean Queueing Delay (min)")
    print(f"Class 1:\t{avg_delay1_case1:.3f}")
    print(f"Class 2:\t{avg_delay2_case1:.3f}")

    print("\n# Case 2 (µ1 = 1.2, µ2 = 1.6):")
    print("Class\t\tMean Queueing Delay (min)")
    print(f"Class 1:\t{avg_delay1_case2:.3f}")
    print(f"Class 2:\t{avg_delay2_case2:.3f}\n\n")

if __name__ == "__main__":
    main()
