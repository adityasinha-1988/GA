import random
import matplotlib.pyplot as plt
import base64
import io
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

def genetic_algorithm(population_size, num_generations, mutation_rate, crossover_rate, selection_method, elitism):
    population = create_initial_population(population_size)
    best_fitness_values = []
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
        best_fitness_values.append(evaluate_fitness(best_individual))

    return generations, best_fitness_values

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_genetic_algorithm', methods=['POST'])
def run_genetic_algorithm():
    population_size = int(request.form['population_size'])
    num_generations = int(request.form['num_generations'])
    mutation_rate = float(request.form['mutation_rate'])
    crossover_rate = float(request.form['crossover_rate'])
    selection_method = request.form['selection_method']
    elitism = request.form.get('elitism') == 'on'

    generations, best_fitness_values = genetic_algorithm(population_size, num_generations, mutation_rate, crossover_rate, selection_method, elitism)

    plt.figure(figsize=(8, 6))
    plt.plot(generations, best_fitness_values, marker='o', linestyle='-', color='b')
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness Value")
    plt.title("Fitness Value vs. Generation")
    plt.grid(True)

    # Convert the plot to a base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')

    plt.close()

    return jsonify(plot_data=plot_data, best_fitness_values=best_fitness_values)

if __name__ == '__main__':
    app.run(debug=True)
