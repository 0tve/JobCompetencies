import time
from typing import Any

import requests

from database_manager import (conn, create_table_key_skills,
                              create_table_professional_roles,
                              create_table_vacancies,
                              create_table_vacancy_key_skills,
                              create_table_vacancy_professional_roles, cur,
                              insert_key_skills, insert_professional_roles,
                              insert_vacancies, insert_vacancy_key_skills,
                              insert_vacancy_professional_roles)
from secret import access_token, app_name, email

vacancy_request_url = 'https://api.hh.ru/vacancies/'
vacancy_search_text = "Frontend-разработчик"
vacancy_search_areas = [1, 2]
vacancy_search_period = 1825
experience_ranges_by_name = {
    'Нет опыта': [0, 0],
    'От 1 года до 3 лет': [1, 3],
    'От 3 до 6 лет': [3, 6],
    'Более 6 лет': [6, None],
    None: [None, None]
}

def get_page_num_count() -> int:
    time.sleep(0.15)
    return requests.get(
        url = vacancy_request_url,
        params = {
            'text': vacancy_search_text,
            'area': vacancy_search_areas,
            'period': vacancy_search_period 
        },
        headers = {
            'User-Agent': f'{app_name} ({email})',
            'Authorization': f'Bearer {access_token}'  
        }
    ).json()['pages']

def get_vacancy_page(page_num: int) -> dict[str, Any]:
    time.sleep(0.15)
    return requests.get(
        url = vacancy_request_url,
        params = {
            'text': vacancy_search_text,
            'area': vacancy_search_areas,
            'period': vacancy_search_period,
            'page': page_num
        },
        headers = {
            'User-Agent': f'{app_name} {email}',
            'Authorization': f'Bearer {access_token}'
        }
    ).json()['items']

def get_vacancy_id_all(page_num_count: int) -> list[str]:
    vacancy_id_all = []
    
    for page_num in range(page_num_count):
        vacancy_page = get_vacancy_page(page_num)
        vacancy_id_all.extend(vacancy_preview_data['id'] for vacancy_preview_data in vacancy_page)
        
    return vacancy_id_all

def get_vacancy_data(vacancy_id: str) -> dict[str, Any]:
    time.sleep(0.15)
    return requests.get(
        url = f'{vacancy_request_url}{vacancy_id}/',
        headers = {
            'User-Agent': f'{app_name} ({email})',
            'Authorization': f'Bearer {access_token}'
        }
    ).json()

def get_vacancy_data_all(vacancy_id_all: list[str]) -> list[dict[str, Any]]:
    vacancy_data_all = []
    
    for i, vacancy_id in enumerate(vacancy_id_all):
        vacancy_data = get_vacancy_data(vacancy_id)
        
        if 'errors' in vacancy_data:
            break
              
        vacancy_data_all.append(vacancy_data)
    
    return vacancy_data_all

def get_vacancy_key_skills(vacancy_data: dict[str, Any]) -> list[dict[str, Any]]:
    vacancy_key_skills = vacancy_data.get('key_skills')
    return vacancy_key_skills if vacancy_key_skills != None else {}

def get_vacancy_professional_roles(vacancy_data: dict[str, Any]) -> list[dict[str, Any]]:
    vacancy_professional_roles = vacancy_data.get('professional_roles')
    return vacancy_professional_roles if vacancy_professional_roles != None else {}

def get_vacancy_data_clean(vacancy_data: dict[str, Any]) -> tuple[str, str, bool, bool, str, int, int, str, bool, int, int, str, str, str, str, str]:
    vacancy_id = vacancy_data.get('id')
    vacancy_employer = vacancy_data.get('employer')
    vacancy_salary = vacancy_data.get('salary')
    vacancy_experience = vacancy_data.get('experience')
    vacancy_employment = vacancy_data.get('employment')
    vacancy_schedule = vacancy_data.get('schedule')
    vacancy_area = vacancy_data.get('area')
    vacancy_description = vacancy_data.get('description')
    vacancy_employer = {} if vacancy_employer == None else vacancy_employer
    vacancy_employer_rating = vacancy_employer.get('employer_rating')
    vacancy_employer_rating = {} if vacancy_employer_rating == None else vacancy_employer_rating
    vacancy_salary = {} if vacancy_salary == None else vacancy_salary
    vacancy_experience = {} if vacancy_experience == None else vacancy_experience
    vacancy_employment = {} if vacancy_employment == None else vacancy_employment
    vacancy_schedule = {} if vacancy_schedule == None else vacancy_schedule
    vacancy_area = {} if vacancy_area == None else vacancy_area
    vacancy_experience_from, vacancy_experience_to = experience_ranges_by_name[vacancy_experience.get('name')]
    return (
        vacancy_id,
        vacancy_employer.get('name'),
        vacancy_employer.get('trusted'),
        vacancy_employer.get('accredited_it_employer'),
        vacancy_employer_rating.get('total_rating'),
        vacancy_salary.get('from'),
        vacancy_salary.get('to'),
        vacancy_salary.get('currency'),
        vacancy_salary.get('gross'),
        vacancy_experience_from,
        vacancy_experience_to,
        vacancy_employment.get('name'),
        vacancy_schedule.get('name'),
        vacancy_description,
        vacancy_search_text,
        vacancy_area.get('name'),
    )
    
def main() -> None:
    vacancy_data_clean_all = []
    vacancy_professional_roles_all = []
    vacancy_key_skills_all = []
    key_skill_all = set()
    professional_role_all = set()
    page_num_count = get_page_num_count()
    vacancy_id_all = get_vacancy_id_all(page_num_count)
    vacancy_data_all = get_vacancy_data_all(vacancy_id_all)

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
    
if __name__ == '__main__':
    main()