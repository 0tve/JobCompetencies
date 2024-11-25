import os
import textwrap

from src.database import export_query_result

if __name__ == '__main__':
    dir_path = 'output/'
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    query = textwrap.dedent(f"""\
        SELECT
            VPR.PROFESSIONAL_ROLE_NAME,
            VKS.KEY_SKILL_NAME,
            V.VACANCY_EMPLOYER_NAME,
            V.VACANCY_EMPLOYER_TRUSTED,
            V.VACANCY_EMPLOYER_IT_ACCREDITED,
            V.VACANCY_SALARY_FROM,
            V.VACANCY_SALARY_TO,
            V.VACANCY_SALARY_CURRENCY,
            V.VACANCY_SALARY_GROSS,
            V.VACANCY_EXPERIENCE_FROM,
            V.VACANCY_EXPERIENCE_TO,
            V.VACANCY_EMPLOYMENT_NAME,
            V.VACANCY_SCHEDULE_NAME,
            V.VACANCY_SEARCH_TEXT,
            V.VACANCY_AREA
        FROM
            VACANCIES AS V
        JOIN 
            VACANCY_KEY_SKILLS AS VKS 
        ON 
            V.VACANCY_ID = VKS.VACANCY_ID
        JOIN 
            VACANCY_PROFESSIONAL_ROLES AS VPR 
        ON 
            V.VACANCY_ID = VPR.VACANCY_ID\
        """)
    file_path = f'{dir_path}df.csv'
    export_query_result(file_path, query)