import json
import math
import random
import csv

# STEP 1: Read input file
# You can change file name here to run different test cases
with open("data.json", "r") as file:
    data = json.load(file)

# STEP 2: Prepare warehouse data
# Sometimes data is in list format, sometimes in dictionary
# So handling both cases
if isinstance(data["warehouses"], list):
    warehouse_dict = {w["id"]: w["location"] for w in data["warehouses"]}
else:
    warehouse_dict = data["warehouses"]

# STEP 3: Prepare agent data (same logic as warehouses)
if isinstance(data["agents"], list):
    agent_dict = {a["id"]: a["location"] for a in data["agents"]}
else:
    agent_dict = data["agents"]

# Get packages list
packages = data["packages"]

# BONUS: Adding one new agent dynamically
# This simulates a new agent joining during the day
agent_dict["A_new"] = [50, 50]

# STEP 4: Function to calculate distance between two points
def distance(p1, p2):
    # Using Euclidean distance formula
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# STEP 5: Assign each package to nearest agent
assignment = {}

for package in packages:

    # Package may have key "warehouse_id" or "warehouse"
    if "warehouse_id" in package:
        warehouse_id = package["warehouse_id"]
    else:
        warehouse_id = package["warehouse"]

    warehouse_loc = warehouse_dict[warehouse_id]

    min_dist = float("inf")   # start with very large value
    assigned_agent = None

    # Check distance from all agents to this warehouse
    for agent_id, agent_loc in agent_dict.items():
        d = distance(agent_loc, warehouse_loc)

        # Select agent with minimum distance
        if d < min_dist:
            min_dist = d
            assigned_agent = agent_id

    # Store assigned package
    assignment.setdefault(assigned_agent, []).append(package)

# STEP 6: Simulate delivery and calculate report
report = {}

for agent_id, agent_packages in assignment.items():
    total_distance = 0
    agent_loc = agent_dict[agent_id]

    for package in agent_packages:

        # Again handling both key formats
        if "warehouse_id" in package:
            warehouse_id = package["warehouse_id"]
        else:
            warehouse_id = package["warehouse"]

        warehouse_loc = warehouse_dict[warehouse_id]
        destination = package["destination"]

        # Distance: agent → warehouse
        d1 = distance(agent_loc, warehouse_loc)

        # Distance: warehouse → destination
        d2 = distance(warehouse_loc, destination)

        # BONUS: adding small random delay to simulate real-world scenario
        delay = random.uniform(1, 5)

        total_distance += (d1 + d2 + delay)

        # BONUS: simple route display
        print(f"{agent_id} -> {warehouse_id} -> {destination}")

    # Number of packages delivered by this agent
    count = len(agent_packages)

    # Efficiency = average distance per package
    efficiency = total_distance / count if count > 0 else 0

    # Store result
    report[agent_id] = {
        "packages_delivered": count,
        "total_distance": round(total_distance, 2),
        "efficiency": round(efficiency, 2)
    }

# STEP 7: Find best agent (lowest efficiency is better)
best_agent = min(report, key=lambda x: report[x]["efficiency"])
report["best_agent"] = best_agent

# STEP 8: Save report to JSON file
with open("report.json", "w") as file:
    json.dump(report, file, indent=4)

# BONUS: Save best agent details into CSV file
best = report["best_agent"]

with open("best_agent.csv", "w", newline="") as file:
    writer = csv.writer(file)

    # Header row
    writer.writerow(["Agent ID", "Packages Delivered", "Total Distance", "Efficiency"])

    # Data row
    writer.writerow([
        best,
        report[best]["packages_delivered"],
        report[best]["total_distance"],
        report[best]["efficiency"]
    ])

print("\nReport generated successfully!")
print(f"Best Agent: {best_agent}")
