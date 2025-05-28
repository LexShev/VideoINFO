# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_allert.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect)
from PySide6.QtGui import (QFont, QPixmap)
from PySide6.QtWidgets import (QLabel, QVBoxLayout, QWidget)


class Ui_AlertDialog(object):
    def setupUi(self, AlertDialog):
        if not AlertDialog.objectName():
            AlertDialog.setObjectName(u"AlertDialog")
        AlertDialog.resize(393, 99)
        AlertDialog.setWindowOpacity(0.900000000000000)
        AlertDialog.setStyleSheet(u"background-color: rgb(65, 65, 70);\n"
"color: white;\n"
"font-family: Noto Sans;\n"
"")
        self.alert_logo = QLabel(AlertDialog)
        self.alert_logo.setObjectName(u"alert_logo")
        self.alert_logo.setGeometry(QRect(20, 20, 55, 55))
        self.alert_logo.setStyleSheet(u"color: rgb(255, 255, 255);\n"
"background-color:rgba(195,75,60,255);\n"
"border-radius: 3px\n"
"\n"
"\n"
"")
        self.alert_logo.setPixmap(QPixmap(u":/wt_img/icons/WT_60x48_problem_FILL0_wght400_GRAD0_opsz24.svg"))
        self.alert_logo.setScaledContents(True)
        self.widget = QWidget(AlertDialog)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(100, 20, 261, 54))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.alert_header = QLabel(self.widget)
        self.alert_header.setObjectName(u"alert_header")
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setPointSize(14)
        self.alert_header.setFont(font)

        self.verticalLayout.addWidget(self.alert_header)

        self.alert_paragraph = QLabel(self.widget)
        self.alert_paragraph.setObjectName(u"alert_paragraph")
        font1 = QFont()
        font1.setFamilies([u"Noto Sans"])
        font1.setPointSize(11)
        self.alert_paragraph.setFont(font1)
        self.alert_paragraph.setWordWrap(True)

        self.verticalLayout.addWidget(self.alert_paragraph)


        self.retranslateUi(AlertDialog)

        QMetaObject.connectSlotsByName(AlertDialog)
    # setupUi

    def retranslateUi(self, AlertDialog):
        AlertDialog.setWindowTitle(QCoreApplication.translate("AlertDialog", u"Dialog", None))
        self.alert_logo.setText("")
        self.alert_header.setText(QCoreApplication.translate("AlertDialog", u"\u0412 \u0440\u0430\u0431\u043e\u0442\u0435", None))
        self.alert_paragraph.setText(QCoreApplication.translate("AlertDialog", u"\u0417\u0430\u043f\u0443\u0449\u0435\u043d\u043e \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
    # retranslateUi

