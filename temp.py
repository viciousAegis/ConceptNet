import json

with open("food_stats.json", "r") as file:
    data = json.load(file)
    # count number of 1s and 0s
    counts = [0, 0]
    for item in data.values():
        counts[item] += 1

print(counts)