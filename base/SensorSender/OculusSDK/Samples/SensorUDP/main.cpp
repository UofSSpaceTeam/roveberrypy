
#include "OVR_CAPI.h"
#include <cstdio>

ovrHmd           HMD;
ovrHmdDesc       HMDDesc;
   
//-------------------------------------------------------------------------------------

int Init()
{
    ovr_Initialize();

	HMD = ovrHmd_Create(0);
  

	// Start the sensor which informs of the Rift's pose and motion
    ovrHmd_StartSensor(HMD, ovrSensorCap_Orientation |
                            ovrSensorCap_YawCorrection |
                            ovrSensorCap_Position, 0);
    return 0;
}


void Release(void)
{
    ovrHmd_Destroy(HMD);
    ovr_Shutdown(); 
}

int main(int argc, char* argv[])
{
	Init();
	printf("running!\n");
	Release();
}

