function GamePad(){
  //Added by Liam//
  var buttonInfo ='{"button": "0"}'
  var obj = JSON.parse(buttonInfo);
  var hasGP = false;
  var repGP;

  var Test = 0;
  var RoverYPos = 0;
  var RoverXPos = 0;
  RoverXPos = parseFloat(document.getElementById("XPos").value);
  RoverYPos = parseFloat(document.getElementById("YPos").value);

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
      
      //Updates Rover Position//
      if(gp.buttons[1].pressed){
        RoverXPos+=0.001;
        document.getElementById("XPos").value = RoverXPos;
        updateRoverPos();

      }
      else if(gp.buttons[0].pressed){ 
        RoverYPos-=0.001;
        document.getElementById("YPos").value = RoverYPos;
        updateRoverPos();
      }
      else if(gp.buttons[3].pressed){ 
        RoverYPos+=0.001;
        document.getElementById("YPos").value = RoverYPos;
        updateRoverPos();
      }
      else if(gp.buttons[2].pressed){ 
        RoverXPos-=0.001;
        document.getElementById("XPos").value = RoverXPos;
        updateRoverPos();
      }
    }




    for(var i=0;i<gp.axes.length; i+=2) {
      html+= "Stick "+(Math.ceil(i/2)+1)+": "+gp.axes[i]+","+gp.axes[i+1]+"<br/>";
    }

    $("#gamepadDisplay").html(html);
	
	$.ajax({
		url: "/gamepadAxes",
		type: "POST",
		data: JSON.stringify({"axes" : gp.axes}),
		contentType: "application/json"
	});


   
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

function UpdateRoverPos(){
  RoverXPos = document.getElementById("XPos").value;

  document.getElementById("XPos").value = 20;

}


