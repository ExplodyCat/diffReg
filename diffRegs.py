#  diffRegs.py - Copyright (C) 2013  504ENSICS Labs
#  Report on the key\value paths that exist in one registry hive and not the other
#  Developers: Jerry Stormo
#
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pprint
import pyregf
import os

DEBUG = False


def main(argv=None):
    fileA, fileB = parseArgs(argv)

    #open the files
    regA = pyregf.file()
    regB = pyregf.file()
    
    regA.open(fileA)
    regB.open(fileB)

    #process the registry
    setA = processRoot(regA.get_root_key())
    setB = processRoot(regB.get_root_key())


    #Print metrics on how many we managed to remove
    if DEBUG:
        report(len(setA),'count-A: ')    
        report(len(setA.difference(setB)),'count-A !B: ')
    
    report(setA.difference(setB), 'UNIQUE-A: {0}'.format(fileA))


def processRoot(root):
    '''
    Helper function to start recursive call
    @root: pyregf file's root key
    @return: set() containing all parsed registry keys/values
    '''    
    coll = set()
    for cur in root.sub_keys:
        processKey(cur, coll)
    return coll


def processKey(key, coll, path=''):
    '''
    Recursive function loads set object with all the keys/values for a provided key & children
    @key: the pyregf key acting as starting point of recursion
    @coll: the set object to collect parsed info into
    @path: parent key's path string built by recursive calls
    '''
    #build & save printable key path
    expanded = os.path.join(path, key.get_name().encode('ascii','ignore'))
    coll.add(expanded)
    
    for cur in key.values: #build & save printable value record paths
        curName = cur.get_name()
        if curName is None:
            curName = 'NONETYPE'
        tmpStr = '{}___value'.format(curName.encode('ascii','ignore'))
        tmpPath = os.path.join(expanded, tmpStr)
        coll.add(tmpPath)
        
    for cur in key.sub_keys: #recursive call on each subkey
        processKey(cur, coll, expanded)


def report(reportSet, reportName):
    #print a well formatted report
    print(reportName)
    pprint.pprint(reportSet, indent=2)
    print()

    
def parseArgs(argv):
    '''
    Parse cmd line arguments
    @argv: array of command line arguments
    '''
    import argparse
    parser = argparse.ArgumentParser(description='Prints registryA.difference(registryB)')
    parser.add_argument('--debug', help='Print debugging statements.', action='store_true')
    parser.add_argument('fileA', help='Primary registry file to diff with')
    parser.add_argument('fileB', help='Second registry file to diff with') 
    args = parser.parse_args()
    
    #Set global debug value
    global DEBUG
    DEBUG = args.debug
    
    #return the filenames
    return os.path.abspath(args.fileA), os.path.abspath(args.fileB)

    
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))