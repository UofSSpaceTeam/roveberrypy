#pragma once
#include <sstream>
#include <algorithm>

#define MAX_VELS 90

class Emulator;

class MotorEmulator
{
public:
	MotorEmulator(int pina, int pinb, int pinpwm, int pinai = -1) 
		: PINA(pina), PINB(pinb), PINPWM(pinpwm), PINAI(pinai)
	{
		position = 512;
		pina_v = 1;
		pinb_v = 0;
		dc_log.push_back(0);
		pos_log.push_back(512);
		time_log.push_back(0);
	}
	void setDutyCycle(int dc) {
		duty = dc;
	}

	void stepTime(int elapsed_ms) {
		dc_log.push_back(duty);
		if (duty < 0 || duty > 255) throw std::exception("negative duty cycle");
		if(pina_v == 1 && pinb_v == 0)
			position += MAX_VELS * duty / 255 * elapsed_ms / 1000;
		else if (pina_v == 0 && pinb_v == 1)
			position -= MAX_VELS * duty / 255 * elapsed_ms / 1000;
		else
			throw std::exception("incorrect PINA, PINB configuration");
		 pos_log.push_back(position);
		 time_log.push_back(time_log.back() + elapsed_ms);
	}

	void setPINA(int v) {
		pina_v = v;
	}

	void setPINB(int v) {
		pinb_v = v;
	}

	int readPosition() const {
		return position;
	}

	std::string getDCLog() {
		std::stringstream ss;
		std::for_each(dc_log.cbegin(), dc_log.cend(), [&](int v) {
			ss << v << ", ";
		});
		return ss.str().substr(0, ss.str().size() - 2);
	}
	std::string getPosLog() {
		std::stringstream ss;
		std::for_each(pos_log.cbegin(), pos_log.cend(), [&](int v) {
			ss << v << ", ";
		});
		return ss.str().substr(0, ss.str().size() - 2);
	}
	std::string getTimeLog() {
		std::stringstream ss;
		std::for_each(time_log.cbegin(), time_log.cend(), [&](int v) {
			ss << v << ", ";
		});
		return ss.str().substr(0, ss.str().size() - 2);
	}
	const int PINA;
	const int PINB;
	const int PINPWM;
	const int PINAI;
	int pina_v;
	int pinb_v;
	int duty;
	int position;
	std::vector<int> dc_log;
	std::vector<int> pos_log;
	std::vector<int> time_log;
};
