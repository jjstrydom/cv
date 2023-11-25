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
	<link rel="stylesheet" type="text/css" href="resume.css" media="all" />

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

with open("cv.html","w") as html_file:
    html_file.write(soup.prettify())