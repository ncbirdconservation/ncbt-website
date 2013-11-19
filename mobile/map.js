function mapSites(){
	$(".site-item-data").each(function(){
		//loop through site item data in site list
		//place markers
		//populate arrays for manipulating markers
		var slug = $(this).find(".slug").text();
		var name = $(this).find(".name").text();
		var group = $(this).find(".group").text();
		var region = $(this).find(".region").text();
		var c = $(this).find(".coords").text().split(",");
		var currPos = new google.maps.LatLng(c[0],c[1]);
		var tempSite = {}
		
		tempSite ["value"] = slug;
		tempSite ["label"] = name;
		sites.push(tempSite);
		
		//build html and populate array for the hover box/label
		var hoverBoxText = "<div class=\"info-title\" style=\"border:none;border-radius:5px;-moz-border-radius:5px;-webkit-border-radius:5px;background:#517098;color:#ffffff;padding:5px;color:white;line-height:1em\"><div style=\"font-weight:bold;font-variant:small-caps;font-size:1.1em;\">" + name + "</div><hr/><div style=\"font-weight:normal;font-variant:normal;font-size:1.1em;\">"+ region + " : " + group + "</div></div>";
		
		
		
		infoWindows[slug] = new InfoBox({
			content: hoverBoxText,
			alignBottom: true,
			pixelOffset: new google.maps.Size(20,22),
			closeBoxURL: "",
			infoBoxClearance: new google.maps.Size(1,1),
			pane: "floatPane",
			boxStyle: {
				opacity:0.9,
				width: "250px"
				}
		});

		//populate array for markers - add event listeners for hover and click
		siteMarkers[slug] = new google.maps.Marker({position:currPos,icon:icons["site"]});
		siteMarkers[slug].setMap(map);

		google.maps.event.addListener(siteMarkers[slug], "click", function() {displaySiteDetails(slug);});
		google.maps.event.addListener(siteMarkers[slug], 'mouseover', function() {infoWindows[slug].open(map, siteMarkers[slug]);});
		google.maps.event.addListener(siteMarkers[slug], 'mouseout', function() {infoWindows[slug].close();});
	});
};