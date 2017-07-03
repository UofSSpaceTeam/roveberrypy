grep "^NavigationProcess" ../log.log > gpslogs
awk '{print $4}' gpslogs > gpslogs.csv
rm gpslogs
python plot_gps.py
