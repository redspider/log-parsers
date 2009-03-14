"""

Test suite for skim

"""

import unittest, tempfile, imp, random, logging

skim_file_handle = open('skim','r')
try:
    skim = imp.load_module('skim', skim_file_handle, 'skim', ('.py','r',imp.PY_SOURCE))
finally:
    skim_file_handle.close()

skim.log.setLevel(logging.DEBUG)

class SkimTestSimple(unittest.TestCase):
    file_handle = None
    def setUp(self):
        self.file_handle = tempfile.TemporaryFile(mode='w+b')
        for i in range(0,10000):
            self.file_handle.write('x'*85+'\n')
        self.file_handle.seek(0,0)
    
    def testSkim(self):
        results = list(skim.skim_generator(100,self.file_handle))
        # 98 seems to be what we get under this scenario. A bit closer look
        # at the math might get us exactly 100 which would be nice
        self.assertEqual(len(results), 98)
    
    def tearDown(self):
        self.file_handle.close()
        
if __name__ == '__main__':
    unittest.main()
