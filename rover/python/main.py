import os
import time
import multiprocessing

from statemanager import StateManager
from roverprocess.jsonserver import JsonServer
from roverprocess.exampleprocess import ExampleProcess
from roverprocess.navigation import Navigation
from roverprocess.driveprocess import DriveProcess
from roverprocess.armprocess import ArmProcess
from roverprocess.drillprocess import  DrillProcess
from roverprocess.cameraprocess import CameraProcess
from roverprocess.lidarprocess import LidarProcess
from roverprocess.oculusprocess import OculusProcess

# system configuration
localPort = 34567
remotePort = 34568
oculusPort = 34569

# build and run the system
if __name__ == "__main__":
	system = StateManager()
	processes = []
	i2cSem = multiprocessing.Semaphore(1)
	print "\nBUILD\n"

	# json server
	process = JsonServer(
		downlink = system.getDownlink(), uplink = system.getUplink(),
		local = localPort, remote = remotePort, sendPeriod = 0.1)
	system.addObserver("exampleTime", process.downlink)
	processes.append(process)

	# Piksi GPS process
	process = Navigation(
		downlink = system.getDownlink(), uplink = system.getUplink())
	system.addObserver("navHeartbeat", process.downlink)
	system.addObserver("gps_pos_lat", process.downlink)
	system.addObserver("gps_pos_lon", process.downlink)
	system.addObserver("gps_pos_height", process.downlink)
	system.addObserver("gps_pos_flags", process.downlink)
	system.addObserver("gps_baseline_n", process.downlink)
	system.addObserver("gps_baseline_e", process.downlink)
	system.addObserver("gps_baseline_d", process.downlink)
	system.addObserver("gps_baseline_flags", process.downlink)
	system.addObserver("compass_heading", process.downlink)
	processes.append(process)

	# drive process
	process = DriveProcess(
	 	downlink = system.getDownlink(), uplink = system.getUplink(),
	 	sem = i2cSem)
	system.addObserver("driveHeartbeat", process.downlink)
	system.addObserver("inputOneLeftY", process.downlink)
	system.addObserver("inputOneRightY", process.downlink)
	processes.append(process)

	# sensor process
	process = LidarProcess(
	 	downlink = system.getDownlink(), uplink = system.getUplink())
	system.addObserver("lidarHeartbeat", process.downlink)
	system.addObserver("scanRate", process.downlink)
	processes.append(process)

	# arm process
	# process = ArmProcess(
		# downlink = system.getDownlink(), uplink = system.getUplink(),
		# sem = i2cSem)
	# system.addObserver("armHeartbeat", process.downlink)
	# system.addObserver("inputTwoLeftY", process.downlink);
	# system.addObserver("inputTwoLeftX", process.downlink);
	# system.addObserver("inputTwoRightY", process.downlink);
	# system.addObserver("inputTwoRightX", process.downlink);
	# system.addObserver("inputTwoAButton", process.downlink);
	# system.addObserver("inputTwoBButton", process.downlink);
	# system.addObserver("inputTwoXButton", process.downlink);
	# system.addObserver("inputTwoYButton", process.downlink);

	# system.addObserver("armBaseSlider", process.downlink)
	# system.addObserver("IK_XVal", process.downlink);
	# system.addObserver("IK_YVal",  process.downlink);
	# system.addObserver("IK_WristVal",  process.downlink);
	# system.addObserver("armWristCw", process.downlink);
	# system.addObserver("armWristCcw",  process.downlink);
	# system.addObserver("armGrpClose",  process.downlink);
	# system.addObserver("armGrpOpen",  process.downlink);
	# processes.append(process)

	# drill process
	# process = DrillProcess(
		# downlink = system.getDownlink(), uplink = system.getUplink(),
		# sem = i2cSem)
	# system.addObserver("drillHeartbeat", process.downlink)
	# system.addObserver("drillRotation", process.downlink)
	# system.addObserver("drillTranslation", process.downlink)
	# processes.append(process)

	# camera process
	process = CameraProcess(
		downlink = system.getDownlink(), uplink = system.getUplink(),
		sem = i2cSem)
	system.addObserver("cameraHeartbeat", process.downlink)
	system.addObserver("videoState", process.downlink)
	system.addObserver("CamUp", process.downlink)
	system.addObserver("CamDown", process.downlink)
	system.addObserver("CamLeft", process.downlink)
	system.addObserver("CamRight", process.downlink)
	processes.append(process)

	process = OculusProcess(
		downlink = system.getDownlink(), uplink = system.getUplink(),
			serialPort = "/dev/ttyAMA0", udpPort = oculusPort)
	
	# start everything
	print "\nSTART: " + str([type(p).__name__ for p in processes]) + "\n"
	for process in processes:
		process.start()

	# wait until ctrl-C or error
	try:
		while True:
			time.sleep(60)
	except KeyboardInterrupt:
		print("\nSTOP: " + str([type(p).__name__ for p in processes]) + "\n")
	finally:
		system.terminate()

