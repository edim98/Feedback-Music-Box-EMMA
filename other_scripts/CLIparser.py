import argparse

parser = argparse.ArgumentParser(description='Emotional Management with Musical Agents')
parser.add_argument('-a', '--azure', action='store_true',
                    help='enable the usage of the Microsoft Azure Cognitive Services')
parser.add_argument('-v', '--version', action='version', version='E.M.M.A. 1.0 alpha', help='print current version')

def parseFlags():
    args = parser.parse_args()

    if args.azure:
        print('E.M.M.A. is using Microsoft Azure!')
    else:
        print('E.M.M.A. is using default model!')

    return args.azure
