import re

from resume_parser import DEGREE_RE, SKILLS, YEARS_EXPLICIT_RE

DEGREE_REQUIRED_RE = re.compile(r'\b(Bachelor|Master|Ph\.?D|B\.?S\.?|M\.?S\.?|M\.?B\.?A\.?|degree)\b', re.I)


def analyze_jd(text):
    required=[]
    preferred=[]
    for name, aliases in SKILLS:
        hit=None
        for alias in aliases:
            try:
                hit=re.search(r'\b(?:'+alias+r')\b',text,re.I)
            except re.error:
                hit=re.search(alias,text,re.I)
            if hit: break
        if not hit: continue
        before=text[max(0,hit.start()-60):hit.start()].lower()
        (preferred if re.search(r'(preferred|nice to have|bonus|plus)[^.]*$',before) else required).append(name)
    match=YEARS_EXPLICIT_RE.search(text)
    return {'skills':{'required':required,'preferred':preferred},'minYears':int(match.group(1)) if match else None,'degreeRequired':bool(DEGREE_REQUIRED_RE.search(text))}
