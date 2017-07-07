#!/usr/bin/env python
'''
Takes the WEKA output files, and for each line, replaces the instance number
with the corresponding protein tag, removes the error column, replaces the
predictions column with the true/false probability columns, and outputs to the
specified file. Here is an example of the headers of an input file:

    inst#,actual,predicted,error,prediction

Here is an example of the headers of the output file:

    Protein Name,Actual,Predicted,True Probability,False Probability

To calculate the true probability, we take the 'predicted' column, and check if
the string 'TRUE' is a substring of said column. If it is, we copy the
'prediction' column to the 'True Probability' column. If it isn't, we take
`1 - prediction`, and insert the result into the 'True Probability' column. The
false probability is calculated and functions similarly.
'''
import argparse as ag

parser = ag.ArgumentParser(
description='Reformats WEKA buffer results (prettifies)',
epilog='Read pydocs for more.'
)

parser.add_argument('ref', help='original CSV file')
parser.add_argument('inp', help='input file with WEKA buffer result format (CSV)')
parser.add_argument('out', help='output filename')

args = parser.parse_args()

refcsv = args.ref
inpcsv = args.inp
outcsv = args.out

HEADERS = [
    'Protein Name',
    'Actual',
    'Predicted',
    'True Probability',
    'False Probability'
]

with open(refcsv, 'r') as r, open(inpcsv, 'r') as i, open(outcsv, 'w') as o:
    # Skip the first line
    r.readline(); i.readline()
    # Write the header
    o.write(','.join(HEADERS) + '\n')

    for i, (l1, l2) in enumerate(zip(r.readlines(), i.readlines())):
        name = l1.split(',')[0]
        s = l2.rstrip().split(',')
        pred = s[2]
        actual = s[1]
        true_prob = s[4] if 'TRUE' in pred else "%0.3f" % (1 - float(s[4]))
        false_prob = s[4] if 'FALSE' in pred else "%0.3f" % (1 - float(s[4]))
        line = [name, actual, pred, true_prob, false_prob]

        o.write(','.join(line) + '\n')
