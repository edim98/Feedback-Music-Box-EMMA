'''
Module which handles the CLI.
'''

import argparse

# Add a description.
parser = argparse.ArgumentParser(description='Emotional Management with Musical Agents')

# Add the Azure flag.
parser.add_argument('-a', '--azure', action='store_true',
                    help='enable the usage of the Microsoft Azure Cognitive Services')

# Add the song selection flag. If flag is true, then the system will play songs which have been played before.
parser.add_argument('-r', '--repeat', action='store_true', help='enable repetition of songs')

# Add the version flag.
parser.add_argument('-v', '--version', action='version', version='E.M.M.A. 1.0 alpha', help='print current version')

# Add the test flag.
parser.add_argument('-t', '--test', action='store_true', help='run in a test environment')


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

    if args.repeat:
        print('E.M.M.A. will repeat songs')

    if args.test:
        print('Running in test environment...')
    return args
