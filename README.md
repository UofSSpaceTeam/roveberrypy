# rover-software

This project includes all of the client, server, and embedded software elements written for the University of Saskatchewan Space Design Team's Mars Rover project. 
For more information on the team, see [usst.ca](http://usst.ca)

## Pulling remote UofSSpaceDesign Code

The gui-software/RoverWebUI repo is reflected inside this repository. In order to get the latest files you must do the following:
       $ git merge -s ours --no-commit WebUI/master
       $ git rm -rf coreRover/WebUI
       $ git read-tree --prefix=coreRover/WebUI/ -u WebUI/master:RoverWebUI
       $ git commit

Or you can temporarily copy and paste the files if you just want to do some quick testing.
__All commits to these files should happen from the gui-software repo!__
	
### Update 09/24

All of the 2014-2015 code has been removed and only a skelleton of the rover main software remains.
To view Legacy Code please download one of our "releases".

We will be doing a near complete rewrite for 2015-2016 of most modules. The main framework aims to be backward compatable with old rover modules.

Please see our Wiki for design information. The team will be updating it over the course of the year.