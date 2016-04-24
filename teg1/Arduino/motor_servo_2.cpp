/*
Code written for Arduino Uno.

The purpose is to read PWM signals coming out of a radio receiver
and either relay them unchanged to ESC/servo or substitute signals from a host system.

The steering servo and ESC(motor) are controlled with PWM signals. These meaning of these signals
may vary with time, and across devices. To get uniform behavior, the user calibrates with each session.
The host system deals only in percent control signals that are assumed to be based on calibrated PWM
signals. Thus, 0 should always mean 'extreme left', 49 should mean 'straight ahead', and 99 'extreme right'
in the percent signals, whereas absolute values of the PWM can vary for various reasons.

April 2016
*/


#include "PinChangeInterrupt.h" // Adafruit library
#include <Servo.h> // Arduino library

// These come from the radio receiver via three black-red-white ribbons.
#define PIN_SERVO_IN 11
#define PIN_MOTOR_IN 10
#define PIN_BUTTON_IN 12

// These go out to ESC (motor controller) and steer servo via black-red-white ribbons.
#define PIN_SERVO_OUT 9
#define PIN_MOTOR_OUT 8

// These define extreme min an max values that should never be broken.
#define SERVO_MAX   2000
#define MOTOR_MAX   SERVO_MAX
#define BUTTON_MAX  SERVO_MAX
#define SERVO_MIN   500
#define MOTOR_MIN   SERVO_MIN
#define BUTTON_MIN  SERVO_MIN

// These are the possible states of the control system.
// States are reached by button presses or drive commands.
#define STATE_HUMAN_FULL_CONTROL            1
#define STATE_LOCK                          2
#define STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR 3
#define STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR 5
#define STATE_LOCK_CALIBRATE                4
#define STATE_ERROR                         -1

// These volatile variables are set by interrupt service routines
// tied to the input pins. These values will be reset manually in the
// STATE_LOCK_CALIBRATE state, so conservative values given here.
volatile int servo_null_pwm_value = 1500;
volatile int servo_max_pwm_value  = 1600;
volatile int servo_min_pwm_value  = 1400;
volatile int motor_null_pwm_value = 1528;
volatile int motor_max_pwm_value  = 1600;
volatile int motor_min_pwm_value  = 1400;

// These are three key values indicating incoming signals.
volatile int button_pwm_value;
volatile int servo_pwm_value;
volatile int motor_pwm_value;

// These are used to interpret interrupt signals.
volatile long int button_prev_interrupt_time = 0;
volatile long int servo_prev_interrupt_time  = 0;
volatile long int motor_prev_interrupt_time  = 0;

// Some intial conditions, putting the system in lock state.
volatile int state = STATE_LOCK;
volatile int previous_state = 0;
volatile int state_transition_time_ms = 0;

// Variable to receive caffe data and format it for output.
long int caffe_last_int_read_time;
int caffe_mode;
int caffe_steer;
int caffe_motor;
int caffe_servo_pwm_value = servo_null_pwm_value;
int caffe_motor_pwm_value = motor_null_pwm_value;

// The host computer is not to worry about PWM values. These variables hold percent values
// that are passed up to host.
int servo_percent;
int motor_percent;

// Servo classes.
Servo servo;
Servo motor; 

void setup()
{
  // Establishing serial communication with host system. The best values for these parameters
  // is an open question.
  Serial.begin(9600);
  Serial.setTimeout(5);

  // Setting up three input pins
  pinMode(PIN_BUTTON_IN, INPUT_PULLUP);
  pinMode(PIN_SERVO_IN, INPUT_PULLUP);
  pinMode(PIN_MOTOR_IN, INPUT_PULLUP);

  // Attach interrupt service routines to pins. A change in signal triggers interrupts.
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_BUTTON_IN),
    button_interrupt_service_routine, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_SERVO_IN),
    servo_interrupt_service_routine, CHANGE);
  attachPinChangeInterrupt(digitalPinToPinChangeInterrupt(PIN_MOTOR_IN),
    motor_interrupt_service_routine, CHANGE);

  // Attach output pins to ESC (motor) and steering servo.
  servo.attach(PIN_SERVO_OUT); 
  motor.attach(PIN_MOTOR_OUT); 
}

