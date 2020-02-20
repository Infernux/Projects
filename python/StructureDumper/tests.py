#!/usr/bin/python3

import unittest

from StructureDumper import extract_name_body_aliases
from StructureDumper import remove_comments_from_line
from StructureDumper import IR_node
from StructureDumper import extract_IR_from_body

class TestCommentsRemover(unittest.TestCase):
    def test_remove_starting_single_liner(self):
        line = "//a"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_middle_single_liner(self):
        line = "int a;//a"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "int a;")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_middle_single_liner_while_in_multiliner(self):
        line = "int a;//a"
        is_multiline_comment = True

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "")
        self.assertEqual(is_multiline_comment, True)

    def test_remove_starting_multiliner(self):
        line = "/* b */int a;"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "int a;")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_middle_multiliner(self):
        line = "int /* b */a;"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "int a;")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_ending_multiliner(self):
        line = "int a;/* adfj */"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "int a;")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_multiliner_while_in_multiline_mode(self):
        line = "int /* b */a;"
        is_multiline_comment = True

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "a;")
        self.assertEqual(is_multiline_comment, False)

    def test_remove_new_multiliner(self):
        line = "int /* b a;"
        is_multiline_comment = False

        line, is_multiline_comment = remove_comments_from_line(line, is_multiline_comment)

        self.assertEqual(line, "int ")
        self.assertEqual(is_multiline_comment, True)

class TestExtraction(unittest.TestCase):

    def test_basic_struct(self):
        body = '''
            typedef struct my_struct
            {
                int a;
            };
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_body = 'int a;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_no_space(self):
        body = '''
            typedef struct my_struct{int x;
            int a;};
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_body = 'int x;\nint a;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_with_single_alias(self):
        body = '''
            typedef struct my_struct
            {
                int a;
            } with_alias;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_alias")
        expected_body = 'int a;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_with_multiple_aliases(self):
        body = '''
            typedef struct my_struct
            {
                int a;
            } with_alias, alias2;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_alias")
        expected_aliases.append("alias2")
        expected_body = 'int a;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_with_multiple_aliases_and_pointer(self):
        body = '''
            typedef struct my_struct
            {
                int a;
            } with_alias, *alias2;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_alias")
        expected_aliases.append("*alias2")
        expected_body = 'int a;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_with_comments(self):
        body = '''
            typedef /* aa */ struct /* bb */ my_struct
            {
                //int a;
                int b;
            } with_alias/*, **/alias2;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_aliasalias2")
        expected_body = 'int b;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_single_liner(self):
        body = 'typedef struct my_struct { int /*sup */b; } with_alias/*, **/alias2; '
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_aliasalias2")
        expected_body = 'int b;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_shitload_liner(self):
        body = '''
        typedef
        struct
        my_struct
        {
        int
        /*sup */
        b;
        }
        with_alias/*,
        **/,alias2
        ;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_alias")
        expected_aliases.append("alias2")
        expected_body = 'int\n\nb;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

    def test_basic_struct_with_curly_brackets(self):
        body = '''
            typedef /* {a} */ struct /* bb */ my_struct
            {
                int b; // { zztop }
            } with_alias/*, **/alias2;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_aliasalias2")
        expected_body = 'int b;'

        name, body, aliases = extract_name_body_aliases(body)

        self.assertEqual(name, expected_name)
        self.assertEqual(body, expected_body)
        self.assertEqual(aliases, expected_aliases)

def compareIRs(ir1, ir2):
    for ir1_node, ir2_node in zip(ir1, ir2):
        if ir1_node.type != ir2_node.type:
            print(str(ir1_node.type)+" != "+str(ir2_node.type))
            return False
        elif ir1_node.varname != ir2_node.varname:
            print(str(ir1_node.varname)+" != "+str(ir2_node.varname))
            return False
        elif ir1_node.pointer != ir2_node.pointer:
            print(str(ir1_node.pointer)+" != "+str(ir2_node.pointer))
            return False
        elif ir1_node.array != ir2_node.array:
            print("Array comparison : "+str(ir1_node.array)+" != "+str(ir2_node.array))
            return False

    return True

class TestBodyParsing(unittest.TestCase):
    def test_one_known_variable(self):
        body = '''
        int a;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 0)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_two_known_variables(self):
        body = '''
        int a;
        int b;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 0)
        expected_ir.append(node)
        node = IR_node("int", "b", 0)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_two_known_variables_one_liner(self):
        body = '''
        int a;int b;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 0)
        expected_ir.append(node)
        node = IR_node("int", "b", 0)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_two_known_variables_one_liner_with_pointers_1(self):
        body = '''
        int* a;int* b;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 1)
        expected_ir.append(node)
        node = IR_node("int", "b", 1)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))


    def test_two_known_variables_one_liner_with_pointers_2(self):
        body = '''
        int* *a;int* b;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 2)
        expected_ir.append(node)
        node = IR_node("int", "b", 1)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_pointer_1(self):
        body = '''
        int* a;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 1)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_pointer_2(self):
        body = '''
        int * a;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 1)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_pointer_2_space(self):
        body = '''
        int * * a;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 2)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_pointer_3(self):
        body = '''
        int *a;
        '''

        expected_ir = list()
        node = IR_node("int", "a", 1)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_array(self):
        body = '''
        int a[3];
        '''

        expected_array = list()
        expected_array.append("3")
        expected_ir = list()
        node = IR_node("int", "a", 0, expected_array)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_two_dimensional_array(self):
        body = '''
        int a[3][ARRAY_SIZE];
        '''

        expected_array = list()
        expected_array.append("3")
        expected_array.append("ARRAY_SIZE")
        expected_ir = list()
        node = IR_node("int", "a", 0, expected_array)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

    def test_one_known_two_dimensional_array_of_pointers(self):
        body = '''
        int *a[3][ARRAY_SIZE];
        '''

        expected_array = list()
        expected_array.append("3")
        expected_array.append("ARRAY_SIZE")
        expected_ir = list()
        node = IR_node("int", "a", 1, expected_array)
        expected_ir.append(node)

        ir = extract_IR_from_body(body)

        self.assertTrue(compareIRs(ir, expected_ir))

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExtraction)
    #suite2 = unittest.TestLoader().loadTestsFromTestCase(TestCommentsRemover)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.TextTestRunner(verbosity=2).run(suite2)
    unittest.main()
