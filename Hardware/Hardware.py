from pymata4 import pymata4
import time

current_time = 4


# def aux2():


    # taste.set_pin_mode_servo(9)
    # taste.servo_write(9, 0)
    # time.sleep(1)
    # taste.servo_write(9, 180)
    # time.sleep(1)




    # while(True):
    #
    #     time.sleep(current_time)
    #
    #     taste.digital_write(2, 0)
    #     taste.digital_write(3, 0)
    #
    #     time.sleep(1)
    #
    #     taste.digital_write(2, 0)
    #     taste.digital_write(3, 1)
    #     # start = time.time()
    #
    #
    #     # input("P")
    #     time.sleep(current_time)
    #
    #     # end = time.time()
    #
    #     taste.digital_write(2, 0)
    #     taste.digital_write(3, 0)
    #
    #     time.sleep(1)
    #
    #     taste.digital_write(2, 1)
    #     taste.digital_write(3, 0)





    # print(end - start)



##(2,0) (3,1) = y+
##(2,1) (3,0) = y-

def taste():

    taste = pymata4.Pymata4()
    taste.set_pin_mode_digital_output(2)
    taste.set_pin_mode_digital_output(3)


    yMinus(taste)
    yPlus(taste)

def yPlus(taste):
    taste.digital_write(2, 0)
    taste.digital_write(3, 1)

    time.sleep(current_time)

    taste.digital_write(2, 0)
    taste.digital_write(3, 0)


def yMinus(taste):
    taste.digital_write(2, 1)
    taste.digital_write(3, 0)

    time.sleep(current_time)

    taste.digital_write(2, 0)
    taste.digital_write(3, 0)




def cali():

    taste.digital_write(2, 1)
    taste.digital_write(3, 0)

    start = time.time()

    input("P")

    taste.digital_write(2, 0)
    taste.digital_write(3, 0)

    end = time.time()

    print(end-start)




