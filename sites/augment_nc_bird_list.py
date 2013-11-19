### compile_files.py
### parses Excel xml spreadsheet of NCBT Sites
### creates kml and rss feed for squarespace site
### kml for map display
### rss feed for import of site descriptions into a journal

import os
import sys

def main():
	#turn on/off outputs
	# xml_switch = False #build xml string for squarespace map webpage reference (building labels)
	# json_switch = False #build json string for squarespace map webpage reference (building labels)
	# #birdlist_switch = False #build birdlist 
	# kml_switch = False #build kml file for ncbt sites
	# mt_switch = False #build input for moveabletype import to squarespace
	# rss_switch = False #build input for wordpress import to squarespace
	# ae_switch = False #build data for GAE input of birdlist
	# sl_switch = False #build unorderd list of sites (html)
	# js_switch = False # build js file with  hard coded arrays

	#set all switches to false
	switch={"xml":False,"json":False,"kml":False,"mt":False,"rss":False,"ae":False,"sl":False,"js":False}
	#set switch values based on passed arguments
	for arg in sys.argv[1:]: 
		print arg + ' running...'
		switch[arg] = True
	
	class AutoVivification(dict):
		"""Implementation of perl's autovivification feature."""
		def __getitem__(self, item):
			try:
				return dict.__getitem__(self, item)
			except KeyError:
				value = self[item] = type(self)()
				return value

	endash=u'\u2013'
	TEXT_ESCAPE_TABLE = {"&": "and"}
	#REGION_STYLE = {"coastal":"pointCSite", "piedmont":"pointPSite", "mountain":"pointMSite"}
	REGION_STYLE = {"Coastal":"site", "Piedmont":"site", "Mountain":"site"}
	GUIDE_IMG = {"Coastal":"ncbt_guide_coast.png", "Piedmont":"ncbt_guide_piedmont.png", "Mountain":"ncbt_guide_mountains.png"}
	FEATURE_ICONS = {"fee":"a_fee.png", "handicap access":"a_handicapaccess.png", "hiking trails":"a_hikingtrails.png", "interpretive programs":"a_interpretiveprograms.png", "picnic area":"a_picnicarea.png", "restrooms":"a_restrooms.png", "trail maps/information":"a_trailmapsinformation.png","viewing platforms":"a_viewingplatforms.png", "visitor center":"a_visitorcenter.png", "hunting":"a_hunting.png", "boat launch":"a_boatlaunch.png", "boat access only":"a_boataccessonly.png", "camping":"a_camping.png" }

	site_region = {}
	site_group = {}
	region_group = {}
	rgs=AutoVivification() #region,group,site list


	base_url = 'http://ncbirdingtrail.squarespace.com/'
	base_url_img = base_url + 'storage/img/'

	SLUG_ESCAPE_TABLE = {",":"-"," ":"-","/":"-","'":"","&":"and","(":"",")":"", "#":"",".":""}
	SLUG_ESCAPE_TABLE2 = {"----":"-","---":"-","--":"-"}
	def slugify(t,d='-',c='l'):
		#take string input and replace spaces with '-'
		# s = s.replace(' ',d)
		#s.replace(d, ' ')
		if c=='l': t = "".join(SLUG_ESCAPE_TABLE.get(c,c) for c in t.lower())
		if c=='p': t = "".join(SLUG_ESCAPE_TABLE.get(c,c) for c in t)
		t = t.replace("----","-")
		t = t.replace("---","-")
		t = t.replace("--","-")
		
		return t

	def capital(s): #capitalize first letter of string
		return s[0].capitalize() + s[1:]
		
	def text_escape(text): #Produce entities within text.
		return "".join(TEXT_ESCAPE_TABLE.get(c,c) for c in text)
		
	def create_amenities(al): #amenities icons html, from passed string
		#comma delimited
		l = al.strip('" ').split(',')
		r = '<div class="item">'
		for i in l:
			# if len(i.strip(' '))>0: r += '<div class="a_logo"><a href="/sites/tag/' + i + '"><img class="logo_img" title="' + i.strip(' ') + '" src="' + base_url + 'storage/img/' + FEATURE_ICONS[i.strip(' ')] + '"/></a></div>'
			if len(i.strip(' '))>0: r += '<div class="a_logo"><img class="logo_img" title="' + i.strip(' ') + '" src="http://www.ncbirdingtrail.squarespace.com/storage/img/' + FEATURE_ICONS[i.strip(' ')] + '"/></div>'
		
		r += '</div>'
		return r

	def create_amenities_tags(al): #amenities tag html, from passed string
		#comma delimited
		l = al.strip('" ').split(',')
		r = ''
		for i in l:
			if len(i.strip(' '))>0: r += '<category domain="post_tag" nicename="' + capital(i.strip(' ')) + '"><![CDATA[' + capital(i.strip(' ')) + ']]></category>'
		return r
		
	def create_amenities_list(al):
		l = al.strip('" ').split(',')
	#		sd = dict([(h[i],v.strip('"')) for i,v in enumerate(r)])
		return [(i.strip(' ')) for i in l]

	def create_placemark(sd):
		coords = str(sd['lat_dd']) + ',' + str(sd['lon_dd'])
		#from passed data, create a placemark entry
		p = '<Placemark>'
		p += '<name>' + text_escape(sd['name']) + '</name>'
		#if rs[sd['region']]: p += '<styleurl>' + rs[sd['region']] + '</styleurl>'
		
		#ballon html
		p += '<description><![CDATA[<div class="balloon-container"><div class="balloon-title">' 
		p += sd['name']
		p += '</div><div class="guide-balloon">'
		p += '<a href="' + base_url + 'sites/' + sd['slug'] + '">'
		p += '<img class="guide-img" src="' + base_url + 'storage/img/' + GUIDE_IMG[sd['region']] + '"/>'
		p += '</a><br/><a href="' + base_url + 'sites/2012/8/1/' + sd['slug'] + '"><div class="guide-link">Guide Info</div></a></div>'
		p += '<ul class="balloon-list">'
		p += '<li><a href="http://www.ncbirdingtrail.org/ncbirdingsite2/index.php?action=siteView&site=' + sd['siteid'] + '">Bird List</a></li>'
		p += '<li><a href="http://maps.google.com/maps?daddr=' + coords + '">Driving Directions</a></li>'
		p += '</ul></div>]]></description>'
		
		
		if REGION_STYLE[sd['region']]: p += '<styleUrl>#' + REGION_STYLE[sd['region']] + '</styleUrl>'
		p += '<Point><coordinates>' + str(sd['lon_dd']) + ',' + str(sd['lat_dd']) + ',0</coordinates></Point>'
		p += '</Placemark>'
		return p

	def create_map_xml(sd):
		#creates xml file for parsing to create the website map
		coords = str(sd['lat_dd']) + ',' + str(sd['lon_dd'])
		#from passed data, create a placemark entry
		p = '<' + sd['slug'] + '>'
		p += '<slug>' + sd['slug'] + '</slug>'	
		p += '<name>' + text_escape(sd['name']) + '</name>'

		#ballon html

		p += '<region>' + sd['region'] + '</region>'
		p += '<group>' + sd['group'] + '</group>'
		p += '<siteid>' + sd['siteid'] + '</siteid>'
		p += '<coords>' + coords + '</coords>'
		# p += '</Placemark>'
		p += '</' + sd['slug'] + '>'
		
		return p
		
		
		
	def create_site_description(sd):
		coords = str(sd['lat_dd']) + ',' + str(sd['lon_dd'])
		#format html for site description entry and return result
		d = '<div class="site">'
		
		#region:group
		# d += '<div class="region_group"><a href="/sites/category/' + slugify(sd['region']) + '">' + sd['region'] + '</a> : <a href="/sites/category/' + slugify(sd['group']) + '">' + sd['group'] + '</a><br/>Guide page ' + sd['site_pg'] + '</div>'
		# d += '<div class="region_group"><a href="/map?group=' + slugify(sd['group'],'-','p') + '">' + sd['region'] + ' : ' + sd['group'] + '</a><br/>Guide page ' + sd['site_pg']
		d += '<div class="region_group"><div class="group-links"><a href="/map?group=' + slugify(sd['group'],'-','p') + '">' + sd['region'] + ' Region : ' + sd['group'] + ' Group</a><br/>'
		d += sd['region'] + ' Guide page ' + sd['site_pg'] + '</div>'
		d += '<div class="map-external-links">'
		if len(sd['website'])>0: 
			d += '<a href="'
			if sd['website'][0:4]!='http': d += 'http://'
			d += sd['website'] + '" target="_blank">External Website</a></br>'
		d += '<a href="/map">Back to NCBT Map</a></div>'
		d+= '</div>'
		
		#description
		#--------------
		d +='<div class="item"><div class="site_description_text" id="description"><h1 style="display:hidden;">Description</h1>'
		
		#map window
		d += '<div class="map_window" id="map-window"><a href="/map?site=' + sd['slug'] + '"><img src="http://maps.googleapis.com/maps/api/staticmap?center=35.3,-80&zoom=6&size=420x175&maptype=terrain&markers=icon:http://www.ncbirdingtrail.squarespace.com/storage/img/map_dot.png%7C' + coords + '&sensor=false"/></a></div>'
		d += '<p>' + sd['description'].strip('"').replace("?s","'s") + '</p></div></div>'
		#--------------

		# species
		if len(sd['species_of_interest'])>0: d += '<div class="item" id="species"><h1>Species of Interest (<a href="#birdlist-header" style="cursor:pointer;font-decoration:underline;">Full Bird List</a>)</h1><p>' + sd['species_of_interest'] + '</p></div>'

		# habitats
		if len(sd['habitats'])>0: d += '<div class="item" id="habitats"><h1>Habitat</h1><p>' + sd['habitats'] + '</p></div>'
		
		# special features
		if len(sd['special_concern'])>0: d += '<div class="item" id="features"><h1>Special Features/Concerns</h1><p>' + sd['special_concern'] + '</p></div>'
		
		#access parking
		if len(sd['access_parking'])>0: d += '<div class="item" id="access"><h1>Access and Parking</h1><p>' + sd['access_parking'] + '</p></div>'
		
		#amenities
		d += create_amenities(sd['amenities'])
		
		# directions
		d += '<div class="item_directions">'
		d += '<div class="item directions_text" id="directions"><h1>Directions</h1>'
		d += '<div class="map_window" id="map-window-directions"><a href="http://maps.google.com/maps?daddr=' + coords + '" target="_blank"><img src="http://maps.googleapis.com/maps/api/staticmap?center=' + coords +'&zoom=8&size=200x200&maptype=street&markers=icon:http://www.ncbirdingtrail.squarespace.com/storage/img/map_dot.png%7C' + coords + '&sensor=false"/></a></div>'
		d += '<div class="written-directions"><p>' + sd['directions'] + '</p>'
		d += '<p><a href="http://maps.google.com/maps?daddr=' + coords + '" target="_blank">Google Directions</a></p></div></div>'
		d += '<div class="item coords-gazetteer">'
		d += '<div id="coords"><h2>Coordinates</h2><p><a href="http://maps.google.com/maps?daddr=' + coords + '" target="_blank">' + sd['coord_dms_plain'] + '</a></p></div>'
		d += '<div id="gazetteer"><h2>Delorme Gazetteer Page</h2><p>' + sd['gazeteer'] + '</p></div>'
		
		d += '</div></div>'
		
		#some site data to be hidden - accessed by map to display points
		d += '<div id="site-data" style="display:none">'
		d += '<div id="item site-slug"><h1>site-slug</h1><p>' + sd['slug'] + '</p></div>'
		d += '<div id="item site-slug-url"><h1>site-slug-url</h1><p>' + sd['slug'] + '</p></div>'
		d += '<div id="item name"><h1>name</h1><p>' + sd['name'] + '</p></div>'
		d += '<div id="item region"><h1>region</h1><p>' + slugify(sd['region']) + '<p></div>'
		d += '<div id="item group-slug"><h1>group-slug</h1><p>' + slugify(sd['group']) + '</p></div>'
		d += '<div id="item group"><h1>group</h1><p>' + sd['group'] + '</p></div>'
		d += '<div id="item coords"><h1>coords</h1><p>' + coords + '</p></div>'
		d += '</div>'
		
		# contact information
		
		# birdlist
		d += '<div id="birdlist-header" onclick=>Bird List</div>';
		d+= '<div id="birdlist"></div>';
		
		# end site div
		d += '</div>'
		
		return d

	def create_mt_item(sd):
		i = 'TITLE: ' + text_escape(sd['name']) + nl
		i += 'BASENAME: ' + sd['slug'] + nl
		i += 'AUTHOR: NC Birding Trail Coordinator' + nl
		i += 'STATUS: publish' + nl
		i += 'ALLOW COMMENTS: 1' + nl
		i += 'CATEGORY: ' + sd['region'] + nl
		i += 'CATEGORY: ' + sd['group'] + nl
		i += 'TAGS: "' + '","'.join(create_amenities_list(sd['amenities'])) + '"' + nl
		i += 'DATE: 08/01/2012 01:00:00 PM' + nl
		i += 'CONVERT BREAKS: 0' + nl
		i += '-----' + nl + 'BODY:' + nl
		i += create_site_description(sd) + nl
		i += '-----' + nl + '--------'
		return i
		
	def create_item(sd):
		#from passed data, create an rss item
		i = '<item>'
		i += '<title>' + text_escape(sd['name']) + '</title>'
		# i += '<link>http://ncbirdingtrail.org/sites/' + sd['slug'] + '</link>'
		if len(sd['website'])>0: i += '<link>' + sd['website'] + '</link>'
		i += '<pubDate>Thu, 1 Aug 2012 13:00:00 +0000</pubDate>'
		i += '<dc:creator>ncbirdingtrail</dc:creator>'
		i += '<guid isPermaLink="true">https://ncbirdingtrail.org/sites/' + sd['slug'] + '</guid>'
		i += '<description>' + '</description>'
		i += '<content:encoded><![CDATA[' + create_site_description(sd) +']]></content:encoded>'
		i += '<excerpt:encoded><![CDATA[]]></excerpt:encoded>'
		i += '<wp:post_id>' + sd['siteid'] + '</wp:post_id>'
		i += '<wp:post_date>2012-08-01 13:00:00:00</wp:post_date>'
		i += '<wp:post_date_gmt>2012-08-01 13:00:00:00</wp:post_date_gmt>'
		i += '<wp:comment_status>closed</wp:comment_status>'
		i += '<wp:ping_status>open</wp:ping_status>'
		i += '<wp:post_name>' + sd['slug'] + '</wp:post_name>'
		i += '<wp:status>publish</wp:status>'
		i += '<wp:post_parent>0</wp:post_parent>'
		i += '<wp:menu_order>0</wp:menu_order>'
		i += '<wp:post_type>post</wp:post_type>'
		i += '<wp:post_password></wp:post_password>'
		i += '<wp:is_sticky>0</wp:is_sticky>'
		i += '<category domain="post_tag" nicename="' + capital(sd['group']) + '"><![CDATA[' + capital(sd['group']) + ']]></category>'
		i += '<category domain="category" nicename="' + capital(sd['region']) + '"><![CDATA[' + sd['region'] + ']]></category>'
		i += create_amenities_tags(sd['amenities'])	
		i += '<wp:postmeta><wp:meta_key>superawesome</wp:meta_key><wp:meta_value><![CDATA[false]]></wp:meta_value></wp:postmeta>'
		i += '<wp:postmeta><wp:meta_key>_edit_last</wp:meta_key><wp:meta_value><![CDATA[18157085]]></wp:meta_value></wp:postmeta>'
		i += '<wp:postmeta><wp:meta_key>jabber_published</wp:meta_key><wp:meta_value><![CDATA[1290978576]]></wp:meta_value></wp:postmeta>'
		i += '<wp:postmeta><wp:meta_key>_wp_old_slug</wp:meta_key><wp:meta_value><![CDATA[]]></wp:meta_value></wp:postmeta>'
		i += '</item>'
		return i
		
	def create_site_list ():
		html_list = '<div>'
		for k,v in rgs.items(): #region
			r = capital(k)
			html_list += '<div class="region-list" id="region-list-' + r + '">'
			html_list += '<div class="region-header" id="region-header-' + r + '">' + r + ' Region</div>' + nl
			for key,val in v.items(): #group
				g = slugify(key)
				html_list += '<div class="group-list" id="group-list-' + g + '">' + nl
				html_list += '<div class="group-header" id="group-header-' + g + '">'+ key +'</div>' + nl
				for i in val: #site
					s = slugify(i)
					html_list += '<div class="site-item" id="' + s + '">' + i +'</div>' + nl
				html_list += '</div>' + nl # end group
				
			html_list += '</div>' + nl # end region
		html_list += '</div>' + nl #end list
		return str(html_list)
		
	rootdir='D:/@nc_birding_trail/website/squarespace/sites/'
	datadir='D:/@nc_birding_trail/website/squarespace/database/'
	kmldir='D:/@nc_birding_trail/website/squarespace/kml/'

	nl = '\n'
	nl_char = '|'
	d = '~'
	d_pipe='|'
	scale = 1
	pipe_delim = '|'
	sites = {} #global dictionary for site data

	#region_style
	rs = {}
	rs = {'mountain':'pointMSite','piedmont':'pointPSite','coastal':'pointCSite','obs':'pointOBS','bfb':'pointBFB'}

	#point_styles
	ps = {}
	ps['pointPSite'] = '<style id="pointPSite"><IconStyle><scale>'+ str(scale) + '</scale><Icon><href>' + base_url_img + 'map_dot.png</href></Icon></IconStyle></style>'
	ps['pointMSite'] = '<style id="pointPSite"><IconStyle><scale>'+ str(scale) + '</scale><Icon><href>' + base_url_img + 'map_dot.png</href></Icon></IconStyle></style>'
	ps['pointCSite'] = '<style id="pointPSite"><IconStyle><scale>'+ str(scale) + '</scale><Icon><href>' + base_url_img + 'map_dot.png</href></Icon></IconStyle></style>'
	ps['pointBFB'] = '<style id="pointPSite"><IconStyle><scale>'+ str(scale) + '</scale><Icon><href>' + base_url_img + 'map_dot.png</href></Icon></IconStyle></style>'
	ps['pointOBS'] = '<style id="pointPSite"><IconStyle><scale>'+ str(scale) + '</scale><Icon><href>' + base_url_img + 'logo_ebird_icon.png</href></Icon></IconStyle></style>'

	#this is the text that belongs at the beginning and end of a kml file
	#the only items to add will be each placemark element
	#hf = open(rootdir + 'site_kml_header.txt', 'r')
	#header = open(rootdir + 'site_kml_header.txt', 'r').read()
	kml_header = open(rootdir + 'site_kml_header_highlight.txt', 'r').read()
	kml_footer = '</Document></kml>'
	rss_header = open(rootdir + 'rss_header.txt', 'r').read()
	rss_footer = '</channel></rss>'
	h = [] #array for column headings

	#sites file
	#prep this text file by:
	#	1. replace all tabs with ~
	#	2. replace CR/LF with |
	#	3. replace all LF with '<br/>'
	#	4. replace all | with '\n'

	#source text file for NCBT sites
	# s = open(rootdir + 'ncbt_sites.txt', 'r').read()

	s = open(rootdir + 'ncbt_sites.txt', 'r').read()
	sl = s.splitlines()

	#error log
	e = open(rootdir + 'errorlog.txt','w')

	#json for dynamically creating map balloons
	if switch['json']: 
		json_out = open(rootdir + 'ncbt_sites_json.txt','w')
		json = "{"

	#xml for dynamically creating map balloons
	if switch['xml']: 
		xml_out = open(rootdir + 'ncbt_sites.xml', 'w')
		x='<map>'

	#kml output
	# k_out = open(kmldir + 'sites_test3.kml', 'w')
	if switch['kml']:
		k_out = open(kmldir + 'sites_test4.kml', 'w')
		kml=kml_header + nl

	#rss output - import into squarespace for blog posts
	# rss_out = open(rootdir + 'rss.xml','w')
	if switch['rss']: 
		rss_out = open(rootdir + 'rss.xml','w')
		rss = rss_header + nl

	#app engine output - import into google app engine for creating bird lists
	if switch['ae']:
		ae_out = open(rootdir + 'ncbt_sites_ae.txt','w')
		ae = 'region|site_num|group_name|site_name|affiliation|lat_dd|lon_dd|site_id|grp_file|slug' + nl

	# mt format output
	if switch['mt']:
		mt_out = open(rootdir + 'mt_entries.txt', 'w')
		mt = ''

	#create dictionary of elements, then build string out of the dictionary
	for ln,l in enumerate(sl):
		r = l.split(d)
		if ln == 0: 	#get headings
				# should be: Timestamp, name, siteid, info_link_name, db_link_name, region, group, owner, address, counties, website, other address, phone, description, species_of_interest, habitats, special_concern, access_parking, directions, coord_dms_plain, gazeteer, special_features, amenities, lad_dd, lon_dd, slug, site_num, site_pg, group_pg
			for i in r: h.append(i)
		else:
			#create dictionary of table line	
			sd = {}
			sd = dict([(h[i],v.strip('"')) for i,v in enumerate(r)])
			sd['slug'] = slugify(sd['name'])[:60] #add slug to dictionary
			if len(sd['slug']) >60: e.write("slug greater than 60 chars - " + sd['slug'] + nl)
			
			#populate site_region and site_group dictionaries
			site_region[sd['name']] = sd['region']
			site_group[sd['name']] = sd['group']

			if rgs[sd['region']][sd['group']]:rgs[sd['region']][sd['group']].append(sd['name'])
			else:rgs[sd['region']][sd['group']]=[sd['name']]

			#add to global site dictionary - key is site_id
			sites[sd['siteid']] = sd['slug']
			
			#add to kml file
			if switch['kml']: kml += create_placemark(sd) + nl

			#add to rss
			if switch['rss']: rss += create_item(sd) + nl
			
			#add to map xml
			if switch['xml']: x += create_map_xml(sd) + nl
			
			#add to ae text import file - deprecated
			if switch['ae']: ae += d_pipe.join([sd['region'], sd['site_num'],sd['group'], sd['name'], sd['owner'], sd['lat_dd'], sd['lon_dd'], sd['siteid'],'', sd['slug']]) + nl

			#add to mt text import file - deprecated
			if switch['mt']: mt += create_mt_item(sd)
			
			#add to json text import file - deprecated
			#if json_switch: json += '"' + sd['slug'] + '":["name":"' + sd['name'] + '","region":"' + sd['region'] + '","group":"' + sd['group'] + '","coords":"' + sd['lat_dd'] + ',' + sd['lon_dd'] + '"],'
			if switch['json']: json += '"' + sd['slug'] + '":"' +sd['name'] + '",'
			

	#output site group/region list
	if switch['sl']:
		site_list_html = open(rootdir + 'site_list_html.txt', 'w')
		site_list_html.write(create_site_list())
			
	#output kml
	if switch['kml']:
		kml += kml_footer
		k_out.write(kml)

	#output map xml
	if switch['xml']:
		x += '</map>'
		xml_out.write(x)

	#output_rss
	if switch['rss']:
		rss += rss_footer
		rss_out.write(rss)

	#output_ae_text_file
	if switch['ae']: ae_out.write(ae)

	#output mt text file
	if switch['mt']: mt_out.write(mt)

	#output json text file
	if switch['json']: json_out.write(json[:-1] + "}")

	###########################################
	#create bird list file for import into GAE

	if switch['ae']:
		
		# bird database
		# birdID,siteNumber,commonName,scientificName,spring,summer,fall,winter,comment
		b = open(datadir + 'bird.csv', 'r').read()
		bl = b.splitlines()

		out_bl = open(datadir +'bird_all.txt', 'w')
		out_bl.write('site_slug,site_id,commonName,scientificName,spp_slug,spring,summer,fall,winter,comment' + nl)
		#out.write("birdID,siteNumber,commonName,scientificName,spring,summer,fall,winter,comment,scientificSlug" + nl)

		spp = {} #dictionary of species: common name
		hb=[]
		bd ={}
		f_count = 0
		for ln,l in enumerate(bl):
			row = l.split(',')
			if ln==0:
				for iter in row: 
					# should be: birdID, siteNumber, commonName, scientificName, spring, summer, fall, winter, comment
					#print iter
					hb.append(iter)
				
			else:
				#-------------------------------------------------------------------------------------------------------------------	
				# comment out - place all in one file
				#determine if to start a new file
				mod = ln%500
				if mod == 0: 
					out_bl.close()
					f_count +=1
					out_bl = open(datadir +'bird' + str(f_count) + '.txt', 'w')
					out_bl.write('site_slug,site_id,commonName,scientificName,spp_slug,spring,summer,fall,winter,comment' + nl)
				#-------------------------------------------------------------------------------------------------------------------	

				#create dictionary of table line	
				bd = {}
				bd = dict([(hb[iterater],val) for iterater,val in enumerate(row)])
				bd['spp_slug'] = slugify(bd['scientificName']) #add spp_slug to dictionary
				if sites.has_key(bd['siteNumber']):
					# use this line to write out line as in a normal text file
					#---------------------------------------------------------------------------------------------------
					out_bl.write(",".join([sites[bd['siteNumber']],bd['siteNumber'], bd['commonName'],bd['scientificName'],bd['spp_slug'],bd['spring'],bd['summer'],bd['fall'],bd['winter'],bd['comment'] ])+nl)
					
					#use this line to output in format to create a list of line dictionaries
					#---------------------------------------------------------------------------------------------------
					#out_bl.write('{' + ','.join(['"site_slug":"' + sites[bd["siteNumber"]] +'"','"site_id":"' + bd["siteNumber"] + '"', '"commonName":"' + bd["commonName"]+'"', '"scientificName":"' + bd["scientificName"]+'"','"spp_slug":"' + bd["spp_slug"] + '"','"spring":"' + bd["spring"]+ '"','"summer":"' + bd["summer"] + '"','"fall":"' + bd["fall"]+'"','"winter":"' + bd["winter"]+'"','"comment":"' + bd["comment"]+'"' ])+'},')

					#use this line to output in format to create an xml file
					#---------------------------------------------------------------------------------------------------
					# out_string = '<sitespp>'
					# out_string += '<site_slug>' + sites[bd["siteNumber"]] + '</site_slug>'
					# out_string += '<site_id>' + bd["siteNumber"] + '</site_id>'
					# out_string += '<commonName>' + bd["commonName"] + '</commonName>'
					# out_string += '<scientificName>' + bd["scientificName"] + '</scientificName>'
					# out_string += '<spp_slug>' + bd["spp_slug"] + '</spp_slug>'
					# out_string += '<spring>' + bd["spring"] + '</spring>'
					# out_string += '<summer>' + bd["summer"] + '</summer>'
					# out_string += '<winter>' + bd["winter"] + '</winter>'
					# out_string += '<fall>' + bd["fall"] + '</fall>'
					# out_string += '<comment>' + bd["comment"] + '</comment>'
					# out_string += '</sitespp>'
					# out_bl.write(out_string)
					
				#out_bl.write(lstring + nl)
				#out.write(str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "," + slugify(str(row[3])) + "," + str(row[4]) + "," + str(row[5]) + "," + str(row[6]) + "," + str(row[7]) + "," + str(row[8]) + "'")

				#add to spp dictionary for output later	
				if not spp.has_key(bd['spp_slug']):
					spp[bd['spp_slug']] = [bd['scientificName'],bd['commonName'],bd['birdID']]
				

		#finished, now output species list
		slist = open(datadir +'spplist.txt','w')
		slist.write("scientificSlug,scientificName,commonName,birdID" + nl)
		for k,v in spp.iteritems():
			slist.write(k + "," + ",".join(v) + nl)
		
		
if __name__ == "__main__":
	main()