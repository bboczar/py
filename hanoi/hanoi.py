import config
import math
import time

class Tower:
    def __init__(self, height, speed):
        self._left = []
        self._middle = []
        self._right = []
        self._height = height
        self._speed = speed

        self._width = 6*height + 2
        self._line_width = 2*height

        # Starting state
        for floor in range(height):
            self._left.append(height-floor)
            self._middle.append(0)
            self._right.append(0)

    ## PRINT METHODS ##
    def _draw(self):
        print(self._width * '-')
        print(self._width * ' ')
        for line in range(self._height):
            self._draw_line(self._height-line-1)
        print(self._width * ' ')
        print(self._width * '-')

        time.sleep(1 / self._speed)

    def _draw_line(self, line):
        left_line = self._get_line_part(self._left[line])
        middle_line = self._get_line_part(self._middle[line])
        right_line = self._get_line_part(self._right[line])
        print(left_line + '|' + middle_line + '|' + right_line)

    def _get_line_part(self, element_size):
        overhang_size = (self._line_width - element_size*2) // 2
        return overhang_size * ' ' + element_size * '**' + overhang_size * ' '

    ## SOLVE METHODS ##
    def start(self):
        print("Tower will take {} seconds to solve".format(self._get_time()))
        self._draw()
        time.sleep(2)

        n = self._height
        self._solve(n, self._left, self._right, self._middle)

    def _get_time(self):
        return (math.pow(2, self._height) - 1) * (1 / self._speed)

    def _solve(self, n, from_stack, to_stack, aux_stack):
        if (n == 1):
            self._transfer(from_stack, to_stack)
            self._draw()
            return

        self._solve(n - 1, from_stack, aux_stack, to_stack)
        self._transfer(from_stack, to_stack)
        self._draw()
        self._solve(n - 1, aux_stack, to_stack, from_stack)

    def _transfer(self, from_stack, to_stack):
        floor = len(from_stack) - 1
        while (from_stack[floor] == 0):
            floor = floor - 1
        elemet = from_stack[floor]
        from_stack[floor] = 0

        floor = len(to_stack) - 1
        while (floor > 0 and to_stack[floor-1] == 0):
            floor = floor - 1
        to_stack[floor] = elemet


tower = Tower(config.height, config.speed)
tower.start()
