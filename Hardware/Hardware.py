from pymata4 import pymata4
import time
import threading

current_time = 4


def aux2():

    while (True):
        print("Radio Check")
        time.sleep(1)

#   movement.set_pin_mode_servo(9)
#   movement.servo_write(9, 0)
#   time.sleep(1)
#   movement.servo_write(9, 180)
#   time.sleep(1)


#   while(True):
#
#     time.sleep(current_time)
#
#     movement.digital_write(2, 0)
#     movement.digital_write(3, 0)
#
#     time.sleep(1)
#
#     movement.digital_write(2, 0)
#     movement.digital_write(3, 1)
#     # start = time.time()
#
#
#     # input("P")
#     time.sleep(current_time)
#
#     # end = time.time()
#
#     movement.digital_write(2, 0)
#     movement.digital_write(3, 0)
#
#     time.sleep(1)
#
#     movement.digital_write(2, 1)
#     movement.digital_write(3, 0)


# print(end - start)

# (2,0) (3,1) = y+
# (2,1) (3,0) = y-

# (4,0) (5,1) = x+
# (4,1) (5,0) = x-


def taste():
    movement = pymata4.Pymata4()
    movement.set_pin_mode_digital_output(2)
    movement.set_pin_mode_digital_output(3)

    movement.set_pin_mode_digital_output(4)
    movement.set_pin_mode_digital_output(5)

    th1 = threading.Thread(target=aux2)
    th1.start()

    while (True):
        x_minus(movement)
        x_plus(movement)


def y_plus(movement):
    movement.digital_write(2, 0)
    movement.digital_write(3, 1)

    time.sleep(current_time)

    movement.digital_write(2, 0)
    movement.digital_write(3, 0)


def y_minus(movement):
    movement.digital_write(2, 1)
    movement.digital_write(3, 0)

    time.sleep(current_time)

    movement.digital_write(2, 0)
    movement.digital_write(3, 0)


def x_plus(movement):
    movement.digital_write(4, 0)
    movement.digital_write(5, 1)

    time.sleep(current_time)

    movement.digital_write(4, 0)
    movement.digital_write(5, 0)


def x_minus(movement):
    movement.digital_write(4, 1)
    movement.digital_write(5, 0)

    time.sleep(current_time)

    movement.digital_write(4, 0)
    movement.digital_write(5, 0)


def cali(movement):
    movement.digital_write(2, 1)
    movement.digital_write(3, 0)

    start = time.time()

    input("P")

    movement.digital_write(2, 0)
    movement.digital_write(3, 0)

    end = time.time()

    print(end - start)
