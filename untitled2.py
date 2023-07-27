import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Genetic Algorithm functions
def create_individual():
    return random.uniform(-10, 10)

def create_initial_population(population_size):
    return [create_individual() for _ in range(population_size)]

def evaluate_fitness(individual):
    x = individual
    return x**2 + 5*x + 6

def tournament_selection(population, num_selections):
    selected_individuals = []
    for _ in range(num_selections):
        candidates = random.sample(population, 5)  # Tournament size of 5
        selected_individuals.append(min(candidates, key=evaluate_fitness))
    return selected_individuals

def genetic_algorithm(population_size, num_generations):
    population = create_initial_population(population_size)
    best_fitness_values = []
    best_individuals = []
    generations = list(range(num_generations + 1))

    for generation in range(num_generations + 1):
        selected_individuals = tournament_selection(population, num_selections=population_size)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_individuals, 2)
            child = (parent1 + parent2) / 2  # Simple average crossover

            new_population.append(child)

        population = new_population

        best_individual = min(population, key=evaluate_fitness)
        best_individuals.append(best_individual)
        best_fitness_values.append(evaluate_fitness(best_individual))

    return generations, best_fitness_values, best_individuals

# GUI Functions
def run_genetic_algorithm():
    global graph_canvas

    population_size = int(population_size_slider.get())
    num_generations = int(num_generations_slider.get())

    generations, best_fitness_values, best_individuals = genetic_algorithm(population_size, num_generations)

    plt.figure(figsize=(8, 6))
    plt.plot(generations, best_fitness_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Value")
    plt.title("Fitness Value vs. Generation")
    plt.grid(True)

    if graph_canvas:
        graph_canvas.get_tk_widget().destroy()

    graph_canvas = FigureCanvasTkAgg(plt.gcf(), right_panel)
    graph_canvas.draw()
    graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    result_label.config(text=f"Best Solution: {min(best_fitness_values)}")

# Create the main window
root = tk.Tk()
root.title("Genetic Algorithm Optimization")

# Left Panel for Input Parameters
left_panel = ttk.Frame(root)
left_panel.pack(side=tk.LEFT, padx=10, pady=10)

# Population Size Slider
population_size_label = ttk.Label(left_panel, text="Population Size:")
population_size_label.pack()
population_size_slider = ttk.Scale(left_panel, from_=10, to=200, orient=tk.HORIZONTAL, length=200)
population_size_slider.set(100)
population_size_slider.pack()

# Number of Generations Slider
num_generations_label = ttk.Label(left_panel, text="Number of Generations:")
num_generations_label.pack()
num_generations_slider = ttk.Scale(left_panel, from_=10, to=500, orient=tk.HORIZONTAL, length=200)
num_generations_slider.set(100)
num_generations_slider.pack()

# Mutation Rate Slider
mutation_rate_label = ttk.Label(left_panel, text="Mutation Rate:")
mutation_rate_label.pack()
mutation_rate_slider = ttk.Scale(left_panel, from_=0, to=1, orient=tk.HORIZONTAL, length=200)
mutation_rate_slider.set(0.1)
mutation_rate_slider.pack()

# Crossover Rate Slider
crossover_rate_label = ttk.Label(left_panel, text="Crossover Rate:")
crossover_rate_label.pack()
crossover_rate_slider = ttk.Scale(left_panel, from_=0, to=1, orient=tk.HORIZONTAL, length=200)
crossover_rate_slider.set(0.8)
crossover_rate_slider.pack()

# Elitism Checkbox
elitism_checkbox_var = tk.BooleanVar()
elitism_checkbox = ttk.Checkbutton(left_panel, text="Elitism", variable=elitism_checkbox_var)
elitism_checkbox.pack()

# Encoding Scheme Dropdown
encoding_scheme_label = ttk.Label(left_panel, text="Encoding Scheme:")
encoding_scheme_label.pack()
encoding_scheme_var = tk.StringVar()
encoding_scheme_choices = ["Binary", "Real-Valued"]
encoding_scheme_dropdown = ttk.Combobox(left_panel, textvariable=encoding_scheme_var, values=encoding_scheme_choices)
encoding_scheme_dropdown.set("Binary")
encoding_scheme_dropdown.pack()

# Crossover Operator Dropdown
crossover_operator_label = ttk.Label(left_panel, text="Crossover Operator:")
crossover_operator_label.pack()
crossover_operator_var = tk.StringVar()
crossover_operator_choices = ["Single-Point", "Multi-Point"]
crossover_operator_dropdown = ttk.Combobox(left_panel, textvariable=crossover_operator_var, values=crossover_operator_choices)
crossover_operator_dropdown.set("Single-Point")
crossover_operator_dropdown.pack()

# Mutation Operator Dropdown
mutation_operator_label = ttk.Label(left_panel, text="Mutation Operator:")
mutation_operator_label.pack()
mutation_operator_var = tk.StringVar()
mutation_operator_choices = ["Bit Flip", "Random Value Change"]
mutation_operator_dropdown = ttk.Combobox(left_panel, textvariable=mutation_operator_var, values=mutation_operator_choices)
mutation_operator_dropdown.set("Bit Flip")
mutation_operator_dropdown.pack()

# Convergence Criteria Slider
convergence_criteria_label = ttk.Label(left_panel, text="Convergence Criteria:")
convergence_criteria_label.pack()
convergence_criteria_slider = ttk.Scale(left_panel, from_=0, to=100, orient=tk.HORIZONTAL, length=200)
convergence_criteria_slider.set(1.0)
convergence_criteria_slider.pack()

# Run Button
run_button = ttk.Button(left_panel, text="Run Genetic Algorithm", command=run_genetic_algorithm)
run_button.pack()

# Result Label
result_label = ttk.Label(left_panel, text="")
result_label.pack()

# Right Panel for Graph
right_panel = ttk.Frame(root)
right_panel.pack(side=tk.RIGHT, padx=10, pady=10)

# Initial Plot
plt.figure(figsize=(8, 6))
plt.plot([], [], marker='o', linestyle='-', color='b')
plt.xlabel("Generation")
plt.ylabel("Best Fitness Value")
plt.title("Fitness Value vs. Generation")
plt.grid(True)

graph_canvas = None

root.mainloop()