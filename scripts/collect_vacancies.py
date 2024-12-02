import logging
import os

from src.database import (conn, create_table_key_skills,
                          create_table_professional_roles,
                          create_table_vacancies,
                          create_table_vacancy_key_skills,
                          create_table_vacancy_professional_roles, cur,
                          insert_key_skills, insert_professional_roles,
                          insert_vacancies, insert_vacancy_key_skills,
                          insert_vacancy_professional_roles)
from src.parser import (get_page_num_count, get_vacancy_data_all,
                        get_vacancy_data_clean, get_vacancy_id_all,
                        get_vacancy_key_skills, get_vacancy_professional_roles)

log_dir = 'logs/'

if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logging.basicConfig(
    filename=f'{log_dir}collect_vacancies.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

if __name__ == '__main__':
    vacancy_data_clean_all = []
    vacancy_professional_roles_all = []
    vacancy_key_skills_all = []
    key_skill_all = set()
    professional_role_all = set()
    page_num_count = get_page_num_count()
    vacancy_id_all = get_vacancy_id_all(page_num_count)
    vacancy_data_all = get_vacancy_data_all(vacancy_id_all)
    logging.info(f'Вакансии собраны: {vacancy_data_all}')

    for vacancy_data in vacancy_data_all:
        vacancy_id = vacancy_data.get('id')
        vacancy_data_clean = get_vacancy_data_clean(vacancy_data)
        vacancy_professional_roles = get_vacancy_professional_roles(vacancy_data)
        vacancy_key_skills = get_vacancy_key_skills(vacancy_data)
        vacancy_data_clean_all.append(vacancy_data_clean)
        
        for vacancy_key_skill_data in vacancy_key_skills:
            vacancy_key_skill_name = vacancy_key_skill_data.get('name')
            key_skill_all.add(vacancy_key_skill_name)
            vacancy_key_skills_all.append((vacancy_id, vacancy_key_skill_name))
            
        for vacancy_professional_role_data in vacancy_professional_roles:
            vacancy_professional_role_name = vacancy_professional_role_data.get('name')
            professional_role_all.add(vacancy_professional_role_name)
            vacancy_professional_roles_all.append((vacancy_id, vacancy_professional_role_name))
            
    try:
        create_table_vacancies()
        create_table_key_skills()
        create_table_professional_roles()
        create_table_vacancy_key_skills()
        create_table_vacancy_professional_roles()
        insert_vacancies(vacancy_data_clean_all)
        insert_key_skills(key_skill_all)
        insert_professional_roles(professional_role_all)
        insert_vacancy_key_skills(vacancy_key_skills_all)
        insert_vacancy_professional_roles(vacancy_professional_roles_all)
        conn.commit()
        
    except Exception as e:
        print("An error occured:\n", e)
        conn.rollback()
        print('rollback performed')

    finally:
        cur.close()