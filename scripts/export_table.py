import os

from src.database import export_table

if __name__ == '__main__':
    dir_path = 'output/'
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    
    print('Введите название таблицы:', end=' ')
    table_name = input()
    file_path = f'{dir_path}{table_name}.csv'
    export_table(file_path, table_name)