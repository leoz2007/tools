$(document).ready(function(){


/*
    document.getElementByTagName("iframe").contentWindow.document.body.onclick = 
	function() {
	    alert("iframe clicked");
	}
*/
    $("button").click(function(){
        var d =  $(".departure").val();
        var a =  $(".arrival").val();

        var mygc = new google.maps.Geocoder();
        var departure;
        var arrival;
        var latdeparture  = 0;
        var longdeparture = 0;
        var latarrival  = 0;
        var longarrival = 0;

        mygc.geocode({'address' : d}, function(results, status){
            departure = results[0].geometry.location;
            latdeparture   = results[0].geometry.location.lat();
            longdeparture  = results[0].geometry.location.lng();
            mygc.geocode({'address' : a}, function(results, status){
		arrival = results[0].geometry.location;
		latarrival  = results[0].geometry.location.lat();
		longarrival = results[0].geometry.location.lng();
		distance = google.maps.geometry.spherical.computeDistanceBetween(departure, arrival);
		$.getJSON('/data/',{ "departure": d, "arrival": a, "distance": distance  })
		
            });
        });
    });

    function create_image()
    {
	var $word   = $("#letter-container h2 a"),
        lettering   = $word.lettering();

        var extensionPlugin         = {
            wrapper     : function() {
		var $w      = this;
		$w.children('span').each( function(i) {
                    var $el = $(this),
		    t   = $el.text();

		    if( t !== ' ' ) {
			var $newStruc = $('<div class="twrap"><div class="tbg"><span>' + t + '</span></div><div class="tup"><div class="tfront"><span>' + t + '</span></div><div class="tback"><span>' + t + '</span></div></div><div class="tdown"><spa\
n>' + t + '</span></div></div>');

			$newStruc.insertAfter( $el );
			$el.remove();
		    }
		});
            }
        };
        $.extend( true, lettering, extensionPlugin );
        lettering.wrapper();
    }

    function init()
    {
	
	$.getJSON('/s/travels.json', function(data){
	    var i = 0;
	    var distance = 0;
	    var json = jQuery.parseJSON(data);
	    var html = "";
	    while (data[i])
	    {
		distance = Number(distance) + Number(data[i].distance);
		d = data[i].from.split(',');
		a = data[i].to.split(',');
		html += "<tr><th>"+data[i].from+"</th><th>"+data[i].to+"</th><th>"+Math.round(data[i].distance/1000)+"KM</th><th><a href='/timeline/?d="+d[0]+"&a="+a[0]+"&dist="+Math.round(data[i].distance/1000)+"&t="+Math.round(distance/1000)+"'>map</a></th></tr>";
		i++;
	    }
	    $(".result").append(html);
	    distance = Number(distance) / 1000;
	    distancemiles = Number(distance) * 0.621371192;
	    $(".total").append("<h1>"+Math.round(distance)+" KM</h1>")
	    $(".totalmiles").append("<h1>"+Math.round(distancemiles)+" Miles</h1>")
	})
    }

    init();
    create_image();
});
