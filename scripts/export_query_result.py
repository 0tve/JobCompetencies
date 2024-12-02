import os
import textwrap

from src.database import export_query_result

if __name__ == '__main__':
    dir_path = 'output/'
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    print('Введите запрос:')
    query = textwrap.dedent(input())
    print('Введите имя файла:', end=' ')
    file_name = input()
    file_path = f'{dir_path}{file_name}.csv'
    export_query_result(file_path, query)
    