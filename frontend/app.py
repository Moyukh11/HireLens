import io, re, json
from pathlib import Path
import streamlit as st

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None
try:
    from docx import Document
except Exception:
    Document = None

st.set_page_config(page_title='HireLens — Resume Screener & Job Matcher', page_icon='◉', layout='wide', initial_sidebar_state='expanded')

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
MIN_YEARS_RE = YEARS_EXPLICIT_RE
DEGREE_REQUIRED_RE = re.compile(r'\b(Bachelor|Master|Ph\.?D|B\.?S\.?|M\.?S\.?|M\.?B\.?A\.?|degree)\b', re.I)


def skill_hits(text):
    found=[]
    for name, aliases in SKILLS:
        for a in aliases:
            try:
                if re.search(r'\b(?:' + a + r')\b', text, re.I): found.append(name); break
            except re.error:
                if re.search(a, text, re.I): found.append(name); break
    return found

def normalize_degree(raw):
    s=raw.replace('.','').strip(); k=re.sub(r'\s+','',s).lower()
    return {'phd':'Ph.D.','doctorate':'Ph.D.','ms':'M.S.','ma':'M.A.','mba':'M.B.A.','bs':'B.S.','ba':'B.A.','btech':'B.Tech.'}.get(k,s)

def parse_resume(text, filename='Pasted resume'):
    lines=[x.strip() for x in text.splitlines() if x.strip()][:8]
    header=re.compile(r'^(resume|curriculum vitae|cv|summary|profile|objective|experience|education|skills|contact|projects)\b',re.I)
    name='Unnamed candidate'
    for line in lines:
        words=line.split()
        if 2<=len(words)<=4 and 2<=len(line)<=60 and not EMAIL_RE.search(line) and not PHONE_RE.search(line) and not re.search(r'\d',line) and not header.search(line) and all(re.match(r"^[A-Z][a-zA-Z'.-]*$|^[A-Z.]+$",w) for w in words): name=line; break
    if name=='Unnamed candidate' and lines: name=lines[0][:60]
    degrees=[]
    for m in DEGREE_RE.findall(text):
        d=normalize_degree(m)
        if d not in degrees: degrees.append(d)
    schools=[]
    for m in SCHOOL_RE.findall(text):
        if m.strip() not in schools: schools.append(m.strip())
    education=schools if not degrees else [f'{d} — {schools[i]}' if i<len(schools) else d for i,d in enumerate(degrees)]
    explicit=YEARS_EXPLICIT_RE.search(text)
    if explicit: years=int(explicit.group(1)); method='stated'
    else:
        ys=[int(x) for x in YEAR_RE.findall(text)]
        if len(ys)>=2:
            span=max(ys)-min(ys); years=span if 0<span<=45 else None; method='estimated' if years else 'unknown'
        else: years=None; method='unknown'
    return {'id':str(len(st.session_state.candidates))+filename,'fileName':filename,'rawText':text,'name':name,'email':(EMAIL_RE.search(text).group(0) if EMAIL_RE.search(text) else None),'phone':(PHONE_RE.search(text).group(0).strip() if PHONE_RE.search(text) else None),'skills':skill_hits(text),'education':education,'experienceYears':years,'experienceMethod':method,'status':'ready'}

def extract_file(f):
    ext=Path(f.name).suffix.lower()
    data=f.getvalue()
    if ext=='.txt': return data.decode('utf-8',errors='ignore')
    if ext=='.pdf':
        if PdfReader is None: raise RuntimeError('Install pypdf to read PDF files.')
        reader=PdfReader(io.BytesIO(data)); return '\n'.join((p.extract_text() or '') for p in reader.pages)
    if ext=='.docx':
        if Document is None: raise RuntimeError('Install python-docx to read DOCX files.')
        doc=Document(io.BytesIO(data)); return '\n'.join(p.text for p in doc.paragraphs)
    raise RuntimeError(f'{ext} is not supported yet — use PDF, DOCX, or TXT.')

