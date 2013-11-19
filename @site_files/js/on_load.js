
var currSiteSlug = '';
var currSiteName = '';
var currSppSlug='';
var currSppName='';
var gKey = 'AIzaSyBq3s5965sCxAclqaIJnvYgW80RNvuELB0'; //access google key
var ftSiteBirdList = '1T3WpajUsWBB-o9PjnKqV1J2KIYVDwnfwcqJ0Qiw'; //google key for sitebirdlist fusion table
var ftSiteBirdListTest = '10S7ruCevzaVkjQE1dWrq_3xy0vqtq7UumAAR7hs'; //google key for sitebirdlist_testing fusion table
var ftBirdList = '1eP6OoUbNBFKuXPknXuDp4gEepGb8Ml08F3EVQ5Q'; //google key for birdlist fusion table
var ftUrl = 'https://www.googleapis.com/fusiontables/v1/'
var corsSupport = $.support.cors;
var img_text = {'0001':'Winter','0010':'Fall','0011':'Fall, Winter','0100':'Summer','0101':'Summer, Winter','0110':'Summer, Fall','0111':'Summer, Fall, Winter','1000':'Spring','1001':'Spring, Winter','1010':'Spring, Fall','1011':'Spring, Fall, Winter','1100':'Spring, Summer','1101':'Spring, Summer, Winter','1110':'Spring, Summer, Fall', '1111':'Spring, Summer, Fall, Winter'}
$(document).ready(function() {
	/* $('#navigationTop-sectionContent5159729 .content-navigation').after($('#moduleContent15899782')); */
	$('#social_logos').after($('#moduleContent15899782'));
	document.getElementById("mc_embed_signup_field").value = "subscribe by email";
	
	//likelihood array for birdlists
	likelihood = {};
	likelihood['0'] = '';
	likelihood['1']='rare';
	likelihood['2']='uncommon';
	likelihood['3']='occasional';
	likelihood['4']='fairly common';
	likelihood['5']='common';
	
	//ll_class array for formatting birdlists
	llclass = {};
	llclass['0'] = ' uncommon';
	llclass['1']=' uncommon';
	llclass['2']=' uncommon';
	llclass['3']=' common';
	llclass['4']=' common';
	llclass['5']=' common';
	
	
	//detect mobile browser
	
	if (document.cookie.indexOf('fullsite') > -1) {
        return; // skip redirect
    }
    if (location.search.indexOf('fullsite') > -1) {
        document.cookie = 'fullsite=true; path=/;'
        return; // skip redirect
    } 

	if (!($.inArray("sites",window.location.href.split("/")[3]))) {
		var mobile = (/iphone|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));  
		if (mobile) {document.location = "http://www.ncbirdingtrail.appspot.com";};
	};
	});

function clearsearch() {document.getElementById("mc_embed_signup_field").value = "";};
	
//takes array of items, parses out season/bird likelihood, and translates to appropriate image
function get_img_file(a) {
	//a should be an array 0=spring, 1=summer, 2=fall, 3=winter
	return cal_llhood(a[0]) + cal_llhood(a[1]) +cal_llhood(a[2]) +cal_llhood(a[3]);
};
function cal_llhood (i) {
  //take passed text, translate to binary value
  //1= likely to see, 0=unlikely to see
  var r = "0";
  if (parseInt(i)>2){ r = "1"};
  return r;
};

