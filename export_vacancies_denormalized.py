from database_manager import export_vacancies_denormalized

if __name__ == '__main__':
    print('Set file name:', end=' ')
    file_name = input()
    export_vacancies_denormalized(f'{file_name}.csv')