def analyze_jd(text):
    req=[]; pref=[]
    for name, aliases in SKILLS:
        hit=None
        for a in aliases:
            try: hit=re.search(r'\b(?:'+a+r')\b',text,re.I)
            except re.error: hit=re.search(a,text,re.I)
            if hit: break
        if not hit: continue
        before=text[max(0,hit.start()-60):hit.start()].lower()
        (pref if re.search(r'(preferred|nice to have|bonus|plus)[^.]*$',before) else req).append(name)
    m=MIN_YEARS_RE.search(text)
    return {'skills':{'required':req,'preferred':pref},'minYears':int(m.group(1)) if m else None,'degreeRequired':bool(DEGREE_REQUIRED_RE.search(text))}

def score(c,jd):
    req=jd['skills']['required']; pref=jd['skills']['preferred']; cs=set(c['skills'])
    mr=[x for x in req if x in cs]; missr=[x for x in req if x not in cs]; mp=[x for x in pref if x in cs]; missp=[x for x in pref if x not in cs]
    if not req and not pref: ss=1
    else:
        rs=len(mr)/len(req) if req else 1; ps=len(mp)/len(pref) if pref else 1; ss=rs*.85+ps*.15 if req else ps
    es=1; en='Not specified in job description'
    if jd['minYears'] is not None:
        y=c['experienceYears']
        if y is None: es=.5; en=f"Requires {jd['minYears']}+ yrs — candidate's experience length couldn't be read"
        elif y>=jd['minYears']: en=f"Meets the {jd['minYears']}+ yr requirement ({y} yrs found)"
        else: es=max(0,y/jd['minYears']); en=f"Below the {jd['minYears']}+ yr requirement ({y} yrs found)"
    ed=1; dn='Not specified in job description'
    if jd['degreeRequired']:
        if c['education']: dn='Degree found on resume'
        else: ed=.4; dn='Job description implies a degree; none detected on resume'
    total=ss*.7+es*.2+ed*.1
    return {'score':round(total*100),'matchedRequired':mr,'missingRequired':missr,'matchedPreferred':mp,'missingPreferred':missp,'breakdown':{'skills':round(ss*100),'experience':round(es*100),'education':round(ed*100),'experienceNote':en,'educationNote':dn}}

from resume_parser import extract_file, parse_resume
from job_analyzer import analyze_jd
from scoring import score

