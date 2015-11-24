% rebase('layout.tpl', title=title, year=year)
<html>
<meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <script type="text/javascript" src="jquery/jquery v2.1.0.min.js"></script>
        <script type="text/javascript" src = "js/Gamepad.js"></script>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
        <link rel="stylesheet" href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">


<head>
</head> 
<body onload="GamePad();">>
<div class="container">
       <center>
       <div class="jumbotron">
           <h1>USST Rover GUI</h1>
           <script>
				function GamePad(){

					var hasGP = false;
					var repGP;

					function canGame() {
						return "getGamepads" in navigator;
					}

					function reportOnGamepad() {
						var gp = navigator.getGamepads()[0];
						var html = "";
							html += "id: "+gp.id+"<br/>";

						for(var i=0;i<gp.buttons.length;i++) {
							html+= "Button "+(i+1)+": ";
							if(gp.buttons[i].pressed) html+= " pressed";
							html+= "<br/>";

						}

						for(var i=0;i<gp.axes.length; i+=2) {
							html+= "Stick "+(Math.ceil(i/2)+1)+": "+gp.axes[i]+","+gp.axes[i+1]+"<br/>";
						}

						$("#gamepadDisplay").html(html);

					}

					$(document).ready(function() {

						if(canGame()) {

							var prompt = "To begin using your gamepad, connect it and press any button!";
							$("#gamepadPrompt").text(prompt);

							$(window).on("gamepadconnected", function() {
								hasGP = true;
								$("#gamepadPrompt").html("Gamepad connected!");
								console.log("connection event");
								repGP = window.setInterval(reportOnGamepad,100);
							});

							$(window).on("gamepaddisconnected", function() {
								console.log("disconnection event");
								$("#gamepadPrompt").text(prompt);
								window.clearInterval(repGP);
							});

							//setup an interval for Chrome
							var checkGP = window.setInterval(function() {
								console.log('checkGP');
								if(navigator.getGamepads()[0]) {
									if(!hasGP) $(window).trigger("gamepadconnected");
									window.clearInterval(checkGP);
								}
							}, 500);
						}

					});
				}
           </script>
           <button class = "btn btn-primary" onclick ="location.href='/home'">Back</button>
       <div id="gamepadPrompt" class = "row"></div>
       <div id="gamepadDisplay" class = "row"></div>
 </div>
   </center>

</body>
</html>
