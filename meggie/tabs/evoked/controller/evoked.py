# coding: utf-8

"""
"""

import logging
import os

import mne
import numpy as np
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import get_channel_average_fig_size
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.validators import assert_arrays_same

from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_unit


def plot_channel_averages(experiment, evoked):
    """
    """

    colors = color_cycle(len(list(evoked.content.keys())))
    times = list(evoked.content.values())[0].times

    averages = {}
    for key, mne_evoked in sorted(evoked.content.items()):
        data_labels, averaged_data = create_averages(experiment, mne_evoked)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, averaged_data[label_idx]))

    ch_groups = sorted(set([label[1] for label in averages.keys()]))
    ch_types = sorted(set([label[0] for label in averages.keys()]))

    ncols = 4
    nrows = int((len(ch_groups) - 1) / ncols + 1)

    for ch_type in ch_types:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
        fig.set_size_inches(*get_channel_average_fig_size(nrows, ncols))
        for ch_group_idx, ch_group in enumerate(ch_groups):
            ax = axes[ch_group_idx // ncols, ch_group_idx % ncols]
            ax.set_title(ch_group)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power ({})'.format(
                get_unit(ch_type)))

            handles = []
            for color_idx, (key, curve) in enumerate(averages[(ch_type, ch_group)]):
                handles.append(ax.plot(times, curve, color=colors[color_idx], label=key)[0])

            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        fig.legend(handles=handles)
        title_elems = [evoked.name, ch_type]
        fig.canvas.set_window_title('_'.join(title_elems))
        fig.suptitle(' '.join(title_elems))
        fig.tight_layout()

    plt.show()


def create_averages(experiment, mne_evoked):
    """
    """
    channel_groups = experiment.channel_groups

    mne_evoked = mne_evoked.copy().drop_channels(mne_evoked.info['bads'])

    data_labels, averaged_data = average_to_channel_groups(
        mne_evoked.data, mne_evoked.info, 
        mne_evoked.info['ch_names'], channel_groups)

    return data_labels, averaged_data


@threaded
def group_average_evoked(experiment, evoked_name, groups, new_name):
    """
    """
    keys = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                evoked = subject.evoked.get(evoked_name)

                mne_evokeds = evoked.content
                for mne_evoked in mne_evokeds.values():
                    time_arrays.append(mne_evoked.times)
            except Exception as exc:
                continue

    assert_arrays_same(time_arrays)

    grand_evokeds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            evoked = subject.evoked.get(evoked_name)
            if not evoked:
                logging.getLogger('ui_logger').warning(
                    evoked_name + ' not present for ' + subject.name)
                continue

            for evoked_item_key, evoked_item in evoked.content.items():
                grand_key = (group_key, evoked_item_key)

                if grand_key not in grand_evokeds:
                    grand_evokeds[grand_key] = []
                grand_evokeds[grand_key].append(evoked_item)

    grand_averages = {}
    new_keys = []
    for key, grand_evoked in grand_evokeds.items():
        new_key = str(key[1]) + '_' + str(key[0])
        if len(grand_evoked) == 1:
            grand_averages[new_key] = grand_evoked[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(grand_evoked)
        new_keys.append(new_key)

    subject = experiment.active_subject

    evoked_directory = subject.evoked_directory

    params = {'conditions': new_keys,
              'groups': groups}

    grand_average_evoked = Evoked(new_name, evoked_directory, params,
                                  content=grand_averages)

    grand_average_evoked.save_content()
    subject.add(grand_average_evoked, 'evoked')

@threaded
def save_all_channels(experiment, selected_name):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():
            column_names = format_floats(mne_evoked.times)

            for ch_idx, ch_name in enumerate(mne_evoked.info['ch_names']):
                if ch_name in mne_evoked.info['bads']:
                    continue
                csv_data.append(mne_evoked.data[ch_idx].tolist())

                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels_evoked.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_channel_averages(experiment, selected_name):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():

            data_labels, averaged_data = create_averages(
                experiment, mne_evoked)

            csv_data.extend(averaged_data.tolist())
            column_names = format_floats(mne_evoked.times)

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages_evoked.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

