"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.preprocessing.dialogs.eventsFromAnnotationsDialogUi import Ui_EventsFromAnnotationsDialog
from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded

from meggie.tabs.preprocessing.controller.events import events_from_annotations


class EventsFromAnnotationsDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_EventsFromAnnotationsDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent

        self.items = []

        subject = self.experiment.active_subject
        raw = subject.get_raw()

        for annotation_name in sorted(list(set(raw.annotations.description))):
            self.ui.comboBoxAnnotation.addItem(annotation_name)

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment


    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return

        annotation_name = self.ui.comboBoxAnnotation.currentText()
        event_id = self.ui.spinBoxEventID.value()
        use_start = True if self.ui.radioButtonStart.isChecked() else False

        self.items.append((annotation_name, event_id, use_start))
        self.update_list()

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return

        self.items = []
        self.update_list()

    def update_list(self):
        """
        """
        self.ui.listWidgetItems.clear()

        for item in self.items:
            text = 'Annotation: ' + str(item[0]) + ', event id: ' + str(item[1]) + ', '
            if item[2]:
                text = text + 'use start'
            else:
                text = text + 'use end'

            item = QtWidgets.QListWidgetItem(str(text))
            self.ui.listWidgetItems.addItem(item)

    def accept(self):
        """
        """

        subject = self.experiment.active_subject

        @threaded
        def evs_from_annots():
            try:
                events_from_annotations(subject, self.items)
            except Exception as exc:
                exc_messagebox(self, exc)
                return

            subject.save()

        evs_from_annots(do_meanwhile=self.parent.update_ui)
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished creating events from annotations.')
        self.close()

    def acceptBatch(self):
        """
        """

        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    @threaded
                    def evs_from_annots():
                        events_from_annotations(subject, self.items)
                        subject.save()
                        subject.release_memory()

                    evs_from_annots(do_meanwhile=self.parent.update_ui)
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        logging.getLogger('ui_logger').info('Finished creating events from annotations.')

        self.parent.initialize_ui()

        self.close()
