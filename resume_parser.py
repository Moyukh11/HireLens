import io
import re
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None
try:
    from docx import Document
except Exception:
    Document = None

SKILLS = [
('JavaScript',['js','javascript','es6']),('TypeScript',['typescript','ts']),('Python',['python','py']),('Java',['java']),('C++',[r'c\+\+','cpp']),('C#',['c#','csharp']),('Go',['golang']),('Rust',['rust']),('Ruby',['ruby']),('PHP',['php']),('Swift',['swift']),('Kotlin',['kotlin']),('Scala',['scala']),('R',[r'\br\b(?=.*(stat|data|analysis))']),('SQL',['sql']),('HTML',['html','html5']),('CSS',['css','css3']),
('React',['react',r'react\.js','reactjs']),('Vue.js',['vue',r'vue\.js','vuejs']),('Angular',['angular','angularjs']),('Next.js',[r'next\.js','nextjs']),('Svelte',['svelte']),('Redux',['redux']),('Tailwind CSS',['tailwind']),
('Node.js',[r'node\.js','nodejs','node']),('Express.js',[r'express\.js','express']),('Django',['django']),('Flask',['flask']),('Spring Boot',['spring boot','spring']),('Ruby on Rails',['rails','ruby on rails']),('.NET',[r'\.net','dotnet']),('GraphQL',['graphql']),('REST APIs',['rest api','restful',r'\brest\b']),
('Machine Learning',['machine learning',r'\bml\b']),('Deep Learning',['deep learning']),('TensorFlow',['tensorflow']),('PyTorch',['pytorch']),('NLP',['nlp','natural language processing']),('Pandas',['pandas']),('NumPy',['numpy']),('Data Analysis',['data analysis','data analytics']),('Data Visualization',['data visualization','tableau','power bi']),('ETL',['etl','data pipelines']),
('PostgreSQL',['postgresql','postgres']),('MySQL',['mysql']),('MongoDB',['mongodb','mongo']),('Redis',['redis']),('Elasticsearch',['elasticsearch']),('SQLite',['sqlite']),
('AWS',['aws','amazon web services']),('Azure',['azure']),('Google Cloud',['gcp','google cloud']),('Docker',['docker']),('Kubernetes',['kubernetes','k8s']),('CI/CD',['ci/cd','continuous integration','continuous deployment']),('Terraform',['terraform']),('Linux',['linux']),('Git',['git','github','gitlab']),
('Product Management',['product management','product manager']),('Agile',['agile','scrum']),('Figma',['figma']),('UX Design',['ux design','user experience']),('UI Design',['ui design','user interface design']),('Roadmapping',['roadmap','roadmapping']),('A/B Testing',['a/b testing','ab testing']),
('Project Management',['project management']),('Stakeholder Management',['stakeholder management']),('Salesforce',['salesforce']),('SEO',['seo','search engine optimization']),('Content Marketing',['content marketing']),('Digital Marketing',['digital marketing']),('Financial Modeling',['financial modeling','financial modelling']),('Excel',['excel','microsoft excel']),('Negotiation',['negotiation']),('Budgeting',['budgeting','budget management']),
('Leadership',['leadership']),('Communication',['communication skills',r'\bcommunication\b']),('Cross-functional Collaboration',['cross-functional','cross functional']),('Mentorship',['mentorship','mentoring']),('Problem Solving',['problem solving','problem-solving'])]

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(r'(\+?\d{1,3}[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b')
DEGREE_RE = re.compile(r"\b(Ph\.?D\.?|Doctorate|Master(?:'s)?(?: of [A-Za-z]+)?|M\.?S\.?|M\.?B\.?A\.?|M\.?A\.?|Bachelor(?:'s)?(?: of [A-Za-z]+)?|B\.?S\.?|B\.?A\.?|B\.?Tech\.?|Associate(?:'s)?(?: Degree)?)\b", re.I)
SCHOOL_RE = re.compile(r'\b([A-Z][A-Za-z.&\'-]*(?:\s+[A-Z][A-Za-z.&\'-]*)*\s+(?:University|College|Institute of Technology|Institute|Polytechnic))\b')
YEARS_EXPLICIT_RE = re.compile(r'(\d{1,2})\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:relevant\s+)?experience', re.I)
YEAR_RE = re.compile(r'\b(19|20)\d{2}\b')


