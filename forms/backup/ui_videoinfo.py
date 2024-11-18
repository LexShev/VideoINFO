# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_videoinfo.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QSizePolicy, QSpacerItem, QSplitter,
    QTableWidget, QTableWidgetItem, QToolButton, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1400, 870)
        icon = QIcon()
        icon.addFile(u":/logo/icons/LOGO_VideoInfo_450x450_Sh.svg", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.buttons = QFrame(self.centralwidget)
        self.buttons.setObjectName(u"buttons")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons.sizePolicy().hasHeightForWidth())
        self.buttons.setSizePolicy(sizePolicy)
        self.buttons.setMinimumSize(QSize(46, 0))
        self.buttons.setMaximumSize(QSize(46, 16777215))
        self.buttons.setBaseSize(QSize(46, 0))
        self.buttons.setStyleSheet(u"color: rgb(146, 146, 146);\n"
"border: 0px;")
        self.buttons.setFrameShape(QFrame.Box)
        self.buttons.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.buttons)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(3, 30, 3, 3)
        self.playButton = QToolButton(self.buttons)
        self.playButton.setObjectName(u"playButton")
        self.playButton.setMinimumSize(QSize(40, 30))
        self.playButton.setMaximumSize(QSize(40, 30))
        self.playButton.setBaseSize(QSize(40, 30))
        self.playButton.setStyleSheet(u"QToolButton{\n"
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
        icon1 = QIcon()
        icon1.addFile(u":/wt_img/icons/WT_play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.playButton, 2, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout.addItem(self.verticalSpacer, 9, 0, 1, 1)

        self.queueButton = QToolButton(self.buttons)
        self.queueButton.setObjectName(u"queueButton")
        self.queueButton.setMinimumSize(QSize(40, 30))
        self.queueButton.setMaximumSize(QSize(40, 30))
        self.queueButton.setBaseSize(QSize(40, 30))
        self.queueButton.setStyleSheet(u"QToolButton{\n"
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
        icon2 = QIcon()
        icon2.addFile(u":/wt_img/icons/WT_playlist_play_FILL0_wght400_GRAD0_opsz24 copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.queueButton.setIcon(icon2)
        self.queueButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.queueButton, 5, 0, 1, 1)

        self.slncDtctButton = QToolButton(self.buttons)
        self.slncDtctButton.setObjectName(u"slncDtctButton")
        self.slncDtctButton.setMinimumSize(QSize(40, 30))
        self.slncDtctButton.setMaximumSize(QSize(40, 30))
        self.slncDtctButton.setBaseSize(QSize(40, 30))
        self.slncDtctButton.setStyleSheet(u"QToolButton{\n"
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
        icon3 = QIcon()
        icon3.addFile(u":/wt_img/icons/WT_queue_music_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.slncDtctButton.setIcon(icon3)
        self.slncDtctButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.slncDtctButton, 7, 0, 1, 1)

        self.exportButton = QToolButton(self.buttons)
        self.exportButton.setObjectName(u"exportButton")
        self.exportButton.setMinimumSize(QSize(40, 30))
        self.exportButton.setMaximumSize(QSize(40, 30))
        self.exportButton.setBaseSize(QSize(40, 30))
        self.exportButton.setStyleSheet(u"QToolButton{\n"
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
        icon4 = QIcon()
        icon4.addFile(u":/wt_img/icons/WT_upgrade_FILL0_wght400_GRAD0_opsz24 copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportButton.setIcon(icon4)
        self.exportButton.setIconSize(QSize(20, 35))
        self.exportButton.setAutoRaise(False)

        self.gridLayout.addWidget(self.exportButton, 8, 0, 1, 1)

        self.settingsButton = QToolButton(self.buttons)
        self.settingsButton.setObjectName(u"settingsButton")
        self.settingsButton.setMinimumSize(QSize(40, 30))
        self.settingsButton.setMaximumSize(QSize(40, 30))
        self.settingsButton.setBaseSize(QSize(40, 30))
        self.settingsButton.setStyleSheet(u"QToolButton{\n"
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
        icon5 = QIcon()
        icon5.addFile(u":/wt_img/icons/WT_settings_FILL0_wght400_GRAD0_opsz24 copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsButton.setIcon(icon5)
        self.settingsButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.settingsButton, 10, 0, 1, 1)

        self.wfrmButton = QToolButton(self.buttons)
        self.wfrmButton.setObjectName(u"wfrmButton")
        self.wfrmButton.setMinimumSize(QSize(40, 30))
        self.wfrmButton.setMaximumSize(QSize(40, 30))
        self.wfrmButton.setBaseSize(QSize(40, 30))
        self.wfrmButton.setStyleSheet(u"QToolButton{\n"
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
        icon6 = QIcon()
        icon6.addFile(u":/wt_img/icons/WT_equalizer_FILL0_wght400_GRAD0_opsz24 copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.wfrmButton.setIcon(icon6)
        self.wfrmButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.wfrmButton, 4, 0, 1, 1)

        self.blckDtctButton = QToolButton(self.buttons)
        self.blckDtctButton.setObjectName(u"blckDtctButton")
        self.blckDtctButton.setMinimumSize(QSize(40, 30))
        self.blckDtctButton.setMaximumSize(QSize(40, 30))
        self.blckDtctButton.setBaseSize(QSize(40, 30))
        self.blckDtctButton.setStyleSheet(u"QToolButton{\n"
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
        icon7 = QIcon()
        icon7.addFile(u":/wt_img/icons/WT_remove_from_queue_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blckDtctButton.setIcon(icon7)
        self.blckDtctButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.blckDtctButton, 6, 0, 1, 1)

        self.openButton = QToolButton(self.buttons)
        self.openButton.setObjectName(u"openButton")
        self.openButton.setMinimumSize(QSize(40, 30))
        self.openButton.setMaximumSize(QSize(40, 30))
        self.openButton.setBaseSize(QSize(40, 30))
        self.openButton.setStyleSheet(u"QToolButton{\n"
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
        icon8 = QIcon()
        icon8.addFile(u":/wt_img/icons/WT_folder_open_FILL0_wght400_GRAD0_opsz24 copy.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.openButton.setIcon(icon8)
        self.openButton.setIconSize(QSize(20, 35))
        self.openButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.gridLayout.addWidget(self.openButton, 3, 0, 1, 1)

        self.delButton = QToolButton(self.buttons)
        self.delButton.setObjectName(u"delButton")
        self.delButton.setMinimumSize(QSize(40, 30))
        self.delButton.setMaximumSize(QSize(40, 30))
        self.delButton.setBaseSize(QSize(40, 30))
        self.delButton.setStyleSheet(u"QToolButton{\n"
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
        icon9 = QIcon()
        icon9.addFile(u":/wt_img/icons/WT_remove_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.delButton.setIcon(icon9)
        self.delButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.delButton, 1, 0, 1, 1)

        self.addButton = QToolButton(self.buttons)
        self.addButton.setObjectName(u"addButton")
        self.addButton.setMinimumSize(QSize(40, 30))
        self.addButton.setMaximumSize(QSize(40, 30))
        self.addButton.setBaseSize(QSize(40, 30))
        self.addButton.setStyleSheet(u"QToolButton{\n"
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
        icon10 = QIcon()
        icon10.addFile(u":/wt_img/icons/WT_add_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addButton.setIcon(icon10)
        self.addButton.setIconSize(QSize(20, 35))

        self.gridLayout.addWidget(self.addButton, 0, 0, 1, 1)


        self.gridLayout_3.addWidget(self.buttons, 0, 0, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_01 = QTableWidget(self.layoutWidget)
        if (self.tableWidget_01.columnCount() < 21):
            self.tableWidget_01.setColumnCount(21)
        self.tableWidget_01.setObjectName(u"tableWidget_01")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tableWidget_01.sizePolicy().hasHeightForWidth())
        self.tableWidget_01.setSizePolicy(sizePolicy1)
        self.tableWidget_01.setMinimumSize(QSize(800, 400))
        self.tableWidget_01.setBaseSize(QSize(800, 320))
        self.tableWidget_01.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_01.setDragEnabled(True)
        self.tableWidget_01.setDragDropOverwriteMode(False)
        self.tableWidget_01.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.tableWidget_01.setAlternatingRowColors(False)
        self.tableWidget_01.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_01.setGridStyle(Qt.SolidLine)
        self.tableWidget_01.setSortingEnabled(True)
        self.tableWidget_01.setColumnCount(21)
        self.tableWidget_01.horizontalHeader().setMinimumSectionSize(60)
        self.tableWidget_01.verticalHeader().setVisible(False)
        self.tableWidget_01.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_4.addWidget(self.tableWidget_01)

        self.frame_wave = QFrame(self.layoutWidget)
        self.frame_wave.setObjectName(u"frame_wave")
        self.frame_wave.setStyleSheet(u"QFrame#frame_wave{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_wave.setFrameShape(QFrame.StyledPanel)
        self.frame_wave.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_wave)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.resizeButtonDown = QToolButton(self.frame_wave)
        self.resizeButtonDown.setObjectName(u"resizeButtonDown")
        icon11 = QIcon()
        icon11.addFile(u":/bl_img/icons/expand_more_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resizeButtonDown.setIcon(icon11)

        self.verticalLayout_2.addWidget(self.resizeButtonDown, 0, Qt.AlignHCenter)

        self.wave_view = QLabel(self.frame_wave)
        self.wave_view.setObjectName(u"wave_view")
        sizePolicy1.setHeightForWidth(self.wave_view.sizePolicy().hasHeightForWidth())
        self.wave_view.setSizePolicy(sizePolicy1)
        self.wave_view.setMinimumSize(QSize(800, 320))
        self.wave_view.setMaximumSize(QSize(16777215, 500))
        self.wave_view.setBaseSize(QSize(250, 320))
        self.wave_view.setTextFormat(Qt.AutoText)
        self.wave_view.setPixmap(QPixmap(u":/imgs/img/WaveForm_04.png"))
        self.wave_view.setScaledContents(True)
        self.wave_view.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.wave_view)

        self.r128_loudness = QLabel(self.frame_wave)
        self.r128_loudness.setObjectName(u"r128_loudness")
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setPointSize(15)
        self.r128_loudness.setFont(font)
        self.r128_loudness.setStyleSheet(u"color: white;\n"
"background-color: rgba(146, 146, 146, 146);\n"
"margin: 4px;")

        self.verticalLayout_2.addWidget(self.r128_loudness, 0, Qt.AlignHCenter)

        self.resizeButtonUp = QToolButton(self.frame_wave)
        self.resizeButtonUp.setObjectName(u"resizeButtonUp")
        self.resizeButtonUp.setStyleSheet(u"")
        icon12 = QIcon()
        icon12.addFile(u":/bl_img/icons/expand_less_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resizeButtonUp.setIcon(icon12)

        self.verticalLayout_2.addWidget(self.resizeButtonUp, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addWidget(self.frame_wave)

        self.splitter.addWidget(self.layoutWidget)
        self.main_frame_tbl_02 = QFrame(self.splitter)
        self.main_frame_tbl_02.setObjectName(u"main_frame_tbl_02")
        self.main_frame_tbl_02.setMinimumSize(QSize(370, 0))
        self.main_frame_tbl_02.setMaximumSize(QSize(450, 16777215))
        self.main_frame_tbl_02.setStyleSheet(u"QFrame#main_frame_tbl_02{\n"
"	color: white;\n"
"	border: none;\n"
"}")
        self.main_frame_tbl_02.setFrameShape(QFrame.StyledPanel)
        self.main_frame_tbl_02.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_frame_tbl_02)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 1, 0, 0)
        self.frame_tags = QFrame(self.main_frame_tbl_02)
        self.frame_tags.setObjectName(u"frame_tags")
        self.frame_tags.setStyleSheet(u"QFrame#frame_tags{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_2 = QGridLayout(self.frame_tags)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SetMaximumSize)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setVerticalSpacing(2)
        self.gridLayout_2.setContentsMargins(6, 6, 6, 6)
        self.tag_v1_r_frame_rate = QLabel(self.frame_tags)
        self.tag_v1_r_frame_rate.setObjectName(u"tag_v1_r_frame_rate")
        self.tag_v1_r_frame_rate.setStyleSheet(u"color: white")

        self.gridLayout_2.addWidget(self.tag_v1_r_frame_rate, 2, 3, 1, 1)

        self.tag_resolution = QLabel(self.frame_tags)
        self.tag_resolution.setObjectName(u"tag_resolution")
        self.tag_resolution.setStyleSheet(u"color: white")

        self.gridLayout_2.addWidget(self.tag_resolution, 2, 4, 1, 1)

        self.S1 = QLabel(self.frame_tags)
        self.S1.setObjectName(u"S1")
        self.S1.setStyleSheet(u"color: white")

        self.gridLayout_2.addWidget(self.S1, 5, 0, 1, 1)

        self.tag_s2_title = QLabel(self.frame_tags)
        self.tag_s2_title.setObjectName(u"tag_s2_title")
        self.tag_s2_title.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_s2_title, 6, 1, 1, 3)

        self.tag_a1_channel_layout = QLabel(self.frame_tags)
        self.tag_a1_channel_layout.setObjectName(u"tag_a1_channel_layout")
        self.tag_a1_channel_layout.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a1_channel_layout, 3, 4, 1, 1)

        self.tag_file_path = QLabel(self.frame_tags)
        self.tag_file_path.setObjectName(u"tag_file_path")
        sizePolicy1.setHeightForWidth(self.tag_file_path.sizePolicy().hasHeightForWidth())
        self.tag_file_path.setSizePolicy(sizePolicy1)
        self.tag_file_path.setStyleSheet(u"color: rgb(146, 146, 146)")
        self.tag_file_path.setWordWrap(True)

        self.gridLayout_2.addWidget(self.tag_file_path, 1, 0, 1, 5, Qt.AlignTop)

        self.tag_a1_codec_name = QLabel(self.frame_tags)
        self.tag_a1_codec_name.setObjectName(u"tag_a1_codec_name")
        self.tag_a1_codec_name.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a1_codec_name, 3, 1, 1, 2)

        self.S2 = QLabel(self.frame_tags)
        self.S2.setObjectName(u"S2")
        self.S2.setStyleSheet(u"color: white")

        self.gridLayout_2.addWidget(self.S2, 6, 0, 1, 1)

        self.tag_s1_title = QLabel(self.frame_tags)
        self.tag_s1_title.setObjectName(u"tag_s1_title")
        self.tag_s1_title.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_s1_title, 5, 1, 1, 3)

        self.tag_v1_codec_name = QLabel(self.frame_tags)
        self.tag_v1_codec_name.setObjectName(u"tag_v1_codec_name")
        self.tag_v1_codec_name.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_v1_codec_name, 2, 1, 1, 1)

        self.tag_s1_language = QLabel(self.frame_tags)
        self.tag_s1_language.setObjectName(u"tag_s1_language")
        self.tag_s1_language.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_s1_language, 5, 4, 1, 1)

        self.tag_duration = QLabel(self.frame_tags)
        self.tag_duration.setObjectName(u"tag_duration")
        self.tag_duration.setStyleSheet(u"color: white")

        self.gridLayout_2.addWidget(self.tag_duration, 0, 4, 1, 1, Qt.AlignRight|Qt.AlignTop)

        self.tag_s2_language = QLabel(self.frame_tags)
        self.tag_s2_language.setObjectName(u"tag_s2_language")
        self.tag_s2_language.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_s2_language, 6, 4, 1, 1)

        self.tag_file_name = QLabel(self.frame_tags)
        self.tag_file_name.setObjectName(u"tag_file_name")
        self.tag_file_name.setStyleSheet(u"color: white")
        self.tag_file_name.setWordWrap(True)

        self.gridLayout_2.addWidget(self.tag_file_name, 0, 0, 1, 4)

        self.tag_a2_sample_rate = QLabel(self.frame_tags)
        self.tag_a2_sample_rate.setObjectName(u"tag_a2_sample_rate")
        self.tag_a2_sample_rate.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a2_sample_rate, 4, 3, 1, 1)

        self.tag_v1_profile = QLabel(self.frame_tags)
        self.tag_v1_profile.setObjectName(u"tag_v1_profile")
        self.tag_v1_profile.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_v1_profile, 2, 2, 1, 1)

        self.A2 = QLabel(self.frame_tags)
        self.A2.setObjectName(u"A2")
        self.A2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.A2, 4, 0, 1, 1)

        self.A1 = QLabel(self.frame_tags)
        self.A1.setObjectName(u"A1")
        self.A1.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.A1, 3, 0, 1, 1)

        self.tag_a1_sample_rate = QLabel(self.frame_tags)
        self.tag_a1_sample_rate.setObjectName(u"tag_a1_sample_rate")
        self.tag_a1_sample_rate.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a1_sample_rate, 3, 3, 1, 1)

        self.tag_a2_channel_layout = QLabel(self.frame_tags)
        self.tag_a2_channel_layout.setObjectName(u"tag_a2_channel_layout")
        self.tag_a2_channel_layout.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a2_channel_layout, 4, 4, 1, 1)

        self.V1 = QLabel(self.frame_tags)
        self.V1.setObjectName(u"V1")
        self.V1.setStyleSheet(u"color: white\n"
"")

        self.gridLayout_2.addWidget(self.V1, 2, 0, 1, 1)

        self.tag_a2_codec_name = QLabel(self.frame_tags)
        self.tag_a2_codec_name.setObjectName(u"tag_a2_codec_name")
        self.tag_a2_codec_name.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.tag_a2_codec_name, 4, 1, 1, 2)

        self.gridLayout_2.setColumnStretch(1, 1)
        self.gridLayout_2.setColumnStretch(2, 2)
        self.gridLayout_2.setColumnStretch(3, 2)
        self.gridLayout_2.setColumnStretch(4, 2)

        self.verticalLayout.addWidget(self.frame_tags)

        self.frame_tbl_02 = QFrame(self.main_frame_tbl_02)
        self.frame_tbl_02.setObjectName(u"frame_tbl_02")
        self.frame_tbl_02.setStyleSheet(u"QFrame#frame_tbl_02{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.verticalLayout_3 = QVBoxLayout(self.frame_tbl_02)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetMaximumSize)
        self.verticalLayout_3.setContentsMargins(6, 6, 6, 6)
        self.label_8 = QLabel(self.frame_tbl_02)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setStyleSheet(u"color: white")

        self.verticalLayout_3.addWidget(self.label_8)

        self.tableWidget_02 = QTableWidget(self.frame_tbl_02)
        if (self.tableWidget_02.columnCount() < 2):
            self.tableWidget_02.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_02.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_02.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tableWidget_02.setObjectName(u"tableWidget_02")
        self.tableWidget_02.setStyleSheet(u"border: 0px")
        self.tableWidget_02.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget_02.setShowGrid(False)
        self.tableWidget_02.setGridStyle(Qt.CustomDashLine)
        self.tableWidget_02.setCornerButtonEnabled(False)
        self.tableWidget_02.horizontalHeader().setVisible(False)
        self.tableWidget_02.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget_02.verticalHeader().setVisible(False)

        self.verticalLayout_3.addWidget(self.tableWidget_02)


        self.verticalLayout.addWidget(self.frame_tbl_02)

        self.splitter.addWidget(self.main_frame_tbl_02)

        self.gridLayout_3.addWidget(self.splitter, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"VideoINFO", None))
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.queueButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.slncDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
        self.wfrmButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.blckDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.delButton.setText(QCoreApplication.translate("MainWindow", u"Del", None))
#if QT_CONFIG(tooltip)
        self.addButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.addButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
        self.resizeButtonDown.setText("")
        self.wave_view.setText("")
        self.r128_loudness.setText(QCoreApplication.translate("MainWindow", u"LOUDNESS METER", None))
        self.resizeButtonUp.setText(QCoreApplication.translate("MainWindow", u"switch", None))
        self.tag_v1_r_frame_rate.setText(QCoreApplication.translate("MainWindow", u"fps", None))
        self.tag_resolution.setText(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.S1.setText(QCoreApplication.translate("MainWindow", u"S1", None))
        self.tag_s2_title.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.tag_a1_channel_layout.setText(QCoreApplication.translate("MainWindow", u"Ch", None))
        self.tag_file_path.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Path</p><p><br/></p></body></html>", None))
        self.tag_a1_codec_name.setText(QCoreApplication.translate("MainWindow", u"Audio codec", None))
        self.S2.setText(QCoreApplication.translate("MainWindow", u"S2", None))
        self.tag_s1_title.setText(QCoreApplication.translate("MainWindow", u"Title", None))
        self.tag_v1_codec_name.setText(QCoreApplication.translate("MainWindow", u"Codec", None))
        self.tag_s1_language.setText(QCoreApplication.translate("MainWindow", u"Lang", None))
        self.tag_duration.setText(QCoreApplication.translate("MainWindow", u"Duration", None))
        self.tag_s2_language.setText(QCoreApplication.translate("MainWindow", u"Lang", None))
        self.tag_file_name.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Filename</p><p><br/></p></body></html>", None))
        self.tag_a2_sample_rate.setText(QCoreApplication.translate("MainWindow", u"Sample rate", None))
        self.tag_v1_profile.setText(QCoreApplication.translate("MainWindow", u"Profile", None))
        self.A2.setText(QCoreApplication.translate("MainWindow", u"A2", None))
        self.A1.setText(QCoreApplication.translate("MainWindow", u"A1", None))
        self.tag_a1_sample_rate.setText(QCoreApplication.translate("MainWindow", u"Sample rate", None))
        self.tag_a2_channel_layout.setText(QCoreApplication.translate("MainWindow", u"Ch", None))
        self.V1.setText(QCoreApplication.translate("MainWindow", u"V1", None))
        self.tag_a2_codec_name.setText(QCoreApplication.translate("MainWindow", u"Audio codec", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Details", None))
        ___qtablewidgetitem = self.tableWidget_02.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Header", None));
        ___qtablewidgetitem1 = self.tableWidget_02.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Data", None));
    # retranslateUi

