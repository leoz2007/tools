$(document).ready(function(){
    console.log("YOUHOU");

    $("button").click(function(){
	$('div .active').attr('style', $('div .active').attr('style') + ';width:1280px;height:800px;position:absolute;margin-left:-600px');
	$('div .active').children("iframe").css("-webkit-transform:scale(0.9,0.9)");
    });

});
