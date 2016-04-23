<html>
<meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
        <title></title>
        <meta name="description" content="">
        <meta name="viewport" content="width=device-width">
        <script src="/static/scripts/jquery.min.js"></script>
        <script src="/static/scripts/bootstrap.min.js"></script>
        <link rel="stylesheet" href="/static/css/bootstrap.min.css">


<head>
   <div class="dropdown">
                    <ul class="nav nav-tabs">
                        <ul class="nav nav-tabs">
                          <li><a href="/home">Navigation</a></li>
                          <li><a href="/camera">Camera</a></li>
                          <li class="active"><a href="/gamepad">Gamepad</a></li>
                          <li><a href="/gamepadoptions">Gamepad Options</a></li>
                      </ul>
                    </ul>
                </div>  
</head>
<body onload="GamePad();">
<div align ="center" class="container">
    <div align ="center" class="jumbotron">
            <h1>Gamepad</h1>
      <script src="/static/scripts/gamepad.js"></script>
          <input id = "GamepadValueChange"></input>
          <div id="gamepadPrompt" class = "row"></div>
          <div id="gamepadDisplay" class = "row"></div>
        </div>
  </div>

</body>
</html>
