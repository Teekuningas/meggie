# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forwardSolutionDialogUi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_forwardSolutionDialog(object):
    def setupUi(self, forwardSolutionDialog):
        forwardSolutionDialog.setObjectName(_fromUtf8("forwardSolutionDialog"))
        forwardSolutionDialog.resize(572, 361)
        forwardSolutionDialog.setModal(True)
        self.formLayout_3 = QtGui.QFormLayout(forwardSolutionDialog)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.labelForwardSolutionName = QtGui.QLabel(forwardSolutionDialog)
        self.labelForwardSolutionName.setObjectName(_fromUtf8("labelForwardSolutionName"))
        self.horizontalLayout_6.addWidget(self.labelForwardSolutionName)
        self.lineEditForwardSolutionName = QtGui.QLineEdit(forwardSolutionDialog)
        self.lineEditForwardSolutionName.setObjectName(_fromUtf8("lineEditForwardSolutionName"))
        self.horizontalLayout_6.addWidget(self.lineEditForwardSolutionName)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.SpanningRole, self.horizontalLayout_6)
        self.groupBoxSourceSpaceSetup = QtGui.QGroupBox(forwardSolutionDialog)
        self.groupBoxSourceSpaceSetup.setObjectName(_fromUtf8("groupBoxSourceSpaceSetup"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxSourceSpaceSetup)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.labelIco = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelIco.setObjectName(_fromUtf8("labelIco"))
        self.gridLayout_3.addWidget(self.labelIco, 0, 0, 1, 1)
        self.comboBoxSurfaceDecimMethod = QtGui.QComboBox(self.groupBoxSourceSpaceSetup)
        self.comboBoxSurfaceDecimMethod.setObjectName(_fromUtf8("comboBoxSurfaceDecimMethod"))
        self.comboBoxSurfaceDecimMethod.addItem(_fromUtf8(""))
        self.comboBoxSurfaceDecimMethod.addItem(_fromUtf8(""))
        self.comboBoxSurfaceDecimMethod.addItem(_fromUtf8(""))
        self.comboBoxSurfaceDecimMethod.addItem(_fromUtf8(""))
        self.gridLayout_3.addWidget(self.comboBoxSurfaceDecimMethod, 0, 1, 1, 2)
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.SpanningRole, self.groupBoxSourceSpaceSetup)
        self.groupBoxSetupBem = QtGui.QGroupBox(forwardSolutionDialog)
        self.groupBoxSetupBem.setObjectName(_fromUtf8("groupBoxSetupBem"))
        self.gridLayout = QtGui.QGridLayout(self.groupBoxSetupBem)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelHomog = QtGui.QLabel(self.groupBoxSetupBem)
        self.labelHomog.setObjectName(_fromUtf8("labelHomog"))
        self.gridLayout.addWidget(self.labelHomog, 1, 0, 1, 1)
        self.comboBoxCompartmentModel = QtGui.QComboBox(self.groupBoxSetupBem)
        self.comboBoxCompartmentModel.setObjectName(_fromUtf8("comboBoxCompartmentModel"))
        self.comboBoxCompartmentModel.addItem(_fromUtf8(""))
        self.comboBoxCompartmentModel.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBoxCompartmentModel, 1, 1, 1, 1)
        self.frame_2 = QtGui.QFrame(self.groupBoxSetupBem)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.frame_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.labelConductivity = QtGui.QLabel(self.frame_2)
        self.labelConductivity.setObjectName(_fromUtf8("labelConductivity"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.SpanningRole, self.labelConductivity)
        self.labelBrainComp = QtGui.QLabel(self.frame_2)
        self.labelBrainComp.setObjectName(_fromUtf8("labelBrainComp"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelBrainComp)
        self.doubleSpinBoxBrainConductivity = QtGui.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBoxBrainConductivity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxBrainConductivity.setDecimals(2)
        self.doubleSpinBoxBrainConductivity.setProperty("value", 0.3)
        self.doubleSpinBoxBrainConductivity.setObjectName(_fromUtf8("doubleSpinBoxBrainConductivity"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxBrainConductivity)
        self.labelSkullComp = QtGui.QLabel(self.frame_2)
        self.labelSkullComp.setObjectName(_fromUtf8("labelSkullComp"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelSkullComp)
        self.doubleSpinBoxSkullConductivity = QtGui.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBoxSkullConductivity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxSkullConductivity.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxSkullConductivity.setDecimals(3)
        self.doubleSpinBoxSkullConductivity.setProperty("value", 0.006)
        self.doubleSpinBoxSkullConductivity.setObjectName(_fromUtf8("doubleSpinBoxSkullConductivity"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxSkullConductivity)
        self.labelScalpComp = QtGui.QLabel(self.frame_2)
        self.labelScalpComp.setObjectName(_fromUtf8("labelScalpComp"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelScalpComp)
        self.doubleSpinBoxScalpConductivity = QtGui.QDoubleSpinBox(self.frame_2)
        self.doubleSpinBoxScalpConductivity.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxScalpConductivity.setProperty("value", 0.03)
        self.doubleSpinBoxScalpConductivity.setObjectName(_fromUtf8("doubleSpinBoxScalpConductivity"))
        self.formLayout_2.setWidget(3, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxScalpConductivity)
        self.gridLayout.addWidget(self.frame_2, 2, 1, 1, 1)
        self.labelTriangIco = QtGui.QLabel(self.groupBoxSetupBem)
        self.labelTriangIco.setObjectName(_fromUtf8("labelTriangIco"))
        self.gridLayout.addWidget(self.labelTriangIco, 0, 0, 1, 1)
        self.spinBoxTriangFilesIco = QtGui.QSpinBox(self.groupBoxSetupBem)
        self.spinBoxTriangFilesIco.setEnabled(True)
        self.spinBoxTriangFilesIco.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxTriangFilesIco.setProperty("value", 4)
        self.spinBoxTriangFilesIco.setObjectName(_fromUtf8("spinBoxTriangFilesIco"))
        self.gridLayout.addWidget(self.spinBoxTriangFilesIco, 0, 1, 1, 1)
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBoxSetupBem)
        self.buttonBox = QtGui.QDialogButtonBox(forwardSolutionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.SpanningRole, self.buttonBox)
        self.labelHomog.setBuddy(self.comboBoxCompartmentModel)
        self.labelBrainComp.setBuddy(self.doubleSpinBoxBrainConductivity)
        self.labelSkullComp.setBuddy(self.doubleSpinBoxSkullConductivity)
        self.labelScalpComp.setBuddy(self.doubleSpinBoxScalpConductivity)

        self.retranslateUi(forwardSolutionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), forwardSolutionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), forwardSolutionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(forwardSolutionDialog)

    def retranslateUi(self, forwardSolutionDialog):
        forwardSolutionDialog.setWindowTitle(_translate("forwardSolutionDialog", "Create new forward solution", None))
        self.labelForwardSolutionName.setText(_translate("forwardSolutionDialog", "Forward solution name:", None))
        self.groupBoxSourceSpaceSetup.setTitle(_translate("forwardSolutionDialog", "Source space setup parameters:", None))
        self.labelIco.setText(_translate("forwardSolutionDialog", "Cortical surface decimation method:", None))
        self.comboBoxSurfaceDecimMethod.setItemText(0, _translate("forwardSolutionDialog", "ico4", None))
        self.comboBoxSurfaceDecimMethod.setItemText(1, _translate("forwardSolutionDialog", "oct5", None))
        self.comboBoxSurfaceDecimMethod.setItemText(2, _translate("forwardSolutionDialog", "ico5", None))
        self.comboBoxSurfaceDecimMethod.setItemText(3, _translate("forwardSolutionDialog", "oct6", None))
        self.groupBoxSetupBem.setTitle(_translate("forwardSolutionDialog", "BEM model setup parameters:", None))
        self.labelHomog.setText(_translate("forwardSolutionDialog", "Compartment model (homog) :", None))
        self.comboBoxCompartmentModel.setItemText(0, _translate("forwardSolutionDialog", "single (usually used with MEG)", None))
        self.comboBoxCompartmentModel.setItemText(1, _translate("forwardSolutionDialog", "three layer", None))
        self.labelConductivity.setText(_translate("forwardSolutionDialog", "<html><head/><body><p><span style=\" font-weight:600;\">Conductivity:</span></p></body></html>", None))
        self.labelBrainComp.setText(_translate("forwardSolutionDialog", "inner skull:", None))
        self.doubleSpinBoxBrainConductivity.setSuffix(_translate("forwardSolutionDialog", " S/m", None))
        self.labelSkullComp.setText(_translate("forwardSolutionDialog", "outer skull:", None))
        self.doubleSpinBoxSkullConductivity.setSuffix(_translate("forwardSolutionDialog", " S/m", None))
        self.labelScalpComp.setText(_translate("forwardSolutionDialog", "outer skin:", None))
        self.doubleSpinBoxScalpConductivity.setSuffix(_translate("forwardSolutionDialog", " S/m", None))
        self.labelTriangIco.setText(_translate("forwardSolutionDialog", "Triangulation files ico-number:", None))

