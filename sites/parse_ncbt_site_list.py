### compile_files.py
### parses Excel xml spreadsheet and ammends data

import os
import csv
import re #regular expressions
from BeautifulSoup import BeautifulStoneSoup
from xml.dom import minidom

def format_data(xml):
	#takes xml file and tests for validity of path
	#returns '' if no result
	try:
		result = xml.string
		result = result.replace("\n","")
		result = result.strip(' ()')
		result = result.replace('      ',' ')
		result = result.replace('     ',' ')
		result = result.replace('   ',' ')
		result = result.replace('  ',' ')
		return result.encode("utf-8")
	except:
		return ''

rootdir='D:/projects/google_app_engine/ncbirdconservation_data/'
species_names = [] # list of species names
species_nc = [] #list of nc bird list data
l=[] #output line
out_cols=['name','sci_name','wap_sci_name','tsn','element_code','fed_status','state_status','wap_priority','pif_priority','bna_link','sbr_sprucefir','sbr_nhardwood','sbr_coveforest','sbr_dryconifwood','sbr_oak','sbr_earlysucc','sbr_highelevout','sbr_lowelevout','sbr_cavesmines','sbr_floodforest','sbr_riverine','sbr_bogs','pied_mesicforest','pied_dryconifwood','pied_oak','pied_earlysucc','pied_floodforest','pied_riverine','pied_lakes','pied_smallwetland','coast_mesicforest','coast_dryconifwood','coast_oak','coast_earlysucc','coast_floodforest','coast_riverine','coast_lakes','coast_drylongleaf','coast_pocosin','coast_wetpinesavanna','coast_smallwetland','coast_nonalluvialminearalwetland','coast_tidalswamp','coast_maritimeforest','coast_estuarine','coast_beachdune','ns_spp_name','ns_elcode','ns_nomenclaturalauthor','ns_nomenclaturalcitation','ns_informalgroup','ns_globalrank','ns_globalranklastreviewed','ns_globalrankreasons','ns_uri', 'ns_general description', 'ns_reprodution','ns_habitats', 'ns_foodhabits','ns_lifehistoryeditiondate']

##bird list - load the first line
#b = open(rootdir + 'nc_bird_list.xml', 'r')
#b_soup = BeautifulSoup(b)
bf = open(rootdir + 'nc_bird_list.csv', 'r')
b = csv.reader(bf, delimiter=",")

##output files
out = open('nc_bird_data.txt', 'w')
delim = "|"

refs = open('nc_bird_data_citations.txt','w')

##log file
log = open('log.txt', 'w')

# add column names to output file
line=''
for i in out_cols: line += '"' + i + '"' + delim
out.write(line + '\n')

##natureserve data file
#ns = open(rootdir + 'nc_record_example_short.xml')
ns = open(rootdir + 'ns_spp_data_20101120_u8.xml')
#ns = open(rootdir + 'xml_test.xml')
ns_soup = BeautifulStoneSoup(ns)

#cycle through natureserve records, find matches, write data to new file
ns_spp = ns_soup.findAll('globalspecies')
for spp in ns_spp:
	spp_code = spp['speciescode']
	spp_sci_name_data = spp.classification.names.scientificname
	spp_sci_name = spp_sci_name_data.unformattedname.string
	#print spp_sci_name
	##build line list
	#add nc_spp_list data
	del l[:]
	bf.seek(0)
	for row in b:
		#log.write(spp_sci_name + ': ' + row[1] +'\n')
		if row[1].strip()==spp_sci_name.strip():
			#print 'found:' + row[1]
			for i in row:l.append(i)
			#del l[-1] #remove last column (extra)
			break
	if l: #match found
		#add ns data
		l.append(spp_sci_name)
		l.append(spp_code)
		l.append(format_data(spp_sci_name_data.nomenclaturalauthor))
		l.append(format_data(spp_sci_name_data.conceptreference.formattedfullcitation))
		l.append(format_data(spp.classification.taxonomy.informaltaxonomy.informaltaxonomylevel3name))
		spp_path = spp.conservationstatus.natureservestatus.globalstatus
		l.append(format_data(spp_path.rank.code))
		l.append(format_data(spp_path.statuslastreviewed))
		l.append(format_data(spp_path.reasons))
		l.append(format_data(spp.natureserveexploreruri))
		spp_path = spp.ecologyandlifehistory
		# l.append(format_data(spp_path.ecologyandlifehistorydescription.generaldescription))
		# l.append(format_data(spp_path.reproductioncomments))
		# l.append(format_data(spp_path.habitats.habitatcomments))
		# l.append(format_data(spp_path.foodhabits.foodcomments))
		# l.append(format_data(spp_path.ecologyandlifehistoryeditiondate))
		#build line string
		line=''
		for i in l: line += '"' + i + '"' + delim
        #print line to main data file
		out.write(line.encode("utf-8") + '\n')
		#build line string for refs
		# cits = spp.findAll('citation')
		# for c in cits: 
			# print spp_code
			# print delim
			# print c
			# line = ''.join('"',spp_code,'"',delim,'"',c.encode("utf-8"),'"',delim)
			# refs.write(line + '\n')