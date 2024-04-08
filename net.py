import requests
import os
import csv
from time import sleep
import json

def get(url):
    response = requests.get(url).json()
    return response

def query_item(item):
    try:
        # if item has spaces, replace them with _
        item = item.lower().replace(" ", "_")
        obj = get(f"http://api.conceptnet.io/c/en/{item}?rel=/r/IsA&limit=1000")
        if 'error' in obj:
            print(obj['error'])
            return None
        return obj
    except Exception as e:
        print(e)
        return None

def init_data(file_paths):
    foods = []
    for file_path in file_paths:
        print(file_path)
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            # skip the header
            next(reader)
            for row in reader:
                foods.append((row[0], row[1]))
    return foods

def main():
    # file_paths = os.listdir("data")
    foods = init_data(['unique_ingr_with_main_ingr.csv'])
    # get the data for each food
    food_check_dict = {}
    # init json obj
    with open("data.json", "w") as file:
        json.dump([], file, indent=4) # empty list
    
    with open("food_stats.json", "w") as file:
        json.dump({}, file, indent=4)
    
    for food, main_ing in foods:
        if food in food_check_dict:
            continue
        print(food)
        obj = query_item(food)
        if obj is None:
            with open("food_stats.json", "r") as file:
                food_dict = json.load(file)
            food_dict[food] = 0
            with open("food_stats.json", "w") as file:
                json.dump(food_dict, file, indent=4)
            print(f"Could not find data for {food}")

            # try the main ingredient
            if main_ing in food_check_dict:
                continue
            
            obj = query_item(main_ing)
            if obj == None:
                print(f"Could not find data for {main_ing}")
                with open("food_stats.json", "r") as file:
                    food_dict = json.load(file)
                food_dict[main_ing] = 0
                with open("food_stats.json", "w") as file:
                    json.dump(food_dict, file, indent=4)
            else:
                print(f"Found data for {main_ing}")
                with open("food_stats.json", "r") as file:
                    food_dict = json.load(file)
                food_dict[main_ing] = 1
                with open("food_stats.json", "w") as file:
                    json.dump(food_dict, file, indent=4)
                for edge in obj["edges"]:
                    if edge['rel']['label'] == 'IsA':
                        data = {}
                        data['start'] = edge['start']
                        data['end'] = edge['end']
                        data['rel'] = edge['rel']
                        
                        # load the data from the file
                        with open("data.json", "r") as file:
                            dataset = json.load(file)
                        dataset.append(data)
                        with open("data.json", "w") as file:
                            json.dump(dataset, file, indent=4)
        else:
            print(f"Found data for {food}")
            with open("food_stats.json", "r") as file:
                food_dict = json.load(file)
            food_dict[food] = 1 # found data
            with open("food_stats.json", "w") as file:
                json.dump(food_dict, file, indent=4)
            for edge in obj["edges"]:
                if edge['rel']['label'] == 'IsA':
                    data = {}
                    data['start'] = edge['start']
                    data['end'] = edge['end']
                    data['rel'] = edge['rel']
                    
                    # load the data from the file
                    with open("data.json", "r") as file:
                        dataset = json.load(file)
                    dataset.append(data)
                    with open("data.json", "w") as file:
                        json.dump(dataset, file, indent=4)
        food_check_dict[food] = 1
        food_check_dict[main_ing] = 1
        sleep(2)

if __name__ == "__main__":
    main()
