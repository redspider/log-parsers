"""

Test suite for skim

"""

import unittest, tempfile, imp, random, logging

replace_last_file_handle = open('replace_last','r')
try:
    replace_last = imp.load_module('replace_last', replace_last_file_handle, 'replace_last', ('.py','r',imp.PY_SOURCE))
finally:
    replace_last_file_handle.close()

replace_last.log.setLevel(logging.DEBUG)

class ReplaceLastTestSimple(unittest.TestCase):
    file_handle = None
    def setUp(self):
        self.file_handle = tempfile.TemporaryFile(mode='w+b')
        self.file_handle.write("""
I liek to cat
cat lieks to me
chikken for cat
not cat cat fruit
""")
        self.file_handle.seek(0,0)
    
    def testSkim(self):
        results = list(replace_last.replace_last_generator('cat','hat',self.file_handle))
        # 98 seems to be what we get under this scenario. A bit closer look
        # at the math might get us exactly 100 which would be nice
        self.assertEqual(results[-1], 'not cat hat fruit\n')
        self.assertEqual(results[-2], 'chikken for cat\n')
    
    def tearDown(self):
        self.file_handle.close()
        
if __name__ == '__main__':
    unittest.main()
