'article aside footer header hgroup nav section time'.replace(/\w+/g,function(n){document.createElement(n)})
                
apex.jQuery(window).ready(function(){
                // Initialize HTML5 Elements for IE
                loadHideShowRegions();
});

loadHideShowRegions = function(){
                apex.jQuery("a.uRegionControl").click(function(){
                               link = apex.jQuery(this)
                               content = link.parents("div.uRegionHeading").next();
                               link.toggleClass("uRegionCollapsed");
                               if (content.css("display") == "block") {
                                               content.slideUp("fast","swing");
                               } else {
                                               content.slideDown("fast","swing");
                               }
                });
}
