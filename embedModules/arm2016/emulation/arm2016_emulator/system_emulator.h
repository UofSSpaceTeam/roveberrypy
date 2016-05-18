#pragma once
#include "stdafx.h"
#include "motor_emulator.h"

struct packet;

void digitalWrite(int pin, int v);
void analogWrite(int pin, int v);
int analogRead(int pin);

#include "../../new/arm2016_feedback.h"
#include "../../new/arm2016_control.h"
#include <iostream>

#define A8 19
#define A7 20
#define A6 21

class Emulator
{
public:
	static void initialize() {
		motors.reserve(6);
		motors.push_back(MotorEmulator(1, 3, 18));
		motors.push_back(MotorEmulator(7, 2, 4));
		motors.push_back(MotorEmulator(11, 8, 5));
		motors.push_back(MotorEmulator(17, 16, 10, A8));
		motors.push_back(MotorEmulator(15, 14, 9, A7));
		motors.push_back(MotorEmulator(13, 12, 6, A6));
		updateFeedback();
		updateFeedback();
		updateFeedback();
		updateFeedback();
		updateFeedback();
		updateFeedback();
		updateFeedback();
		updateFeedback();
	}

	static  MotorEmulator* findPINA(int pina) {
		for (int i = 0; i < 6; ++i) {
			if (motors[i].PINA == pina) {
				return &motors[i];
			}
		}
		return nullptr;
	}

	static  MotorEmulator* findPINB(int pinb) {
		for (int i = 0; i < 6; ++i) {
			if (motors[i].PINB == pinb) {
				return &motors[i];
			}
		}
		return nullptr;
	}

	static  MotorEmulator* findPINPWM(int pinpwm) {
		for (int i = 0; i < 6; ++i) {
			if (motors[i].PINPWM == pinpwm) {
				return &motors[i];
			}
		}
		return nullptr;
	}

	static  MotorEmulator* findPINAI(int pinai) {
		for (int i = 0; i < 6; ++i) {
			if (motors[i].PINAI == pinai) {
				return &motors[i];
			}
		}
		return nullptr;
	}

	static void stepTime() {
		for (int i = 0; i < 6; ++i) {
			motors[i].stepTime(100);
		}
	}

	static void emulateMovement(int pos1, int pos2, int pos3, int pos4, int pos5, int pos6) {
		bool done = false;
		g_destination[0] = pos1;
		g_destination[1] = pos2;
		g_destination[2] = pos3;
		g_destination[3] = pos4;
		g_destination[4] = pos5;
		g_destination[5] = pos6;
		while (!done) {
			updateFeedback();
			updateControllers();
			stepTime();
			//std::cout << g_destination[3] - (*g_position)[3] << "\n";
			//std::cout << g_destination[4] - (*g_position)[4] << "\n";
			//std::cout << g_destination[5] - (*g_position)[5] << "\n";

			done = (DCM_stages[0] == DONE
				&& DCM_stages[1] == DONE
				&& DCM_stages[2] == DONE
				&& DCM_stages[3] == DONE
				&& DCM_stages[4] == DONE
				&& DCM_stages[5] == DONE);
		}
		std::cout << "dc(1,:)=[" << motors[3].getDCLog() << "];\n";
		std::cout << "time=[" << motors[3].getTimeLog() << "];\n";
		std::cout << "pos(1,:)=[" << motors[3].getPosLog() << "];\n";
		std::cout << "dc(2,:)=[" << motors[4].getDCLog() << "];\n";
		std::cout << "pos(2,:)=[" << motors[4].getPosLog() << "];\n";
		std::cout << "dc(2,:)=[" << motors[5].getDCLog() << "];\n";
		std::cout << "pos(3,:)=[" << motors[5].getPosLog() << "];\n";
	}
	static std::vector<MotorEmulator> motors;


};


void digitalWrite(int pin, int v) {
	MotorEmulator* motor;
	motor = Emulator::findPINA(pin);
	if (motor == nullptr) {
		motor = Emulator::findPINB(pin);
		motor->setPINB(v);
		if (motor == nullptr) {
			throw std::exception("Inavlid digitalWrite pin");
		}
	}
	else {
		motor->setPINA(v);
	}

}

void analogWrite(int pin, int v) {
	MotorEmulator* motor = Emulator::findPINPWM(pin);
	if (pin == INT_MAX)
		Emulator::motors[0].setDutyCycle(v);
	else
		motor->setDutyCycle(v);
}

int analogRead(int pin) {
	MotorEmulator* motor = Emulator::findPINAI(pin);
	return motor->position;
}