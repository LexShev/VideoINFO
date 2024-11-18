# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_videoinfo_player.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QSizePolicy, QSpacerItem, QSplitter, QTableWidget,
    QTableWidgetItem, QToolButton, QVBoxLayout, QWidget)
import icons_rc

class Ui_BlckSlncDialog(object):
    def setupUi(self, BlckSlncDialog):
        if not BlckSlncDialog.objectName():
            BlckSlncDialog.setObjectName(u"BlckSlncDialog")
        BlckSlncDialog.resize(1003, 606)
        BlckSlncDialog.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.gridLayout_3 = QGridLayout(BlckSlncDialog)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.splitter = QSplitter(BlckSlncDialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.frame_tables = QFrame(self.splitter)
        self.frame_tables.setObjectName(u"frame_tables")
        self.frame_tables.setStyleSheet(u"QFrame#frame_tables{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_tables.setFrameShape(QFrame.StyledPanel)
        self.frame_tables.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_tables)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label = QLabel(self.frame_tables)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 25))
        self.label.setStyleSheet(u"color: white")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label)

        self.blck_table = QTableWidget(self.frame_tables)
        if (self.blck_table.columnCount() < 3):
            self.blck_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.blck_table.setObjectName(u"blck_table")
        self.blck_table.setMinimumSize(QSize(0, 250))
        self.blck_table.setMaximumSize(QSize(280, 350))
        self.blck_table.setStyleSheet(u"border: none")
        self.blck_table.setAlternatingRowColors(True)
        self.blck_table.setShowGrid(False)
        self.blck_table.setCornerButtonEnabled(False)
        self.blck_table.setColumnCount(3)
        self.blck_table.horizontalHeader().setMinimumSectionSize(30)
        self.blck_table.horizontalHeader().setDefaultSectionSize(80)
        self.blck_table.verticalHeader().setVisible(False)
        self.blck_table.verticalHeader().setDefaultSectionSize(24)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.blck_table)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout_2.setItem(2, QFormLayout.FieldRole, self.verticalSpacer_3)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.frame_tables)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 25))
        self.label_2.setStyleSheet(u"color: white")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.slnc_table = QTableWidget(self.frame_tables)
        if (self.slnc_table.columnCount() < 3):
            self.slnc_table.setColumnCount(3)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.slnc_table.setObjectName(u"slnc_table")
        self.slnc_table.setMinimumSize(QSize(260, 0))
        self.slnc_table.setMaximumSize(QSize(280, 350))
        self.slnc_table.setStyleSheet(u"border: none")
        self.slnc_table.setAlternatingRowColors(True)
        self.slnc_table.setShowGrid(False)
        self.slnc_table.setCornerButtonEnabled(False)
        self.slnc_table.setColumnCount(3)
        self.slnc_table.horizontalHeader().setDefaultSectionSize(80)
        self.slnc_table.verticalHeader().setVisible(False)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.slnc_table)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(2, QFormLayout.FieldRole, self.verticalSpacer_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.splitter.addWidget(self.frame_tables)
        self.frame_videoplayer = QFrame(self.splitter)
        self.frame_videoplayer.setObjectName(u"frame_videoplayer")
        self.frame_videoplayer.setStyleSheet(u"QFrame#frame_videoplayer{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_videoplayer.setFrameShape(QFrame.StyledPanel)
        self.frame_videoplayer.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.frame_videoplayer)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_3 = QLabel(self.frame_videoplayer)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(100, 25))
        self.label_3.setStyleSheet(u"color: white")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1, Qt.AlignLeft)

        self.label_4 = QLabel(self.frame_videoplayer)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(0, 25))
        self.label_4.setMaximumSize(QSize(150, 25))
        self.label_4.setStyleSheet(u"color: grey\n"
"")

        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1, Qt.AlignRight)

        self.video_player_img = QLabel(self.frame_videoplayer)
        self.video_player_img.setObjectName(u"video_player_img")
        self.video_player_img.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_player_img.sizePolicy().hasHeightForWidth())
        self.video_player_img.setSizePolicy(sizePolicy)
        self.video_player_img.setMinimumSize(QSize(500, 280))
        self.video_player_img.setMaximumSize(QSize(900, 400))
        self.video_player_img.setBaseSize(QSize(500, 280))
        self.video_player_img.setPixmap(QPixmap(u":/imgs/img/video_player.png"))
        self.video_player_img.setScaledContents(True)
        self.video_player_img.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.video_player_img.setWordWrap(False)
        self.video_player_img.setIndent(-1)

        self.gridLayout.addWidget(self.video_player_img, 1, 0, 1, 3, Qt.AlignHCenter)

        self.Buttons = QFrame(self.frame_videoplayer)
        self.Buttons.setObjectName(u"Buttons")
        self.Buttons.setMinimumSize(QSize(250, 50))
        self.Buttons.setMaximumSize(QSize(300, 60))
        self.Buttons.setStyleSheet(u"QToolButton{\n"
"	 color: rgb(255, 255, 255);\n"
"     background-color:rgba(255,255,255,30);\n"
"     border: 1px solid rgba(255,255,255,40);\n"
"     border-radius:3px;\n"
"}\n"
"QToolButton:hover{\n"
"background-color:rgba(255,255,255,50);\n"
"}\n"
"QToolButton:pressed{\n"
"background-color:rgba(255,255,255,70);\n"
"}")
        self.horizontalLayout = QHBoxLayout(self.Buttons)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.blck_openButton = QToolButton(self.Buttons)
        self.blck_openButton.setObjectName(u"blck_openButton")
        self.blck_openButton.setMinimumSize(QSize(40, 30))
        self.blck_openButton.setMaximumSize(QSize(40, 30))
        icon = QIcon()
        icon.addFile(u":/bl_img/icons/folder_open_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blck_openButton.setIcon(icon)
        self.blck_openButton.setIconSize(QSize(20, 30))

        self.horizontalLayout.addWidget(self.blck_openButton)

        self.blck_prevButton = QToolButton(self.Buttons)
        self.blck_prevButton.setObjectName(u"blck_prevButton")
        self.blck_prevButton.setMinimumSize(QSize(40, 30))
        self.blck_prevButton.setMaximumSize(QSize(40, 30))
        icon1 = QIcon()
        icon1.addFile(u":/bl_img/icons/skip_previous_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blck_prevButton.setIcon(icon1)
        self.blck_prevButton.setIconSize(QSize(20, 30))

        self.horizontalLayout.addWidget(self.blck_prevButton)

        self.blck_playButton = QToolButton(self.Buttons)
        self.blck_playButton.setObjectName(u"blck_playButton")
        self.blck_playButton.setMinimumSize(QSize(50, 38))
        self.blck_playButton.setMaximumSize(QSize(45, 35))
        icon2 = QIcon()
        icon2.addFile(u":/bl_img/icons/play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blck_playButton.setIcon(icon2)
        self.blck_playButton.setIconSize(QSize(25, 35))

        self.horizontalLayout.addWidget(self.blck_playButton)

        self.blck_nextButton = QToolButton(self.Buttons)
        self.blck_nextButton.setObjectName(u"blck_nextButton")
        self.blck_nextButton.setMinimumSize(QSize(40, 30))
        self.blck_nextButton.setMaximumSize(QSize(40, 30))
        icon3 = QIcon()
        icon3.addFile(u":/bl_img/icons/skip_next_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blck_nextButton.setIcon(icon3)
        self.blck_nextButton.setIconSize(QSize(20, 30))

        self.horizontalLayout.addWidget(self.blck_nextButton)

        self.blck_muteButton = QToolButton(self.Buttons)
        self.blck_muteButton.setObjectName(u"blck_muteButton")
        self.blck_muteButton.setMinimumSize(QSize(40, 30))
        self.blck_muteButton.setMaximumSize(QSize(40, 30))
        icon4 = QIcon()
        icon4.addFile(u":/bl_img/icons/no_sound_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blck_muteButton.setIcon(icon4)
        self.blck_muteButton.setIconSize(QSize(20, 30))

        self.horizontalLayout.addWidget(self.blck_muteButton)


        self.gridLayout.addWidget(self.Buttons, 2, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.splitter.addWidget(self.frame_videoplayer)

        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.video_player_img.setBuddy(self.Buttons)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(BlckSlncDialog)

        QMetaObject.connectSlotsByName(BlckSlncDialog)
    # setupUi

    def retranslateUi(self, BlckSlncDialog):
        BlckSlncDialog.setWindowTitle(QCoreApplication.translate("BlckSlncDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("BlckSlncDialog", u"Black detetct", None))
        ___qtablewidgetitem = self.blck_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("BlckSlncDialog", u"Start", None));
        ___qtablewidgetitem1 = self.blck_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("BlckSlncDialog", u"End", None));
        ___qtablewidgetitem2 = self.blck_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("BlckSlncDialog", u"Duration", None));
        self.label_2.setText(QCoreApplication.translate("BlckSlncDialog", u"Silence detetct", None))
        ___qtablewidgetitem3 = self.slnc_table.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("BlckSlncDialog", u"Start", None));
        ___qtablewidgetitem4 = self.slnc_table.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("BlckSlncDialog", u"End", None));
        ___qtablewidgetitem5 = self.slnc_table.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("BlckSlncDialog", u"Duration", None));
        self.label_3.setText(QCoreApplication.translate("BlckSlncDialog", u"Video preview", None))
        self.label_4.setText(QCoreApplication.translate("BlckSlncDialog", u"\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u0432 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0435", None))
        self.video_player_img.setText("")
        self.blck_openButton.setText(QCoreApplication.translate("BlckSlncDialog", u"...", None))
        self.blck_prevButton.setText(QCoreApplication.translate("BlckSlncDialog", u"...", None))
        self.blck_playButton.setText(QCoreApplication.translate("BlckSlncDialog", u"...", None))
        self.blck_nextButton.setText(QCoreApplication.translate("BlckSlncDialog", u"...", None))
        self.blck_muteButton.setText(QCoreApplication.translate("BlckSlncDialog", u"...", None))
    # retranslateUi

