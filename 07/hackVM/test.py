import unittest
import io
import main


class TestHackVM(unittest.TestCase):

    def test_simple_add_asm_compare(self):
        main.main('../StackArithmetic/SimpleAdd/SimpleAdd.vm')
        test_path = '../StackArithmetic/SimpleAdd/SimpleAdd.asm'
        ref_path = '../test_compare/SimpleAdd.asm'
        self.assertListEqual(list(io.open(test_path)), list(io.open(ref_path)))

    def test_stack_test_asm_compare(self):
        main.main('../StackArithmetic/StackTest/StackTest.vm')
        test_path = '../StackArithmetic/StackTest/StackTest.asm'
        ref_path = '../test_compare/StackTest.asm'
        self.assertListEqual(list(io.open(test_path)), list(io.open(ref_path)))


if __name__ == '__main__':
    unittest.main()
