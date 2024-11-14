import textwrap
from typing import Any

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import execute_values

from cfg.secret import database_config
from cfg.database_cfg import (key_skills_fields, professional_roles_fields,
                               vacancies_fields, vacancy_key_skills_fields,
                               vacancy_professional_roles_fields)

conn: connection = psycopg2.connect(**database_config)
cur = conn.cursor()

def create_table_vacancies() -> None:
    cur.execute(textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id VARCHAR(255),
            vacancy_employer_name VARCHAR(255),
            vacancy_employer_trusted BOOLEAN,
            vacancy_employer_it_accredited BOOLEAN,
            vacancy_employer_total_rating VARCHAR(255),
            vacancy_salary_from INT,
            vacancy_salary_to INT,
            vacancy_salary_currency VARCHAR(3),
            vacancy_salary_gross BOOLEAN,
            vacancy_experience_from INT,
            vacancy_experience_to INT,
            vacancy_employment_name VARCHAR(255),
            vacancy_schedule_name VARCHAR(255),
            vacancy_description TEXT,
            vacancy_search_text TEXT,
            vacancy_area VARCHAR(100),
            PRIMARY KEY (vacancy_id)
        );\
        """))
    
def create_table_key_skills() -> None:
    cur.execute(textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS key_skills (
            key_skill_name VARCHAR(255),
            PRIMARY KEY (key_skill_name)
        );\
        """))
    
def create_table_professional_roles() -> None:
    cur.execute(textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS professional_roles (
            professional_role_name VARCHAR(255),
            PRIMARY KEY (professional_role_name)
        );\
        """))
    
def create_table_vacancy_key_skills() -> None:
    cur.execute(textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS vacancy_key_skills (
            vacancy_id VARCHAR(255) REFERENCES vacancies(vacancy_id),
            key_skill_name VARCHAR(255) REFERENCES key_skills(key_skill_name),
            PRIMARY KEY (vacancy_id, key_skill_name)
        );\
        """))
    
def create_table_vacancy_professional_roles() -> None:
    cur.execute(textwrap.dedent(f"""\
        CREATE TABLE IF NOT EXISTS vacancy_professional_roles (
            vacancy_id VARCHAR(255) REFERENCES vacancies(vacancy_id),
            professional_role_name VARCHAR(255) REFERENCES professional_roles(professional_role_name),
            PRIMARY KEY (vacancy_id, professional_role_name)
        );\
        """))

def insert_vacancies(vacancy_data_clean_all: list[dict[str, Any]]) -> None:
    execute_values(
        cur,
        textwrap.dedent(f"""\
            INSERT INTO vacancies ({', '.join(vacancies_fields)})
            VALUES %s
            ON CONFLICT DO NOTHING;\
            """),
        vacancy_data_clean_all
    )   
    
def insert_key_skills(key_skill_all: set[str]) -> None:
    execute_values(
        cur,
        textwrap.dedent(f"""\
            INSERT INTO key_skills ({', '.join(key_skills_fields)})
            VALUES %s
            ON CONFLICT DO NOTHING;\
            """),
        [(key_skill, ) for key_skill in key_skill_all]
    )    
    
def insert_professional_roles(professional_role_all: set[str]) -> None:
    execute_values(
        cur,
        textwrap.dedent(f"""\
            INSERT INTO professional_roles ({', '.join(professional_roles_fields)})
            VALUES %s
            ON CONFLICT DO NOTHING;\
            """),
        [(professional_role, ) for professional_role in professional_role_all]
    )
        
def insert_vacancy_key_skills(vacancy_key_skills_all: list[tuple[str, str]]) -> None:
    execute_values(
        cur,
        textwrap.dedent(f"""\
            INSERT INTO vacancy_key_skills ({', '.join(vacancy_key_skills_fields)})
            VALUES %s
            ON CONFLICT DO NOTHING;\
            """),
        vacancy_key_skills_all
    )
        
def insert_vacancy_professional_roles(vacancy_professional_roles_all: list[tuple[str, str]]) -> None:
    execute_values(
        cur,
        textwrap.dedent(f"""\
            INSERT INTO vacancy_professional_roles ({', '.join(vacancy_professional_roles_fields)})
            VALUES %s
            ON CONFLICT DO NOTHING;\
            """),
        vacancy_professional_roles_all
    )
    
def export_vacancies_denormalized(file_path: str):
    
    with open(file_path, 'w+', encoding='utf-8') as f:
        cur.copy_expert(
            textwrap.dedent(f"""\
                COPY (
                    SELECT
                        v.*,
                        vks.vacancy_key_skills,
                        vpr.vacancy_professional_roles
                    FROM vacancies AS v
                    LEFT JOIN (
                        SELECT vks.vacancy_id,
                            STRING_AGG(REPLACE(vks.key_skill_name, ' ', '_'), ' ') AS vacancy_key_skills
                        FROM vacancy_key_skills AS vks
                        GROUP BY vks.vacancy_id
                    ) AS vks ON vks.vacancy_id = v.vacancy_id
                    LEFT JOIN (
                        SELECT vpr.vacancy_id,
                            STRING_AGG(REPLACE(vpr.professional_role_name, ' ', '_'), ' ') AS vacancy_professional_roles
                        FROM vacancy_professional_roles AS vpr
                        GROUP BY vpr.vacancy_id
                    ) AS vpr ON vpr.vacancy_id = v.vacancy_id
                ) TO STDOUT WITH (
                        FORMAT csv,
                        ENCODING 'UTF8',
                        HEADER true
                    );\
                """),
            f
        )