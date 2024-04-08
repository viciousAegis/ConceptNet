import requests
import csv
import argparse

# Replace 'YOUR_APP_ID' and 'YOUR_APP_KEY' with your actual app ID and app key
app_id = "f788f9ed"
app_key = "b560345ad298986662e16696f5277cb7"


def query_food_database(ingredient_name, app_id, app_key):
    url = "https://api.edamam.com/api/food-database/v2/parser"
    params = {
        "ingr": ingredient_name,
        "app_id": app_id,
        "app_key": app_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None

def query_food_nutrients(food_id, app_id, app_key, uri):
    url = "https://api.edamam.com/api/food-database/v2/nutrients"
    params = {
        "app_id": app_id,
        "app_key": app_key
    }
    data = {
        "ingredients": [
            {
                "quantity": 1,
                "measureURI": uri,
                "foodId": food_id
            }
        ]
    }
    response = requests.post(url, params=params, json=data)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
        return None

def run(filename):
    ingredient_data = []
    # Open the CSV file containing ingredient list
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ingredient_name = row['Ingredient']
            print(ingredient_name)
            
            # Query the first access point to get food ID, nutrients, and category
            data = query_food_database(ingredient_name, app_id, app_key)
            try:
                if data:
                    # if hints is not empty
                    if not data['hints']:
                        print("No data found for", ingredient_name)
                        print(" ")
                        continue
                    food_id = data['hints'][0]['food']['foodId']
                    print(food_id)
                    nutrients = data['hints'][0]['food']['nutrients']
                    print(nutrients)
                    category = data['hints'][0]['food']['category']
                    print(category)

                    # if data['hints']['measures']:
                    label = data['hints'][0]['measures'][0]['label']
                    print(label)
                    weight = data['hints'][0]['measures'][0]['weight']
                    print(weight)
                    uri = data['hints'][0]['measures'][0]['uri']
                    print(uri)
                    
                    # Query the second access point to get health labels
                    health_labels = []
                    health_data = query_food_nutrients(food_id, app_id, app_key, uri)
                    if health_data:
                        health_labels = health_data.get('healthLabels', [])
                        print(health_labels)
                        print(" ")
                    
                    # Append data to the list
                    ingredient_data.append({
                        'ingredient_name': ingredient_name,
                        'food_id': food_id,
                        'category': category,
                        'nutrients': nutrients,
                        'health_labels': health_labels,
                        'label': label,
                        'weight': weight,
                        'uri': uri
                    })
            except:
                print("No data found for", ingredient_name)
                ingredient_data.append({
                    'ingredient_name': ingredient_name,
                    'food_id': None,
                    'category': None,
                    'nutrients': None,
                    'health_labels': None,
                    'label': None,
                    'weight': None,
                    'uri': None
                })
                continue
    return ingredient_data

def save(output_file, ingredient_data):
    fieldnames = ['ingredient_name', 'food_id', 'category', 'nutrients', 'health_labels', 'label', 'weight', 'uri']

    # Write the data to the new CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        
        # Write each item in ingredient_data to the CSV file
        for item in ingredient_data:
            writer.writerow({
                'ingredient_name': item['ingredient_name'],
                'food_id': item['food_id'],
                'category': item['category'],
                'nutrients': item['nutrients'],
                'health_labels': ', '.join(item['health_labels']),
                'label': item['label'],
                'weight': item['weight'],
                'uri': item['uri']
            })

    print(f"Data has been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the Edamam Food Database API")
    parser.add_argument("filename", help="The name of the input CSV file")
    args = parser.parse_args()

    outfile = args.filename.split(".")[0] + "_output.csv"
    
    ingredient_data = run(args.filename)
    save(outfile, ingredient_data)