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
            <script = "GamePad()">
            </script>
            <button class = "btn btn-primary" onclick ="location.href='/home'">Back</button>
        <div id="gamepadPrompt" class = "row"></div>
        <div id="gamepadDisplay" class = "row"></div>
  </div>
    </center> 

</body>
</html>
