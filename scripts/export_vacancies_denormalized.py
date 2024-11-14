import os

from src.database import export_vacancies_denormalized

if __name__ == '__main__':
    dir_path = 'output/'
    file_path = f'{dir_path}vacancies_denormalized.csv'
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    export_vacancies_denormalized(file_path)