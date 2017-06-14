'''
Takes the CSV input file, and converts the entire file into a separate CSV file.
This process takes 3 steps:

1. Removing the 2 unneeded columns
2. Converting the file to WEKA friendly ARFF format
3. Making sure that the effector attribute is correctly placed and ordered
   correctly

Temporary files are used in the process. They are deleted at the end of the
script. This script only works on systems with stream editor `sed` (most linux
machines).
'''
import weka.core.jvm as jvm
from weka.core.converters import Loader, Saver
from tempfile import mkstemp
import sys
import os
import subprocess as sub
import argparse as ap

EFFECTOR = 'Effector'
ATTRIBUTE_FIXER = "s/\@attribute %s.*/@attribute %s {FALSE,TRUE}/" % (
    EFFECTOR, EFFECTOR)

parser = ap.ArgumentParser(
description='Converts correctly formatted CSV files into corresponding ARFFs',
epilog='See bioinf-data-collection repo as, in theory, the output is plugged into this script.'
)

parser.add_argument('file', help='CSV file filename')
parser.add_argument('-o', '--out', help='Output ARFF filename', default='a.out')

args = parser.parse_args()

# A 3 staged process requires 2 intermediate steps, making it necessary to have
# 2 temporary files
fn = args.file
newfn = mkstemp()[1]
arffn = mkstemp()[1]
out = args.out

# Stage 1
# Remove unneeded columns (A280 Molar 1mg and Protein Name)
with open(fn, 'r') as read, open(newfn, 'w') as write:
    for l in read.readlines():
        s = l.split(',')
        del s[13], s[0]
        write.write(','.join(s))

# Stage 2
jvm.start()

csvloader = Loader(classname='weka.core.converters.CSVLoader')
arffsaver = Saver(classname='weka.core.converters.ArffSaver')

data = csvloader.load_file(newfn)

# Set relation name
data.relationname = fn.replace('.csv', '')
# Checks to see if attribute "Effector" is in the correct order
eff = data.attribute_by_name(EFFECTOR)

# Sanity checking
if eff is None:
    print('error: cannot find attribute "%s"' % EFFECTOR)
    sys.exit(-1)

arffsaver.save_file(data, arffn)

jvm.stop()

# Stage 3
# Run process to fix weka attribute
sub.call(['sed', ATTRIBUTE_FIXER, arffn], stdout=open(out, 'w'))

# Delete temporary files
os.remove(newfn)
os.remove(arffn)