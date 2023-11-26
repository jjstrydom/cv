import markdown2 as markdown
from bs4 import BeautifulSoup
import jinja2

template_dir = './templates'
loader = jinja2.FileSystemLoader(template_dir)
environment = jinja2.Environment(loader=loader)

with open("cv.md","r") as md_file:
    md_str = md_file.read()
    html = markdown.markdown(md_str)

soup = BeautifulSoup(html, features="html.parser")

def split_segments(elements: list[BeautifulSoup], segment_break_tags:list=["h1", "h2"]):
    segments = []
    segment = None
    for element in elements:
        if element.name in segment_break_tags:
            segment = []
            segments.append(segment)
        if segment is not None:
            segment.append(element)
    return segments

segments = split_segments(soup.find_all(recursive=False))

def extract_contents_string(element: BeautifulSoup):
    return ''.join([str(e) for e in element.contents])

def extract_contents_string_list(elements: list[BeautifulSoup], tag: str):
    return [extract_contents_string(s) 
            for s in elements.find_all(tag)]

def extract_contents_edu(text:str, sep:str, assignments: list):
    d = {}
    for t, a in zip(text.split(sep), assignments):
        d[a] = t.strip()
    return d

def extract_edu(elements):
    return [extract_contents_edu(
        e.text, '|', ['school', 'quali', 'time']
        ) for e in elements.find_all('li')]

def extract_contents_exp(seg):
    d = {}
    for s in seg:
        if s.name == 'h3':
            d['role'] = s.text
        elif s.name == 'p':
            s_split = s.text.split('|')
            d['company'] = s_split[0].strip()
            d['time'] = s_split[1].strip()
        elif s.name == 'ul':
            d['exp'] = s.text.strip()
    return d
    

def extract_exp(elements):
    seg = split_segments(elements, ["h3"])
    return [extract_contents_exp(s) for s in seg]

test = extract_exp(segments[3][1:])

kwargs = {
    'name': segments[0][0].text,
    'title': segments[0][1].text,
    'contacts': extract_contents_string_list(segments[0][2],'li'),
    'profile_heading': segments[1][0].text,
    'profile_text': segments[1][1].text,
    'achievement_heading': segments[2][0].text,
    'achievements_text': [s.text for s in segments[2][1].find_all('li')],
    'experience_heading': segments[3][0].text,
    'experience_text': extract_exp(segments[3][1:]),
    'education_heading': segments[4][0].text,
    'education_text': extract_edu(segments[4][1]),
}

template = environment.get_template("srt-resume.html")
html_output = template.render(**kwargs)

with open("cv.html","w") as html_file:
    html_file.write(html_output)