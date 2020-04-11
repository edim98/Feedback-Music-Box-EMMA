from matplotlib import pyplot as plt

plt.style.use('dark_background')  # Responsible for making the plots in dark mode

HISTORY_SIZE = 5  # Number of observations for mean calculation and progress plot

azure_flag = False  # Let the plotter know if we are using Azure or our model in order to react to their
# different outputs.

COLORS = {  # Used for color coding the graphs
    'anger': '#dd3418',  # red
    'contempt': '#dd8518',  # orange
    'disgust': '#4a8a4d',  # puke green
    'fear': '#cccccc',  # ghost white
    'happiness': '#f0f417',  # bright yellow
    'neutral': '#808080',  # gray
    'sadness': '#5d7293',  # sad blue
    'surprise': '#b665b6'  # surprise violet
}

emotion_history = {  # Used to track the progress of the recognized emotion values
    'anger': [0.0],
    'contempt': [0.0],
    'disgust': [0.0],
    'fear': [0.0],
    'happiness': [0.0],
    'neutral': [0.0],
    'sadness': [0.0],
    'surprise': [0.0]
}

means_history = {  # Used in case we want to track the progress of the means
    'anger': [],
    'contempt': [],
    'disgust': [],
    'fear': [],
    'happiness': [],
    'neutral': [],
    'sadness': [],
    'surprise': []
}


def init():
    """
    Currently adjusts the global dictionaries to smaller sizes, according to the output of our own model,
    if azure_flag is set to True.
    """
    global COLORS, emotion_history, means_history, azure_flag
    if not azure_flag:
        COLORS = {
            'anger': '#dd3418',  # red
            'neutral': '#808080',  # gray
            'happiness': '#f0f417',  # bright yellow
            'sadness': '#5d7293'  # sad blue
        }

        emotion_history = {
            'anger': [0.0],
            'neutral': [0.0],
            'happiness': [0.0],
            'sadness': [0.0],
        }

        means_history = {
            'anger': [],
            'neutral': [],
            'happiness': [],
            'sadness': [],
        }


def write_plot(emotions_dict):
    """
    Creates two plots: one representing the live values of recognized emotions and another showing the progress of
    those values over a set period of time (HISTORY_SIZE).
    :param emotions_dict: Dictionary containing the values of the recognized emotions.
    """
    if not emotions_dict:
        return
    emotions = []
    values = []
    for face_id in emotions_dict:
        for emotion, value in emotions_dict[face_id].items():
            if emotion not in emotion_history.keys():
                continue
            emotions.append(emotion)
            values.append(value)
            emotion_history[emotion].append(value)

            if len(emotion_history[emotion]) > HISTORY_SIZE:  # Keeping the list to the size of HISTORY_SIZE
                emotion_history[emotion].pop(0)
        break  # Just to be sure we are only taking the first face available

    live_fig = plt.figure(figsize=(8, 6))
    prog_fig, live_prog = plt.subplots()
    prog_fig.set_size_inches(8, 4)

    live = live_fig.add_subplot(111)
    live.set_ylim(0, 1)

    live_prog.set_ylim(0, 1)
    live_prog.set_xlim(0, HISTORY_SIZE)

    barlist = live.bar(emotions, values)  # The barplot

    live_length = len(emotion_history['neutral'])
    means_length = 1 if len(means_history['neutral']) == 0 else len(means_history['neutral']) + 1

    x_axis = [i for i in range(0, HISTORY_SIZE, 1)]
    i = 0
    for emotion, history in emotion_history.items():
        means_history[emotion].append(sum(history) / means_length)
        if len(means_history[emotion]) > HISTORY_SIZE:  # Keeping the list to the size of HISTORY_SIZE
            means_history[emotion].pop(0)

        live_prog.plot(x_axis,
                       fill_gaps(history, live_length),
                       color=COLORS[emotion],
                       label=emotion,
                       linewidth=2)

        live_prog.set_xlim(0, HISTORY_SIZE - 1)
        live_prog.set_xticks(x_axis)

        barlist[i].set_color(COLORS[emotion])
        barlist[i].set_alpha(0.75)
        barlist[i].set_linewidth(1.3)
        barlist[i].set_edgecolor("#ffffff")
        i += 1

    live_means = [means_history[emotion][-1] for emotion, history in emotion_history.items()]
    live.plot(emotions, live_means, 'D', label="mean (last {} frames)".format(HISTORY_SIZE))
    live.legend()
    live_prog.legend(loc=2)

    plt.tight_layout()
    plt.figure(live_fig.number)
    plt.grid(linewidth=0.2)
    plt.text(len(emotion_history.keys())/2 - 0.5, 0.5, 'live observation', horizontalalignment='center',
             verticalalignment='center', alpha=0.1, fontsize=50)
    plt.savefig("emotions_plot.png")
    plt.close(live_fig)
    plt.figure(prog_fig.number)
    plt.grid(linewidth=0.2)
    plt.text(2, 0.5, 'progress', horizontalalignment='center', verticalalignment='center', alpha=0.1, fontsize=50)
    plt.savefig("progress_plot.png")
    plt.close(prog_fig)


def fill_gaps(history_list, current_length):
    """
    Used to fill history with empty data so that it can be displayed while its length being < HISTORY_SIZE
    :param history_list: current observations as a list
    :param current_length: current length of the observation
    :return: history with length of HISTORY_SIZE, gaps filled with empty data
    """
    if current_length >= HISTORY_SIZE:
        return history_list
    else:
        copy = history_list.copy()
        for i in range(current_length, HISTORY_SIZE):
            copy.append(None)
        return copy


def set_history_size(value):
    """
    Sets HISTORY_SIZE/number of observations for progress plotting to a specified value.
    :param value: (hopefully) an integer
    """
    global HISTORY_SIZE
    if value is int:
        HISTORY_SIZE = value


def get_history_size():
    """
    Returns the number of observations that we are plotting for the progress plot.
    :return: plotter.HISTORY_SIZE
    """
    return HISTORY_SIZE


def get_emotions_history():
    """
    Returns a dictionary containing lists of observed values for each emotion. The length of the lists <= HISTORY_SIZE.
    :return: plotter.emotion_history
    """
    return emotion_history


def get_means_history():
    """
    Returns a dictionary containing list of mean values for each emotion. The length of the lists <= HISTORY_SIZE.
    :return: plotter.means_history
    """
    return means_history


def get_colors():
    """
    Returns a dictionary containing a hex representation of colors associated with specific emotions.
    :return: plotter.COLORS
    """
    return COLORS


def set_azure_flag():
    """
    Sets the azure_flag global variable to True. Should be used at initialization.
    """
    global azure_flag
    azure_flag = True


