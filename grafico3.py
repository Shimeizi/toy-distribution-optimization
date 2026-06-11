from pulp import *
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import time

def run_solver(input_data):
    # Initialize variable count
    N_var = 0
    # Parse input data
    n, m, t = map(int, input_data[0].strip().split())
    prob = LpProblem("C_sat", LpMaximize)

    # Read factories data
    fabrica_dados = []
    for i in range(1, n + 1):
        fi, pi, fmax = map(int, input_data[i].strip().split())
        fabrica_dados.append((fi, pi, fmax))

    # Read countries data
    pais_dados = []
    for i in range(n + 1, n + 1 + m):
        pj, pmax, pmin = map(int, input_data[i].strip().split())
        pais_dados.append((pj, pmax, pmin))

    # Read children's preferences
    crianca_dados = []
    for i in range(n + 1 + m, len(input_data)):
        dados_crianca = list(map(int, input_data[i].strip().split()))
        crianca_dados.append(dados_crianca)

    # Define decision variables
    x = {}
    for k in range(t):
        for f in crianca_dados[k][2:]:
            x[k, f] = LpVariable(f"x_{k}_{f}", 0, 1, LpBinary)
            N_var += 1

    # Define objective function
    prob += lpSum(x[k, f] for k in range(t) for f in crianca_dados[k][2:])

    # Add constraints
    for k in range(t):
        prob += lpSum(x[k, f] for f in crianca_dados[k][2:]) <= 1

    for fi, pi, fmax in fabrica_dados:
        prob += lpSum(x[k, fi] for k in range(t) if fi in crianca_dados[k][2:]) <= fmax

    for pj, pmax, pmin in pais_dados:
        prob += lpSum(x[k, f] for k in range(t) for f in crianca_dados[k][2:] if crianca_dados[k][1] == pj) >= pmin
        prob += lpSum(
            x[k, f] for k in range(t) for f in crianca_dados[k][2:]
            if any(fab[1] == pj and crianca_dados[k][1] != pj for fab in fabrica_dados if fab[0] == f)
        ) <= pmax

    # Solve the problem
    prob.solve(PULP_CBC_CMD(msg=0))

    # Output results
    if LpStatus[prob.status] == "Optimal":
        print(int(value(prob.objective)))  # Print objective value
    else:
        print(-1)  # Indicate infeasibility
    
    # Print or return N_var
    print(N_var)
    return N_var  # Return N_var explicitly

def simulate_execution(input_data):
    # Execute your project and measure time
    start_time = time.time()
    result = run_solver(input_data)
    end_time = time.time()

    # Measure execution time and return
    execution_time = end_time - start_time
    return execution_time, result

def generate_input(num_factories, num_countries, num_children):
    factories = []
    countries = []
    requests = []

    # Create factories
    for i in range(1, num_factories + 1):
        country_id = (i % num_countries) + 1
        stock = 10
        factories.append(f"{i} {country_id} {stock}")

    # Create countries
    for i in range(1, num_countries + 1):
        max_exports = 15
        min_presents = 5
        countries.append(f"{i} {max_exports} {min_presents}")

    # Create requests
    for i in range(1, num_children + 1):
        country_id = (i % num_countries) + 1
        num_requests = min(5, num_factories)
        factories_ids = list(range(1, num_requests + 1))
        requests.append(f"{i} {country_id} " + " ".join(map(str, factories_ids)))

    # Ensure the first line has n, m, t as expected
    input_data = [f"{num_factories} {num_countries} {num_children}"]  # First line
    input_data += factories + countries + requests  # Append all the other lines
    return input_data


# Run experiments
results = []
increments = 10  # Increment size for n, m
initial_values = (10, 3)  # Initial values for n and m
num_tests = 60
k = 5  # Proportionality constant for t = k * n

for i in range(num_tests):
    n = initial_values[0] + i * increments
    m = initial_values[1] + i * increments
    t = k * n  # Ensure t grows proportionally to n

    # Generate input
    input_data = generate_input(n, m, t)

    # Measure execution
    exec_time, n_vars = simulate_execution(input_data)
    complexity = n_vars
    results.append((n, m, t, complexity, exec_time))

# Sort and plot
results.sort(key=lambda x: x[3])
complexities, times = zip(*[(r[3], r[4]) for r in results])

print("Complexities:", complexities)
print("Times:", [f"{time:.3f}" for time in times])

# Exponential model function
def exponential(x, a, b):
    return a * np.exp(b * x)

# Provide initial guesses for the parameters (a, b)
initial_guess = [times[0], 0.001]  # a is the first time value, b is a small number for the rate of growth

# Fit the exponential model to the data with initial guesses
params, covariance = curve_fit(exponential, complexities, times, p0=initial_guess)

# Extract the fitted parameters (a, b)
a, b = params

# Print the fitted parameters to see if they make sense
print(f"Fitted parameters: a = {a}, b = {b}")

# Generate points for the fitted curve
x_fit = np.linspace(min(complexities), max(complexities), 100)
y_fit = exponential(x_fit, a, b)

# Plot the original data and the regression line
plt.figure(figsize=(10, 6))
plt.plot(complexities, times, marker="o", linestyle="-", color="b", label="Execution Time")
plt.plot(x_fit, y_fit, color='red', label=f'Exponential Fit: y = {a:.2f} * e^({b:.2f} * x)')

# Customize the plot
plt.xlabel("Numero de Variáveis (u)")
plt.ylabel("Execution Time (s)")
plt.title("Execution Time vs Complexity")
plt.grid(True)
plt.legend()

# Show the plot
plt.show()

# Print table
print(f"{'Factories':<10}{'Countries':<10}{'Children':<10}{'Complexity':<15}{'Execution Time (s)'}")
for r in results:
    print(f"{r[0]:<10}{r[1]:<10}{r[2]:<10}{r[3]:<15}{r[4]:.4f}")
