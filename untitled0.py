import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt

# Genetic Algorithm functions
def create_individual(num_items):
    return [random.randint(0, 1) for _ in range(num_items)]

def create_initial_population(population_size, num_items):
    return [create_individual(num_items) for _ in range(population_size)]

def evaluate_fitness(individual, items, capacity):
    total_value = 0
    total_weight = 0

    for i in range(len(individual)):
        if individual[i] == 1:
            total_value += items[i][1]
            total_weight += items[i][0]
            if total_weight > capacity:
                return 0

    return total_value

def tournament_selection(population, items, capacity, num_selections):
    selected_individuals = []
    for _ in range(num_selections):
        candidates = random.sample(population, 5)  # Tournament size of 5
        selected_individuals.append(max(candidates, key=lambda x: evaluate_fitness(x, items, capacity)))
    return selected_individuals

def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def mutation(individual, mutation_rate):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]  # Flip the bit
    return individual

def genetic_algorithm(items, capacity, population_size, num_generations, mutation_rate):
    num_items = len(items)
    population = create_initial_population(population_size, num_items)

    best_fitness_values = []
    generations = list(range(num_generations + 1))
    best_individual = None
    best_fitness = None

    for generation in range(num_generations + 1):
        selected_individuals = tournament_selection(population, items, capacity, num_selections=population_size)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_individuals, 2)
            child1, child2 = single_point_crossover(parent1, parent2)

            child1 = mutation(child1, mutation_rate)
            child2 = mutation(child2, mutation_rate)

            new_population.append(child1)
            new_population.append(child2)

        population = new_population

        best_individual = max(population, key=lambda x: evaluate_fitness(x, items, capacity))
        best_fitness_values.append(evaluate_fitness(best_individual, items, capacity))

    return generations, best_fitness_values, best_individual, evaluate_fitness(best_individual, items, capacity)


# GUI Functions
def update_output_values(event=None):
    capacity = capacity_slider.get()
    population_size = int(population_size_slider.get())  # Convert to integer
    num_generations = int(num_generations_slider.get())  # Convert to integer
    mutation_rate = mutation_rate_slider.get() / 100  # Divide by 100 to simulate 2 decimal places

    generations, best_fitness_values, best_individual, best_fitness = genetic_algorithm(items, capacity, population_size, num_generations, mutation_rate)

    capacity_label.config(text=f"Capacity: {capacity}")
    population_size_label.config(text=f"Population Size: {population_size}")
    num_generations_label.config(text=f"Number of Generations: {num_generations}")
    mutation_rate_label.config(text=f"Mutation Rate: {mutation_rate:.2f}")
    best_solution_label.config(text=f"Best Solution: {best_individual}")
    best_fitness_label.config(text=f"Best Fitness: {best_fitness}")

    # (same as before)

# Create the main window
root = tk.Tk()
root.title("Knapsack Problem Genetic Algorithm")

# Items
items = [
    (2, 10000),
    (4, 5000),
    (3, 1500),
    (1, 800),
    (2, 1200)
]

# Capacity Slider
capacity_label = ttk.Label(root, text="Capacity:")
capacity_label.grid(row=0, column=0, padx=5, pady=5)
capacity_slider = ttk.Scale(root, from_=1, to=100, orient="horizontal", length=200, command=update_output_values)
capacity_slider.set(7)
capacity_slider.grid(row=0, column=1, padx=5, pady=5)

# Population Size Slider
population_size_label = ttk.Label(root, text="Population Size:")
population_size_label.grid(row=1, column=0, padx=5, pady=5)
population_size_slider = ttk.Scale(root, from_=1, to=500, orient="horizontal", length=200, command=update_output_values)
population_size_slider.set(100)
population_size_slider.grid(row=1, column=1, padx=5, pady=5)

# Number of Generations Slider
num_generations_label = ttk.Label(root, text="Number of Generations:")
num_generations_label.grid(row=2, column=0, padx=5, pady=5)
num_generations_slider = ttk.Scale(root, from_=1, to=500, orient="horizontal", length=200, command=update_output_values)
num_generations_slider.set(100)
num_generations_slider.grid(row=2, column=1, padx=5, pady=5)

# Mutation Rate Slider
mutation_rate_label = ttk.Label(root, text="Mutation Rate:")
mutation_rate_label.grid(row=3, column=0, padx=5, pady=5)
mutation_rate_slider = ttk.Scale(root, from_=1, to=100, orient="horizontal", length=200, command=update_output_values)
mutation_rate_slider.set(10)
mutation_rate_slider.grid(row=3, column=1, padx=5, pady=5)

# Run Button
run_button = ttk.Button(root, text="Run Genetic Algorithm", command=update_output_values)
run_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Result Labels
capacity_label = ttk.Label(root, text="Capacity: 7")
capacity_label.grid(row=5, column=0, padx=5, pady=2)
population_size_label = ttk.Label(root, text="Population Size: 100")
population_size_label.grid(row=6, column=0, padx=5, pady=2)
num_generations_label = ttk.Label(root, text="Number of Generations: 100")
num_generations_label.grid(row=7, column=0, padx=5, pady=2)
mutation_rate_label = ttk.Label(root, text="Mutation Rate: 0.10")
mutation_rate_label.grid(row=8, column=0, padx=5, pady=2)
best_solution_label = ttk.Label(root, text="Best Solution:")
best_solution_label.grid(row=9, column=0, padx=5, pady=2)
best_fitness_label = ttk.Label(root, text="Best Fitness:")
best_fitness_label.grid(row=10, column=0, padx=5, pady=2)

root.mainloop()
