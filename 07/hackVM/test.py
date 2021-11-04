import unittest
import subprocess
import io
import main


class TestHackVM(unittest.TestCase):

    def test_simple_add(self):
        main.main('../StackArithmetic/SimpleAdd/SimpleAdd.vm')
        subprocess.run(
            ['../../../tools/CPUEmulator.sh', '../StackArithmetic/SimpleAdd/SimpleAdd.tst'])
        cmp_path = '../StackArithmetic/SimpleAdd/SimpleAdd.cmp'
        out_path = '../StackArithmetic/SimpleAdd/SimpleAdd.out'
        self.assertListEqual(list(io.open(cmp_path)), list(io.open(out_path)))

    def test_stack_test(self):
        main.main('../StackArithmetic/StackTest/StackTest.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../StackArithmetic/StackTest/StackTest.tst'])
        cmp_path = '../StackArithmetic/StackTest/StackTest.cmp'
        out_path = '../StackArithmetic/StackTest/StackTest.out'
        self.assertListEqual(list(io.open(cmp_path)), list(io.open(out_path)))

    def test_basic_test(self):
        main.main('../MemoryAccess/BasicTest/BasicTest.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../MemoryAccess/BasicTest/BasicTest.tst'])
        cmp_path = '../MemoryAccess/BasicTest/BasicTest.cmp'
        out_path = '../MemoryAccess/BasicTest/BasicTest.out'
        self.assertListEqual(list(io.open(cmp_path)), list(io.open(out_path)))

    def test_pointer_test(self):
        main.main('../MemoryAccess/PointerTest/PointerTest.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../MemoryAccess/PointerTest/PointerTest.tst'])
        cmp_path = '../MemoryAccess/PointerTest/PointerTest.cmp'
        out_path = '../MemoryAccess/PointerTest/PointerTest.out'
        self.assertListEqual(list(io.open(cmp_path)), list(io.open(out_path)))

    def test_static_test(self):
        main.main('../MemoryAccess/StaticTest/StaticTest.vm')
        subprocess.call(
            ['../../../tools/CPUEmulator.sh', '../MemoryAccess/StaticTest/StaticTest.tst'])
        cmp_path = '../MemoryAccess/StaticTest/StaticTest.cmp'
        out_path = '../MemoryAccess/StaticTest/StaticTest.out'
        self.assertListEqual(list(io.open(cmp_path)), list(io.open(out_path)))


if __name__ == '__main__':
    unittest.main()
