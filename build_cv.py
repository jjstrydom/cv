import markdown2 as markdown
from bs4 import BeautifulSoup

with open("cv.md","r") as md_file:
    md_str = md_file.read()
    html = markdown.markdown(md_str)

prefix = """\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
	<title>CV</title>
	<link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/reset-fonts-grids/reset-fonts-grids.css" media="all" /> 
	<link rel="stylesheet" type="text/css" href="cv.css" media="all" />
</head>
<body>
<div id="doc2" class="yui-t7">
	<div id="inner">
"""

postfix = """\
	</div><!-- // inner -->
</div><!--// doc -->
</body>
</html>
"""

soup = BeautifulSoup(prefix + html + postfix, features="html.parser")

def multi_wrap(element, wrappers: list):
    for wrapper in wrappers:
        element.wrap(wrapper)

multi_wrap(soup.find('h1'),[
    soup.new_tag('div', **{"id": "hd"}),
    soup.new_tag('div', **{"class": "yui-gc"}),
    soup.new_tag('div', **{"class": "yui-u first"}),
])

with open("cv.html","w") as html_file:
    html_file.write(soup.prettify())