import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    update_fitness_plot(generations, best_fitness_values)

def update_fitness_plot(generations, best_fitness_values):
    ax.clear()
    ax.plot(generations, best_fitness_values, marker='o', linestyle='-', color='b')
    ax.set_xlabel("Generation")
    ax.set_ylabel("Best Fitness Value")
    ax.set_title("Fitness Value vs. Generation")
    ax.grid(True)
    canvas.draw()

# Create the main window
root = tk.Tk()
root.title("Knapsack Problem Genetic Algorithm")

# Set minimum window size
root.minsize(800, 400)

items = [
    (2, 10000),
    (4, 5000),
    (3, 1500),
    (1, 800),
    (2, 1200)
]

# Left Panel - Inputs
left_panel = ttk.Frame(root)
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5)

# Capacity Slider
capacity_label = ttk.Label(left_panel, text="Capacity:")
capacity_label.pack(pady=5)
capacity_slider = ttk.Scale(left_panel, from_=10, to=100, orient=tk.HORIZONTAL)
capacity_slider.pack(pady=5)
capacity_slider.set(7)

# Population Size Slider
population_size_label = ttk.Label(left_panel, text="Population Size:")
population_size_label.pack(pady=5)
population_size_slider = ttk.Scale(left_panel, from_=10, to=200, orient=tk.HORIZONTAL)
population_size_slider.pack(pady=5)
population_size_slider.set(100)

# Number of Generations Slider
num_generations_label = ttk.Label(left_panel, text="Number of Generations:")
num_generations_label.pack(pady=5)
num_generations_slider = ttk.Scale(left_panel, from_=10, to=500, orient=tk.HORIZONTAL)
num_generations_slider.pack(pady=5)
num_generations_slider.set(100)

# Mutation Rate Slider
mutation_rate_label = ttk.Label(left_panel, text="Mutation Rate:")
mutation_rate_label.pack(pady=5)
mutation_rate_slider = ttk.Scale(left_panel, from_=0, to=100, orient=tk.HORIZONTAL)
mutation_rate_slider.pack(pady=5)
mutation_rate_slider.set(10)

# Run Button
run_button = ttk.Button(left_panel, text="Run Genetic Algorithm", command=update_output_values)
run_button.pack(pady=5)

# Result Labels
capacity_label = ttk.Label(left_panel, text="Capacity: ")
capacity_label.pack(pady=5)

population_size_label = ttk.Label(left_panel, text="Population Size: ")
population_size_label.pack(pady=5)

num_generations_label = ttk.Label(left_panel, text="Number of Generations: ")
num_generations_label.pack(pady=5)

mutation_rate_label = ttk.Label(left_panel, text="Mutation Rate: ")
mutation_rate_label.pack(pady=5)

best_solution_label = ttk.Label(left_panel, text="Best Solution: ")
best_solution_label.pack(pady=5)

best_fitness_label = ttk.Label(left_panel, text="Best Fitness: ")
best_fitness_label.pack(pady=5)

# Right Panel - Output Graph
right_panel = ttk.Frame(root)
right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Create the figure and canvas for the fitness plot
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=right_panel)
canvas.get_tk_widget().pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

# Initial update of output values and fitness plot
update_output_values()

root.mainloop()
