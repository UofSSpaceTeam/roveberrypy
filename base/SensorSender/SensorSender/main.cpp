#include "OVR_CAPI.h"
#include "Kernel/OVR_Math.h"
#include <cstdio>
#include <Windows.h>

using namespace OVR;
using namespace std;

struct serialCommand
{
	char h1;
	char h2;
	char h3;
	byte panHigh;
	byte panLow;
	byte tilt;
};

ovrHmd hmd;
ovrSensorState ss;
sockaddr_in rover;

SOCKET makeSocket(char* roverAddr, int roverPort)
{
	WSAData data;

	rover.sin_family = AF_INET;
	rover.sin_addr.s_addr = inet_addr(roverAddr);
	rover.sin_port = htons(roverPort);

	if (WSAStartup(MAKEWORD(2, 2), &data))
	{
		fprintf(stderr, "Windows error!\n");
		exit(-1);
	}

	int sock = socket(AF_INET, SOCK_DGRAM, 0);
	if (sock == INVALID_SOCKET)
	{
		fprintf(stderr, "Socket error!\n");
		WSACleanup();
		exit(-1);
	}

	SOCKET s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	return s;
}

int main(int argc, char* argv[])
{
	if (argc != 3)
	{
		fprintf(stderr, "args: rover IP, rover port\n");
		exit(0);
	}
	struct serialCommand data;
	data.h1 = 'm';
	data.h2 = 's';
	data.h3 = 'g';
	SOCKET sock = makeSocket(argv[1], atoi(argv[2]));
	ovr_Initialize();
	hmd = ovrHmd_Create(0);
	if(hmd)
		ovrHmd_StartSensor(hmd, ovrSensorCap_Orientation | ovrSensorCap_YawCorrection, ovrSensorCap_Orientation);
	else
		fprintf(stderr, "no HMD!\n");
	while(hmd)
	{
		ss = ovrHmd_GetSensorState(hmd, 0.0);
		if(ss.StatusFlags & (ovrStatus_OrientationTracked))
		{
			Transformf pose = ss.Recorded.Pose;
			float fyaw, fpitch, froll;
			pose.Rotation.GetEulerAngles<Axis_Y, Axis_X, Axis_Z>(&fyaw, &fpitch, &froll);
			int pan = int(540 - RadToDegree(fyaw));
			int tilt = int(RadToDegree(1.7 * fpitch) + 90);
			if(pan > 360)
				pan -= 360;
			else if(pan < 0)
				pan += 360;
			if(tilt > 180)
				tilt = 180;
			else if(tilt < 0)
				tilt = 0;
			data.panHigh = (byte)(pan >> 8);
			data.panLow = (byte)pan;
			data.tilt = (byte)tilt;
			//printf("pan: %i\n", ((data.panHigh << 8) + (data.panLow)));
			//printf("tilt: %i\n", data.tilt);
			sendto(sock, (char*)&data, sizeof(data), 0, (struct sockaddr*)&rover, sizeof(rover));
			Sleep(50);
		}
	}
	ovrHmd_Destroy(hmd);
	ovr_Shutdown();
	return 0;
}