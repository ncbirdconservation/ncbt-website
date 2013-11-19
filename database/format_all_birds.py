import os
import sys

rootdir='D:/@nc_birding_trail/website/squarespace/database/'
ab = open(rootdir + 'all_birds.csv', 'r').read()
bl = ab.splitlines()
d=","
nl="\n"
out = open(rootdir + 'all_birds_html.txt','w')

# <div class="site-item" onclick="google.maps.event.trigger(siteMarkers["airlie-gardens"], "click")" onmouseout="infoWindows["airlie-gardens"].close()" onmouseover="google.maps.event.trigger(siteMarkers["airlie-gardens"], "mouseover")">Airlie Gardens</div>
# <div class="site-item" onclick="google.maps.event.trigger(siteMarkers["croatan-national-forest-island-creek-forest-walk"], "click")" onmouseout="infoWindows["croatan-national-forest-island-creek-forest-walk"].close()" onmouseover="google.maps.event.trigger(siteMarkers["croatan-national-forest-island-creek-forest-walk"], "mouseover")">Croatan National Forest - Island Creek Forest Walk</div>

div1 = '<div class="site-item" onclick="getSppSites(\''
div2 = '\')"><span class="common-name-item">'
div3 = '</span> (<span class="sci-name-item">'
div4 = '</span>)</div>'

for ln,l in enumerate(bl):
	r = l.split(d)
	if ln != 0: 	#get headings
		out.write("".join([div1,r[2],div2,r[0],div3,r[1],div4,nl]))
		
