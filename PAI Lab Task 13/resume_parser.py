import spacy
import re

nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "python", "java", "c++", "machine learning", "deep learning",
    "sql", "flask", "django", "html", "css", "javascript",
    "data analysis", "pandas", "numpy", "tensorflow"
]

JOB_SKILLS = ["python", "machine learning", "sql", "data analysis"]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))


def get_total_experience_months(text):
    text = text.lower()

    years = re.findall(r'(\d+)\s*(?:years?|yrs?)', text)
    months = re.findall(r'(\d+)\s*(?:months?|mos?)', text)

    total = 0

    if years:
        total += int(years[0]) * 12
    if months:
        total += int(months[0])

    return total

def calculate_score(skills, match_percent):
    base_score = match_percent * 0.7   # 70% weight to job match
    bonus = (len(skills) / len(SKILLS_DB)) * 30  # 30% bonus for extra skills

    return round(base_score + bonus, 2)


def job_match(skills):
    missing = list(set(JOB_SKILLS) - set(skills))
    matched = list(set(JOB_SKILLS).intersection(set(skills)))

    match_percent = (len(matched) / len(JOB_SKILLS)) * 100

    return matched, missing, round(match_percent, 2)


def analyze_resume(text):
    skills = extract_skills(text)

    total_exp_months = get_total_experience_months(text)

    matched, missing, match_percent = job_match(skills)

    score = calculate_score(skills, match_percent)

    if match_percent == 100 and total_exp_months >= 36:
        score = 100

    feedback = []

    if len(skills) < 4:
        feedback.append("Add more relevant technical skills.")

    if total_exp_months < 12:
        feedback.append("Try to gain more practical experience.")

    if match_percent < 50:
        feedback.append("Your resume does not match the job well.")

    if score == 100:
        feedback.append("Excellent! Perfect match for the job.")

    elif score > 70:
        feedback.append("Strong resume!")

    return {
        "skills": skills,
        "experience": f"{total_exp_months // 12} years",
        "score": score,
        "matched": matched,
        "missing": missing,
        "match_percent": match_percent,
        "feedback": feedback
    }