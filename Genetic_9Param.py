import tkinter as tk
from tkinter import ttk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import exp, sqrt, cos, pi

# Genetic Algorithm functions
def create_binary_individual(individual_length):
    return [random.choice([0, 1]) for _ in range(individual_length)]

def create_real_valued_individual(bounds):
    return [random.uniform(bounds[i][0], bounds[i][1]) for i in range(len(bounds))]

def create_initial_population(population_size, encoding_scheme, individual_length=None, bounds=None):
    if encoding_scheme == "Binary":
        return [create_binary_individual(individual_length) for _ in range(population_size)]
    elif encoding_scheme == "Real-Valued":
        return [create_real_valued_individual(bounds) for _ in range(population_size)]
    else:
        return []

def evaluate_fitness(individual, selected_function):
    x, y = individual
    if selected_function == "Sphere Function":
        return x**2 + y**2
    elif selected_function == "Rosenbrock Function":
        a = 1
        b = 100
        return (a - x)**2 + b * (y - x**2)**2
    elif selected_function == "Ackley Function":
        return -20 * exp(-0.2 * sqrt(0.5 * (x**2 + y**2))) - exp(0.5 * (cos(2 * pi * x) + cos(2 * pi * y))) + exp(1) + 20
    elif selected_function == "Rastringin Function":
        return 10 + x**2 - 10 * cos(2 * pi * x) + y**2 - 10 * cos(2 * pi * y)
    elif selected_function == "Beale Function":
        return (1.5 - x + x * y)**2 + (2.25 - x + x * y**2)**2 + (2.625 - x + x * y**3)**2
    else:
        return 0

def tournament_selection(population, num_selections):
    selected_individuals = []
    for _ in range(num_selections):
        candidates = random.sample(population, 5)  # Tournament size of 5
        selected_individuals.append(min(candidates, key=lambda ind: evaluate_fitness(ind, function_var.get())))
    return selected_individuals

def single_point_crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point] + parent2[crossover_point:]
    return child

def multi_point_crossover(parent1, parent2):
    num_crossover_points = random.randint(1, len(parent1) - 1)
    crossover_points = sorted(random.sample(range(1, len(parent1)), num_crossover_points))
    child = parent1[:crossover_points[0]]
    for i in range(num_crossover_points):
        if i % 2 == 0:
            child += parent1[crossover_points[i]:crossover_points[i+1]]
        else:
            child += parent2[crossover_points[i]:crossover_points[i+1]]
    child += parent2[crossover_points[-1]:]
    return child

def bit_flip_mutation(individual):
    mutation_point = random.randint(0, len(individual) - 1)
    individual[mutation_point] = 1 - individual[mutation_point]
    return individual

def random_value_change_mutation(individual, bounds):
    mutation_point = random.randint(0, len(individual) - 1)
    individual[mutation_point] = random.uniform(bounds[mutation_point][0], bounds[mutation_point][1])
    return individual

def genetic_algorithm(population_size, num_generations, encoding_scheme, bounds=None):
    if encoding_scheme == "Binary":
        individual_length = 2  # Binary encoding for x and y
        population = create_initial_population(population_size, encoding_scheme, individual_length=individual_length)
    elif encoding_scheme == "Real-Valued":
        population = create_initial_population(population_size, encoding_scheme, bounds=bounds)
    else:
        return [], [], []

    best_fitness_values = []
    best_individuals = []
    generations = list(range(num_generations + 1))

    for generation in range(num_generations + 1):
        selected_individuals = tournament_selection(population, num_selections=population_size)
        new_population = []

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_individuals, 2)

            if random.random() < crossover_rate_slider.get():
                if crossover_operator_var.get() == "Single-Point":
                    child = single_point_crossover(parent1, parent2)
                elif crossover_operator_var.get() == "Multi-Point":
                    child = multi_point_crossover(parent1, parent2)
            else:
                child = parent1  # No crossover, choose one of the parents as the child

            if random.random() < mutation_rate_slider.get():
                if mutation_operator_var.get() == "Bit Flip":
                    child = bit_flip_mutation(child)
                elif mutation_operator_var.get() == "Random Value Change":
                    child = random_value_change_mutation(child, bounds)

            new_population.append(child)

        if elitism_checkbox_var.get():
            # Preserve the best individual from the previous generation
            elitism_individual = min(population, key=lambda ind: evaluate_fitness(ind, function_var.get()))
            new_population[random.randint(0, population_size - 1)] = elitism_individual

        population = new_population

        best_individual = min(population, key=lambda ind: evaluate_fitness(ind, function_var.get()))
        best_individuals.append(best_individual)
        best_fitness_values.append(evaluate_fitness(best_individual, function_var.get()))

    return generations, best_fitness_values, best_individuals

# GUI Functions
def run_genetic_algorithm():
    global graph_canvas

    population_size = int(population_size_slider.get())
    num_generations = int(num_generations_slider.get())
    encoding_scheme = encoding_scheme_var.get()

    if encoding_scheme == "Binary":
        bounds = None
    elif encoding_scheme == "Real-Valued":
        bounds = [(-10, 10), (-10, 10)]  # Set the bounds for x and y

    generations, best_fitness_values, best_individuals = genetic_algorithm(population_size, num_generations, encoding_scheme, bounds)

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

    best_individual = min(best_individuals, key=lambda ind: evaluate_fitness(ind, function_var.get()))
    result_label.config(text=f"Best Solution: x = {best_individual[0]}, y = {best_individual[1]}")

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

function_label = ttk.Label(left_panel, text="Objective Function:")
function_label.pack()
function_var = tk.StringVar()
function_choices = ["Sphere Function", "Rosenbrock Function", "Ackley Function", "Rastringin Function", "Beale Function"]
function_dropdown = ttk.Combobox(left_panel, textvariable=function_var, values=function_choices)
function_dropdown.set("Sphere Function")
function_dropdown.pack()

# Run Button
run_button = ttk.Button(left_panel, text="Run Genetic Algorithm", command=run_genetic_algorithm)
run_button.pack()

# Result Label
result_label = ttk.Label(left_panel, text="")
result_label.pack()

# Right Panel for Graph
right_panel = ttk.Frame(root)
right_panel.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)  # Allow the right panel to expand

# Initial Plot
plt.figure(figsize=(8, 6))
plt.plot([], [], marker='o', linestyle='-', color='b')
plt.xlabel("Generation")
plt.ylabel("Best Fitness Value")
plt.title("Fitness Value vs. Generation")
plt.grid(True)

graph_canvas = FigureCanvasTkAgg(plt.gcf(), right_panel)
graph_canvas.draw()
graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root.mainloop()
