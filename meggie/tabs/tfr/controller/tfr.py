# coding: utf-8
"""
"""

import os
import logging

import numpy as np
import matplotlib.pyplot as plt
import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import get_channel_average_fig_size
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import clean_names
from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_scaling
from meggie.utilities.units import get_unit
from meggie.utilities.units import get_power_unit
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.decorators import threaded

from meggie.datatypes.tfr.tfr import TFR


def _compute_tse(meggie_tfr, fmin, fmax):
    """
    """
    tfrs = meggie_tfr.content

    fmin_idx = np.where(meggie_tfr.freqs >= fmin)[0][0]
    fmax_idx = np.where(meggie_tfr.freqs <= fmax)[0][-1]

    if fmax_idx <= fmin_idx:
        raise Exception('Something wrong with the frequencies')

    tses = {}
    for key, tfr in tfrs.items():
        tse = np.mean(tfr.data[:, fmin_idx:fmax_idx+1, :], axis=1)
        tses[key] = tse

    return tses


def _crop_and_correct_to_baseline(tse, blmode, blstart, blend, tmin, tmax, times):
    """
    """
    tmin_idx = np.where(times >= tmin)[0][0]
    tmax_idx = np.where(times <= tmax)[0][-1]

    if blmode:
        if blstart < tmin:
            raise Exception(
                'Baseline start should not be earlier than crop start.')

        if blend > tmax:
            raise Exception(
                'Baseline end should not be later than crop end.')

        # correct to baseline
        tse = mne.baseline.rescale(tse, times, baseline=(blstart, blend), 
                                   mode=blmode)

        # crop
        tse = tse[:, tmin_idx:tmax_idx+1]

    return times[tmin_idx:tmax_idx+1], tse


def plot_tse_topo(experiment, subject, tfr_name, blmode, blstart, blend, 
                  tmin, tmax, fmin, fmax, ch_type):
    """
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    tses = _compute_tse(meggie_tfr, fmin, fmax)

    info = meggie_tfr.info
    if ch_type == 'meg':
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                            if ch_idx in mne.pick_types(info, meg=True, eeg=False)]
    else:
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                            if ch_idx in mne.pick_types(info, meg=False, eeg=True)]
    info = info.copy().pick_channels(picked_channels)

    ch_names = meggie_tfr.ch_names
    colors = color_cycle(len(tses))

    def individual_plot(ax, info_idx, names_idx):
        """
        """
        ch_name = ch_names[names_idx]

        title_elems = [tfr_name, ch_name]
        ax.figure.canvas.set_window_title('_'.join(title_elems))
        ax.figure.suptitle(' '.join(title_elems))
        ax.set_title('')

        for color_idx, (key, tse) in enumerate(sorted(tses.items())):
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)
            ax.plot(times, tse[names_idx], color=colors[color_idx], label=key)
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        ax.legend()

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, info_idx),
            False
        )))

        plt.show()

    fig = plt.figure()
    for ax, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, individual_plot):

        handles = []
        for color_idx, (key, tse) in enumerate(sorted(tses.items())):
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)
            handles.append(ax.plot(times, tse[names_idx], linewidth=0.2, 
                           color=colors[color_idx],
                           label=key)[0])

    fig.legend(handles=handles)
    title = '{0}_{1}'.format(tfr_name, ch_type)
    fig.canvas.set_window_title(title)
    plt.show()


def plot_tse_averages(experiment, subject, tfr_name, blmode, blstart, blend,
                      tmin, tmax, fmin, fmax):
    """
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    tses = _compute_tse(meggie_tfr, fmin, fmax)

    ch_names = meggie_tfr.ch_names
    info = meggie_tfr.info
    colors = color_cycle(len(tses))

    channel_groups = experiment.channel_groups

    averages = {}
    for key, tse in sorted(tses.items()):
        data_labels, averaged_data = average_to_channel_groups(
            tse, info, ch_names, channel_groups)

        times, averaged_data = _crop_and_correct_to_baseline(
            averaged_data, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, times, averaged_data[label_idx]))

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
            ax.set_ylabel('Power ({})'.format(get_power_unit(
                ch_type, False)))

            handles = []
            for color_idx, (key, times, curve) in enumerate(averages[(ch_type, ch_group)]):
                handles.append(ax.plot(times, curve, color=colors[color_idx], label=key)[0])

            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        fig.legend(handles=handles)
        title_elems = [tfr_name, ch_type]
        fig.canvas.set_window_title('_'.join(title_elems))
        fig.suptitle(' '.join(title_elems))
        fig.tight_layout()

    plt.show()


