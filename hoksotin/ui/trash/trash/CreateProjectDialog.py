# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createProjectDialog.ui'
#
# Created: Wed Mar 13 17:39:55 2013
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

class Ui_CreateProjectDialog(object):
    def setupUi(self, CreateProjectDialog):
        CreateProjectDialog.setObjectName(_fromUtf8("CreateProjectDialog"))
        CreateProjectDialog.setWindowModality(QtCore.Qt.WindowModal)
        CreateProjectDialog.resize(514, 314)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(CreateProjectDialog)
        self.cancelOkButtonBox.setGeometry(QtCore.QRect(270, 220, 176, 31))
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.layoutWidget = QtGui.QWidget(CreateProjectDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(80, 20, 337, 136))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.splitter = QtGui.QSplitter(self.layoutWidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.FilePathLineEdit = QtGui.QLineEdit(self.splitter)
        self.FilePathLineEdit.setObjectName(_fromUtf8("FilePathLineEdit"))
        self.browseButton = QtGui.QPushButton(self.splitter)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.verticalLayout.addWidget(self.splitter)
        self.showFileInfoButton = QtGui.QPushButton(self.layoutWidget)
        self.showFileInfoButton.setObjectName(_fromUtf8("showFileInfoButton"))
        self.verticalLayout.addWidget(self.showFileInfoButton)

        self.retranslateUi(CreateProjectDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CreateProjectDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CreateProjectDialog.reject)
        #QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CreateProjectDialog.openFileChooserDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateProjectDialog)

    def retranslateUi(self, CreateProjectDialog):
        CreateProjectDialog.setWindowTitle(_translate("CreateProjectDialog", "Create new project", None))
        self.label.setText(_translate("CreateProjectDialog", "***project created in the same folder as picked file", None))
        self.browseButton.setText(_translate("CreateProjectDialog", "Browse...", None))
        self.showFileInfoButton.setText(_translate("CreateProjectDialog", "Show file info", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    CreateProjectDialog = QtGui.QDialog()
    ui = Ui_CreateProjectDialog()
    ui.setupUi(CreateProjectDialog)
    CreateProjectDialog.show()
    sys.exit(app.exec_())
