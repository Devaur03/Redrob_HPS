import sys
import os

# Add the root directory to sys.path so we can import config and app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import RESUMES_PATH, JOB_DESCRIPTIONS_PATH, SKILL_ALIASES_PATH, DEBUG
from app.models.skill_alias import SkillAliasLoader
from app.services.resume_service import ResumeService
from app.services.job_description_service import JobDescriptionService
from app.services.matching_service import MatchingService

def main():
    # 1. Load configuration and aliases
    if DEBUG:
        print("Loading Skill Aliases...")
    skill_aliases = SkillAliasLoader.load_aliases(SKILL_ALIASES_PATH)

    # 2. Initialize services
    resume_service = ResumeService(skill_aliases)
    jd_service = JobDescriptionService(skill_aliases)

    # 3. Load and process resumes
    if DEBUG:
        print("Loading and Processing Resumes...")
    resumes = resume_service.load_resumes(RESUMES_PATH)
    vocabulary, df = resume_service.process_resumes(resumes)
    
    if DEBUG:
        print(f"Vocabulary Size: {len(vocabulary)}")

    # 4. Load and process job descriptions
    if DEBUG:
        print("Loading and Processing Job Descriptions...")
    jds = jd_service.load_job_descriptions(JOB_DESCRIPTIONS_PATH)
    jd_service.process_job_descriptions(jds, vocabulary)

    # 5. Rank candidates and output
    for jd in jds:
        print(f"{jd.name}:")
        top_3 = MatchingService.rank_candidates(jd, resumes)
        for name, score in top_3:
            print(f"{name} ({score:.2f})")
        print()

if __name__ == "__main__":
    main()
