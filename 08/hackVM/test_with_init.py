import unittest
import subprocess
import io
import main


class TestHackVM(unittest.TestCase):

    def test_fibonacci_element(self):
        main.main('../FunctionCalls/FibonacciElement')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../FunctionCalls/FibonacciElement/FibonacciElement.tst'])
        cmp_path = io.open(
            '../FunctionCalls/FibonacciElement/FibonacciElement.cmp')
        out_path = io.open(
            '../FunctionCalls/FibonacciElement/FibonacciElement.out')
        self.assertListEqual(list((cmp_path)), list((out_path)))
        cmp_path.close()
        out_path.close()

    def test_nested_call(self):
        main.main('../FunctionCalls/NestedCall')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../FunctionCalls/NestedCall/NestedCall.tst'])
        cmp_path = io.open('../FunctionCalls/NestedCall/NestedCall.cmp')
        out_path = io.open('../FunctionCalls/NestedCall/NestedCall.out')
        self.assertListEqual(list((cmp_path)), list((out_path)))
        cmp_path.close()
        out_path.close()

    def test_static_test(self):
        main.main('../FunctionCalls/StaticsTest')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../FunctionCalls/StaticsTest/StaticsTest.tst'])
        cmp_path = io.open('../FunctionCalls/StaticsTest/StaticsTest.cmp')
        out_path = io.open('../FunctionCalls/StaticsTest/StaticsTest.out')
        self.assertListEqual(list((cmp_path)), list((out_path)))
        cmp_path.close()
        out_path.close()


if __name__ == '__main__':
    unittest.main()
