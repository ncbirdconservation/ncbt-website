function getBirdListSlug(slug){
	//build and insert bird list table - called from json request
	var list = $("#birdlist");
	//clear out current list (if any)
	list.html("");
	//insert header row into table
	var hrow = $('<div/>',{"class":'header_row'});
	var firstCell = $('<div/>',{"class": "data_cell common_name",text: 'Common Name'});
	$('<br/>').appendTo(firstCell);
	$('<span/>',{"class":'scientific_name',text:'Scientific Name'}).appendTo(firstCell);
	firstCell.appendTo(hrow);

	$('<div/>',{"class":"data_cell bnc", text:'Birds of NC Link'}).appendTo(hrow);
	$('<div/>',{"class": "data_cell season",text: 'Spring'}).appendTo(hrow);
	$('<div/>',{"class": "data_cell season",text: 'Summer'}).appendTo(hrow);
	$('<div/>',{"class": "data_cell season",text: 'Fall'}).appendTo(hrow);
	$('<div/>',{"class": "data_cell season",text: 'Winter'}).appendTo(hrow);

	hImgDiv = $('<div/>', {"class": "data_cell season-icon"});
	$("<img/>",{"src":"/storage/img/1111.png"}).appendTo(hImgDiv);
	hImgDiv.appendTo(hrow);
	hrow.appendTo(list);

	if (corsSupport) {
		//browser supports CORS
		var i=0; //counter for row (even or odd formatting)
		//loop through json, build table	

		$.getJSON( ftUrl + "query?sql=SELECT commonName, scientificName, spp_slug, spring, summer, fall, winter, aou, bnc FROM " + ftSiteBirdList + " WHERE site_slug='" + slug + "' ORDER BY commonName ASC&key=" + gKey,{jsonp:false})
		.done(function(data) {

			$.each(data["rows"], function(k,v) {
				//cycle through json values
				//check info list for record
				//place error checking here - test to make sure values from gae exist on map
				//highlight every other row
				
				var r = 'row';
				i += 1;
				if (i%2 ==0){r = 'row';}
				else {r = 'odd_row';}
				var row = $('<div/>', {"class": r});

				//spp name, scientific
				var nameCell = $('<div/>',{"class": "data_cell common_name"});
				$('<a/>',{"class":"spp-link",text:v[0],"href":"/map?aou="+ v[7]}).appendTo(nameCell);
				$('<br/>').appendTo(nameCell);
				$('<span/>', {"class":'scientific_name',text:v[1]}).appendTo(nameCell);
				nameCell.appendTo(row);

				//bnc link
				bncDiv = $('<div class="data_cell bnc"><a  target="_blank" href="http://www.carolinabirdclub.org/ncbirds/view.php?species_id=' + v[8] + '"><img title="Birds of NC Info" src="/storage/img/bnc_icon.png"/></a></div>').appendTo(row);

				//add code to insert appropriate icon...
				s = "/storage/img/" + get_img_file(v.slice(3)) + ".png"

				$('<div/>', {"class": 'data_cell spring' + llclass[v[3]],text:likelihood[v[3]]}).appendTo(row);
				$('<div/>', {"class": 'data_cell summer' + llclass[v[4]],text:likelihood[v[4]]}).appendTo(row);
				$('<div/>', {"class": 'data_cell fall' + llclass[v[5]],text:likelihood[v[5]]}).appendTo(row);
				$('<div/>', {"class": 'data_cell winter' + llclass[v[6]],text:likelihood[v[6]]}).appendTo(row);
				imgDiv = $('<div/>', {"class": "data_cell season-icon"});
				$('<img/>', {"title":img_text[get_img_file(v.slice(3))],src:s}).appendTo(imgDiv);
				imgDiv.appendTo(row);
				
				row.appendTo(list);
			});


		});
		}
	else { //browser does not support CORS
		var row = $('<div/>', {"class": "odd_row"});
		var nameCell = $('<div/>',{"class":"data_cell common_name",text:"Bird List Unavailable"});
		nameCell.appendTo(row);
		row.appendTo(list);

		};
};