import markdown2 as markdown
from bs4 import BeautifulSoup

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

segments = split_segments(soup.find_all())


with open("cv.html","w") as html_file:
    html_file.write(soup.prettify())