import csv

def split(file, num_parts=2):
    # read the file
    contents = [[] for _ in range(num_parts)]
    with open(file, "r") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            contents[i % num_parts].append(row)
    
    # write the files
    for i, content in enumerate(contents):
        with open(f"{i}__{file}.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(content)

if __name__ == "__main__":
    split("unique_ingr_with_main_ingr.csv", 4)