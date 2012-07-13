$(document).ready(function(){
    console.log("YOUHOU");
    var dstyle = "";
    var istyle = "";

    $("button").toggle(function(){
	dstyle = $('div .active').attr("style");
	console.log(dstyle);
	istyle = $('div .active').children("iframe").attr("style");
	console.log(istyle);
	$('div .active').attr('style', $('div .active').attr('style') + ';margin-left:-100px;width:1280px;height:800px;position:absolute;');
	$('div .active').children("iframe").attr("style","margin-left:-300px;position:absolute;-webkit-transform:scale(0.8,0.8)");}
		       , function() {
	    		   $('div .active').attr('style',dstyle);
			   $('div .active').children("iframe").attr("style",istyle);
		       });

});
