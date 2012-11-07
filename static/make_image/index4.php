<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Typography Effects with CSS3 and jQuery</title>
        <link rel="stylesheet" type="text/css" href="css/demo.css" />
        <link rel="stylesheet" type="text/css" href="css/style4.css" />
        <link href='http://fonts.googleapis.com/css?family=Aldrich|Prociono' rel='stylesheet' type='text/css' />
	<script type="text/javascript" src="js/modernizr.custom.40443.js"></script>
    </head>
    <body style="background: url('./images/background-timeline.png')">

        <div class="container">
          <div id="letter-container" class="letter-container">
	    <h2>
	      <a href="#" style="color:#f6bd49">~<?php echo($argv[1]) ?>KM</a>
	    </h2>
	    <h2>
	      <a href="#"><?php echo($argv[2]."-".$argv[3])?></a>
	    </h2>
	    <h2>
	      <a href="#" style="color:#32cccc">+<?php echo($argv[4]) ?>KM</a>
	    </h2>
	  </div>
	  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
	  <script type="text/javascript" src="js/jquery.lettering.js"></script>
	  <script type="text/javascript">
	    $(function() {
	    
	    var $word		= $("#letter-container h2 a"),
	    lettering 	= $word.lettering();

	    var extensionPlugin = {
	    wrapper	: function() {
	    var $w = this;
	    $w.children('span').each( function(i) {
								var $el	= $(this),
	    t 	= $el.text();
	    
	    if( t !== ' ' ) {	
	    var $newStruc = $('<div class="twrap"><div class="tbg"><span>' + t + '</span></div><div class="tup"><div class="tfront"><span>' + t + '</span></div><div class="tback"><span>' + t + '</span></div></div><div class="tdown"><span>' + t + '</span></div></div>');
	    
	    $newStruc.insertAfter( $el );
	    $el.remove();
	    }
	    
	    });
	    }
	    };
	    $.extend( true, lettering, extensionPlugin );
	    lettering.wrapper();
					
	    });
	  </script>
        </div>
    </body>
</html>
