import mne
import logging
import inspect


RAW_TYPE = mne.io.Raw
EVOKED_TYPE = mne.Evoked
EPOCHS_TYPE = mne.Epochs
PROJECTION_TYPE = mne.io.Projection
SELECTIONS = mne.selection._SELECTIONS


def wrap(log_level, original_func):
    def wrapped(*args, **kwargs):
        logger = logging.getLogger("mne_wrapper_logger")
        numeric_level = getattr(logging, log_level.upper())
        
        try:
            # if function
            callargs = inspect.getcallargs(original_func, *args, **kwargs)
        except:
            # if class
            callargs = inspect.getcallargs(original_func.__init__, 
                *((object(),) + args), **kwargs)
        
        message = ("Calling " + str(original_func.__name__) + 
            " with args " + str(callargs))

        logger.log(numeric_level, message)

        return original_func(*args, **kwargs)
    return wrapped


read_raw_fif = wrap('debug', mne.io.read_raw_fif)
_has_eeg_average_ref_proj = wrap('debug', mne.io.proj._has_eeg_average_ref_proj)
make_fixed_length_events = wrap('debug', mne.make_fixed_length_events)
read_layout = wrap('debug', mne.channels.layout.read_layout) 
read_evokeds = wrap('debug', mne.read_evokeds)
read_epochs = wrap('debug', mne.read_epochs)
_merge_grad_data = wrap('debug', mne.channels.layout._merge_grad_data)
plot_evoked_topo = wrap('debug', mne.viz.plot_evoked_topo)
iter_topography = wrap('debug', mne.viz.iter_topography)
create_info = wrap('debug', mne.create_info)
_clean_names = wrap('debug', mne.utils._clean_names)    
tfr_morlet = wrap('debug', mne.time_frequency.tfr.tfr_morlet)
psd_welch = wrap('debug', mne.time_frequency.psd_welch)
compute_proj_ecg = wrap('debug', mne.preprocessing.compute_proj_ecg)
compute_proj_eog = wrap('debug', mne.preprocessing.compute_proj_eog)
compute_proj_evoked = wrap('debug', mne.compute_proj_evoked)
find_eog_events = wrap('debug', mne.preprocessing.find_eog_events)
find_ecg_events = wrap('debug', mne.preprocessing.find_ecg_events)
write_proj = wrap('debug', mne.write_proj)
read_proj = wrap('debug', mne.read_proj)
write_events = wrap('debug', mne.write_events)
pick_types = wrap('debug', mne.pick_types)
read_selection = wrap('debug', mne.read_selection)
pick_channels_evoked = wrap('debug', mne.pick_channels_evoked)
pick_channels_regexp = wrap('debug', mne.pick_channels_regexp)
grand_average = wrap('debug', mne.grand_average)
rescale = wrap('debug', mne.baseline.rescale)
channel_type = wrap('debug', mne.channels.channels.channel_type)
stft = wrap('debug', mne.time_frequency.stft)
stftfreq = wrap('debug', mne.time_frequency.stftfreq)
read_cov = wrap('debug', mne.read_cov)
write_cov = wrap('debug', mne.write_cov)
coregistration = wrap('info', mne.gui.coregistration)
make_watershed_bem = wrap('info', mne.bem.make_watershed_bem)
setup_source_space = wrap('debug', mne.setup_source_space)
make_bem_model = wrap('debug', mne.make_bem_model)
make_bem_solution = wrap('debug', mne.make_bem_solution)
make_forward_solution = wrap('debug', mne.make_forward_solution)
read_forward_solution = wrap('debug', mne.read_forward_solution)
write_forward_solution = wrap('debug', mne.write_forward_solution)
make_inverse_operator = wrap('debug', mne.minimum_norm.make_inverse_operator)
write_inverse_operator = wrap('debug', mne.minimum_norm.write_inverse_operator)
read_inverse_operator = wrap('debug', mne.minimum_norm.read_inverse_operator)
compute_raw_covariance = wrap('debug', mne.cov.compute_raw_covariance)
compute_covariance = wrap('debug', mne.cov.compute_covariance)
apply_inverse_raw = wrap('debug', mne.minimum_norm.apply_inverse_raw)
apply_inverse_epochs = wrap('debug', mne.minimum_norm.apply_inverse_epochs)
apply_inverse = wrap('debug', mne.minimum_norm.apply_inverse)
read_labels_from_annot = wrap('debug', mne.read_labels_from_annot)
read_source_estimate = wrap('debug', mne.read_source_estimate)
find_events = wrap('debug', mne.find_events)
write_evokeds = wrap('debug', mne.evoked.write_evokeds)
plot_bem = wrap('debug', mne.viz.plot_bem)
plot_epochs_image = wrap('debug', mne.viz.plot_epochs_image)
make_lcmv = wrap('debug', mne.beamformer.make_lcmv)
apply_lcmv = wrap('debug', mne.beamformer.apply_lcmv)
apply_lcmv_epochs = wrap('debug', mne.beamformer.apply_lcmv_epochs)
apply_lcmv_raw = wrap('debug', mne.beamformer.apply_lcmv_raw)
read_tfrs = wrap('debug', mne.time_frequency.read_tfrs)
ICA = wrap('debug', mne.preprocessing.ICA)
AverageTFR = wrap('debug', mne.time_frequency.AverageTFR)
Epochs = wrap('debug', mne.Epochs)
