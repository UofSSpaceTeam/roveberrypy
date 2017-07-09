grep "^SimpleNavigationProcess" Prospector1.log > gpslogs
awk '{print $3}' gpslogs > gpslogs1.csv
rm gpslogs
grep "^SimpleNavigationProcess" Prospector2.log > gpslogs
awk '{print $3}' gpslogs > gpslogs2.csv
rm gpslogs
#python plot_gps.py
