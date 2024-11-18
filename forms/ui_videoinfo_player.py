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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QHeaderView,
    QLabel, QPushButton, QSizePolicy, QSlider,
    QSpacerItem, QTableWidget, QTableWidgetItem, QToolBox,
    QToolButton, QVBoxLayout, QWidget)
import icons_rc

class Ui_VideoINFO_Player(object):
    def setupUi(self, VideoINFO_Player):
        if not VideoINFO_Player.objectName():
            VideoINFO_Player.setObjectName(u"VideoINFO_Player")
        VideoINFO_Player.resize(1325, 901)
        VideoINFO_Player.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.gridLayout = QGridLayout(VideoINFO_Player)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.frame_tables = QFrame(VideoINFO_Player)
        self.frame_tables.setObjectName(u"frame_tables")
        self.frame_tables.setMinimumSize(QSize(300, 0))
        self.frame_tables.setStyleSheet(u"color: white;\n"
"QFrame#frame_tables{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_tables.setFrameShape(QFrame.StyledPanel)
        self.frame_tables.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_tables)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.toolBox = QToolBox(self.frame_tables)
        self.toolBox.setObjectName(u"toolBox")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.page.setGeometry(QRect(0, 0, 297, 768))
        self.gridLayout_6 = QGridLayout(self.page)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.blck_table = QTableWidget(self.page)
        if (self.blck_table.columnCount() < 7):
            self.blck_table.setColumnCount(7)
        __qtablewidgetitem = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.blck_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.blck_table.setObjectName(u"blck_table")
        self.blck_table.setMinimumSize(QSize(250, 0))
        self.blck_table.setMaximumSize(QSize(16777215, 16777215))
        self.blck_table.setBaseSize(QSize(250, 0))
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setUnderline(False)
        self.blck_table.setFont(font)
        self.blck_table.setStyleSheet(u"border: none;\n"
"color: rgb(138, 180, 247)")
        self.blck_table.setDragDropOverwriteMode(False)
        self.blck_table.setAlternatingRowColors(False)
        self.blck_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.blck_table.setShowGrid(False)
        self.blck_table.setCornerButtonEnabled(False)
        self.blck_table.setColumnCount(7)
        self.blck_table.horizontalHeader().setVisible(False)
        self.blck_table.horizontalHeader().setMinimumSectionSize(20)
        self.blck_table.horizontalHeader().setDefaultSectionSize(50)
        self.blck_table.horizontalHeader().setHighlightSections(False)
        self.blck_table.verticalHeader().setVisible(False)

        self.gridLayout_6.addWidget(self.blck_table, 0, 0, 1, 1)

        self.toolBox.addItem(self.page, u"Black detection")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 297, 768))
        self.gridLayout_5 = QGridLayout(self.page_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.slnc_table = QTableWidget(self.page_2)
        if (self.slnc_table.columnCount() < 7):
            self.slnc_table.setColumnCount(7)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.slnc_table.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        self.slnc_table.setObjectName(u"slnc_table")
        self.slnc_table.setMinimumSize(QSize(250, 0))
        self.slnc_table.setMaximumSize(QSize(16777215, 16777215))
        self.slnc_table.setFont(font)
        self.slnc_table.setStyleSheet(u"border: none;\n"
"color: rgb(138, 180, 247)")
        self.slnc_table.setAlternatingRowColors(False)
        self.slnc_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.slnc_table.setShowGrid(False)
        self.slnc_table.setCornerButtonEnabled(False)
        self.slnc_table.setColumnCount(7)
        self.slnc_table.horizontalHeader().setVisible(False)
        self.slnc_table.horizontalHeader().setMinimumSectionSize(20)
        self.slnc_table.horizontalHeader().setDefaultSectionSize(50)
        self.slnc_table.horizontalHeader().setHighlightSections(False)
        self.slnc_table.verticalHeader().setVisible(False)

        self.gridLayout_5.addWidget(self.slnc_table, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_2, u"Silence detection")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 297, 768))
        self.gridLayout_4 = QGridLayout(self.page_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frz_table = QTableWidget(self.page_3)
        if (self.frz_table.columnCount() < 7):
            self.frz_table.setColumnCount(7)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.frz_table.setHorizontalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.frz_table.setHorizontalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.frz_table.setHorizontalHeaderItem(2, __qtablewidgetitem8)
        self.frz_table.setObjectName(u"frz_table")
        self.frz_table.setMinimumSize(QSize(250, 0))
        self.frz_table.setMaximumSize(QSize(16777215, 16777215))
        self.frz_table.setFont(font)
        self.frz_table.setStyleSheet(u"border: none;\n"
"color: rgb(138, 180, 247)")
        self.frz_table.setAlternatingRowColors(False)
        self.frz_table.setSelectionMode(QAbstractItemView.NoSelection)
        self.frz_table.setShowGrid(False)
        self.frz_table.setCornerButtonEnabled(False)
        self.frz_table.setColumnCount(7)
        self.frz_table.horizontalHeader().setVisible(False)
        self.frz_table.horizontalHeader().setMinimumSectionSize(20)
        self.frz_table.horizontalHeader().setDefaultSectionSize(50)
        self.frz_table.horizontalHeader().setHighlightSections(False)
        self.frz_table.verticalHeader().setVisible(False)

        self.gridLayout_4.addWidget(self.frz_table, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_3, u"Freeze detection")

        self.horizontalLayout_2.addWidget(self.toolBox)


        self.horizontalLayout_6.addWidget(self.frame_tables)

        self.frame_videoplayer = QFrame(VideoINFO_Player)
        self.frame_videoplayer.setObjectName(u"frame_videoplayer")
        self.frame_videoplayer.setStyleSheet(u"QFrame#frame_videoplayer{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_videoplayer.setFrameShape(QFrame.StyledPanel)
        self.frame_videoplayer.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_videoplayer)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.VideoPreview = QLabel(self.frame_videoplayer)
        self.VideoPreview.setObjectName(u"VideoPreview")
        self.VideoPreview.setMaximumSize(QSize(16777215, 16777215))
        self.VideoPreview.setStyleSheet(u"color: white")

        self.horizontalLayout.addWidget(self.VideoPreview)

        self.file_path = QLabel(self.frame_videoplayer)
        self.file_path.setObjectName(u"file_path")
        self.file_path.setMinimumSize(QSize(0, 0))
        self.file_path.setMaximumSize(QSize(16777215, 16777215))
        self.file_path.setStyleSheet(u"color: grey\n"
"")
        self.file_path.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.file_path.setWordWrap(True)

        self.horizontalLayout.addWidget(self.file_path)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.video_player_img = QLabel(self.frame_videoplayer)
        self.video_player_img.setObjectName(u"video_player_img")
        self.video_player_img.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.video_player_img.sizePolicy().hasHeightForWidth())
        self.video_player_img.setSizePolicy(sizePolicy)
        self.video_player_img.setMinimumSize(QSize(960, 540))
        self.video_player_img.setMaximumSize(QSize(960, 540))
        self.video_player_img.setBaseSize(QSize(960, 540))
        self.video_player_img.setPixmap(QPixmap(u":/imgs/img/video_player.png"))
        self.video_player_img.setScaledContents(True)
        self.video_player_img.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.video_player_img.setWordWrap(False)
        self.video_player_img.setIndent(-1)

        self.verticalLayout.addWidget(self.video_player_img)

        self.videoSlider = QSlider(self.frame_videoplayer)
        self.videoSlider.setObjectName(u"videoSlider")
        sizePolicy.setHeightForWidth(self.videoSlider.sizePolicy().hasHeightForWidth())
        self.videoSlider.setSizePolicy(sizePolicy)
        self.videoSlider.setMinimumSize(QSize(960, 0))
        self.videoSlider.setMaximumSize(QSize(960, 16777215))
        self.videoSlider.setBaseSize(QSize(960, 0))
        self.videoSlider.setOrientation(Qt.Horizontal)
        self.videoSlider.setTickPosition(QSlider.NoTicks)

        self.verticalLayout.addWidget(self.videoSlider)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.pos_dur_tc = QLabel(self.frame_videoplayer)
        self.pos_dur_tc.setObjectName(u"pos_dur_tc")
        self.pos_dur_tc.setMaximumSize(QSize(16777215, 16777215))
        self.pos_dur_tc.setStyleSheet(u"color: white")

        self.horizontalLayout_3.addWidget(self.pos_dur_tc)

        self.Buttons = QFrame(self.frame_videoplayer)
        self.Buttons.setObjectName(u"Buttons")
        self.Buttons.setMinimumSize(QSize(250, 50))
        self.Buttons.setMaximumSize(QSize(400, 60))
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
        self.horizontalLayout_5 = QHBoxLayout(self.Buttons)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.player_openButton = QToolButton(self.Buttons)
        self.player_buttonGroup = QButtonGroup(VideoINFO_Player)
        self.player_buttonGroup.setObjectName(u"player_buttonGroup")
        self.player_buttonGroup.addButton(self.player_openButton)
        self.player_openButton.setObjectName(u"player_openButton")
        self.player_openButton.setMinimumSize(QSize(40, 30))
        self.player_openButton.setMaximumSize(QSize(40, 30))
        self.player_openButton.setStyleSheet(u"icon-color: white")
        icon = QIcon()
        icon.addFile(u":/bl_img/icons/folder_open_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_openButton.setIcon(icon)
        self.player_openButton.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_openButton)

        self.player_prev_fr_Button = QToolButton(self.Buttons)
        self.player_buttonGroup.addButton(self.player_prev_fr_Button)
        self.player_prev_fr_Button.setObjectName(u"player_prev_fr_Button")
        self.player_prev_fr_Button.setMinimumSize(QSize(40, 30))
        self.player_prev_fr_Button.setMaximumSize(QSize(40, 30))
        icon1 = QIcon()
        icon1.addFile(u":/bl_img/icons/prev_fr_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_prev_fr_Button.setIcon(icon1)
        self.player_prev_fr_Button.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_prev_fr_Button)

        self.player_prev_mark_Button = QToolButton(self.Buttons)
        self.player_prev_mark_Button.setObjectName(u"player_prev_mark_Button")
        self.player_prev_mark_Button.setMinimumSize(QSize(40, 30))
        self.player_prev_mark_Button.setMaximumSize(QSize(40, 30))
        icon2 = QIcon()
        icon2.addFile(u":/bl_img/icons/skip_previous_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_prev_mark_Button.setIcon(icon2)
        self.player_prev_mark_Button.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_prev_mark_Button)

        self.player_playButton = QToolButton(self.Buttons)
        self.player_buttonGroup.addButton(self.player_playButton)
        self.player_playButton.setObjectName(u"player_playButton")
        self.player_playButton.setMinimumSize(QSize(50, 38))
        self.player_playButton.setMaximumSize(QSize(45, 35))
        self.player_playButton.setStyleSheet(u"")
        icon3 = QIcon()
        icon3.addFile(u":/bl_img/icons/play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_playButton.setIcon(icon3)
        self.player_playButton.setIconSize(QSize(25, 35))

        self.horizontalLayout_5.addWidget(self.player_playButton)

        self.player_next_mark_Button = QToolButton(self.Buttons)
        self.player_next_mark_Button.setObjectName(u"player_next_mark_Button")
        self.player_next_mark_Button.setMinimumSize(QSize(40, 30))
        self.player_next_mark_Button.setMaximumSize(QSize(40, 30))
        icon4 = QIcon()
        icon4.addFile(u":/bl_img/icons/skip_next_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_next_mark_Button.setIcon(icon4)
        self.player_next_mark_Button.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_next_mark_Button)

        self.player_next_fr_Button = QToolButton(self.Buttons)
        self.player_buttonGroup.addButton(self.player_next_fr_Button)
        self.player_next_fr_Button.setObjectName(u"player_next_fr_Button")
        self.player_next_fr_Button.setMinimumSize(QSize(40, 30))
        self.player_next_fr_Button.setMaximumSize(QSize(40, 30))
        icon5 = QIcon()
        icon5.addFile(u":/bl_img/icons/next_fr_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_next_fr_Button.setIcon(icon5)
        self.player_next_fr_Button.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_next_fr_Button)

        self.player_fullButton = QToolButton(self.Buttons)
        self.player_buttonGroup.addButton(self.player_fullButton)
        self.player_fullButton.setObjectName(u"player_fullButton")
        self.player_fullButton.setMinimumSize(QSize(40, 30))
        self.player_fullButton.setMaximumSize(QSize(40, 30))
        icon6 = QIcon()
        icon6.addFile(u":/bl_img/icons/fullscreen_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_fullButton.setIcon(icon6)
        self.player_fullButton.setIconSize(QSize(20, 30))

        self.horizontalLayout_5.addWidget(self.player_fullButton)


        self.horizontalLayout_3.addWidget(self.Buttons, 0, Qt.AlignHCenter)

        self.player_muteButton = QToolButton(self.frame_videoplayer)
        self.player_muteButton.setObjectName(u"player_muteButton")
        self.player_muteButton.setMinimumSize(QSize(40, 30))
        self.player_muteButton.setMaximumSize(QSize(40, 30))
        self.player_muteButton.setStyleSheet(u"background-color:rgba(255,255,255,0);")
        icon7 = QIcon()
        icon7.addFile(u":/bl_img/icons/volume_up_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.player_muteButton.setIcon(icon7)
        self.player_muteButton.setIconSize(QSize(20, 30))

        self.horizontalLayout_3.addWidget(self.player_muteButton)

        self.volumeSlider = QSlider(self.frame_videoplayer)
        self.volumeSlider.setObjectName(u"volumeSlider")
        sizePolicy.setHeightForWidth(self.volumeSlider.sizePolicy().hasHeightForWidth())
        self.volumeSlider.setSizePolicy(sizePolicy)
        self.volumeSlider.setMinimumSize(QSize(157, 0))
        self.volumeSlider.setMaximumSize(QSize(157, 16777215))
        self.volumeSlider.setBaseSize(QSize(157, 0))
        self.volumeSlider.setTracking(True)
        self.volumeSlider.setOrientation(Qt.Horizontal)
        self.volumeSlider.setTickPosition(QSlider.NoTicks)
        self.volumeSlider.setTickInterval(10)

        self.horizontalLayout_3.addWidget(self.volumeSlider)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_3.setStretch(3, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.player_add_mark = QPushButton(self.frame_videoplayer)
        self.player_add_mark.setObjectName(u"player_add_mark")
        self.player_add_mark.setMaximumSize(QSize(160, 16777215))
        self.player_add_mark.setStyleSheet(u"color: white;")

        self.verticalLayout_2.addWidget(self.player_add_mark)

        self.player_dell_mark = QPushButton(self.frame_videoplayer)
        self.player_dell_mark.setObjectName(u"player_dell_mark")
        self.player_dell_mark.setMaximumSize(QSize(160, 16777215))
        self.player_dell_mark.setStyleSheet(u"color: white;")

        self.verticalLayout_2.addWidget(self.player_dell_mark)

        self.player_save_marks = QPushButton(self.frame_videoplayer)
        self.player_save_marks.setObjectName(u"player_save_marks")
        self.player_save_marks.setMaximumSize(QSize(160, 16777215))
        self.player_save_marks.setStyleSheet(u"color: white;")

        self.verticalLayout_2.addWidget(self.player_save_marks)


        self.horizontalLayout_4.addLayout(self.verticalLayout_2)

        self.tableMarks = QTableWidget(self.frame_videoplayer)
        if (self.tableMarks.columnCount() < 3):
            self.tableMarks.setColumnCount(3)
        self.tableMarks.setObjectName(u"tableMarks")
        self.tableMarks.setMinimumSize(QSize(0, 200))
        self.tableMarks.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.tableMarks.setShowGrid(False)
        self.tableMarks.setColumnCount(3)
        self.tableMarks.horizontalHeader().setVisible(False)

        self.horizontalLayout_4.addWidget(self.tableMarks)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)


        self.horizontalLayout_6.addWidget(self.frame_videoplayer)


        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)

#if QT_CONFIG(shortcut)
        self.video_player_img.setBuddy(self.Buttons)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(VideoINFO_Player)

        self.toolBox.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(VideoINFO_Player)
    # setupUi

    def retranslateUi(self, VideoINFO_Player):
        VideoINFO_Player.setWindowTitle(QCoreApplication.translate("VideoINFO_Player", u"VideoINFO Player", None))
        ___qtablewidgetitem = self.blck_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("VideoINFO_Player", u"Start", None));
        ___qtablewidgetitem1 = self.blck_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("VideoINFO_Player", u"End", None));
        ___qtablewidgetitem2 = self.blck_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("VideoINFO_Player", u"Duration", None));
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), QCoreApplication.translate("VideoINFO_Player", u"Black detection", None))
        ___qtablewidgetitem3 = self.slnc_table.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("VideoINFO_Player", u"Start", None));
        ___qtablewidgetitem4 = self.slnc_table.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("VideoINFO_Player", u"End", None));
        ___qtablewidgetitem5 = self.slnc_table.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("VideoINFO_Player", u"Duration", None));
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("VideoINFO_Player", u"Silence detection", None))
        ___qtablewidgetitem6 = self.frz_table.horizontalHeaderItem(0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("VideoINFO_Player", u"Start", None));
        ___qtablewidgetitem7 = self.frz_table.horizontalHeaderItem(1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("VideoINFO_Player", u"End", None));
        ___qtablewidgetitem8 = self.frz_table.horizontalHeaderItem(2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("VideoINFO_Player", u"Duration", None));
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("VideoINFO_Player", u"Freeze detection", None))
        self.VideoPreview.setText(QCoreApplication.translate("VideoINFO_Player", u"Video preview", None))
        self.file_path.setText(QCoreApplication.translate("VideoINFO_Player", u"file_path", None))
        self.video_player_img.setText("")
        self.pos_dur_tc.setText(QCoreApplication.translate("VideoINFO_Player", u"00:00:00.00 / 00:00:00.00", None))
        self.player_openButton.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_prev_fr_Button.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_prev_mark_Button.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_playButton.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_next_mark_Button.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_next_fr_Button.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_fullButton.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_muteButton.setText(QCoreApplication.translate("VideoINFO_Player", u"...", None))
        self.player_add_mark.setText(QCoreApplication.translate("VideoINFO_Player", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043c\u0435\u0442\u043a\u0443", None))
        self.player_dell_mark.setText(QCoreApplication.translate("VideoINFO_Player", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u043c\u0435\u0442\u043a\u0443", None))
        self.player_save_marks.setText(QCoreApplication.translate("VideoINFO_Player", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u044f", None))
    # retranslateUi

