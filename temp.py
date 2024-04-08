import requests
import os
import csv
from time import sleep
import json

def init_data(file_paths):
    compound_foods = {}
    main_ingr = {}
    count = 0
    for file_path in file_paths:
        print(file_path)
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            # skip the header
            next(reader)
            for row in reader:
                # foods.append((row[0], row[1]))
                if row[1] != '':
                    compound_foods[row[0]] = 0
                    if row[0] != row[1]:
                        main_ingr[row[1]] = 0
                else:
                    compound_foods[row[0]] = 1
    return compound_foods, main_ingr

def main():
    # get the data for each food
    with open('conceptnet_data.json', 'r') as file:
        data = json.load(file)
    
    sense_label_dicts = {}
    
    sense_label_freq = {}
    
    food_set = set()
    count = 0
    st_count = 0
    for res in data:
        if 'sense_label' in res['end']:
            if res['end']['label'] not in food_set:
                food_set.add(res['end']['label'])
                count += 1
                
            sense_label_dicts[res['end']['label']] = res['end']['sense_label']

            if res['end']['sense_label'] in sense_label_freq:
                sense_label_freq[res['end']['sense_label']] += 1
            else:
                sense_label_freq[res['end']['sense_label']] = 1
        if 'sense_label' in res['start']:
            if res['start']['label'] not in food_set:
                food_set.add(res['start']['label'])
                st_count += 1
                
            sense_label_dicts[res['start']['label']] = res['start']['sense_label']

            if res['start']['sense_label'] in sense_label_freq:
                sense_label_freq[res['start']['sense_label']] += 1
            else:
                sense_label_freq[res['start']['sense_label']] = 1
    
    print(st_count)
    print(count)
    
    for key in sense_label_freq:
        print(f"{key}: {sense_label_freq[key]}")
    
    # save the data
    with open('sense_label.json', 'w') as file:
        json.dump(sense_label_dicts, file, indent=4)

    
if __name__ == '__main__':
    main()