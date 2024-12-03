import json
import math
import random
import copy
import time

class Job:
    def __init__(self, name):
        self.name = name

class Zamestnanec:
    def __init__(self, ID, speed_data):
        self.ID = ID
        self.docs = []
        self.speed = speed_data
        self.celkovy_cas = 0

    def add_job(self, job):
        self.docs.append(job)

    def calculate_total_time(self):
        efficiency = 1
        self.celkovy_cas = 0

        for i, job in enumerate(self.docs):
            if i > 0 and self.docs[i - 1].name == job.name:
                efficiency = max(efficiency - 0.05, 0.5)
            else:
                efficiency = 1

            self.celkovy_cas += self.speed.get(job.name, 5) * efficiency
        return self.celkovy_cas


def load_data():
    with open("possible_zamestnanci.json") as file:
        possible_zamestnanci = json.load(file)
    with open("formulare_todo.json") as file:
        formulare_todo = json.load(file)
    return possible_zamestnanci, formulare_todo


def random_assignment(possible_zamestnanci, formulare_todo):
    employees = [Zamestnanec(ID, speed_data) for ID, speed_data in enumerate(possible_zamestnanci)]
    jobs = [Job(name) for name, count in formulare_todo.items() for _ in range(count)]

    for job in jobs:
        random.choice(employees).add_job(job)

    return employees


def evaluate_solution(employees):
    slowest_time = 0
    total_cost = 0
    output_data = []

    for employee in employees:
        time = employee.calculate_total_time()
        slowest_time = max(slowest_time, time)
        total_cost += math.ceil(time / 60) * 30  # 30 EUR/hodina
        output_data.append({
            'zam_id': str(employee.ID),
            'zamestnanec': {job.name: 1 for job in employee.docs},
            'celkovy cas': time
        })

    return output_data, slowest_time, total_cost


def simulated_annealing(employees, iterations=5000, initial_temp=1.0, cooling_rate=0.999):
    current_solution = copy.deepcopy(employees)
    best_solution = copy.deepcopy(employees)
    current_temp = initial_temp

    for _ in range(iterations):
        new_solution = copy.deepcopy(current_solution)

        # Náhodné prehodenie práce medzi zamestnancami
        emp1, emp2 = random.sample(new_solution, 2)
        if emp1.docs:
            job = random.choice(emp1.docs)
            emp1.docs.remove(job)
            emp2.add_job(job)

        current_eval = evaluate_solution(current_solution)[1]
        new_eval = evaluate_solution(new_solution)[1]

        if new_eval < current_eval or math.exp((current_eval - new_eval) / current_temp) > random.random():
            current_solution = new_solution
            if new_eval < evaluate_solution(best_solution)[1]:
                best_solution = copy.deepcopy(new_solution)

        current_temp *= cooling_rate

    return best_solution


def main():
    possible_zamestnanci, formulare_todo = load_data()
    employees = random_assignment(possible_zamestnanci, formulare_todo)

    # Zmeranie času pred optimalizáciou
    start_time = time.time()

    # Optimalizácia pomocou simulated annealing
    optimized_employees = simulated_annealing(employees)

    # Zmeranie času po optimalizácii
    end_time = time.time()
    compilation_time = end_time - start_time

    # Vyhodnotenie výsledku optimalizácie
    optimized_output, optimized_slowest, optimized_cost = evaluate_solution(optimized_employees)

    # Výpis výsledku
    print(f"Cas kompilácie (optimalizacie): {compilation_time:.2f} sekund")
    print("\nOptimalizované riešenie:")
    for employee in optimized_output:
        print(employee)
    print(f"Optimalizované naklady: {optimized_cost} EUR, Najpomalsi cas: {optimized_slowest} minut")


if __name__ == "__main__":
    main()
