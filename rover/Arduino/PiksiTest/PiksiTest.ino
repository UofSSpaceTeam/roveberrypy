#include <navigation.h>
#include <sbp.h>


sbp_state_t sbp_state;

msg_pos_llh_t      pos_llh;
msg_baseline_ned_t baseline_ned;
msg_vel_ned_t      vel_ned;
msg_dops_t        dops;
msg_gps_time_t    gps_time;

sbp_msg_callbacks_node_t pos_llh_node;
sbp_msg_callbacks_node_t baseline_ned_node;
sbp_msg_callbacks_node_t vel_ned_node;
sbp_msg_callbacks_node_t dops_node;
sbp_msg_callbacks_node_t gps_time_node;

void sbp_pos_llh_callback(u16 sender_id, u8 len, u8 msg[], void *context);
void sbp_baseline_ned_callback(u16 sender_id, u8 len, u8 msg[], void *context);
void sbp_vel_ned_callback(u16 sender_id, u8 len, u8 msg[], void *context);
void sbp_dops_callback(u16 sender_id, u8 len, u8 msg[], void *context);
void sbp_gps_time_callback(u16 sender_id, u8 len, u8 msg[], void *context);



void setup() {
  //initialize sbp parser
  sbp_state_init(&sbp_state);
  
  //register nodes and callbacks with specific message ID's
  sbp_register_callback(&sbp_state, SBP_MSG_GPS_TIME, &sbp_gps_time_callback, NULL, &gps_time_node);
  sbp_register_callback(&sbp_state, SBP_MSG_POS_LLH, &sbp_pos_llh_callback, NULL, &pos_llh_node);
  sbp_register_callback(&sbp_state, SBP_MSG_BASELINE_NED, &sbp_baseline_ned_callback, NULL, &baseline_ned_node);
  sbp_register_callback(&sbp_state, SBP_MSG_VEL_NED, &sbp_vel_ned_callback, NULL, &vel_ned_node);
  sbp_register_callback(&sbp_state, SBP_MSG_DOPS, &sbp_dops_callback, NULL, &dops_node);
  

}

void loop() {
  // put your main code here, to run repeatedly:

}


void sbp_pos_llh_callback(u16 sender_id, u8 len, u8 msg[], void *context) {
  pos_llh = *(msg_pos_llh_t *)msg;
}


void sbp_baseline_ned_callback(u16 sender_id, u8 len, u8 msg[], void *context) {
  baseline_ned = *(msg_baseline_ned_t *)msg;
}


void sbp_vel_ned_callback(u16 sender_id, u8 len, u8 msg[], void *context) {
  vel_ned = *(msg_vel_ned_t *)msg;
}


void sbp_dops_callback(u16 sender_id, u8 len, u8 msg[], void *context) {
  dops = *(msg_dops_t *)msg;
}


void sbp_gps_time_callback(u16 sender_id, u8 len, u8 msg[], void *context) {
  gps_time = *(msg_gps_time_t *)msg;
}
