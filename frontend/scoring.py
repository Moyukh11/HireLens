def score(candidate, job_description):
    required=job_description['skills']['required']
    preferred=job_description['skills']['preferred']
    candidate_skills=set(candidate['skills'])
    matched_required=[skill for skill in required if skill in candidate_skills]
    missing_required=[skill for skill in required if skill not in candidate_skills]
    matched_preferred=[skill for skill in preferred if skill in candidate_skills]
    missing_preferred=[skill for skill in preferred if skill not in candidate_skills]
    if not required and not preferred:
        skill_score=1
    else:
        required_score=len(matched_required)/len(required) if required else 1
        preferred_score=len(matched_preferred)/len(preferred) if preferred else 1
        skill_score=required_score*.85+preferred_score*.15 if required else preferred_score
    experience_score=1
    experience_note='Not specified in job description'
    if job_description['minYears'] is not None:
        years=candidate['experienceYears']
        if years is None:
            experience_score=.5
            experience_note=f"Requires {job_description['minYears']}+ yrs — candidate's experience length couldn't be read"
        elif years>=job_description['minYears']:
            experience_note=f"Meets the {job_description['minYears']}+ yr requirement ({years} yrs found)"
        else:
            experience_score=max(0,years/job_description['minYears'])
            experience_note=f"Below the {job_description['minYears']}+ yr requirement ({years} yrs found)"
    education_score=1
    education_note='Not specified in job description'
    if job_description['degreeRequired']:
        if candidate['education']:
            education_note='Degree found on resume'
        else:
            education_score=.4
            education_note='Job description implies a degree; none detected on resume'
    total=skill_score*.7+experience_score*.2+education_score*.1
    return {'score':round(total*100),'matchedRequired':matched_required,'missingRequired':missing_required,'matchedPreferred':matched_preferred,'missingPreferred':missing_preferred,'breakdown':{'skills':round(skill_score*100),'experience':round(experience_score*100),'education':round(education_score*100),'experienceNote':experience_note,'educationNote':education_note}}
