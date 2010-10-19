/**
 * plonecommunity.mobi application specific js
 * 
 */

/**
 * Make feedfeeder links tileable
 * 
 * - Front page news
 * 
 * - Feedfolder items
 * 
 */
function makeTileLinks() {
        jQuery(".feed-folder-item a, .news-item a").each(function() {
	       var a = jQuery(this);
	       var target = a.attr("href");
	       	  
	       var parent = a.parents("div").filter(':first');
	       parent.css("cursor", "pointer");
               
	       parent.click(function() {
	       	       window.location = target;
	       });	
	});
}


jQuery(document).ready(function() {
        makeTileLinks();
})
