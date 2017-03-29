import os
import re
from itertools import islice

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


def exclude_files(list_files):
    result = []
    for file in list_files:

        if file.endswith('.doctest'):
            #print(file)
            continue

        f = file.rfind(os.sep)
        #print(file[f+1:])

        if file[f+1:].startswith('test_'):
            #print('continue')
            continue

        if find_test_from_pattern(file,PATTERN='#DOCTEST'):
            print(file)


if __name__ == '__main__':
    res = get_filepaths_tests('D:\Repositories\pyteamcity', True)
    #print(res)
    exclude_files(res)
