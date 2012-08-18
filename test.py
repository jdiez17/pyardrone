from lib.pyardrone import PyARDrone
import time
import sys

if __name__ == '__main__':
    drone = PyARDrone()
    def takeoff_land():
        drone.reset()
        drone.takeoff()
        drone.hover()
        time.sleep(5)
        drone.move_up()
        time.sleep(5)
        drone.move_left()
        time.sleep(1)
        drone.move_right()
        time.sleep(1)
        drone.land()
        sys.exit(0)
    takeoff_land() 