# --- styling ---
st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600;8..60,700&family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap');
:root{--bg:#f7f4ee;--panel:#fffdf8;--text:#27251f;--soft:#777267;--line:#ded8cc;--green:#3d7257;--amber:#b07b22;--rust:#a64c3d;--gold:#c19a55}
html,body,[class*="css"]{font-family:'IBM Plex Sans',sans-serif;color:var(--text)} .stApp{background:var(--bg)}
.block-container{max-width:1120px;padding:28px 34px 50px}.apphead{display:flex;align-items:center;border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:26px}.mark{width:36px;height:36px;border:2px solid #292720;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;margin-right:12px}.brand h1{font-family:'Source Serif 4',serif;font-size:27px;margin:0}.brand p{font-size:12px;color:var(--soft);margin:1px 0}.meta{margin-left:auto;color:var(--soft);font-size:12px}.step{display:flex;gap:10px;margin-bottom:35px}.stepitem{display:flex;align-items:center;gap:8px;color:#989186;font-size:12px}.stepitem.active{color:var(--text);font-weight:600}.num{width:25px;height:25px;border:1px solid #cfc8bb;border-radius:50%;display:flex;align-items:center;justify-content:center}.active .num{background:#292720;color:#fff;border-color:#292720}.done .num{background:var(--green);color:white;border-color:var(--green)}.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:32px}.title{font-family:'Source Serif 4',serif;font-size:28px;margin-bottom:5px}.sub{color:var(--soft);font-size:13px;line-height:1.6;max-width:850px;margin-bottom:25px}.drop{border:1.5px dashed #c8c0b2;border-radius:9px;padding:45px 25px;text-align:center;background:#fcfaf5}.drop h3{font-family:'Source Serif 4',serif;font-size:21px;margin:10px 0 5px}.hint{color:var(--soft);font-size:12px}.pill{display:inline-block;padding:5px 9px;border-radius:20px;font-size:11px;background:#f0ede5;margin:3px}.ok{color:var(--green)}.bad{color:var(--rust)}.summary{display:flex;border:1px solid var(--line);border-radius:8px;background:#fcfaf5;margin:20px 0}.sumcell{flex:1;padding:17px;border-right:1px solid var(--line)}.sumcell:last-child{border:0}.sumval{font-family:'Source Serif 4',serif;font-size:28px}.sumlabel{font-size:11px;color:var(--soft)}.card{border:1px solid var(--line);border-radius:9px;background:var(--panel);margin:12px 0;overflow:hidden}.cardtop{padding:18px;display:flex;align-items:center;gap:14px}.rank{font-size:12px;color:var(--soft);width:24px}.score{width:48px;height:48px;border:2px solid var(--green);border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'IBM Plex Mono';font-size:13px}.cname{font-family:'Source Serif 4',serif;font-size:19px}.contact{font-size:11px;color:var(--soft)}.tier{margin-left:auto;font-size:11px;padding:6px 9px;border-radius:15px}.strong{color:var(--green);background:#edf4ee}.moderate{color:var(--amber);background:#faf2df}.weak{color:var(--rust);background:#faece8}.body{padding:0 18px 20px;border-top:1px solid var(--line)}.bar{height:7px;background:#e7e2d8;border-radius:5px;overflow:hidden;margin:7px 0}.fill{height:100%;background:var(--green)}.note{font-size:11px;color:var(--soft);margin-bottom:14px}.chip{display:inline-block;padding:5px 8px;border-radius:14px;font-size:11px;margin:2px}.matched{background:#eaf2ec;color:var(--green)}.missing{background:#f5ebe7;color:var(--rust)}
.stButton>button{border-radius:6px;border:1px solid #c9c1b3;background:#fffdf8;color:#2d2a24}.stButton>button[kind="primary"]{background:#2d2a24;color:white;border-color:#2d2a24}.stTextArea textarea{background:#fffdf8}.dashboard-head{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:1px solid var(--line);padding-bottom:20px;margin-bottom:18px}.eyebrow{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:var(--soft)}.role-signal{padding:13px 16px;border-left:3px solid var(--green);background:#f4f1e9;color:#625d53;font-size:14px;line-height:1.6;margin:14px 0 20px}.rank-row{border:1px solid var(--line);border-radius:8px;background:#fffdf8;padding:16px 18px;margin:10px 0 0}.rank-name{font-family:'Source Serif 4',serif;font-size:20px}.rank-meta{font-size:13px;color:var(--soft);margin-top:3px}.evidence{font-size:13px;color:var(--soft);line-height:1.65;margin-top:10px}.evidence b{color:var(--text)}.section-label{font-size:13px;color:var(--soft);text-transform:uppercase;letter-spacing:.08em;margin:24px 0 7px}.footer{text-align:center;color:#938d82;font-size:13px;margin-top:28px}
</style>''', unsafe_allow_html=True)

st.markdown('''<style>
.block-container{max-width:980px}
.apphead{display:flex;background:#fbfaf6;padding:16px 18px 20px}
.panel{background:transparent;border:0;border-radius:0;padding:0}
.section-rule{width:100%;border-top:1px solid var(--line);margin:18px 0 14px}.workflow-heading{display:inline-block;background:#e8dcc4;padding:8px 14px;margin-bottom:8px}.stepitem.completed .num{background:var(--green);color:white;border-color:var(--green)}
.detected-requirements{background:#fbfaf6;border:1px solid #ded8cc;border-left:4px solid var(--green);border-radius:8px;padding:16px 18px;margin:18px 0 22px;line-height:1.7}
.candidate-row{background:#f1e8d8;border:1px solid #ded1bc;border-left:4px solid var(--green);border-radius:8px;padding:12px 16px;margin:8px 0;font-size:21px;line-height:1.5}.candidate-row small{font-size:14px;color:#777}
html,body,[class*="css"]{font-size:18px}
.mark{font-size:19px}.brand h1{font-size:29px}.brand p,.meta,.stepitem,.hint{font-size:14px}
.title{font-size:30px}.sub{font-size:15px}.drop h3{font-size:23px}.pill{font-size:13px}
.sumval{font-size:30px}.sumlabel{font-size:13px}.dashboard-head .eyebrow,.section-label{font-size:15px}
.role-signal{font-size:16px}.rank-name{font-size:22px}.rank-meta,.evidence{font-size:15px}.footer{font-size:15px}
.stExpander .note,.stExpander .chip,.stExpander .contact{font-size:16px}.stExpander details{background:#fbfaf6;border:1px solid #ded8cc;border-radius:8px}
</style>''', unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step=1
if 'candidates' not in st.session_state: st.session_state.candidates=[]
if 'uploader_version' not in st.session_state: st.session_state.uploader_version=0
if 'jd' not in st.session_state: st.session_state.jd=''
if 'jd_detected_text' not in st.session_state: st.session_state.jd_detected_text=''
if 'dashboard_completed' not in st.session_state: st.session_state.dashboard_completed=False

ready_count=sum(c.get('status')=='ready' for c in st.session_state.candidates)
jd_ready=bool(st.session_state.jd.strip()) and st.session_state.jd==st.session_state.jd_detected_text
with st.sidebar:
    if st.button('UPLOAD RESUMES',type='primary' if st.session_state.step==1 else 'secondary',use_container_width=True):
        st.session_state.step=1; st.rerun()
    if st.button('JOB DESCRIPTION',type='primary' if st.session_state.step==2 else 'secondary',disabled=ready_count==0,use_container_width=True):
        st.session_state.step=2; st.rerun()
    if st.button('DASHBOARD',type='primary' if st.session_state.step==3 else 'secondary',use_container_width=True):
        st.session_state.step=3; st.rerun()

def start_over():
    st.session_state.step=1; st.session_state.candidates=[]; st.session_state.uploader_version+=1; st.session_state.jd=''; st.session_state.jd_detected_text=''; st.session_state.dashboard_completed=False

def header():
    ready=sum(c.get('status')=='ready' for c in st.session_state.candidates)
    st.markdown(f'''<div class="apphead"><div class="mark">◉</div><div class="brand"><h1>HireLens</h1></div><div class="meta">{ready} candidate{'s' if ready!=1 else ''} in session &nbsp; · &nbsp; explainable matching</div></div>''',unsafe_allow_html=True)
    labels=['UPLOAD RESUMES','JOB DESCRIPTION','DASHBOARD']; html='<div class="step">'
    completed=[ready>0, jd_ready, st.session_state.dashboard_completed]
    for i,l in enumerate(labels,1): html+=f'<div class="stepitem {"active completed" if i==st.session_state.step and completed[i-1] else "active" if i==st.session_state.step else "done" if completed[i-1] else ""}"><span class="num">{"✓" if completed[i-1] else i}</span>{l}</div>'
    html+='</div>'; st.markdown(html,unsafe_allow_html=True)

header()

if st.session_state.step==1:
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    st.markdown('<div class="section-rule"></div><div class="workflow-heading"><strong>UPLOAD RESUMES</strong></div><div class="sub">Upload PDF or DOCX resumes — one at a time or a whole shortlist at once — or paste resume text directly. HireLens reads each one for contact details, skills, education, and experience.</div>',unsafe_allow_html=True)
    files=st.file_uploader('Upload resumes',type=['pdf','docx','txt'],accept_multiple_files=True,label_visibility='collapsed',key=f'resume_uploader_{st.session_state.uploader_version}')
    if files:
        existing={c['fileName'] for c in st.session_state.candidates}
        added=False
        for f in files:
            if f.name in existing: continue
            try: st.session_state.candidates.append(parse_resume(extract_file(f),f.name,len(st.session_state.candidates)))
            except Exception as e: st.session_state.candidates.append({'id':f.name,'fileName':f.name,'name':f.name,'status':'error','errorMessage':str(e),'skills':[],'education':[],'experienceYears':None,'experienceMethod':'unknown'})
            added=True
        if added: st.rerun()
    st.markdown('#### Or paste a resume')
    pasted=st.text_area('Resume text',placeholder='Paste the full text of one resume here…',height=180,label_visibility='collapsed')
    if st.button('Add this resume',disabled=not pasted.strip()): st.session_state.candidates.append(parse_resume(pasted,candidate_count=len(st.session_state.candidates))); st.rerun()
    if st.session_state.candidates:
        st.markdown('#### Candidates')
        for idx,c in enumerate(st.session_state.candidates):
            col1,col2,col3=st.columns([6,2,1])
            with col1: st.markdown(f"<div class='candidate-row'><strong>{c.get('name',c['fileName'])}</strong><br><small>{c.get('email') or c.get('errorMessage') or 'No email detected'}</small></div>",unsafe_allow_html=True)
            with col2: st.markdown(f'<span class="pill {"ok" if c.get("status")=="ready" else "bad"}" style="font-size:16px">{"Parsed" if c.get("status")=="ready" else "Failed"}</span>',unsafe_allow_html=True)
            with col3:
                if st.button('×',key=f'del{idx}'):
                    st.session_state.candidates.pop(idx)
                    st.session_state.uploader_version+=1
                    st.rerun()
    ready=sum(c.get('status')=='ready' for c in st.session_state.candidates)
    st.divider()
    if st.button('Continue to job description',type='primary',disabled=ready==0): st.session_state.step=2; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

elif st.session_state.step==2:
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    st.markdown('<div class="section-rule"></div><div class="workflow-heading"><strong>JOB DESCRIPTION</strong></div><div class="sub">Paste the job description below. HireLens will detect required and preferred skills, an experience threshold, and whether a degree is implied.</div>',unsafe_allow_html=True)
    st.session_state.jd=st.text_area('Job description',value=st.session_state.jd,placeholder='Paste the complete job description here…',height=320,label_visibility='collapsed')
    detected=bool(st.session_state.jd.strip()) and st.session_state.jd==st.session_state.jd_detected_text
    if st.button('Detect skills',type='primary',disabled=not st.session_state.jd.strip()):
        st.session_state.jd_detected_text=st.session_state.jd
        detected=True
    if detected:
        info=analyze_jd(st.session_state.jd)
        st.markdown(f'<div class="detected-requirements"><strong>DETECTED REQUIREMENTS</strong><br><b>Required:</b> {", ".join(info["skills"]["required"]) or "None detected"}<br><b>Preferred:</b> {", ".join(info["skills"]["preferred"]) or "None detected"}<br><b>Experience:</b> {str(info["minYears"])+"+ years" if info["minYears"] is not None else "Not specified"} &nbsp;&nbsp; <b>Degree:</b> {"Implied" if info["degreeRequired"] else "Not detected"}</div>',unsafe_allow_html=True)
    elif st.session_state.jd.strip():
        st.info('Click Detect skills to analyze this job description.')
    c1,c2=st.columns([1,1])
    with c1:
        if st.button('Back to resumes'): st.session_state.step=1; st.rerun()
    with c2:
        if st.button('Review matches',type='primary',disabled=not detected): st.session_state.dashboard_completed=True; st.session_state.step=3; st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

else:
    ready=[c for c in st.session_state.candidates if c.get('status')=='ready']; jd=analyze_jd(st.session_state.jd)
    ranked=sorted([(c,score(c,jd)) for c in ready],key=lambda x:x[1]['score'],reverse=True)
    st.markdown('<div class="panel">',unsafe_allow_html=True)
    avg=round(sum(m['score'] for _,m in ranked)/len(ranked)) if ranked else 0; strong=sum(m['score']>=75 for _,m in ranked); top=ranked[0][1]['score'] if ranked else 0
    st.markdown('<div class="section-rule"></div><div class="dashboard-head"><div><div class="workflow-heading"><strong>DASHBOARD</strong></div><div class="title">Ranked shortlist</div></div><div class="eyebrow">Explainable scoring</div></div>',unsafe_allow_html=True)
    required=', '.join(jd['skills']['required']) or 'No required skills detected'
    preferred=', '.join(jd['skills']['preferred']) or 'No preferred skills detected'
    st.markdown(f'<div class="role-signal"><b>Role signals</b><br><b>Required:</b> {required}<br><b>Preferred:</b> {preferred} &nbsp; · &nbsp; <b>Experience:</b> {str(jd["minYears"])+"+ years" if jd["minYears"] is not None else "Not specified"} &nbsp; · &nbsp; <b>Degree:</b> {"Implied" if jd["degreeRequired"] else "Not detected"}</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="summary"><div class="sumcell"><div class="sumval">{len(ranked)}</div><div class="sumlabel">Candidates screened</div></div><div class="sumcell"><div class="sumval">{top}</div><div class="sumlabel">Top score</div></div><div class="sumcell"><div class="sumval">{avg}</div><div class="sumlabel">Average score</div></div><div class="sumcell"><div class="sumval">{strong}</div><div class="sumlabel">Strong matches (75+)</div></div></div>',unsafe_allow_html=True)
    if not ranked:
        st.info('No candidates to show yet. Upload and parse resumes, then detect a job description to generate matches.')
    c1,c2=st.columns([1,1])
    with c1: threshold=st.selectbox('Show candidates',[(0,'All candidates'),(50,'Score 50+'),(75,'Strong matches (75+)'),(90,'Top matches (90+)')],format_func=lambda x:x[1])[0]
    with c2: query=st.text_input('Find a candidate',placeholder='Search by name, email, or source').strip().lower()
    filtered=[x for x in ranked if x[1]['score']>=threshold and (not query or query in ' '.join([x[0].get('name',''),x[0].get('email') or '',x[0].get('fileName','')]).lower())]
    st.markdown(f'<div class="section-label">Showing {len(filtered)} of {len(ranked)} candidates</div>',unsafe_allow_html=True)
    for rank,(c,m) in enumerate(filtered,1):
        cls='strong' if m['score']>=75 else 'moderate' if m['score']>=50 else 'weak'; label='Strong match' if cls=='strong' else 'Moderate match' if cls=='moderate' else 'Weak match'
        matched=len(m['matchedRequired'])+len(m['matchedPreferred']); missing=len(m['missingRequired'])+len(m['missingPreferred'])
        st.markdown(f'<div class="rank-row"><div class="eyebrow">Rank {rank} &nbsp; · &nbsp; <span class="{("ok" if cls=="strong" else "bad" if cls=="weak" else "")}">{label}</span></div><div class="rank-name">{c["name"]}</div><div class="rank-meta">{c.get("email") or "No email detected"} · {c["fileName"]}</div><div class="evidence"><b>{m["score"]}/100</b> &nbsp; · &nbsp; <b>{matched}</b> detected skills matched &nbsp; · &nbsp; <b>{missing}</b> gaps &nbsp; · &nbsp; Skills {m["breakdown"]["skills"]}% &nbsp; · &nbsp; Experience {m["breakdown"]["experience"]}% &nbsp; · &nbsp; Education {m["breakdown"]["education"]}%</div></div>',unsafe_allow_html=True)
        with st.expander(f'View explanation for {c["name"]}',expanded=(rank==1 and not query)):
            st.markdown(f"<div class='contact'>{c.get('email') or ''} {' · '+c.get('phone') if c.get('phone') else ''}</div>",unsafe_allow_html=True)
            for lab,key,note in [('Skills (70%)','skills',''),('Experience (20%)','experience',m['breakdown']['experienceNote']),('Education (10%)','education',m['breakdown']['educationNote'])]:
                val=m['breakdown'][key]; st.markdown(f'<div style="font-size:16px;margin-top:14px"><b>{lab} — {val}%</b><div class="bar"><div class="fill" style="width:{val}%"></div></div></div><div class="note">{note}</div>',unsafe_allow_html=True)
            st.markdown('**Matched skills**')
            chips=' '.join(f"<span class='chip matched'>✓ {s}{' (pref.)' if s in m['matchedPreferred'] else ''}</span>" for s in m['matchedRequired']+m['matchedPreferred']) or '<span class="note">None of the role’s detected skills were found</span>'
            st.markdown(chips,unsafe_allow_html=True)
            st.markdown('**Missing skills**')
            chips=' '.join(f"<span class='chip missing'>{s}{' (pref.)' if s in m['missingPreferred'] else ''}</span>" for s in m['missingRequired']+m['missingPreferred']) or '<span class="note">Nothing required was missing</span>'
            st.markdown(chips,unsafe_allow_html=True)
            st.markdown(f"<div class='note' style='margin-top:16px'><b>Experience:</b> {str(c['experienceYears'])+' yrs ('+c['experienceMethod']+')' if c['experienceYears'] is not None else 'Not detected'} &nbsp; · &nbsp; <b>Education:</b> {'; '.join(c['education']) if c['education'] else 'Not detected'} &nbsp; · &nbsp; <b>Source:</b> {c['fileName']}</div>",unsafe_allow_html=True)
    if not filtered: st.info('No candidates at this threshold. Try lowering the score filter above.')
    c1,c2=st.columns(2)
    with c1:
        if st.button('Back to job description'): st.session_state.step=2; st.rerun()
    with c2:
        if st.button('Screen a new batch',type='primary'): start_over(); st.rerun()
    st.markdown('</div>',unsafe_allow_html=True)

st.markdown('<div class="footer">Parsing and scoring run locally in the Streamlit app — resumes are not sent to an external AI service.</div>',unsafe_allow_html=True)
