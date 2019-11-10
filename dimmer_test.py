import unittest
import logging
from dimmer import Dimmer


class StubTime():
    def __init__(self):
        self.time = 0

    @staticmethod
    def is_available():
        return True

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time


class StubOutput():
    def __init__(self):
        self.value = 0

    def set(self, value):
        self.value = value

    def get_value(self):
        return self.value


class TestDimmer(unittest.TestCase):

    def perform_test(self, time_table, test_values):
        logging.basicConfig(level=logging.ERROR)
        time = StubTime()
        output = StubOutput()

        d = Dimmer("dimmer", time, output, time_table)

        for t, expected in test_values:
            time.set_time(t)
            d.update()
            self.assertEqual(output.get_value(), expected,
                             "invalid output value for time %d, expected %f got %f" % (t, expected,
                                                                                       output.get_value()))

    def test_dimmer_01(self):
        table = [[-2, 0], [0, 1], [2, 0]]
        test_set = [[-3, 0.0],
                    [-2, 0.0],
                    [-1, 0.5],
                    [0, 1.0],
                    [1, 0.5],
                    [2, 0],
                    [3, 0]]

        self.perform_test(table, test_set)

    def test_dimmer_02(self):
        table = [[-2, 0], [2, 1]]
        test_set = [[-3, 0.0],
                    [-2, 0.0],
                    [-1, 0.25],
                    [0, 0.50],
                    [1, 0.75],
                    [2, 1.0],
                    [3, 1.0]]

        self.perform_test(table, test_set)


if __name__ == '__main__':
    unittest.main()
