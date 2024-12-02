import json

import pandas as pd

from src.model import replace_rare_with_frequent

if __name__ == '__main__':
    output_path = 'output/'
    key_skills_rare_to_frequent_path = f'{output_path}key_skills_rare_to_frequent.json'
    print('Введите имя csv-файла: ', end='')
    csv_name = input()
    df = pd.read_csv(f'{output_path}{csv_name}.csv')
    key_skills_rare_to_frequent = {}
    
    with open(key_skills_rare_to_frequent_path, encoding='utf-8') as f:
        key_skills_rare_to_frequent = json.load(f)
        
    df = replace_rare_with_frequent(df, 'key_skill_name', key_skills_rare_to_frequent)
    df.to_csv(f'{output_path}{csv_name}_replaced.csv', index=False)
    