// The hand-held radio controller has two buttons. Pressing the upper or lower
// allows for reaching for separate PWM levels: 1710, 1200, 1000, and 888
// These are used for different control states.
void button_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-button_prev_interrupt_time;
  // Human in full control of driving
  if (dt>BUTTON_MIN && dt<BUTTON_MAX) {
    button_pwm_value = dt;
    if (abs(button_pwm_value-1710)<50) {
      if (state != STATE_HUMAN_FULL_CONTROL) {
        previous_state = state;
        state = STATE_HUMAN_FULL_CONTROL;
        state_transition_time_ms = m/1000.0;
      }
    }
    // Lock state
    else if (abs(button_pwm_value-1200)<50) {
      if (state != STATE_LOCK) {
        previous_state = state;
        state = STATE_LOCK;
        state_transition_time_ms = m/1000.0;
      }
    }
    // Caffe steering, human on accelerator
    else if (abs(button_pwm_value-1000)<50) {
      if (state != STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR && state != STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR) {
        previous_state = state;
        state = STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR;
        state_transition_time_ms = m/1000.0;
      }
    }
    // Calibration of steering and motor control ranges
    else if (abs(button_pwm_value-888)<50) {
      if (state != STATE_LOCK_CALIBRATE) {
        previous_state = state;
        state = STATE_LOCK_CALIBRATE;
        state_transition_time_ms = m/1000.0;
        servo_null_pwm_value = servo_pwm_value;
        servo_max_pwm_value = servo_null_pwm_value;
        servo_min_pwm_value = servo_null_pwm_value;
        motor_null_pwm_value = motor_pwm_value;
        motor_max_pwm_value = motor_null_pwm_value;
        motor_min_pwm_value = motor_null_pwm_value;
      }
      if (servo_pwm_value > servo_max_pwm_value) {
        servo_max_pwm_value = servo_pwm_value;
      }
      if (servo_pwm_value < servo_min_pwm_value) {
        servo_min_pwm_value = servo_pwm_value;
      }
      if (motor_pwm_value > motor_max_pwm_value) {
        motor_max_pwm_value = motor_pwm_value;
      }
      if (motor_pwm_value < motor_min_pwm_value) {
        motor_min_pwm_value = motor_pwm_value;
      }
    }
  }
  button_prev_interrupt_time = m;
}


// Servo interrupt service routine. This would be very short except that the human can take
// control from Caffe, and Caffe can take back control if steering left in neutral position.
void servo_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-servo_prev_interrupt_time;
  if (dt>SERVO_MIN && dt<SERVO_MAX) {
    servo_pwm_value = dt;
    if (state == STATE_HUMAN_FULL_CONTROL) {
      servo.writeMicroseconds(servo_pwm_value);
    }
    else if (state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR) {
      if (abs(servo_pwm_value-servo_null_pwm_value)<=50 && (m-state_transition_time_ms)>500) {
        previous_state = state;
        state = STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR;
        state_transition_time_ms = m/1000.0;
        servo.writeMicroseconds((caffe_servo_pwm_value+servo_pwm_value)/2);
      }
      else {
        servo.writeMicroseconds(servo_pwm_value);
      }
    }
    else if (state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR) {
      if (abs(servo_pwm_value-servo_null_pwm_value)>50) {
        previous_state = state;
        state = STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR;
        state_transition_time_ms = m/1000.0;
        servo.writeMicroseconds(servo_pwm_value);   
      }
      else {
        servo.writeMicroseconds(caffe_servo_pwm_value);
      }
    }
    else {
      servo.writeMicroseconds(servo_null_pwm_value);
    }
  } 
  servo_prev_interrupt_time = m;
}


// Motor interrupt service routine. This is simple because right now only human controls motor.
void motor_interrupt_service_routine(void) {
  long int m = micros();
  int dt = m-motor_prev_interrupt_time;
  if (dt>MOTOR_MIN && dt<MOTOR_MAX) {
    motor_pwm_value = dt;
    if (state == STATE_HUMAN_FULL_CONTROL) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else if (state == STATE_CAFFE_HUMAN_STEER_HUMAN_MOTOR) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else if (state == STATE_CAFFE_CAFFE_STEER_HUMAN_MOTOR) {
      motor.writeMicroseconds(motor_pwm_value);
    }
    else {
      motor.writeMicroseconds(motor_null_pwm_value);
    }
  } 
  motor_prev_interrupt_time = m;
}



void check_for_error_conditions(void) {
/* Check state of all of these variables for out of bound conditions

  volatile int servo_null_pwm_value = 1500;
  volatile int servo_max_pwm_value  = 1600;
  volatile int servo_min_pwm_value  = 1400;

  volatile int motor_null_pwm_value = 1528;
  volatile int motor_max_pwm_value  = 1600;
  volatile int motor_min_pwm_value  = 1400;

  volatile int button_pwm_value;
  volatile int servo_pwm_value;
  volatile int motor_pwm_value;

  volatile long int button_prev_interrupt_time = 0;
  volatile long int servo_prev_interrupt_time  = 0;
  volatile long int motor_prev_interrupt_time  = 0;

  volatile int state = STATE_LOCK;
  volatile int previous_state = 0;
  volatile int state_transition_time_ms = 0;

  long int caffe_last_int_read_time;
  int caffe_mode;
  int caffe_steer;
  int caffe_motor;
  int caffe_servo_pwm_value = servo_null_pwm_value;
  int caffe_motor_pwm_value = motor_null_pwm_value;

  int servo_percent;
  int motor_percent;

*/

// Make LED blink if error state
}





