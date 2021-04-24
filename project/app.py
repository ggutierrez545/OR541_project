import gurobipy as gp
import numpy as np
import time
from data_generation.generate import generate_data

start = time.time()
print("Generating data...")
personnel, specialties, skills, grades, units, bins, sbs = generate_data()
print(f"...completed in {round(time.time() - start, 2)}s\n")
now = time.time()

print("Initializing model...")
model = gp.Model('OR541_Project')
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Setting up assignment cost matrices...")
grade_cost_matrix = np.zeros((len(personnel), len(bins)))
skills_cost_matrix = np.zeros((len(personnel), len(bins)))
specialty_cost_matrix = np.zeros((len(personnel), len(bins)))
billet_preference_cost_matrix = np.zeros((len(personnel), len(bins)))
personnel_preference_cost_matrix = np.zeros((len(personnel), len(bins)))

for i, person in enumerate(personnel):
    for j, billet in enumerate(bins):
        # Calculate grade cost
        if person.grade in billet.grade_subs_pool:
            if person.grade != billet.grade:
                grade_cost_matrix[i][j] = 10
        else:
            grade_cost_matrix[i][j] = 1000

        # Calculate skills cost
        for z, skill in enumerate(billet.skills):
            if skill not in person.skills:
                skills_cost_matrix[i][j] += (z+1)*5

        # Calculate specialty cost
        if billet.specialty not in person.specialties:
            specialty_cost_matrix[i][j] = 1000

        # Calculate person's preferential cost
        if billet in person.ranked_billets:
            preference_spot = person.ranked_billets.index(billet)
        else:
            preference_spot = len(person.ranked_billets) + 1
        personnel_preference_cost_matrix[i][j] = preference_spot

        # Calculate billet's preferential cost
        if person in billet.ranked_personnel:
            preference_spot = billet.ranked_personnel.index(person)
        else:
            preference_spot = len(billet.ranked_personnel) + 1
        billet_preference_cost_matrix[i][j] = preference_spot

total_cost_matrix = grade_cost_matrix + skills_cost_matrix + specialty_cost_matrix + personnel_preference_cost_matrix + billet_preference_cost_matrix
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

# Decision Variables
print("Defining decision variables...")
ASSIGN = model.addMVar((len(personnel), len(bins)), vtype=gp.GRB.BINARY, name='ASSIGN')
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Defining objective function...")
model.setObjective(sum(total_cost_matrix[p].reshape(1, -1) @ ASSIGN[p] for p in range(len(personnel))), gp.GRB.MINIMIZE)
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Defining billet constraints...")
for billet in range(len(bins)):
    model.addConstr(ASSIGN[:, billet].sum() <= 1, name='Billet may or may not be filled')
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Defining unit fill constraints...")
for unit in units:
    unit_size = len(unit.billets)
    ASSIGN_VARS = []
    for billet in unit.billets:
        b_idx = bins.index(billet)
        ASSIGN_VARS.append(ASSIGN[:, b_idx])
    model.addConstr(sum(ASSIGN_VAR.sum() for ASSIGN_VAR in ASSIGN_VARS) / unit_size >= 0.8, name="Unit Fill Constraint")
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Defining personnel assignment constraints...")
for person in range(len(personnel)):
    model.addConstr(ASSIGN[person, :].sum() == 1, name="Person must be assigned")
print(f"...completed in {round(time.time() - now, 2)}s\n")
now = time.time()

print("Optimizing...")
model.optimize()
print(f"...completed in {round(time.time() - now, 2)}s")
now = time.time()
