import os
import re

from itertools import islice

project_root_dir = os.path.dirname(os.path.abspath(__file__))
print(project_root_dir)

def get_filepaths_tests(directory, ALL_PY=False):
    """
    This function will generate the file names in a directory
    tree by walking the tree either top-down or bottom-up. For each
    directory in the tree rooted at directory top (including top itself),
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        if ALL_PY:
            files[:] = [f  for f in files if f.endswith('.doctest') or f.endswith('.py')]
        else:
            files[:] = [f for f in files if (f.startswith('test_') and f.endswith('.py')) or f.endswith('.doctest')]
        #print(files)
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return file_paths  # Self-explanatory.


def find_test_from_pattern(file,PATTERN):
    with open(file, 'r') as f:

        for i in range(10):
            #print(f.readline())
            line = f.readline()
            item = re.findall(r'(#DOCTEST+)', line)

            if len(item) == 0:
                continue

            return True

    return False

def relative_path_for_py_doc_test(paths):
    count = 0
    for p in paths:
        p = p.replace(project_root_dir + os.sep, '')
        p = p.replace('.py' , '')
        p = p.replace(os.sep, '.')

        paths[count] = p
        count += 1

    return paths


def exclude_files(list_files):
    res = {}
    res['text_doctest_files'] = []
    res['py_doctest_files'] = []

    result = []
    for file in list_files:

        f = file.rfind(os.sep)
        # print(file[f+1:])

        if file[f + 1:].startswith('test_'):
            continue

        if file.endswith('.doctest'):
            print(file)
            result.append(file)
            res['text_doctest_files'].append(file)
            continue

        if find_test_from_pattern(file,PATTERN='#DOCTEST'):
            print(file)
            result.append(file)
            res['py_doctest_files'].append(file)
            continue

    relative_path_for_py_doc_test(res['py_doctest_files'])
    return res

def generate_test_suit(tests_dictonary, patterns='test_*.py'):
    TestLoader = unittest.TestLoader()
    TestSuit = TestLoader.discover(start_dir=project_root_dir,
                                  pattern=patterns)
    for text_doc_file in tests_dictonary['text_doctest_files']:
        DocTest = doctest.DocFileSuite(text_doc_file, module_relative=False)
        TestSuit.addTests(DocTest)

    for py_doc_test in tests_dictonary['py_doctest_files']:
        DocTest = doctest.DocTestSuite(module=py_doc_test)
        TestSuit.addTests(DocTest)

    return TestSuit




if __name__ == '__main__':
    res = get_filepaths_tests('/home/administrator/PycharmProjects/test_searcher/tests_for_searcher', True)
    print(res)
    tests = exclude_files(res)
    print(tests)

    import unittest
    import doctest

    TS = generate_test_suit(tests)
    print(TS)
    result = unittest.TestResult()
    Test_result = TS.run(result=result)
    fail = Test_result.failures
    print(fail)
    print(Test_result)






    '''
    Test_Suit = unittest.TestLoader()
    All_Test = Test_Suit.discover(start_dir='/home/administrator/PycharmProjects/test_searcher/tests_for_searcher',
                                  pattern="test_*.py")

    #DocTest = doctest.testfile(filename='/home/administrator/PycharmProjects/'
    #                                    'test_searcher/tests_for_searcher/d/doc_t2.doctest')

    DocTest = doctest.DocFileSuite('/home/administrator/PycharmProjects/test_searcher/'
                                   'tests_for_searcher/d/doc_t4.doctest', module_relative=False)
    print(DocTest)

    All_Test.addTests(DocTest)
    DocTest = doctest.DocTestSuite('tests_for_searcher.example_1')
    #print(All_Test)
    print(DocTest)
    All_Test.addTests(DocTest)

    result = unittest.TestResult()
    Test_result = All_Test.run(result=result)
    fail = Test_result.failures
    print(fail)
    print(Test_result)

    '''
#    test = Test_Suit.loadTestsFromName('tests_for_searcher.test.test_t2')

