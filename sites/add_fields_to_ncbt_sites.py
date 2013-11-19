
import os


	
rootdir='D:/@nc_birding_trail/website/squarespace/sites/'
nl = '\n'
d = '~'
pipe_delim = '|'

#source text file for NCBT sites
# s = open(rootdir + 'ncbt_sites.txt', 'r').read()
s = open(rootdir + 'ncbt_sites.txt', 'r').read()
sl = s.splitlines()


#xml for dynamically creating map balloons
txt_out = open(rootdir + 'ncbt_sites_new.txt', 'w')
t=''

for ln,l in enumerate(sl):
	r = l.split(d)
	if ln == 0: 	#get headings
			# should be: Timestamp, name, siteid, info_link_name, db_link_name, region, group, owner, address, counties, website, other address, phone, description, species_of_interest, habitats, special_concern, access_parking, directions, coord_dms_plain, gazeteer, special_features, amenities, lad_dd, lon_dd, site_grp_num
		t += l + site_grp_num
	else:
		t = l + d + 


#save text file
txt_out.write(t)