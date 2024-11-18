# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_db_editor.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QGridLayout,
    QHeaderView, QPushButton, QSizePolicy, QSpacerItem,
    QSplitter, QTableView, QTextBrowser, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_db_editor(object):
    def setupUi(self, db_editor):
        if not db_editor.objectName():
            db_editor.setObjectName(u"db_editor")
        db_editor.resize(1156, 852)
        db_editor.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.gridLayout_2 = QGridLayout(db_editor)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.splitter = QSplitter(db_editor)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.tableView = QTableView(self.splitter)
        self.tableView.setObjectName(u"tableView")
        self.splitter.addWidget(self.tableView)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.textBrowser = QTextBrowser(self.frame)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 0, 1, 1, 1)

        self.textEdit = QTextEdit(self.frame)
        self.textEdit.setObjectName(u"textEdit")

        self.gridLayout.addWidget(self.textEdit, 1, 1, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.openDB = QPushButton(self.frame)
        self.openDB.setObjectName(u"openDB")
        self.openDB.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.openDB)

        self.closeDB = QPushButton(self.frame)
        self.closeDB.setObjectName(u"closeDB")
        self.closeDB.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.closeDB)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.frame)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self.frame)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self.frame)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_5)

        self.pushButton_6 = QPushButton(self.frame)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_6)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.pushButton_7 = QPushButton(self.frame)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_7)

        self.pushButton_9 = QPushButton(self.frame)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_9)

        self.pushButton_8 = QPushButton(self.frame)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_8)

        self.pushButton_10 = QPushButton(self.frame)
        self.pushButton_10.setObjectName(u"pushButton_10")
        self.pushButton_10.setStyleSheet(u"color: white;")

        self.verticalLayout.addWidget(self.pushButton_10)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 2, 1)

        self.splitter.addWidget(self.frame)

        self.gridLayout_2.addWidget(self.splitter, 0, 0, 1, 1)


        self.retranslateUi(db_editor)

        QMetaObject.connectSlotsByName(db_editor)
    # setupUi

    def retranslateUi(self, db_editor):
        db_editor.setWindowTitle(QCoreApplication.translate("db_editor", u"DB Editor", None))
        self.openDB.setText(QCoreApplication.translate("db_editor", u"\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0438\u0442\u044c\u0441\u044f \u043a \u0411\u0414", None))
        self.closeDB.setText(QCoreApplication.translate("db_editor", u"\u0417\u0430\u043a\u0440\u044b\u0442\u044c \u0441\u043e\u0435\u0434\u0438\u043d\u0435\u043d\u0438\u0435 \u0441 \u0411\u0414", None))
        self.pushButton.setText(QCoreApplication.translate("db_editor", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.pushButton_2.setText(QCoreApplication.translate("db_editor", u"\u0412\u043d\u0435\u0441\u0442\u0438 \u0441\u0442\u0440\u043e\u043a\u0443", None))
        self.pushButton_3.setText(QCoreApplication.translate("db_editor", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f", None))
        self.pushButton_4.setText(QCoreApplication.translate("db_editor", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043a\u043e\u043b\u043e\u043d\u043a\u0443", None))
        self.pushButton_5.setText(QCoreApplication.translate("db_editor", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None))
        self.pushButton_6.setText(QCoreApplication.translate("db_editor", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u0432\u0441\u0435\u0445 \u043a\u043e\u043b\u043e\u043d\u043e\u043a", None))
        self.pushButton_7.setText(QCoreApplication.translate("db_editor", u"\u0414\u0443\u0431\u043b\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.pushButton_9.setText(QCoreApplication.translate("db_editor", u"\u0421\u043e\u0437\u0434\u0430\u0442\u044c \u043d\u043e\u0432\u0443\u044e \u043a\u043d\u0438\u0433\u0443", None))
        self.pushButton_8.setText(QCoreApplication.translate("db_editor", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445", None))
        self.pushButton_10.setText(QCoreApplication.translate("db_editor", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445", None))
    # retranslateUi

