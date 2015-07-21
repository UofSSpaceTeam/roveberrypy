#include <navigation.h>
#include <sbp.h>

#define FIFO_SIZE 512 //UART FIFO size
//Fifo stack to hold Uart bytes before parsing.
//This is uses in the piksi integratin tutorial, not sure how usefull it really is to us.
class FIFO {
 private:
  int head;
  int tail;
  byte data[FIFO_SIZE];
 public:
   FIFO();
   bool empty();
   bool full();
   bool push(byte b);
   bool pop(char *out); 
} uart_fifo;
  


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

u32 getData(u8 *buff, u32 n, void *content); //must conform to this definition to be passed to sbp_process()


void setup() {
  Serial.begin(9600);
  /* This Stuff doesn't compile (linking error)
   * initialize sbp parser*/
  sbp_state_init(&sbp_state);
  
  //register nodes and callbacks with specific message ID's
  sbp_register_callback(&sbp_state, SBP_MSG_GPS_TIME, &sbp_gps_time_callback, NULL, &gps_time_node);
  sbp_register_callback(&sbp_state, SBP_MSG_POS_LLH, &sbp_pos_llh_callback, NULL, &pos_llh_node);
  sbp_register_callback(&sbp_state, SBP_MSG_BASELINE_NED, &sbp_baseline_ned_callback, NULL, &baseline_ned_node);
  sbp_register_callback(&sbp_state, SBP_MSG_VEL_NED, &sbp_vel_ned_callback, NULL, &vel_ned_node);
  sbp_register_callback(&sbp_state, SBP_MSG_DOPS, &sbp_dops_callback, NULL, &dops_node);
  //*/

}

void loop() {
  //s8 ret = sbp_process(&sbp_state, &getData);
  Serial.print(pos_llh.lat);
  Serial.print(", ");
  Serial.print(pos_llh.lon);
  Serial.println();

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



u32 getData(u8 *buff, u32 n, void *content) {
  int i;
  for (i=0; i<n; i++)
    if (!uart_fifo.pop((char *)(buff + i)))
      break;
  return i;
}

/****************
**FIFO Methods**
****************/

FIFO::FIFO() {
  head = 0;
  tail = 0;
}
  

bool FIFO::empty() {
  return head == tail;
}

bool FIFO::full() {
  return ((tail+1) % FIFO_SIZE) == head;
}

bool FIFO::push(byte b) {
  if(full())
    return false;
  data[tail] = b;
  tail = (tail+1) % FIFO_SIZE;
  return true;
}

bool FIFO::pop(char *out) {
  if(empty())
    return 0;
  *out = data[head];
  head = (head+1) % FIFO_SIZE;
  return 1;
  
}
