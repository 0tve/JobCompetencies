import json

import pandas as pd
from imblearn.under_sampling import RandomUnderSampler
from sklearn.linear_model import LogisticRegression

from src.model import get_features_coefs_by_class

if __name__ == '__main__':
    data_path = 'data/'
    print('Введите имя csv-файла: ', end='')
    csv_name = input()
    df = pd.read_csv(f'{data_path}{csv_name}.csv')
    value_counts = df['professional_role_name'].value_counts()
    df = df[df['professional_role_name'].isin(value_counts[value_counts >= 1000].index)]
    X = df['key_skill_name']
    y = df['professional_role_name']
    X = pd.get_dummies(X)
    undersampler = RandomUnderSampler(random_state=42)
    X, y = undersampler.fit_resample(X, y)
    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X, y)
    maps = get_features_coefs_by_class(model, X.columns, 10)
    
    with open(f'{data_path}maps.json', 'w+', encoding='utf-8') as f:
        json.dump(maps, f, ensure_ascii=False, indent=4)
    