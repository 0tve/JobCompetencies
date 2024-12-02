import json
import os

import pandas as pd
from sentence_transformers import SentenceTransformer

from src.model import get_rare_to_frequent, get_similar_clusters

if __name__ == '__main__':
    models_path = 'models/'
    output_path = 'output/'
    model_name = 'distiluse-base-multilingual-cased-v1'
    similarity_threshold = 0.8
    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    df_path = f'{output_path}key_skills_frequencies.csv'
    df = pd.read_csv(df_path)
    key_skills_names = df['key_skill_name'].tolist()
    key_skills_frequencies = dict(zip(df['key_skill_name'], df['key_skill_frequency']))
    
    if os.path.exists(f'{models_path}{model_name}'):
        model = SentenceTransformer(f'{models_path}{model_name}')

    else:
        model = SentenceTransformer(f"sentence-transformers/{model_name}")
        model.save(f'{models_path}{model_name}')
        
    similar_key_skills_clusters = get_similar_clusters(model, similarity_threshold, key_skills_names)
    key_skills_rare_to_frequent = get_rare_to_frequent(similar_key_skills_clusters, key_skills_frequencies)
    
    with open(f'{output_path}key_skills_rare_to_frequent.json', 'w+', encoding='utf-8') as f:
        json.dump(key_skills_rare_to_frequent, f, ensure_ascii=False, indent=4)