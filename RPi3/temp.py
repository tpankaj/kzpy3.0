


pwm_steer.ChangeDutyCycle(7.8)
pwm_steer.ChangeDutyCycle(0)

for nino in np.arange(2.2,10,0.1):
    pwm_steer.ChangeDutyCycle(nino)
    time.sleep(0.1);pwm_steer.ChangeDutyCycle(0);time.sleep(0.3)
    print nino