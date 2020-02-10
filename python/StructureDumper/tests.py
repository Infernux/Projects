#!/usr/bin/python3

import unittest

from StructureDumper import extract_name_body_aliases

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
        **/alias2;
        '''
        expected_name = 'my_struct'
        expected_aliases = list()
        expected_aliases.append("with_aliasalias2")
        expected_body = 'int b;'

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
    unittest.TextTestRunner(verbosity=2).run(suite)
    unittest.main()
