# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_confirm_action.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QWidget)

class Ui_ConfirmDialog(object):
    def setupUi(self, ConfirmDialog):
        if not ConfirmDialog.objectName():
            ConfirmDialog.setObjectName(u"ConfirmDialog")
        ConfirmDialog.resize(476, 143)
        ConfirmDialog.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.gridLayout_2 = QGridLayout(ConfirmDialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.yesButton = QPushButton(ConfirmDialog)
        self.yesButton.setObjectName(u"yesButton")
        self.yesButton.setStyleSheet(u"color: white")

        self.horizontalLayout.addWidget(self.yesButton)

        self.cancelButton = QPushButton(ConfirmDialog)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setStyleSheet(u"color: white")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.conf_label = QLabel(ConfirmDialog)
        self.conf_label.setObjectName(u"conf_label")
        self.conf_label.setStyleSheet(u"color: white")

        self.gridLayout.addWidget(self.conf_label, 1, 0, 1, 2, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 2, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 0, 0, 1, 2)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.retranslateUi(ConfirmDialog)

        QMetaObject.connectSlotsByName(ConfirmDialog)
    # setupUi

    def retranslateUi(self, ConfirmDialog):
        ConfirmDialog.setWindowTitle(QCoreApplication.translate("ConfirmDialog", u"Confirm the action", None))
        self.yesButton.setText(QCoreApplication.translate("ConfirmDialog", u"Yes", None))
        self.cancelButton.setText(QCoreApplication.translate("ConfirmDialog", u"Cancel", None))
        self.conf_label.setText(QCoreApplication.translate("ConfirmDialog", u"\u0421onfirm the action", None))
    # retranslateUi

