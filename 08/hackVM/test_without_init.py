import unittest
import subprocess
import io
import main


class TestHackVM(unittest.TestCase):

    def test_basic_loop(self):
        main.main('../ProgramFlow/BasicLoop/BasicLoop.vm')
        subprocess.run(
            ['../../../tools/CPUEmulator.sh', '../ProgramFlow/BasicLoop/BasicLoop.tst'])
        cmp_path = io.open('../ProgramFlow/BasicLoop/BasicLoop.cmp')
        out_path = io.open('../ProgramFlow/BasicLoop/BasicLoop.out')
        self.assertListEqual(list(cmp_path), list(out_path))
        cmp_path.close()
        out_path.close()

    def test_fibonacci_siries(self):
        main.main('../ProgramFlow/FibonacciSeries/FibonacciSeries.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../ProgramFlow/FibonacciSeries/FibonacciSeries.tst'])
        cmp_path = io.open(
            '../ProgramFlow/FibonacciSeries/FibonacciSeries.cmp')
        out_path = io.open(
            '../ProgramFlow/FibonacciSeries/FibonacciSeries.out')
        self.assertListEqual(list((cmp_path)), list((out_path)))
        cmp_path.close()
        out_path.close()

    def test_simple_function(self):
        main.main('../FunctionCalls/SimpleFunction/SimpleFunction.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../FunctionCalls/SimpleFunction/SimpleFunction.tst'])
        cmp_path = io.open(
            '../FunctionCalls/SimpleFunction/SimpleFunction.cmp')
        out_path = io.open(
            '../FunctionCalls/SimpleFunction/SimpleFunction.out')
        self.assertListEqual(list((cmp_path)), list((out_path)))
        cmp_path.close()
        out_path.close()


if __name__ == '__main__':
    unittest.main()
