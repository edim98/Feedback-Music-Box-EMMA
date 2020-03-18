from matplotlib import pyplot as plt
import matplotlib as mpl
import numpy as np

# TODO: Add the possibility of plotting our model's results.

plt.style.use('dark_background')

HISTORY_SIZE = 5  # Number of observations for mean calculation and progress plot

COLORS = {
    'anger': '#dd3418',  # red
    'contempt': '#dd8518',  # orange
    'disgust': '#4a8a4d',  # puke green
    'fear': '#808080',  # ghost white
    'happiness': '#f0f417',  # bright yellow
    'neutral': '#808080',  # gray
    'sadness': '#5d7293',  # sad blue
    'surprise': '#b665b6'  # surprise violet
}

emotion_history = {
    'anger': [0.0],
    'contempt': [0.0],
    'disgust': [0.0],
    'fear': [0.0],
    'happiness': [0.0],
    'neutral': [0.0],
    'sadness': [0.0],
    'surprise': [0.0]
}

means_history = {
    'anger': [],
    'contempt': [],
    'disgust': [],
    'fear': [],
    'happiness': [],
    'neutral': [],
    'sadness': [],
    'surprise': []
}


def write_plot(emotions_dict):
    if not emotions_dict:
        return
    emotions = []
    values = []
    for face_id in emotions_dict:
        for emotion, value in emotions_dict[face_id].items():
            emotions.append(emotion)
            values.append(value)
            emotion_history[emotion].append(value)

            if len(emotion_history[emotion]) > HISTORY_SIZE:
                emotion_history[emotion].pop(0)
        break  # Just to be sure we are only taking the first face available

    live_fig = plt.figure(figsize=(8, 6))
    prog_fig, live_prog = plt.subplots()
    prog_fig.set_size_inches(8, 4)

    live = live_fig.add_subplot(111)
    live.set_ylim(0, 1)

    live_prog.set_ylim(0, 1)
    live_prog.set_xlim(0, HISTORY_SIZE)

    barlist = live.bar(emotions, values)

    live_length = len(emotion_history['neutral'])
    means_length = 1 if len(means_history['neutral']) == 0 else len(means_history['neutral']) + 1

    x_axis = [i for i in range(0, HISTORY_SIZE, 1)]
    i = 0
    for emotion, history in emotion_history.items():
        means_history[emotion].append(sum(history) / means_length)
        if len(means_history[emotion]) > HISTORY_SIZE:
            means_history[emotion].pop(0)

        live_prog.plot(x_axis,
                       fill_gaps(history, live_length),
                       color=COLORS[emotion],
                       label=emotion,
                       linewidth=2)

        live_prog.set_xlim(0, HISTORY_SIZE - 1)
        live_prog.set_xticks(x_axis)

        # means_prog.plot(x_axis,
        #                 fill_gaps(means_history[emotion], means_length),
        #                 color=COLORS[emotion],
        #                 label=emotion,
        #                 linewidth=2)
        #
        # means_prog.set_xlim(0, HISTORY_SIZE - 1)
        # means_prog.set_xticks(x_axis)

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
    plt.text(3.5, 0.5, 'live observation', horizontalalignment='center', verticalalignment='center', alpha=0.05,
             fontsize=50)
    plt.savefig("emotions_plot.png")
    plt.close(live_fig)
    plt.figure(prog_fig.number)
    plt.grid(linewidth=0.2)
    plt.text(2, 0.5, 'progress', horizontalalignment='center', verticalalignment='center', alpha=0.05, fontsize=50)
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


def get_history_size():
    return HISTORY_SIZE


def get_emotions_history():
    return emotion_history


def get_means_history():
    return means_history


def get_colors():
    return COLORS
