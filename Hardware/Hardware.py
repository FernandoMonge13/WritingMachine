from pymata4 import pymata4
import time


class Hardware:

    def __init__(self):
        self.movement = pymata4.Pymata4()
        self.movement.set_pin_mode_digital_output(2)
        self.movement.set_pin_mode_digital_output(3)

        self.movement.set_pin_mode_digital_output(4)
        self.movement.set_pin_mode_digital_output(5)

        self.movement.set_pin_mode_servo(9)

        self.current_time_yminus = 0.4
        self.current_time_yplus = 0.44
        self.current_time_xplus = 0.5
        self.current_time_xminus = 0.54
        self.current_time_diagonal = 0.65

        self.x = 1
        self.y = 1

        self.speed = 1

    """
    This method allows diagonal movements
    to the first quadrant 
    """
    def diagonal1(self):

        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        # X
        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        # Y
        self.movement.digital_write(2, 1)
        self.movement.digital_write(3, 1)

        # X start
        self.movement.digital_write(4, 1)

        # Y start
        self.movement.digital_write(2, 0)

        time.sleep(self.current_time_diagonal)

        self.movement.digital_write(2, 1)
        self.movement.digital_write(4, 0)

        time.sleep(1)

    """
    This method allows diagonal movements
    to the second quadrant 
    """
    def diagonal2(self):

        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        # X
        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        # Y
        self.movement.digital_write(2, 1)
        self.movement.digital_write(3, 1)

        # X start
        self.movement.digital_write(5, 1)

        # Y start
        self.movement.digital_write(2, 0)

        time.sleep(self.current_time_diagonal)

        self.movement.digital_write(2, 1)
        self.movement.digital_write(5, 0)

        time.sleep(1)

    """
    This method allows diagonal movements
    to the third quadrant 
    """
    def diagonal3(self):

        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        # X
        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        # Y
        self.movement.digital_write(2, 1)
        self.movement.digital_write(3, 1)

        # X start
        self.movement.digital_write(4, 1)

        # Y start
        self.movement.digital_write(3, 0)

        time.sleep(self.current_time_diagonal)

        self.movement.digital_write(3, 1)
        self.movement.digital_write(4, 0)

        time.sleep(1)

    """
    This method allows diagonal movements
    to the fourth quadrant 
    """
    def diagonal4(self):

        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        # X
        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        # Y
        self.movement.digital_write(2, 1)
        self.movement.digital_write(3, 1)

        # X start
        self.movement.digital_write(5, 1)

        # Y start
        self.movement.digital_write(3, 0)

        time.sleep(self.current_time_diagonal)

        self.movement.digital_write(3, 1)
        self.movement.digital_write(5, 0)

        time.sleep(1)

    # (2,0) (3,1) = y+
    # (2,1) (3,0) = y-

    # (4,0) (5,1) = x+
    # (4,1) (5,0) = x-

    """
    This method retracts both colors
    """
    def up(self):
        self.movement.servo_write(9, 90)
        time.sleep(1)

    """
    This method takes out the black color
    """
    def down_black(self):
        self.movement.servo_write(9, 0)
        time.sleep(1)

    """
    This method takes out the black color
    """
    def down_blue(self):
        self.movement.servo_write(9, 180)
        time.sleep(1)

    """
    Provide movements on Y+ 
    """
    def y_plus(self):
        self.movement.digital_write(2, 0)
        self.movement.digital_write(3, 1)

        time.sleep(self.current_time_yplus)

        self.movement.digital_write(2, 0)
        self.movement.digital_write(3, 0)

        time.sleep(self.speed)

    """
    Provide movements on Y- 
    """
    def y_minus(self):

        self.movement.digital_write(2, 1)
        self.movement.digital_write(3, 0)

        time.sleep(self.current_time_yminus)

        self.movement.digital_write(2, 0)
        self.movement.digital_write(3, 0)

        time.sleep(self.speed)

    """
    Provide movements on X+ 
    """
    def x_plus(self):
        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 1)

        time.sleep(self.current_time_xplus)

        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        time.sleep(self.speed)

    """
    Provide movements on X- 
    """
    def x_minus(self):

        self.movement.digital_write(4, 1)
        self.movement.digital_write(5, 0)

        time.sleep(self.current_time_xminus)

        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        time.sleep(self.speed)

    """
    This method moves to an x cord
    :param pos: x cord
    """
    def x_movement(self, pos):
        aux = pos - self.x
        if 1 <= pos <= 9 and aux > 0:
            if (self.x + aux) <= 9:
                for i in range(self.x, self.x + aux):
                    self.x_plus()
                self.x += aux
            else:
                print("Error: PosX fuera de rango")

        elif 1 <= pos <= 9 and aux < 0:
            if (self.x + aux) >= 1:
                aux2 = self.x
                while aux2 > (self.x + aux):
                    self.x_minus()
                    print("LEFT")
                    aux2 -= 1
                self.x = aux2
            else:
                print("Error: PosX fuera de rango")

    """
    This method moves to an y cord
    :param pos: y cord
    """
    def y_movement(self, pos):
        aux = pos - self.y
        if 1 <= pos <= 10 and aux > 0:
            if (self.y + aux) <= 10:
                for i in range(self.y, self.y + aux):
                    self.y_plus()
                self.y += aux
            else:
                print("Error: PosY fuera de rango")

        elif 1 <= pos <= 10 and aux < 0:
            if (self.y + aux) >= 1:
                aux2 = self.y
                while aux2 > (self.y + aux):
                    self.y_minus()
                    aux2 -= 1
                self.y = aux2
            else:
                print("Error: PosY fuera de rango")

    """
    Method used control the drawing speed
    """
    def set_speed(self, speed):
        if 1 <= speed <= 5:
            self.speed = 6-speed
        else:
            print("Speed most be ->  1 <= speed <= 5 ")

    """
    Method used to reset y axy
    """
    def cali_y(self):
        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        self.movement.digital_write(2, 0)
        self.movement.digital_write(3, 1)

        start = time.time()

        input("P")

        self.movement.digital_write(2, 0)
        self.movement.digital_write(3, 0)

        end = time.time()

        print(end - start)

    """
    Method used to reset y axy
    """
    def cali_x(self):
        # (2,0) (3,1) = y+
        # (2,1) (3,0) = y-

        # (4,0) (5,1) = x+
        # (4,1) (5,0) = x-

        self.movement.digital_write(4, 1)
        self.movement.digital_write(5, 0)

        start = time.time()

        input("P")

        self.movement.digital_write(4, 0)
        self.movement.digital_write(5, 0)

        end = time.time()

        print(end - start)