def skill_hits(text):
    found=[]
    for name, aliases in SKILLS:
        for alias in aliases:
            try:
                if re.search(r'\b(?:' + alias + r')\b', text, re.I):
                    found.append(name)
                    break
            except re.error:
                if re.search(alias, text, re.I):
                    found.append(name)
                    break
    return found


def normalize_degree(raw):
    cleaned=raw.replace('.','').strip(); key=re.sub(r'\s+','',cleaned).lower()
    return {'phd':'Ph.D.','doctorate':'Ph.D.','ms':'M.S.','ma':'M.A.','mba':'M.B.A.','bs':'B.S.','ba':'B.A.','btech':'B.Tech.'}.get(key,cleaned)


def parse_resume(text, filename='Pasted resume', candidate_count=0):
    lines=[x.strip() for x in text.splitlines() if x.strip()][:8]
    header=re.compile(r'^(resume|curriculum vitae|cv|summary|profile|objective|experience|education|skills|contact|projects)\b',re.I)
    name='Unnamed candidate'
    for line in lines:
        words=line.split()
        if 2<=len(words)<=4 and 2<=len(line)<=60 and not EMAIL_RE.search(line) and not PHONE_RE.search(line) and not re.search(r'\d',line) and not header.search(line) and all(re.match(r"^[A-Z][a-zA-Z'.-]*$|^[A-Z.]+$",word) for word in words):
            name=line
            break
    if name=='Unnamed candidate' and lines: name=lines[0][:60]
    degrees=[]
    for match in DEGREE_RE.findall(text):
        degree=normalize_degree(match)
        if degree not in degrees: degrees.append(degree)
    schools=[]
    for match in SCHOOL_RE.findall(text):
        if match.strip() not in schools: schools.append(match.strip())
    education=schools if not degrees else [f'{degree} — {schools[i]}' if i<len(schools) else degree for i,degree in enumerate(degrees)]
    explicit=YEARS_EXPLICIT_RE.search(text)
    if explicit:
        years=int(explicit.group(1)); method='stated'
    else:
        years_found=[int(value) for value in YEAR_RE.findall(text)]
        if len(years_found)>=2:
            span=max(years_found)-min(years_found); years=span if 0<span<=45 else None; method='estimated' if years else 'unknown'
        else: years=None; method='unknown'
    email_match=EMAIL_RE.search(text)
    phone_match=PHONE_RE.search(text)
    return {'id':str(candidate_count)+filename,'fileName':filename,'rawText':text,'name':name,'email':email_match.group(0) if email_match else None,'phone':phone_match.group(0).strip() if phone_match else None,'skills':skill_hits(text),'education':education,'experienceYears':years,'experienceMethod':method,'status':'ready'}


def extract_file(uploaded_file):
    ext=Path(uploaded_file.name).suffix.lower()
    data=uploaded_file.getvalue()
    if ext=='.txt': return data.decode('utf-8',errors='ignore')
    if ext=='.pdf':
        if PdfReader is None: raise RuntimeError('Install pypdf to read PDF files.')
        reader=PdfReader(io.BytesIO(data)); return '\n'.join((page.extract_text() or '') for page in reader.pages)
    if ext=='.docx':
        if Document is None: raise RuntimeError('Install python-docx to read DOCX files.')
        document=Document(io.BytesIO(data)); return '\n'.join(paragraph.text for paragraph in document.paragraphs)
    raise RuntimeError(f'{ext} is not supported yet — use PDF, DOCX, or TXT.')
