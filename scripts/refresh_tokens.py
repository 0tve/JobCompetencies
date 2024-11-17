import json
import os

from src.tokens import refresh_tokens

if __name__ == '__main__':
    dir_path = 'output/'
    file_path = f"{dir_path}refresh_tokens.txt"
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    with open(file_path, 'w') as f:
        json.dump(refresh_tokens(), f, indent=4)