void loop() {

  // Try to read the "caffe_int" sent by the host system (there is a timeout on serial reads, so the Arduino
  // doesn't wait long to get one -- in which case the caffe_int is set to zero.)
  int caffe_int = Serial.parseInt();
  // If it is received, decode it to yield three control values (i.e., caffe_mode, caffe_steer, and caffe_motor)
  if (caffe_int > 0) {
      caffe_last_int_read_time = micros()/1000;
      caffe_mode = caffe_int/10000;
      caffe_steer = (caffe_int-caffe_mode*10000)/100;
      caffe_motor = (caffe_int-caffe_steer*100-caffe_mode*10000);
    } else if (caffe_int < 0) {
      caffe_mode = caffe_int/10000;
  }
  // Turn the caffe_steer and caffe_motor values from 0 to 99 values into PWM values that can be sent 
  // to ESC (motor) and servo.
  if (caffe_mode > 0) {
    if (caffe_steer >= 49) {
      caffe_servo_pwm_value = (caffe_steer-49)/50.0 * (servo_max_pwm_value - servo_null_pwm_value) + servo_null_pwm_value;
    }
    else {
      caffe_servo_pwm_value = (caffe_steer - 50)/50.0 * (servo_null_pwm_value - servo_min_pwm_value) + servo_null_pwm_value;
    }
    if (caffe_motor >= 49) {
      caffe_motor_pwm_value = (caffe_motor-49)/50.0 * (motor_max_pwm_value - motor_null_pwm_value) + motor_null_pwm_value;
    }
    else {
      caffe_motor_pwm_value = (caffe_motor - 50)/50.0 * (motor_null_pwm_value - motor_min_pwm_value) + motor_null_pwm_value;
    }
  }

  // Compute command signal percents from signals from the handheld radio controller
  // to be sent to host computer, which doesn't bother with PWM values
  if (servo_pwm_value >= servo_null_pwm_value) {
    servo_percent = 49+50.0*(servo_pwm_value-servo_null_pwm_value)/(servo_max_pwm_value-servo_null_pwm_value);
  }
  else {
    servo_percent = 49 - 49.0*(servo_null_pwm_value-servo_pwm_value)/(servo_null_pwm_value-servo_min_pwm_value);
  }
  if (motor_pwm_value >= motor_null_pwm_value) {
    motor_percent = 49+50.0*(motor_pwm_value-motor_null_pwm_value)/(motor_max_pwm_value-motor_null_pwm_value);
  }
  else {
    motor_percent = 49 - 49.0*(motor_null_pwm_value-motor_pwm_value)/(motor_null_pwm_value-motor_min_pwm_value);
  }


  if (false) {
    Serial.print("(");
    Serial.print(state);
    Serial.print(",");
    Serial.print(button_pwm_value);
    Serial.print(",");
    Serial.print(servo_pwm_value);
    Serial.print(",[");
    Serial.print(servo_min_pwm_value);
    Serial.print(",");
    Serial.print(servo_null_pwm_value);
    Serial.print(",");
    Serial.print(servo_max_pwm_value);  
    Serial.print("],[");
    Serial.print(motor_min_pwm_value);
    Serial.print(",");
    Serial.print(motor_null_pwm_value);
    Serial.print(",");
    Serial.print(motor_max_pwm_value);
    Serial.print("],");
    Serial.print(caffe_mode);
    Serial.print(",");
    Serial.print(caffe_steer);
    Serial.print(",");
    Serial.print(caffe_motor);
    Serial.print(",");
    Serial.print(caffe_servo_pwm_value);
    Serial.print(",");
    Serial.print(caffe_motor_pwm_value);
    Serial.println(")");
  }
  else {
    // Send data string which looks like a python tuple.
    Serial.print("(");
    Serial.print(state);
    Serial.print(",");
    Serial.print(servo_percent);
    Serial.print(",");
    Serial.print(motor_percent);
    Serial.print(",");
    Serial.print(state_transition_time_ms);
    Serial.println(")");
  }

  delay(10); // How long should this be? Note, this is in ms, whereas most other times are in micro seconds.
}