def plot_tfr_averages(experiment, subject, tfr_name, tfr_condition, 
                      blmode, blstart, blend,
                      tmin, tmax, fmin, fmax):

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    data = tfr.data
    ch_names = meggie_tfr.ch_names
    channel_groups = experiment.channel_groups

    sfreq = meggie_tfr.info['sfreq']
    times = meggie_tfr.times
    freqs = meggie_tfr.freqs

    # compared to spectrums, evoked and tse, tfr is plotted with only one condition.
    # it makes the plotting a bit simpler. we will also misuse 
    # AverageTFR object to do the heavy work.

    data_labels, averaged_data = average_to_channel_groups(
        data, meggie_tfr.info, ch_names, channel_groups)

    averages = {}
    for label_idx, label in enumerate(data_labels):
        averages[label] = averaged_data[label_idx]

    ch_groups = sorted(set([label[1] for label in data_labels]))
    ch_types = sorted(set([label[0] for label in data_labels]))

    ncols = 4
    nrows = int((len(ch_groups) - 1) / ncols + 1)

    for ch_type in ch_types:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
        fig.set_size_inches(*get_channel_average_fig_size(nrows, ncols))

        for ch_group_idx, ch_group in enumerate(ch_groups):
            ax = axes[ch_group_idx // ncols, ch_group_idx % ncols]
            ax.set_title(ch_group)

            info = mne.create_info(ch_names=['grand_average'], sfreq=sfreq, ch_types='mag')
            tfr = mne.time_frequency.tfr.AverageTFR(info,
                averages[(ch_type, ch_group)][np.newaxis, :], times, freqs, 1)

            # prevent interaction as no topography is involved now
            def onselect(*args, **kwargs):
                pass
            tfr._onselect = onselect

            tfr.plot(baseline=bline, mode=mode, title='', 
                     fmin=fmin, fmax=fmax, 
                     tmin=tmin, tmax=tmax, axes=ax)

        fig.tight_layout()
        title_elems = [tfr_name, tfr_condition, ch_type]
        fig.canvas.set_window_title('_'.join(title_elems))
        fig.suptitle(' '.join(title_elems))


def plot_tfr_topo(experiment, subject, tfr_name, tfr_condition, 
                  blmode, blstart, blend,
                  tmin, tmax, fmin, fmax, ch_type):

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    if ch_type == 'eeg':
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=True, meg=False)]
    else:
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=False, meg=True)]

    tfr = tfr.copy().drop_channels(dropped_names)

    title = '{0}_{1}_{2}'.format(tfr_name, tfr_condition, ch_type)
    fig = tfr.plot_topo(show=False,
                        baseline=bline, mode=mode,
                        tmin=tmin, tmax=tmax,
                        fmin=fmin, fmax=fmax,
                        title="")

    fig.canvas.set_window_title(title)

    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gca().set_title('')

        title_elems = [tfr_name, channel]
        plt.gcf().canvas.set_window_title('_'.join(title_elems))
        plt.gcf().suptitle(' '.join(title_elems))

        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()

@threaded
def create_tfr(subject, tfr_name, epochs_names,
               freqs, decim, n_cycles, subtract_evoked):

    time_arrays = []
    for name in epochs_names:
        collection = subject.epochs.get(name)
        if collection:
            time_arrays.append(collection.content.times)
    assert_arrays_same(time_arrays)

    tfrs = {}
    for epoch_name in epochs_names:
        epochs = subject.epochs[epoch_name].content
        if subtract_evoked:
            epochs = epochs.copy().subtract_evoked()

        tfr = mne.time_frequency.tfr.tfr_morlet(epochs, 
                                                freqs=freqs, 
                                                n_cycles=n_cycles,
                                                decim=decim, 
                                                average=True,
                                                return_itc=False)
        tfrs[epoch_name] = tfr

    # convert list-like to list
    if hasattr(n_cycles, '__len__'):
        n_cycles = list(n_cycles)

    params = {
        'decim': decim,
        'n_cycles': n_cycles,
        'evoked_subtracted': subtract_evoked,
        'conditions': epochs_names
    }

    meggie_tfr = TFR(tfr_name, subject.tfr_directory, params, tfrs)

    meggie_tfr.save_content()
    subject.add(meggie_tfr, "tfr")


