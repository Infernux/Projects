#!/usr/bin/python3

import unittest

from StructureDumper import extract_name_body_aliases
from StructureDumper import remove_comments_from_line

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

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExtraction)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(TestCommentsRemover)
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.TextTestRunner(verbosity=2).run(suite2)
    unittest.main()
