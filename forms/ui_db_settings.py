# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_db_settings.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QGridLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_DB_Settings(object):
    def setupUi(self, DB_Settings):
        if not DB_Settings.objectName():
            DB_Settings.setObjectName(u"DB_Settings")
        DB_Settings.resize(422, 157)
        DB_Settings.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.gridLayout = QGridLayout(DB_Settings)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.db_list = QComboBox(DB_Settings)
        self.db_list.setObjectName(u"db_list")
        self.db_list.setMinimumSize(QSize(150, 0))
        self.db_list.setMaximumSize(QSize(250, 16777215))
        self.db_list.setStyleSheet(u"color: white")

        self.verticalLayout.addWidget(self.db_list)

        self.textEdit = QTextEdit(DB_Settings)
        self.textEdit.setObjectName(u"textEdit")

        self.verticalLayout.addWidget(self.textEdit)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.connectButton = QPushButton(DB_Settings)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setStyleSheet(u"color: white")

        self.horizontalLayout.addWidget(self.connectButton)

        self.cancelButton = QPushButton(DB_Settings)
        self.cancelButton.setObjectName(u"cancelButton")
        self.cancelButton.setStyleSheet(u"color: white")

        self.horizontalLayout.addWidget(self.cancelButton)


        self.gridLayout.addLayout(self.horizontalLayout, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer_2, 1, 0, 1, 1)


        self.retranslateUi(DB_Settings)

        QMetaObject.connectSlotsByName(DB_Settings)
    # setupUi

    def retranslateUi(self, DB_Settings):
        DB_Settings.setWindowTitle(QCoreApplication.translate("DB_Settings", u"Choose database tablename", None))
        self.connectButton.setText(QCoreApplication.translate("DB_Settings", u"Connect", None))
        self.cancelButton.setText(QCoreApplication.translate("DB_Settings", u"Cancel", None))
    # retranslateUi

