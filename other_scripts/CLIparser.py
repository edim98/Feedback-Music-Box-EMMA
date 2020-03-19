'''
Module which handles the CLI interface.
'''

import argparse

# Add a description.
parser = argparse.ArgumentParser(description='Emotional Management with Musical Agents')

# Add the Azure flag.
parser.add_argument('-a', '--azure', action='store_true',
                    help='enable the usage of the Microsoft Azure Cognitive Services')

# Add the version flag.
parser.add_argument('-v', '--version', action='version', version='E.M.M.A. 1.0 alpha', help='print current version')


def parseFlags():
    '''
    Parse the command line arguments.
    :return: True, if Azure flag is found. False, otherwise.
    '''

    args = parser.parse_args()

    if args.azure:
        print('E.M.M.A. is using Microsoft Azure!')
    else:
        print('E.M.M.A. is using default model!')

    return args.azure
