import os
import subprocess

if __name__ == '__main__':
    # get the file paths 
    file_paths = []
    for root, dirs, files in os.walk("mquery"):
        for file in files:
            if file.endswith(".csv"):
                file_paths.append(os.path.join(root, file))
    
    # run the mquery.py script parallelly for each file
    for file_path in file_paths:
        subprocess.Popen(["python", "mquery.py", file_path])