import os
import textwrap

from src.database import export_query_result

if __name__ == '__main__':
    dir_path = 'output/'
    
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        
    query = textwrap.dedent(f"""\
        SELECT 
            KEY_SKILL_NAME, 
            COUNT(KEY_SKILL_NAME) AS KEY_SKILL_FREQUENCY 
        FROM 
            VACANCY_KEY_SKILLS 
        GROUP BY 
            KEY_SKILL_NAME 
        ORDER BY 
            KEY_SKILL_FREQUENCY DESC\
        """)
    file_path = f'{dir_path}key_skills_frequencies.csv'
    export_query_result(file_path, query)
    