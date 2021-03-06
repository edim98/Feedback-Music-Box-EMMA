"""
Module for storing song descriptor scores and for computing song scores.
"""

import configparser
import os

struct_descriptors = {

    'genre': {
        'rock': 0,
        'pop': 0,
        'metal': 0,
        'punk': 0,
        'classical': 0,
        'folk': 0,
        'jazz': 0,
        'latin': 0,
        'r&b': 0,
        'electronic': 0,
        'country': 0,
        'blues': 0,
    },

    'dynamics': {
        'low': 0,
        'medium': 0,
        'high': 0
    },

    'tempo': {
        '<30': 0, # grave
        '40-60': 0, # largo
        '60-66': 0, # larghetto
        '66-76': 0, # adagio
        '76-108': 0, # andante
        '108-120': 0, # moderato
        '120-168': 0, # allegro
        '168-200': 0, # presto
        '200+': 0, #prestissimo

    },

    'key': {
        'C major': 0,
        'C minor': 0,
        'Db major': 0,
        'Db minor': 0,
        'D major': 0,
        'D minor': 0,
        'Eb major': 0,
        'Eb minor': 0,
        'E major': 0,
        'E minor': 0,
        'F major': 0,
        'F minor': 0,
        'F# major': 0,
        'F# minor': 0,
        'G major': 0,
        'G minor': 0,
        'Ab major': 0,
        'Ab minor': 0,
        'A major': 0,
        'A minor': 0,
        'Bb major': 0,
        'Bb minor': 0,
        'B major': 0,
        'B minor': 0,
    },

    'lyrics': {
        'yes': 0,
        'no': 0
    },

    'language': {
        'none': 0,
        'english': 0,
        'dutch': 0,
        'german': 0,
        'lithuanian': 0,
        'romanian': 0,
        'spanish': 0,
        'french': 0,
        'italian': 0,
        'portuguese': 0,
        'other': 0
    }
}

'''
Multiplier parameters for determining individual song scores.
'''

config = configparser.ConfigParser()
config.read(os.path.relpath('settings.cfg'))

happinessMultiplier = float(config['BASE_EMOTIONS']['HAPPINESS_MULTIPLIER'])
neutralMultiplier = float(config['BASE_EMOTIONS']['NEUTRAL_MULTIPLIER'])
angerMultiplier = float(config['BASE_EMOTIONS']['ANGER_MULTIPLIER'])
sadnessMultiplier = float(config['BASE_EMOTIONS']['SADNESS_MULTIPLIER'])

surpriseMultiplier = float(config['EXTRA_EMOTIONS']['SURPRISE_MULTIPLIER'])
disgustMultiplier = float(config['EXTRA_EMOTIONS']['DISGUST_MULTIPLIER'])
fearMultiplier = float(config['EXTRA_EMOTIONS']['FEAR_MULTIPLIER'])
contemptMultiplier = float(config['EXTRA_EMOTIONS']['CONTEMPT_MULTIPLIER'])


def get_descriptors():
    """
    Get latest update of the song descriptors dictionary.
    :return: Latest update of the song descriptors dictionary.
    """
    global struct_descriptors

    return struct_descriptors

def get_song_score(song_descriptors):
    """
    Compute the score of a song based on the score of its descriptors.
    :param song_descriptors: The unique descriptors associated with this song.
    :return: The score of the song.
    """
    global struct_descriptors
    score = 0
    for descriptor in song_descriptors:
        score += struct_descriptors[descriptor][song_descriptors[descriptor]]

    return score

def update_descriptors(emotion_list, song_descriptors): # TODO Tinker with parameters.
    """
    Update the scores of each descriptor and its sub-descriptors.
    :param emotion_list: A list of user emotions retrieved from the model at a given time.
    :param song_descriptors: The unique descriptors associated with this song.
    :return: Latest update of the song descriptors dictionary.
    """

    global struct_descriptors

    for descriptor in song_descriptors:
            struct_descriptors[descriptor][song_descriptors[descriptor]] += (happinessMultiplier * emotion_list['happiness']
                                                                             + neutralMultiplier * emotion_list['neutral']
                                                                             + surpriseMultiplier * emotion_list['surprise'])
            struct_descriptors[descriptor][song_descriptors[descriptor]] += (angerMultiplier * emotion_list['anger']
                                                                             + disgustMultiplier * emotion_list['disgust']
                                                                             + fearMultiplier * emotion_list['fear']
                                                                             + sadnessMultiplier * emotion_list['sadness']
                                                                             + contemptMultiplier * emotion_list['contempt'])

    return struct_descriptors
