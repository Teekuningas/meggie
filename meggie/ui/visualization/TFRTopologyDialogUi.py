# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFRtopology.ui'
#
# Created: Fri May 31 13:42:00 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_DialogTFRTopology(object):
    def setupUi(self, DialogTFRTopology):
        DialogTFRTopology.setObjectName(_fromUtf8("DialogTFRTopology"))
        DialogTFRTopology.resize(527, 611)
        self.gridLayout_2 = QtGui.QGridLayout(DialogTFRTopology)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(DialogTFRTopology)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(DialogTFRTopology)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 509, 551))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(197, 134))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.groupBoxFrequencies = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxFrequencies.setGeometry(QtCore.QRect(10, 110, 241, 231))
        self.groupBoxFrequencies.setObjectName(_fromUtf8("groupBoxFrequencies"))
        self.layoutWidget = QtGui.QWidget(self.groupBoxFrequencies)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 221, 191))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.labelMinFreq = QtGui.QLabel(self.layoutWidget)
        self.labelMinFreq.setObjectName(_fromUtf8("labelMinFreq"))
        self.horizontalLayout_13.addWidget(self.labelMinFreq)
        self.doubleSpinBoxMinFreq = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxMinFreq.setMinimum(0.1)
        self.doubleSpinBoxMinFreq.setMaximum(200.0)
        self.doubleSpinBoxMinFreq.setProperty("value", 7.0)
        self.doubleSpinBoxMinFreq.setObjectName(_fromUtf8("doubleSpinBoxMinFreq"))
        self.horizontalLayout_13.addWidget(self.doubleSpinBoxMinFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.labelMaxFreq = QtGui.QLabel(self.layoutWidget)
        self.labelMaxFreq.setObjectName(_fromUtf8("labelMaxFreq"))
        self.horizontalLayout_12.addWidget(self.labelMaxFreq)
        self.doubleSpinBoxMaxFreq = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxMaxFreq.setMinimum(7.0)
        self.doubleSpinBoxMaxFreq.setMaximum(600.0)
        self.doubleSpinBoxMaxFreq.setProperty("value", 30.0)
        self.doubleSpinBoxMaxFreq.setObjectName(_fromUtf8("doubleSpinBoxMaxFreq"))
        self.horizontalLayout_12.addWidget(self.doubleSpinBoxMaxFreq)
        self.verticalLayout_6.addLayout(self.horizontalLayout_12)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelFrequencyInterval = QtGui.QLabel(self.layoutWidget)
        self.labelFrequencyInterval.setObjectName(_fromUtf8("labelFrequencyInterval"))
        self.horizontalLayout.addWidget(self.labelFrequencyInterval)
        self.doubleSpinBoxFreqInterval = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxFreqInterval.setMinimum(0.1)
        self.doubleSpinBoxFreqInterval.setMaximum(99.99)
        self.doubleSpinBoxFreqInterval.setProperty("value", 3.0)
        self.doubleSpinBoxFreqInterval.setObjectName(_fromUtf8("doubleSpinBoxFreqInterval"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxFreqInterval)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelNcycles = QtGui.QLabel(self.layoutWidget)
        self.labelNcycles.setObjectName(_fromUtf8("labelNcycles"))
        self.horizontalLayout_2.addWidget(self.labelNcycles)
        self.spinBoxNcycles = QtGui.QSpinBox(self.layoutWidget)
        self.spinBoxNcycles.setMinimum(1)
        self.spinBoxNcycles.setProperty("value", 7)
        self.spinBoxNcycles.setObjectName(_fromUtf8("spinBoxNcycles"))
        self.horizontalLayout_2.addWidget(self.spinBoxNcycles)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_8.addWidget(self.label_2)
        self.spinBoxDecim = QtGui.QSpinBox(self.layoutWidget)
        self.spinBoxDecim.setProperty("value", 3)
        self.spinBoxDecim.setObjectName(_fromUtf8("spinBoxDecim"))
        self.horizontalLayout_8.addWidget(self.spinBoxDecim)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.groupBoxTopogpraphyType = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxTopogpraphyType.setGeometry(QtCore.QRect(10, 10, 181, 91))
        self.groupBoxTopogpraphyType.setObjectName(_fromUtf8("groupBoxTopogpraphyType"))
        self.gridLayout = QtGui.QGridLayout(self.groupBoxTopogpraphyType)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.radioButtonInduced = QtGui.QRadioButton(self.groupBoxTopogpraphyType)
        self.radioButtonInduced.setChecked(True)
        self.radioButtonInduced.setObjectName(_fromUtf8("radioButtonInduced"))
        self.gridLayout.addWidget(self.radioButtonInduced, 0, 0, 1, 1)
        self.radioButtonPhase = QtGui.QRadioButton(self.groupBoxTopogpraphyType)
        self.radioButtonPhase.setObjectName(_fromUtf8("radioButtonPhase"))
        self.gridLayout.addWidget(self.radioButtonPhase, 1, 0, 1, 1)
        self.groupBoxBaseline = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBaseline.setGeometry(QtCore.QRect(10, 350, 251, 134))
        self.groupBoxBaseline.setObjectName(_fromUtf8("groupBoxBaseline"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxBaseline)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelRescaling = QtGui.QLabel(self.groupBoxBaseline)
        self.labelRescaling.setObjectName(_fromUtf8("labelRescaling"))
        self.horizontalLayout_7.addWidget(self.labelRescaling)
        self.comboBoxMode = QtGui.QComboBox(self.groupBoxBaseline)
        self.comboBoxMode.setObjectName(_fromUtf8("comboBoxMode"))
        self.comboBoxMode.addItem(_fromUtf8(""))
        self.comboBoxMode.addItem(_fromUtf8(""))
        self.comboBoxMode.addItem(_fromUtf8(""))
        self.comboBoxMode.addItem(_fromUtf8(""))
        self.comboBoxMode.addItem(_fromUtf8(""))
        self.horizontalLayout_7.addWidget(self.comboBoxMode)
        self.gridLayout_3.addLayout(self.horizontalLayout_7, 0, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelBaselineStart = QtGui.QLabel(self.groupBoxBaseline)
        self.labelBaselineStart.setEnabled(False)
        self.labelBaselineStart.setObjectName(_fromUtf8("labelBaselineStart"))
        self.horizontalLayout_3.addWidget(self.labelBaselineStart)
        self.doubleSpinBoxBaselineStart = QtGui.QDoubleSpinBox(self.groupBoxBaseline)
        self.doubleSpinBoxBaselineStart.setEnabled(False)
        self.doubleSpinBoxBaselineStart.setDecimals(3)
        self.doubleSpinBoxBaselineStart.setObjectName(_fromUtf8("doubleSpinBoxBaselineStart"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxBaselineStart)
        self.checkBoxBaselineStartNone = QtGui.QCheckBox(self.groupBoxBaseline)
        self.checkBoxBaselineStartNone.setChecked(True)
        self.checkBoxBaselineStartNone.setObjectName(_fromUtf8("checkBoxBaselineStartNone"))
        self.horizontalLayout_3.addWidget(self.checkBoxBaselineStartNone)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelBaselineEnd = QtGui.QLabel(self.groupBoxBaseline)
        self.labelBaselineEnd.setEnabled(False)
        self.labelBaselineEnd.setObjectName(_fromUtf8("labelBaselineEnd"))
        self.horizontalLayout_4.addWidget(self.labelBaselineEnd)
        self.doubleSpinBoxBaselineEnd = QtGui.QDoubleSpinBox(self.groupBoxBaseline)
        self.doubleSpinBoxBaselineEnd.setEnabled(False)
        self.doubleSpinBoxBaselineEnd.setDecimals(3)
        self.doubleSpinBoxBaselineEnd.setObjectName(_fromUtf8("doubleSpinBoxBaselineEnd"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxBaselineEnd)
        self.checkBoxBaselineEndNone = QtGui.QCheckBox(self.groupBoxBaseline)
        self.checkBoxBaselineEndNone.setChecked(True)
        self.checkBoxBaselineEndNone.setObjectName(_fromUtf8("checkBoxBaselineEndNone"))
        self.horizontalLayout_4.addWidget(self.checkBoxBaselineEndNone)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.gridLayout_3.addLayout(self.horizontalLayout_5, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(DialogTFRTopology)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogTFRTopology.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogTFRTopology.reject)
        QtCore.QObject.connect(self.checkBoxBaselineStartNone, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.labelBaselineStart.setDisabled)
        QtCore.QObject.connect(self.checkBoxBaselineStartNone, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxBaselineStart.setDisabled)
        QtCore.QObject.connect(self.checkBoxBaselineEndNone, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxBaselineEnd.setDisabled)
        QtCore.QObject.connect(self.checkBoxBaselineEndNone, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.labelBaselineEnd.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(DialogTFRTopology)
        DialogTFRTopology.setTabOrder(self.scrollArea, self.doubleSpinBoxMinFreq)
        DialogTFRTopology.setTabOrder(self.doubleSpinBoxMinFreq, self.doubleSpinBoxMaxFreq)
        DialogTFRTopology.setTabOrder(self.doubleSpinBoxMaxFreq, self.doubleSpinBoxFreqInterval)
        DialogTFRTopology.setTabOrder(self.doubleSpinBoxFreqInterval, self.spinBoxNcycles)
        DialogTFRTopology.setTabOrder(self.spinBoxNcycles, self.buttonBox)

    def retranslateUi(self, DialogTFRTopology):
        DialogTFRTopology.setWindowTitle(_translate("DialogTFRTopology", "Meggie - Show TFR topologies ", None))
        self.groupBoxFrequencies.setTitle(_translate("DialogTFRTopology", "Frequency window", None))
        self.labelMinFreq.setText(_translate("DialogTFRTopology", "Minimum frequency:", None))
        self.labelMaxFreq.setText(_translate("DialogTFRTopology", "Maximum frequency:", None))
        self.labelFrequencyInterval.setText(_translate("DialogTFRTopology", "Frequency interval:", None))
        self.labelNcycles.setText(_translate("DialogTFRTopology", "Number of cycles:", None))
        self.label_2.setText(_translate("DialogTFRTopology", "Temporal decim factor:", None))
        self.groupBoxTopogpraphyType.setTitle(_translate("DialogTFRTopology", "Topography type", None))
        self.radioButtonInduced.setText(_translate("DialogTFRTopology", "Induced power", None))
        self.radioButtonPhase.setText(_translate("DialogTFRTopology", "Phase locking value", None))
        self.groupBoxBaseline.setTitle(_translate("DialogTFRTopology", "Baseline rescaling and correction", None))
        self.labelRescaling.setText(_translate("DialogTFRTopology", "Rescaling mode:", None))
        self.comboBoxMode.setItemText(0, _translate("DialogTFRTopology", "ratio", None))
        self.comboBoxMode.setItemText(1, _translate("DialogTFRTopology", "logratio", None))
        self.comboBoxMode.setItemText(2, _translate("DialogTFRTopology", "mean", None))
        self.comboBoxMode.setItemText(3, _translate("DialogTFRTopology", "zscore", None))
        self.comboBoxMode.setItemText(4, _translate("DialogTFRTopology", "percent", None))
        self.labelBaselineStart.setText(_translate("DialogTFRTopology", "Baseline start:", None))
        self.doubleSpinBoxBaselineStart.setSuffix(_translate("DialogTFRTopology", "s", None))
        self.checkBoxBaselineStartNone.setText(_translate("DialogTFRTopology", "None", None))
        self.labelBaselineEnd.setText(_translate("DialogTFRTopology", "Baseline end:", None))
        self.doubleSpinBoxBaselineEnd.setSuffix(_translate("DialogTFRTopology", "s", None))
        self.checkBoxBaselineEndNone.setText(_translate("DialogTFRTopology", "None", None))
