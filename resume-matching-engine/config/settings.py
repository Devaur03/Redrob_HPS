import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')

RESUMES_PATH = os.path.join(DATA_DIR, 'resumes.csv')
JOB_DESCRIPTIONS_PATH = os.path.join(DATA_DIR, 'job_descriptions.csv')
SKILL_ALIASES_PATH = os.path.join(DATA_DIR, 'skill_aliases.json')

DEBUG = False
