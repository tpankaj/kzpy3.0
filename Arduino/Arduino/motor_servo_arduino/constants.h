/////////////////////
// All possible states (i.e. first numbers sent in tuples along serial)
//
// These are the possible states of the control system.
// States are reached by button presses or drive commands, except for error state.
#define STATE_A 10
#define STATE_B 20
#define STATE_C 30
#define STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR 5
#define STATE_CAFFE_CAFFE_STEER_CAFFE_MOTOR 6
#define STATE_CAFFE_HUMAN_STEER_CAFFE_MOTOR 7
#define STATE_D 40
#define STATE_ERROR                         -1
// Now for the sensors
#define STATE_GPS                           "'gps'"
#define STATE_GYRO                          "'gyro'"
#define STATE_SONAR                         "'sonar'"
#define STATE_ENCODER                       "'encoder'"
//
/////////////////////


/////////////////////
// Servo constants
//
// These define extreme min an max values that should never be broken.
#define SERVO_MAX   4000
#define MOTOR_MAX   SERVO_MAX
#define BUTTON_MAX  SERVO_MAX
#define SERVO_MIN   500
#define MOTOR_MIN   SERVO_MIN
#define BUTTON_MIN  SERVO_MIN
//
/////////////////////


/////////////////////
// Changed these values 1 Feb. 2017 to avoid falling into state 4 from state 6
// The hand-held radio controller has two buttons. Pressing the upper or lower
// allows for reaching separate PWM levels: ~ 1710, 1200, 1000, and 888
// These are used for different control states.
#define BUTTON_A 1900 //1988 // Human in full control of driving 
#define BUTTON_B 1700 // Lock state
#define BUTTON_C 1424  // Caffe steering, human on accelerator
#define BUTTON_D 870  // Calibration of steering and motor control ranges
#define BUTTON_DELTA 50 // range around button value that is considered in that value
//
/////////////////////

int ButtonStates[] = {10,20,30,40};
int ButtonFreqs[] = {1900,1700,1424,870};

