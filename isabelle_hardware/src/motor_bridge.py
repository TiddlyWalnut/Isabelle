import rospy 
import RPi.GPIO as GPIO
import math
import geometry_msgs.msg as geom

# Constants (Everything is in SI units)
WHEEL_RADIUS = 0.0315 
METERS_PER_REV = WHEEL_RADIUS * math.pi * 2
REVS_PER_METER = 1/METERS_PER_REV
WHEEL_BASE = 0.2
MAX_VEL = 2.4

# Pin Declarations
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
pinL = GPIO.PWM(11, 1000)
pinR = GPIO.PWM(13, 1000)


# Do math to get motor pwm commands then write commands to pins -> motor controller
def cmd_vel_cb(cmd_vel):
	left_vel = cmd_vel.linear.x - (0.5 * cmd_vel.angular.z * WHEEL_BASE)
	right_vel = cmd_vel.linear.x + (0.5 * cmd_vel.angular.z * WHEEL_BASE)
	
	# Get duty cycles
	
	l_duty = 50 + ((left_vel/MAX_VEL) *50)
	r_duty = 50 + ((right_vel/MAX_VEL) * 50)
	
	# Write to pins
	
	pinL.start(l_duty)
	pinR.start(r_duty)

	
		
def main():
	rospy.init_node('motor_bridge',anonymous=True,log_level=rospy.DEBUG)
	
	# Subscribers
	cmd_vel_sub = rospy.Subscriber('/cmd_vel', geom.Twist, callback=cmd_vel_cb)
	
	while not rospy.is_shutdown():
		rospy.spin()
		
if __name__ =='__main__':
	main()

