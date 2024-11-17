from src.database import export_table_to_csv

if __name__ == '__main__':
    print('Введите название таблицы:', end=' ')
    table_name = input()
    export_table_to_csv(table_name)