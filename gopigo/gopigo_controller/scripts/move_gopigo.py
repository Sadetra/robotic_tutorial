#!/usr/bin/env python


import sys
import rospy

from std_msgs.msg import Int8

def move(v,w,t):
    ns = rospy.get_namespace()
    rospy.init_node('gopigo_mover')
    left_publisher = rospy.Publisher(ns+'/motor/pwm/left',Int8,queue_size=10)
    right_publisher = rospy.Publisher(ns+'/motor/pwm/right',Int8,queue_size=10)

    scale = 470
    d = 0.06
    v_l = int(scale*(v + d*w))
    v_r = int(scale*(v - d*w))
    print(v_l,v_r)
    if v_l>127:
        v_l = 127
        print("v_l_max : " + str(v_l))
    elif v_l<-127:
        v_l = -127
        print("v_l_min : " + str(v_l))
    else:
        print("v_l : " + str(v_l))

    if v_r>127:
        v_r = 127
        print("v_r_max : " + str(v_r))
    elif v_r<-127:
        v_r = -127
        print("v_r_min : " + str(v_r))
    else:
        print("v_r : " + str(v_r))

    rate = rospy.Rate(100)

    # XXX : hack for getting simulation time
    time_start = rospy.get_time()
    while time_start==0:
        time_start = rospy.get_time()

    while not rospy.is_shutdown():
        left_publisher.publish(v_l)
        right_publisher.publish(v_r)
        time_from_start = rospy.get_time() - time_start
        print(rospy.get_time(),time_from_start)
        if time_from_start> t:
            break
        rate.sleep()
    left_publisher.publish(0)
    right_publisher.publish(0)

if __name__ == "__main__":
    if len(sys.argv) == 4:
        v = float(sys.argv[1])
        w = float(sys.argv[2])
        t = float(sys.argv[3])
        if v>1:
            v = 1
        elif v<-1:
            v = -1
        if w>1:
            w = 1
        elif w<-1:
            w = -1
        print(v,w)
        move(v,w,t)
    else:
        print("there should be 3 argument (v,w,t)\nv : linear velocity\nw : angular velocity\nt : execution time")
