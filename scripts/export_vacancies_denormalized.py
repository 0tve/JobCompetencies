import os
import textwrap

from src.database import export_query_result

if __name__ == '__main__':
    dir_path = 'output/'
    file_path = f'{dir_path}vacancies_denormalized.csv'
    query = textwrap.dedent(f"""\
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
        ) AS vpr ON vpr.vacancy_id = v.vacancy_id\
        """)
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    export_query_result(file_path, query)
