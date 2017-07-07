#!/usr/bin/env python3
'''
Runs (on default) 6 machine learning algorithms through WEKA using the
python-weka-wrapper3 wrapper. Algorithms include:

1. BayesNet
2. NaiveBayes
3. Logistic
4. Multilayer Perceptron
5. SMO
6. Vote

#6 (Vote) is special since it is the only algorithm that uses a non-default
configuration - The voting algorithm evaluates the training sets and test sets
using any user-supplied machine-learning algorithms, and "votes" to see which
ones should be taken more seriously.

Results are formatted and outputted to the supplied directory, with sensible
filenames (e.g. Testing_BayesNet.accuracy.csv for running the test set on
algorithm BayesNet and that file stores the accuracy results of the session).

Algorithms are run separately, meaning that it could be possible to make the
program use multithreading to somewhat of an advantage.

On a different topic, I find it stupid that the Voting algorithm cannot just
take in the trained models of different algorithms, and use that, instead of
re-running the others. Maybe it's possible, who knows....
'''
import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation, PredictionOutput
import os
import argparse as ap

parser = ap.ArgumentParser(
description='Runs machine learning algorithms through WEKA/java layer',
epilog='Requires java (duh)'
)

parser.add_argument('training', help='Training data in ARFF format')
parser.add_argument('testing', help='Testing data in ARFF format')
parser.add_argument('-d', '--directory', default='results/',
    help='Directory for output files (default: results/)')

args = parser.parse_args()

# Helper vars and functions
int_to_boolstr = {0: 'FALSE', 1: 'TRUE'}

def fns(p):
    '''
    Returns a list of functions used for the accuracy status output.
    '''
    return [
        p.true_positive_rate,
        p.false_positive_rate,
        p.precision,
        p.recall,
        p.f_measure,
        p.matthews_correlation_coefficient,
        p.area_under_roc,
        p.area_under_prc,
        int_to_boolstr.get
    ]
headers = [
    'TP Rate',
    'FP Rate',
    'Precision',
    'Recall',
    'F-Measure',
    'MCC',
    'ROC Area',
    'PRC Area',
    'Class'
]
data_headers = [
    'inst#',
    'actual',
    'predicted',
    'error',
    'prediction'
]

def r_to_str(x):
    '''
    Returns the rounded string up till 3 decimal places if `x` is a float.
    If `x` is a string, behaves as an identity function (doesn't do a thing).
    If `x` is neither a string nor a float, this function raises a `TypeError`.
    '''
    if isinstance(x, float):
        return "%0.3f" % x
    elif isinstance(x, str):
        return x
    else:
        raise TypeError('Unsupported type')

def output_results(evl, out, m):
    '''
    Outputs the results of the evaluations made into separate files for easier
    management.
    '''
    # Predicted output
    pout = open(m + '.out.csv', 'w')
    pout.write(','.join(data_headers) + '\n')
    pout.write(str(out) + '\n')
    pout.close()
    # Summary output
    eout = open(m + '.summary.csv', 'w')
    eout.write(evl.summary() + '\n')
    eout.close()
    # Confusion matrix output
    cout = open(m + '.matrix.csv', 'w')
    cout.write(evl.matrix() + '\n')
    cout.close()
    # Detailed accuracy by class
    aout = open(m + '.accuracy.csv', 'w')
    aout.write(','.join(headers) + '\n')
    for c in [0, 1]:
        aout.write(','.join(map(lambda f: r_to_str(f(c)), fns(evl))) + '\n')
    aout.close()

def intersperse(l, s):
    '''
    Returns a list with item `s` interspersed (placed in between) items.
    Ideally, all items in `l` should be the same type as `s`.
    '''
    res = [s] * (len(l) * 2 - 1)
    res[::2] = l
    return res

P_OUT = "weka.classifiers.evaluation.output.prediction.CSV"

TRAINING_FN = args.training
TESTING_FN = args.testing
RES_FOLDER = args.directory
CLASSIFIERS = list(map(lambda s: "weka.classifiers" + s, [
    ".bayes.BayesNet",
    ".bayes.NaiveBayes",
    ".functions.Logistic",
    ".functions.MultilayerPerceptron",
    ".functions.SMO",
    ".meta.Vote"
]))
OPTIONS = [
    '-D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5'.split(),
    [],
    '-R 1.0E-8 -M -1 -num-decimal-places 4'.split(),
    '-L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a'.split(),
    '-C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K'.split() + ['weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007', '-calibrator', 'weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4'],
    '-S 1 -B'.split() + ['weka.classifiers.bayes.BayesNet -D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5', '-B', 'weka.classifiers.bayes.NaiveBayes', '-B', 'weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4', '-B', 'weka.classifiers.functions.MultilayerPerceptron -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a', '-B', 'weka.classifiers.functions.SMO -C 1.0 -L 0.001 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007\" -calibrator \"weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4\"', '-R', 'AVG'],
]

jvm.start()

loader = Loader(classname="weka.core.converters.ArffLoader")
training = loader.load_file(TRAINING_FN)
testing = loader.load_file(TESTING_FN)

training.class_is_last()
testing.class_is_last()

# Try to make the directory
try:
    os.mkdir(RES_FOLDER)
except OSError:
    # Directory already exists
    print('Directory `%s` already exists' % RES_FOLDER)

# Go through all options + vote
for cfr, op in zip(CLASSIFIERS, OPTIONS):
    method = cfr.split('.')[-1]
    options = None

    cls = Classifier(classname=cfr, options=op)
    test_evl = Evaluation(testing)
    train_evl = Evaluation(training)
    train_out = PredictionOutput(classname=P_OUT)
    test_out = PredictionOutput(classname=P_OUT)

    # Training
    cls.build_classifier(training)
    tres = train_evl.test_model(cls, training, output=train_out)

    # Testing
    res = test_evl.test_model(cls, testing, output=test_out)

    output_results(train_evl, train_out, RES_FOLDER + "Training_" + method)
    output_results(test_evl, test_out, RES_FOLDER + "Testing_" + method)

jvm.stop()