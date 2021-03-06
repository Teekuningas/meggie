import datetime
import re

import mne


class MeasurementInfo(object):
    """ A class for collecting information from raw files.
    """

    def __init__(self, raw):
        self._info = raw.info

    @property
    def high_pass(self):
        try:
            return round(self._info.get('highpass'), 2)
        except Exception as exc:
            pass

    @property
    def low_pass(self):
        try:
            return round(self._info.get('lowpass'), 2)
        except Exception as exc:
            return ""

    @property
    def sampling_freq(self):
        try:
            return round(self._info.get('sfreq'), 2)
        except Exception as exc:
            return ""

    @property
    def date(self):
        try:
            return str(self._info['meas_date'].date())
        except Exception as exc:
            return ""

    @property
    def subject_name(self):
        subj_info = self._info.get('subject_info')

        if not subj_info:
            return ''

        last_name = subj_info.get('last_name', '')
        first_name = subj_info.get('first_name', '')

        return last_name + ' ' + first_name