@threaded
def group_average_tfr(experiment, tfr_name, groups, new_name):

    # check data cohesion
    keys = []
    freq_arrays = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                keys.append(tuple(sorted(tfr.content.keys())))
                freq_arrays.append(tuple(tfr.freqs))
                time_arrays.append(tuple(tfr.times))
            except Exception as exc:
                continue

    assert_arrays_same(keys, 'Conditions do no match')
    assert_arrays_same(freq_arrays, 'Freqs do not match')
    assert_arrays_same(time_arrays)

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                ch_names.append(tuple(clean_names(tfr.ch_names)))
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "TFR's contain different sets of channels. Identifying common ones..")

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger('ui_logger').info(str(len(common_ch_names)) +
                                            ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(common_ch_names))
    else:
        common_ch_names = ch_names[0]

    grand_tfrs = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            meggie_tfr = subject.tfr.get(tfr_name)
            if not meggie_tfr:
                continue

            for tfr_item_key, tfr_item in meggie_tfr.content.items():
                grand_key = (group_key, tfr_item_key)

                # get common channels in "subject specific space"
                subject_ch_names = tfr_item.info['ch_names']
                for ch_idx, ch_name in enumerate(clean_names(subject_ch_names)):
                    drop_names = []
                    if ch_name not in common_ch_names:
                        drop_names.append(subject_ch_names[ch_idx])
                tfr_item = tfr_item.copy().drop_channels(drop_names)

                # sanity check
                if len(tfr_item.info['ch_names']) != len(common_ch_names):
                    raise Exception('Something wrong with the channels')

                if grand_key in grand_tfrs:
                    grand_tfrs[grand_key].append(tfr_item)
                else:
                    grand_tfrs[grand_key] = [tfr_item]

    grand_averages = {}
    for key, grand_tfr in grand_tfrs.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_tfr) == 1:
            grand_averages[new_key] = grand_tfr[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(
                grand_tfr)

    active_subject = experiment.active_subject
    meggie_tfr = active_subject.tfr.get(tfr_name)

    params = {
        'decim': meggie_tfr.decim,
        'n_cycles': meggie_tfr.n_cycles,
        'evoked_subtracted': meggie_tfr.evoked_subtracted,
        'conditions': list(grand_averages.keys()),
        'groups': groups
    }

    meggie_tfr = TFR(new_name, active_subject.tfr_directory, params, grand_averages)

    meggie_tfr.save_content()
    active_subject.add(meggie_tfr, "tfr")


@threaded
def save_tfr_all_channels(experiment, tfr_name,
                          blmode, blstart, blend,
                          tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            data = mne.baseline.rescale(mne_tfr.data, times, baseline=(blstart, blend), 
                                       mode=blmode)

            for ix in range(data.shape[0]):
                for iy in range(data.shape[1]):
                    csv_data.append(data[ix, iy].tolist())

                    row_desc = (subject.name, key, ch_names[ix], freqs[iy])
                    row_descs.append(row_desc)

        folder = filemanager.create_timestamped_folder(experiment)
        fname = tfr_name + '_all_subjects_all_channels_tfr.csv'
        path = os.path.join(folder, fname)

        filemanager.save_csv(path, csv_data, column_names, row_descs)
        logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_tfr_channel_averages(experiment, tfr_name,
                              blmode, blstart, blend,
                              tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names
        info = tfr.info

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            data = mne.baseline.rescale(mne_tfr.data, times, baseline=(blstart, blend), 
                                       mode=blmode)

            data_labels, averaged_data = average_to_channel_groups(
                data, info, ch_names, channel_groups)

            for ix in range(averaged_data.shape[0]):
                for iy in range(averaged_data.shape[1]):
                    ch_type, area = data_labels[ix]

                    csv_data.append(averaged_data[ix, iy].tolist())

                    row_desc = (subject.name, key, ch_type, area, freqs[iy])
                    row_descs.append(row_desc)

        folder = filemanager.create_timestamped_folder(experiment)
        fname = tfr_name + '_all_subjects_channel_averages_tfr.csv'
        path = os.path.join(folder, fname)

        filemanager.save_csv(path, csv_data, column_names, row_descs)
        logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_tse_all_channels(experiment, tfr_name, blmode, blstart, 
                          blend, tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        tses = _compute_tse(tfr, fmin, fmax)

        for key, tse in tses.items():
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, tfr.times)

            csv_data.extend(tse.tolist())

            for ch_name in tfr.ch_names:
                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

        column_names = format_floats(times)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_all_channels_tse.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


@threaded
def save_tse_channel_averages(experiment, tfr_name, blmode, blstart, 
                              blend, tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        tses = _compute_tse(tfr, fmin, fmax)

        for key, tse in tses.items():

            data_labels, averaged_data = average_to_channel_groups(
                tse, tfr.info, tfr.ch_names, channel_groups)

            times, averaged_data = _crop_and_correct_to_baseline(
                averaged_data, blmode, blstart, blend, tmin, tmax, tfr.times)

            csv_data.extend(averaged_data.tolist())

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

        column_names = format_floats(times)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_channel_averages_tse.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


