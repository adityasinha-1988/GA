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

    # Plot and save the graph for fitness vs generation
    plt.figure(figsize=(8, 6))
    plt.plot(generations, best_fitness_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Value")
    plt.title("Fitness Value vs. Generation")
    plt.grid(True)
    plt.savefig("fitness_vs_generation.png")
    plt.close()

    # Plot and save the graph for population size vs fitness values
    population_sizes = list(range(1, population_size + 1))
    fitness_values_population = []

    for size in population_sizes:
        best_individual, best_fitness = genetic_algorithm(items, capacity, size, num_generations, mutation_rate)
        fitness_values_population.append(best_fitness)

    plt.figure(figsize=(8, 6))
    plt.plot(population_sizes, fitness_values_population, marker='o', linestyle='-', color='g')
    plt.xlabel("Population Size")
    plt.ylabel("Best Fitness Value")
    plt.title("Fitness Value vs. Population Size")
    plt.grid(True)
    plt.savefig("fitness_vs_population.png")
    plt.close()

    return best_individual, evaluate_fitness(best_individual, items, capacity)

# GUI Functions
def run_genetic_algorithm():
    capacity = int(capacity_entry.get())
    population_size = int(population_size_entry.get())
    num_generations = int(num_generations_entry.get())
    mutation_rate = float(mutation_rate_entry.get())

    best_individual, best_fitness = genetic_algorithm(items, capacity, population_size, num_generations, mutation_rate)
    result_label.config(text=f"Best Solution: {best_individual}\nBest Fitness: {best_fitness}")

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

# Capacity
capacity_label = ttk.Label(root, text="Capacity:")
capacity_label.grid(row=0, column=0, padx=5, pady=5)
capacity_entry = ttk.Entry(root)
capacity_entry.insert(0, "7")
capacity_entry.grid(row=0, column=1, padx=5, pady=5)

# Population Size
population_size_label = ttk.Label(root, text="Population Size:")
population_size_label.grid(row=1, column=0, padx=5, pady=5)
population_size_entry = ttk.Entry(root)
population_size_entry.insert(0, "100")
population_size_entry.grid(row=1, column=1, padx=5, pady=5)

# Number of Generations
num_generations_label = ttk.Label(root, text="Number of Generations:")
num_generations_label.grid(row=2, column=0, padx=5, pady=5)
num_generations_entry = ttk.Entry(root)
num_generations_entry.insert(0, "100")
num_generations_entry.grid(row=2, column=1, padx=5, pady=5)

# Mutation Rate
mutation_rate_label = ttk.Label(root, text="Mutation Rate:")
mutation_rate_label.grid(row=3, column=0, padx=5, pady=5)
mutation_rate_entry = ttk.Entry(root)
mutation_rate_entry.insert(0, "0.1")
mutation_rate_entry.grid(row=3, column=1, padx=5, pady=5)

# Run Button
run_button = ttk.Button(root, text="Run Genetic Algorithm", command=run_genetic_algorithm)
run_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Result Label
result_label = ttk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

root.mainloop()
