
/**
 * Load upscaled action icon images if we detect high enough screen resolution.
 * 
 * We could scale these icons at the server end, but doing pixel size scales
 * without orignal vector source yields to very bad results.
 * 
 */
function fixMobileImages() {
	
	var multiplier;
	if(window.devicePixelRatio) {
		// iPhone 4
		
		multiplier = window.devicePixelRatio;
	} else {
		multiplier = 1;
	}

        if(multiplier == 2) {
	
	    // Compensate iPhone 4's 2x reported scale with 0.5x zoom
	    // jQuery seemed to have issue manipulating meta tags
	    document.getElementById("viewport").setAttribute("content", "width=device-width; initial-scale=0.5; minimum-scale=0.5; maximum-scale=0.5; user-scalable=no;");
		
	    // Load our special stylesheet having text size fixes for iPhone 4
	    jQuery("head").append("<link>");
	    css = jQuery("head").children(":last");
	    css.attr({
	      rel:  "stylesheet",
	      type: "text/css",
	      href: "++resource++gomobiletheme.basic/iphone4.css"
	    });
	}

        var width = jQuery(window).width() * multiplier;

	if(width > 480) {
	       // Assume smartphone with resolution in 640 x 480 range
	       
	       // Bump size to 24x24 -> 48x48
	       jQuery("img").each( function() {
	       	       var src = jQuery(this).attr("src");
		       src = src.replace("++resource++gomobiletheme.basic/24/", "++resource++gomobiletheme.basic/48/");		     
	       	       jQuery(this).attr("src", src);
	       });
	}
}


jQuery(document).ready(function() {
        fixMobileImages();
})
