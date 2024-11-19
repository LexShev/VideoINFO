# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_videoinfo.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QApplication, QFrame,
    QGridLayout, QHeaderView, QLabel, QLayout,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QSpacerItem, QSplitter, QTableView, QTableWidget,
    QTableWidgetItem, QToolBar, QToolButton, QVBoxLayout,
    QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1500, 924)
        icon = QIcon()
        icon.addFile(u":/logo/logo/LOGO_VideoInfo_450x450.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;")
        self.actionAdd_files = QAction(MainWindow)
        self.actionAdd_files.setObjectName(u"actionAdd_files")
        self.actionAdd_files.setMenuRole(QAction.TextHeuristicRole)
        self.actionDelete_selected_file = QAction(MainWindow)
        self.actionDelete_selected_file.setObjectName(u"actionDelete_selected_file")
        self.actionPlay_selected_file = QAction(MainWindow)
        self.actionPlay_selected_file.setObjectName(u"actionPlay_selected_file")
        self.actionOpen_destination_folder = QAction(MainWindow)
        self.actionOpen_destination_folder.setObjectName(u"actionOpen_destination_folder")
        self.actionOpen_db_editor = QAction(MainWindow)
        self.actionOpen_db_editor.setObjectName(u"actionOpen_db_editor")
        self.actionShow_Loudness = QAction(MainWindow)
        self.actionShow_Loudness.setObjectName(u"actionShow_Loudness")
        self.actionShow_Details = QAction(MainWindow)
        self.actionShow_Details.setObjectName(u"actionShow_Details")
        self.actionRun_Loudness_single_scan = QAction(MainWindow)
        self.actionRun_Loudness_single_scan.setObjectName(u"actionRun_Loudness_single_scan")
        self.actionRun_Loudness_multiple_scan = QAction(MainWindow)
        self.actionRun_Loudness_multiple_scan.setObjectName(u"actionRun_Loudness_multiple_scan")
        self.actionRun_BlackDetect_single_scan = QAction(MainWindow)
        self.actionRun_BlackDetect_single_scan.setObjectName(u"actionRun_BlackDetect_single_scan")
        self.actionRun_BlackDetect_multiple_scan = QAction(MainWindow)
        self.actionRun_BlackDetect_multiple_scan.setObjectName(u"actionRun_BlackDetect_multiple_scan")
        self.actionRun_SilenceDetect_single_scan = QAction(MainWindow)
        self.actionRun_SilenceDetect_single_scan.setObjectName(u"actionRun_SilenceDetect_single_scan")
        self.actionRun_SilenceDetect_multiple_scan = QAction(MainWindow)
        self.actionRun_SilenceDetect_multiple_scan.setObjectName(u"actionRun_SilenceDetect_multiple_scan")
        self.actionRun_FreezeDetect_single_scan = QAction(MainWindow)
        self.actionRun_FreezeDetect_single_scan.setObjectName(u"actionRun_FreezeDetect_single_scan")
        self.actionRun_FreezeDetect_multiple_scan = QAction(MainWindow)
        self.actionRun_FreezeDetect_multiple_scan.setObjectName(u"actionRun_FreezeDetect_multiple_scan")
        self.actionRun_Full_single_scan = QAction(MainWindow)
        self.actionRun_Full_single_scan.setObjectName(u"actionRun_Full_single_scan")
        self.actionRun_Full_multiple_scan = QAction(MainWindow)
        self.actionRun_Full_multiple_scan.setObjectName(u"actionRun_Full_multiple_scan")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.actionExport_table_to_Excel = QAction(MainWindow)
        self.actionExport_table_to_Excel.setObjectName(u"actionExport_table_to_Excel")
        self.actionExport_all_db_to_Excel = QAction(MainWindow)
        self.actionExport_all_db_to_Excel.setObjectName(u"actionExport_all_db_to_Excel")
        self.actionOpen_VideoPlayer = QAction(MainWindow)
        self.actionOpen_VideoPlayer.setObjectName(u"actionOpen_VideoPlayer")
        self.actionOpen_VideoPlayer.setVisible(False)
        self.actionRun_Background_Loudness_scan = QAction(MainWindow)
        self.actionRun_Background_Loudness_scan.setObjectName(u"actionRun_Background_Loudness_scan")
        self.actionRun_Background_BlackDetect_scan = QAction(MainWindow)
        self.actionRun_Background_BlackDetect_scan.setObjectName(u"actionRun_Background_BlackDetect_scan")
        self.actionRun_Background_SilenceDetect_scan = QAction(MainWindow)
        self.actionRun_Background_SilenceDetect_scan.setObjectName(u"actionRun_Background_SilenceDetect_scan")
        self.actionRun_Background_FreezeDetect_scan = QAction(MainWindow)
        self.actionRun_Background_FreezeDetect_scan.setObjectName(u"actionRun_Background_FreezeDetect_scan")
        self.actionRun_Background_Full_scan = QAction(MainWindow)
        self.actionRun_Background_Full_scan.setObjectName(u"actionRun_Background_Full_scan")
        self.actionClear_table = QAction(MainWindow)
        self.actionClear_table.setObjectName(u"actionClear_table")
        self.actionClear_table.setVisible(False)
        self.actionShow_all_tables = QAction(MainWindow)
        self.actionShow_all_tables.setObjectName(u"actionShow_all_tables")
        self.actionShow_all_tables.setEnabled(False)
        self.actionShow_all_tables.setVisible(False)
        self.actionConnect_to_DB = QAction(MainWindow)
        self.actionConnect_to_DB.setObjectName(u"actionConnect_to_DB")
        self.actionConnect_to_DB.setVisible(False)
        self.actionClose_DB = QAction(MainWindow)
        self.actionClose_DB.setObjectName(u"actionClose_DB")
        self.actionClose_DB.setVisible(False)
        self.actionDelete_file_entry = QAction(MainWindow)
        self.actionDelete_file_entry.setObjectName(u"actionDelete_file_entry")
        self.actionDelete_file_entry.setVisible(False)
        self.actionCreate_file_entry = QAction(MainWindow)
        self.actionCreate_file_entry.setObjectName(u"actionCreate_file_entry")
        self.actionCreate_file_entry.setVisible(False)
        self.actionReset_scan_result_for_file = QAction(MainWindow)
        self.actionReset_scan_result_for_file.setObjectName(u"actionReset_scan_result_for_file")
        self.actionCreate_column = QAction(MainWindow)
        self.actionCreate_column.setObjectName(u"actionCreate_column")
        self.actionCreate_column.setVisible(False)
        self.actionDelete_column = QAction(MainWindow)
        self.actionDelete_column.setObjectName(u"actionDelete_column")
        self.actionDelete_column.setVisible(False)
        self.actionUpdate_data_for_file = QAction(MainWindow)
        self.actionUpdate_data_for_file.setObjectName(u"actionUpdate_data_for_file")
        self.actionCreate_table = QAction(MainWindow)
        self.actionCreate_table.setObjectName(u"actionCreate_table")
        self.actionCreate_table.setVisible(False)
        self.actionCreate_db = QAction(MainWindow)
        self.actionCreate_db.setObjectName(u"actionCreate_db")
        self.actionCreate_db.setVisible(False)
        self.actionDelete_DB = QAction(MainWindow)
        self.actionDelete_DB.setObjectName(u"actionDelete_DB")
        self.actionDelete_DB.setVisible(False)
        self.actionDelete_from_db = QAction(MainWindow)
        self.actionDelete_from_db.setObjectName(u"actionDelete_from_db")
        self.actionSelected_files = QAction(MainWindow)
        self.actionSelected_files.setObjectName(u"actionSelected_files")
        self.actionSelected_files.setVisible(False)
        self.actionRun_Loudness_selected_scan = QAction(MainWindow)
        self.actionRun_Loudness_selected_scan.setObjectName(u"actionRun_Loudness_selected_scan")
        self.actionRun_BlackDetect_selected_scan = QAction(MainWindow)
        self.actionRun_BlackDetect_selected_scan.setObjectName(u"actionRun_BlackDetect_selected_scan")
        self.actionRun_SilenceDetect_selected_scan = QAction(MainWindow)
        self.actionRun_SilenceDetect_selected_scan.setObjectName(u"actionRun_SilenceDetect_selected_scan")
        self.actionRun_FreezeDetect_selected_scan = QAction(MainWindow)
        self.actionRun_FreezeDetect_selected_scan.setObjectName(u"actionRun_FreezeDetect_selected_scan")
        self.actionRun_Full_selected_scan = QAction(MainWindow)
        self.actionRun_Full_selected_scan.setObjectName(u"actionRun_Full_selected_scan")
        self.actionChoose_default_directory = QAction(MainWindow)
        self.actionChoose_default_directory.setObjectName(u"actionChoose_default_directory")
        self.actionCheck_DB = QAction(MainWindow)
        self.actionCheck_DB.setObjectName(u"actionCheck_DB")
        self.actionCheck_DB.setVisible(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttons = QFrame(self.centralwidget)
        self.buttons.setObjectName(u"buttons")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttons.sizePolicy().hasHeightForWidth())
        self.buttons.setSizePolicy(sizePolicy)
        self.buttons.setMinimumSize(QSize(46, 0))
        self.buttons.setMaximumSize(QSize(16777215, 16777215))
        self.buttons.setBaseSize(QSize(46, 0))
        self.buttons.setStyleSheet(u"color: rgb(146, 146, 146);\n"
"border: 0px;")
        self.buttons.setFrameShape(QFrame.Box)
        self.buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.buttons)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(3, 1, 3, 3)
        self.switchToolButton = QToolButton(self.buttons)
        self.switchToolButton.setObjectName(u"switchToolButton")
        self.switchToolButton.setMinimumSize(QSize(40, 30))
        self.switchToolButton.setMaximumSize(QSize(40, 30))
        self.switchToolButton.setBaseSize(QSize(40, 30))
        self.switchToolButton.setStyleSheet(u"QToolButton{\n"
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
        icon1.addFile(u":/bl_img/icons/menu_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.switchToolButton.setIcon(icon1)
        self.switchToolButton.setIconSize(QSize(20, 35))
        self.switchToolButton.setPopupMode(QToolButton.DelayedPopup)
        self.switchToolButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.switchToolButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_5.addWidget(self.switchToolButton)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.move_to_tableButton = QToolButton(self.buttons)
        self.move_to_tableButton.setObjectName(u"move_to_tableButton")
        self.move_to_tableButton.setMinimumSize(QSize(40, 30))
        self.move_to_tableButton.setMaximumSize(QSize(40, 30))
        self.move_to_tableButton.setBaseSize(QSize(40, 30))
        self.move_to_tableButton.setStyleSheet(u"QToolButton{\n"
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
        icon2.addFile(u":/bl_img/icons/list_alt_add_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.move_to_tableButton.setIcon(icon2)
        self.move_to_tableButton.setIconSize(QSize(20, 35))
        self.move_to_tableButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_5.addWidget(self.move_to_tableButton)

        self.delete_from_dbButton = QToolButton(self.buttons)
        self.delete_from_dbButton.setObjectName(u"delete_from_dbButton")
        self.delete_from_dbButton.setMinimumSize(QSize(40, 30))
        self.delete_from_dbButton.setMaximumSize(QSize(40, 30))
        self.delete_from_dbButton.setBaseSize(QSize(40, 30))
        self.delete_from_dbButton.setStyleSheet(u"QToolButton{\n"
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
        icon3.addFile(u":/bl_img/icons/scan_delete_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.delete_from_dbButton.setIcon(icon3)
        self.delete_from_dbButton.setIconSize(QSize(20, 35))
        self.delete_from_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_5.addWidget(self.delete_from_dbButton)

        self.move_to_dbButton = QToolButton(self.buttons)
        self.move_to_dbButton.setObjectName(u"move_to_dbButton")
        self.move_to_dbButton.setMinimumSize(QSize(40, 30))
        self.move_to_dbButton.setMaximumSize(QSize(40, 30))
        self.move_to_dbButton.setBaseSize(QSize(40, 30))
        self.move_to_dbButton.setStyleSheet(u"QToolButton{\n"
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
        icon4.addFile(u":/bl_img/icons/move_group_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.move_to_dbButton.setIcon(icon4)
        self.move_to_dbButton.setIconSize(QSize(20, 35))
        self.move_to_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_5.addWidget(self.move_to_dbButton)

        self.addButton = QToolButton(self.buttons)
        self.addButton.setObjectName(u"addButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.addButton.sizePolicy().hasHeightForWidth())
        self.addButton.setSizePolicy(sizePolicy1)
        self.addButton.setMinimumSize(QSize(40, 30))
        self.addButton.setMaximumSize(QSize(110, 30))
        self.addButton.setBaseSize(QSize(40, 30))
        self.addButton.setContextMenuPolicy(Qt.DefaultContextMenu)
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
        icon5 = QIcon()
        icon5.addFile(u":/bl_img/icons/add_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.addButton.setIcon(icon5)
        self.addButton.setIconSize(QSize(20, 35))
        self.addButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_5.addWidget(self.addButton)

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
        icon6 = QIcon()
        icon6.addFile(u":/bl_img/icons/remove_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.delButton.setIcon(icon6)
        self.delButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.delButton)

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
        icon7 = QIcon()
        icon7.addFile(u":/bl_img/icons/play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.playButton.setIcon(icon7)
        self.playButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.playButton)

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
        icon8.addFile(u":/bl_img/icons/folder_open_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.openButton.setIcon(icon8)
        self.openButton.setIconSize(QSize(20, 35))
        self.openButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_5.addWidget(self.openButton)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_3)

        self.r128DtctButton = QToolButton(self.buttons)
        self.r128DtctButton.setObjectName(u"r128DtctButton")
        self.r128DtctButton.setMinimumSize(QSize(40, 30))
        self.r128DtctButton.setMaximumSize(QSize(40, 30))
        self.r128DtctButton.setBaseSize(QSize(40, 30))
        self.r128DtctButton.setStyleSheet(u"QToolButton{\n"
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
        icon9.addFile(u":/bl_img/icons/equalizer_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.r128DtctButton.setIcon(icon9)
        self.r128DtctButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.r128DtctButton)

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
        icon10 = QIcon()
        icon10.addFile(u":/bl_img/icons/playlist_play_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.queueButton.setIcon(icon10)
        self.queueButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.queueButton)

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
        icon11 = QIcon()
        icon11.addFile(u":/bl_img/icons/call_to_action_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.blckDtctButton.setIcon(icon11)
        self.blckDtctButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.blckDtctButton)

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
        icon12 = QIcon()
        icon12.addFile(u":/bl_img/icons/music_video_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.slncDtctButton.setIcon(icon12)
        self.slncDtctButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.slncDtctButton)

        self.frzDtctButton = QToolButton(self.buttons)
        self.frzDtctButton.setObjectName(u"frzDtctButton")
        self.frzDtctButton.setMinimumSize(QSize(40, 30))
        self.frzDtctButton.setMaximumSize(QSize(40, 30))
        self.frzDtctButton.setBaseSize(QSize(40, 30))
        self.frzDtctButton.setStyleSheet(u"QToolButton{\n"
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
        icon13 = QIcon()
        icon13.addFile(u":/bl_img/icons/remove_from_queue_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.frzDtctButton.setIcon(icon13)
        self.frzDtctButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.frzDtctButton)

        self.fullDtctButton = QToolButton(self.buttons)
        self.fullDtctButton.setObjectName(u"fullDtctButton")
        self.fullDtctButton.setMinimumSize(QSize(40, 30))
        self.fullDtctButton.setMaximumSize(QSize(40, 30))
        self.fullDtctButton.setBaseSize(QSize(40, 30))
        self.fullDtctButton.setStyleSheet(u"QToolButton{\n"
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
        icon14 = QIcon()
        icon14.addFile(u":/bl_img/icons/subtitles_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.fullDtctButton.setIcon(icon14)
        self.fullDtctButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.fullDtctButton)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.migrateButton = QToolButton(self.buttons)
        self.migrateButton.setObjectName(u"migrateButton")
        self.migrateButton.setMinimumSize(QSize(40, 30))
        self.migrateButton.setMaximumSize(QSize(40, 30))
        self.migrateButton.setBaseSize(QSize(40, 30))
        self.migrateButton.setStyleSheet(u"QToolButton{\n"
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
        icon15 = QIcon()
        icon15.addFile(u":/bl_img/icons/swap_horiz_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.migrateButton.setIcon(icon15)
        self.migrateButton.setIconSize(QSize(20, 35))
        self.migrateButton.setAutoRaise(False)

        self.verticalLayout_5.addWidget(self.migrateButton)

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
        icon16 = QIcon()
        icon16.addFile(u":/bl_img/icons/upgrade_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.exportButton.setIcon(icon16)
        self.exportButton.setIconSize(QSize(20, 35))
        self.exportButton.setAutoRaise(False)

        self.verticalLayout_5.addWidget(self.exportButton)

        self.switchModeButton = QToolButton(self.buttons)
        self.switchModeButton.setObjectName(u"switchModeButton")
        self.switchModeButton.setMinimumSize(QSize(40, 30))
        self.switchModeButton.setMaximumSize(QSize(40, 30))
        self.switchModeButton.setBaseSize(QSize(40, 30))
        self.switchModeButton.setStyleSheet(u"QToolButton{\n"
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
        icon17 = QIcon()
        icon17.addFile(u":/bl_img/icons/widgets_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.switchModeButton.setIcon(icon17)
        self.switchModeButton.setIconSize(QSize(20, 35))
        self.switchModeButton.setPopupMode(QToolButton.DelayedPopup)
        self.switchModeButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.switchModeButton.setArrowType(Qt.NoArrow)

        self.verticalLayout_5.addWidget(self.switchModeButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer)

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
        icon18 = QIcon()
        icon18.addFile(u":/bl_img/icons/settings_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.settingsButton.setIcon(icon18)
        self.settingsButton.setIconSize(QSize(20, 35))

        self.verticalLayout_5.addWidget(self.settingsButton)


        self.gridLayout.addWidget(self.buttons, 0, 0, 1, 1)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.main_frame_tbl_01 = QFrame(self.splitter)
        self.main_frame_tbl_01.setObjectName(u"main_frame_tbl_01")
        self.verticalLayout_4 = QVBoxLayout(self.main_frame_tbl_01)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.tableWidget_01 = QTableWidget(self.main_frame_tbl_01)
        if (self.tableWidget_01.columnCount() < 22):
            self.tableWidget_01.setColumnCount(22)
        self.tableWidget_01.setObjectName(u"tableWidget_01")
        sizePolicy.setHeightForWidth(self.tableWidget_01.sizePolicy().hasHeightForWidth())
        self.tableWidget_01.setSizePolicy(sizePolicy)
        self.tableWidget_01.setMinimumSize(QSize(800, 400))
        self.tableWidget_01.setBaseSize(QSize(800, 320))
        self.tableWidget_01.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableWidget_01.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_01.setDragEnabled(True)
        self.tableWidget_01.setDragDropOverwriteMode(False)
        self.tableWidget_01.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.tableWidget_01.setAlternatingRowColors(False)
        self.tableWidget_01.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_01.setGridStyle(Qt.SolidLine)
        self.tableWidget_01.setSortingEnabled(True)
        self.tableWidget_01.setColumnCount(22)
        self.tableWidget_01.horizontalHeader().setMinimumSectionSize(60)
        self.tableWidget_01.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget_01.verticalHeader().setVisible(False)
        self.tableWidget_01.verticalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_4.addWidget(self.tableWidget_01)

        self.tableView_db = QTableView(self.main_frame_tbl_01)
        self.tableView_db.setObjectName(u"tableView_db")
        self.tableView_db.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView_db.setSortingEnabled(True)
        self.tableView_db.horizontalHeader().setProperty("showSortIndicator", False)

        self.verticalLayout_4.addWidget(self.tableView_db)

        self.frame_wave = QFrame(self.main_frame_tbl_01)
        self.frame_wave.setObjectName(u"frame_wave")
        self.frame_wave.setMaximumSize(QSize(16777215, 370))
        self.frame_wave.setStyleSheet(u"QFrame#frame_wave{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_wave.setFrameShape(QFrame.StyledPanel)
        self.frame_wave.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_wave)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.resizeButtonDown = QToolButton(self.frame_wave)
        self.resizeButtonDown.setObjectName(u"resizeButtonDown")
        self.resizeButtonDown.setStyleSheet(u"background-color:rgba(255,255,255,0)")
        icon19 = QIcon()
        icon19.addFile(u":/bl_img/icons/expand_more_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resizeButtonDown.setIcon(icon19)

        self.verticalLayout_2.addWidget(self.resizeButtonDown, 0, Qt.AlignHCenter)

        self.wave_view = QLabel(self.frame_wave)
        self.wave_view.setObjectName(u"wave_view")
        sizePolicy.setHeightForWidth(self.wave_view.sizePolicy().hasHeightForWidth())
        self.wave_view.setSizePolicy(sizePolicy)
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
        self.resizeButtonUp.setStyleSheet(u"background-color:rgba(255,255,255,0)")
        icon20 = QIcon()
        icon20.addFile(u":/bl_img/icons/expand_less_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.resizeButtonUp.setIcon(icon20)

        self.verticalLayout_2.addWidget(self.resizeButtonUp, 0, Qt.AlignHCenter)


        self.verticalLayout_4.addWidget(self.frame_wave)

        self.splitter.addWidget(self.main_frame_tbl_01)
        self.main_frame_tbl_02 = QFrame(self.splitter)
        self.main_frame_tbl_02.setObjectName(u"main_frame_tbl_02")
        self.main_frame_tbl_02.setMinimumSize(QSize(380, 0))
        self.main_frame_tbl_02.setMaximumSize(QSize(410, 16777215))
        self.main_frame_tbl_02.setBaseSize(QSize(390, 0))
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
        sizePolicy.setHeightForWidth(self.tag_file_path.sizePolicy().hasHeightForWidth())
        self.tag_file_path.setSizePolicy(sizePolicy)
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

        self.gridLayout.addWidget(self.splitter, 0, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1500, 31))
        self.menuBar.setMinimumSize(QSize(0, 25))
        self.menuBar.setLayoutDirection(Qt.LeftToRight)
        self.menuBar.setAutoFillBackground(False)
        self.menuBar.setStyleSheet(u"QMenuBar{\n"
"	 color: rgb(146, 146, 146);\n"
"	 border: 0px;\n"
"	 padding: 4px;\n"
"}\n"
"\n"
"QMenu{\n"
"	 color: rgb(255, 255, 255);\n"
"     background-color:rgba(255,255,255,20);\n"
"     border: 0px;\n"
"	 \n"
"}\n"
"QMenu:hover{\n"
"background-color:rgba(255,255,255,50);\n"
"}\n"
"QMenu:pressed{\n"
"background-color:rgba(255,255,255,70);\n"
"}")
        self.menuBar.setDefaultUp(False)
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuFile.setMinimumSize(QSize(200, 0))
        self.menuFile.setBaseSize(QSize(200, 0))
        self.menuEdit = QMenu(self.menuBar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuEdit.setMinimumSize(QSize(200, 0))
        self.menuEdit.setBaseSize(QSize(200, 0))
        self.menuEdit.setStyleSheet(u"")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        sizePolicy.setHeightForWidth(self.menuView.sizePolicy().hasHeightForWidth())
        self.menuView.setSizePolicy(sizePolicy)
        self.menuView.setMinimumSize(QSize(200, 0))
        self.menuView.setBaseSize(QSize(200, 0))
        self.menuScanners = QMenu(self.menuBar)
        self.menuScanners.setObjectName(u"menuScanners")
        self.menuScanners.setMinimumSize(QSize(250, 0))
        self.menuScanners.setBaseSize(QSize(250, 0))
        self.menuDataBase = QMenu(self.menuBar)
        self.menuDataBase.setObjectName(u"menuDataBase")
        MainWindow.setMenuBar(self.menuBar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        self.toolBar.setStyleSheet(u"")
        self.toolBar.setMovable(False)
        self.toolBar.setToolButtonStyle(Qt.ToolButtonIconOnly)
        self.toolBar.setFloatable(True)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())
        self.menuBar.addAction(self.menuScanners.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuDataBase.menuAction())
        self.menuFile.addAction(self.actionAdd_files)
        self.menuFile.addAction(self.actionDelete_selected_file)
        self.menuFile.addAction(self.actionPlay_selected_file)
        self.menuFile.addAction(self.actionOpen_destination_folder)
        self.menuFile.addAction(self.actionChoose_default_directory)
        self.menuEdit.addAction(self.actionExport_table_to_Excel)
        self.menuEdit.addAction(self.actionExport_all_db_to_Excel)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionOpen_VideoPlayer)
        self.menuEdit.addAction(self.actionSelected_files)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionSettings)
        self.menuEdit.addSeparator()
        self.menuView.addAction(self.actionOpen_db_editor)
        self.menuView.addAction(self.actionShow_Loudness)
        self.menuView.addAction(self.actionShow_Details)
        self.menuScanners.addAction(self.actionRun_Loudness_selected_scan)
        self.menuScanners.addAction(self.actionRun_Loudness_single_scan)
        self.menuScanners.addAction(self.actionRun_Loudness_multiple_scan)
        self.menuScanners.addSeparator()
        self.menuScanners.addAction(self.actionRun_BlackDetect_selected_scan)
        self.menuScanners.addAction(self.actionRun_BlackDetect_single_scan)
        self.menuScanners.addAction(self.actionRun_BlackDetect_multiple_scan)
        self.menuScanners.addSeparator()
        self.menuScanners.addAction(self.actionRun_SilenceDetect_selected_scan)
        self.menuScanners.addAction(self.actionRun_SilenceDetect_single_scan)
        self.menuScanners.addAction(self.actionRun_SilenceDetect_multiple_scan)
        self.menuScanners.addSeparator()
        self.menuScanners.addAction(self.actionRun_FreezeDetect_selected_scan)
        self.menuScanners.addAction(self.actionRun_FreezeDetect_single_scan)
        self.menuScanners.addAction(self.actionRun_FreezeDetect_multiple_scan)
        self.menuScanners.addSeparator()
        self.menuScanners.addAction(self.actionRun_Full_selected_scan)
        self.menuScanners.addAction(self.actionRun_Full_single_scan)
        self.menuScanners.addAction(self.actionRun_Full_multiple_scan)
        self.menuScanners.addSeparator()
        self.menuScanners.addAction(self.actionRun_Background_Loudness_scan)
        self.menuScanners.addAction(self.actionRun_Background_BlackDetect_scan)
        self.menuScanners.addAction(self.actionRun_Background_SilenceDetect_scan)
        self.menuScanners.addAction(self.actionRun_Background_FreezeDetect_scan)
        self.menuScanners.addAction(self.actionRun_Background_Full_scan)
        self.menuDataBase.addAction(self.actionDelete_file_entry)
        self.menuDataBase.addAction(self.actionCreate_file_entry)
        self.menuDataBase.addAction(self.actionReset_scan_result_for_file)
        self.menuDataBase.addAction(self.actionDelete_from_db)
        self.menuDataBase.addAction(self.actionCreate_column)
        self.menuDataBase.addAction(self.actionDelete_column)
        self.menuDataBase.addAction(self.actionUpdate_data_for_file)
        self.menuDataBase.addSeparator()
        self.menuDataBase.addAction(self.actionShow_all_tables)
        self.menuDataBase.addAction(self.actionClear_table)
        self.menuDataBase.addAction(self.actionCreate_table)
        self.menuDataBase.addSeparator()
        self.menuDataBase.addAction(self.actionCreate_db)
        self.menuDataBase.addAction(self.actionDelete_DB)
        self.menuDataBase.addAction(self.actionConnect_to_DB)
        self.menuDataBase.addAction(self.actionClose_DB)
        self.menuDataBase.addAction(self.actionCheck_DB)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"VideoINFO", None))
        self.actionAdd_files.setText(QCoreApplication.translate("MainWindow", u"Add files", None))
#if QT_CONFIG(shortcut)
        self.actionAdd_files.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete_selected_file.setText(QCoreApplication.translate("MainWindow", u"Delete selected file", None))
#if QT_CONFIG(shortcut)
        self.actionDelete_selected_file.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionPlay_selected_file.setText(QCoreApplication.translate("MainWindow", u"Play selected file", None))
#if QT_CONFIG(shortcut)
        self.actionPlay_selected_file.setShortcut(QCoreApplication.translate("MainWindow", u"Space", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_destination_folder.setText(QCoreApplication.translate("MainWindow", u"Open destination folder", None))
#if QT_CONFIG(shortcut)
        self.actionOpen_destination_folder.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_db_editor.setText(QCoreApplication.translate("MainWindow", u"Switch mode", None))
        self.actionShow_Loudness.setText(QCoreApplication.translate("MainWindow", u"Hide Loudness meter", None))
        self.actionShow_Details.setText(QCoreApplication.translate("MainWindow", u"Hide Details", None))
        self.actionRun_Loudness_single_scan.setText(QCoreApplication.translate("MainWindow", u"Run Loudness single scan", None))
        self.actionRun_Loudness_multiple_scan.setText(QCoreApplication.translate("MainWindow", u"Run Loudness multiple scan", None))
        self.actionRun_BlackDetect_single_scan.setText(QCoreApplication.translate("MainWindow", u"Run BlackDetect single scan", None))
        self.actionRun_BlackDetect_multiple_scan.setText(QCoreApplication.translate("MainWindow", u"Run BlackDetect multiple scan", None))
        self.actionRun_SilenceDetect_single_scan.setText(QCoreApplication.translate("MainWindow", u"Run SilenceDetect single scan", None))
        self.actionRun_SilenceDetect_multiple_scan.setText(QCoreApplication.translate("MainWindow", u"Run SilenceDetect multiple scan", None))
        self.actionRun_FreezeDetect_single_scan.setText(QCoreApplication.translate("MainWindow", u"Run FreezeDetect single scan", None))
        self.actionRun_FreezeDetect_multiple_scan.setText(QCoreApplication.translate("MainWindow", u"Run FreezeDetect multiple scan", None))
        self.actionRun_Full_single_scan.setText(QCoreApplication.translate("MainWindow", u"Run Full single scan", None))
        self.actionRun_Full_multiple_scan.setText(QCoreApplication.translate("MainWindow", u"Run Full multiple scan", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(shortcut)
        self.actionSettings.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionExport_table_to_Excel.setText(QCoreApplication.translate("MainWindow", u"Export table to Excel", None))
        self.actionExport_all_db_to_Excel.setText(QCoreApplication.translate("MainWindow", u"Export all db to Excel", None))
#if QT_CONFIG(shortcut)
        self.actionExport_all_db_to_Excel.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+E", None))
#endif // QT_CONFIG(shortcut)
        self.actionOpen_VideoPlayer.setText(QCoreApplication.translate("MainWindow", u"Open VideoPlayer", None))
        self.actionRun_Background_Loudness_scan.setText(QCoreApplication.translate("MainWindow", u"Run Background Loudness scan", None))
#if QT_CONFIG(shortcut)
        self.actionRun_Background_Loudness_scan.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionRun_Background_BlackDetect_scan.setText(QCoreApplication.translate("MainWindow", u"Run Background BlackDetect scan", None))
        self.actionRun_Background_SilenceDetect_scan.setText(QCoreApplication.translate("MainWindow", u"Run Background SilenceDetect scan", None))
        self.actionRun_Background_FreezeDetect_scan.setText(QCoreApplication.translate("MainWindow", u"Run Background FreezeDetect scan", None))
        self.actionRun_Background_Full_scan.setText(QCoreApplication.translate("MainWindow", u"Run Background Full scan", None))
        self.actionClear_table.setText(QCoreApplication.translate("MainWindow", u"Clear table", None))
        self.actionShow_all_tables.setText(QCoreApplication.translate("MainWindow", u"Show all tables", None))
        self.actionConnect_to_DB.setText(QCoreApplication.translate("MainWindow", u"Connect to DB", None))
        self.actionClose_DB.setText(QCoreApplication.translate("MainWindow", u"Close DB", None))
        self.actionDelete_file_entry.setText(QCoreApplication.translate("MainWindow", u"Delete file entry", None))
        self.actionCreate_file_entry.setText(QCoreApplication.translate("MainWindow", u"Create file entry", None))
        self.actionReset_scan_result_for_file.setText(QCoreApplication.translate("MainWindow", u"Reset scan result for files", None))
#if QT_CONFIG(shortcut)
        self.actionReset_scan_result_for_file.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Shift+R", None))
#endif // QT_CONFIG(shortcut)
        self.actionCreate_column.setText(QCoreApplication.translate("MainWindow", u"Create column", None))
        self.actionDelete_column.setText(QCoreApplication.translate("MainWindow", u"Delete column", None))
        self.actionUpdate_data_for_file.setText(QCoreApplication.translate("MainWindow", u"Update data fo file...", None))
        self.actionCreate_table.setText(QCoreApplication.translate("MainWindow", u"Create table", None))
        self.actionCreate_db.setText(QCoreApplication.translate("MainWindow", u"Create DB", None))
        self.actionDelete_DB.setText(QCoreApplication.translate("MainWindow", u"Delete DB", None))
        self.actionDelete_from_db.setText(QCoreApplication.translate("MainWindow", u"Delete selected  files from DB", None))
        self.actionSelected_files.setText(QCoreApplication.translate("MainWindow", u"Selected files", None))
        self.actionRun_Loudness_selected_scan.setText(QCoreApplication.translate("MainWindow", u"Run Loudness selected scan", None))
        self.actionRun_BlackDetect_selected_scan.setText(QCoreApplication.translate("MainWindow", u"Run BlackDetect selected scan", None))
        self.actionRun_SilenceDetect_selected_scan.setText(QCoreApplication.translate("MainWindow", u"Run SilenceDetect selected scan", None))
        self.actionRun_FreezeDetect_selected_scan.setText(QCoreApplication.translate("MainWindow", u"Run FreezeDetect selected scan", None))
        self.actionRun_Full_selected_scan.setText(QCoreApplication.translate("MainWindow", u"Run Full selected scan", None))
        self.actionChoose_default_directory.setText(QCoreApplication.translate("MainWindow", u"Choose default directory", None))
        self.actionCheck_DB.setText(QCoreApplication.translate("MainWindow", u"Check DB", None))
#if QT_CONFIG(tooltip)
        self.switchToolButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0434\u0440\u043e\u0431\u043d\u0435\u0435", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.switchToolButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.switchToolButton.setText("")
#if QT_CONFIG(tooltip)
        self.move_to_tableButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.move_to_tableButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.delete_from_dbButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.delete_from_dbButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.move_to_dbButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.move_to_dbButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.addButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u0444\u0430\u0439\u043b", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.addButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.addButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.delButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0441\u0442\u0440\u043e\u043a\u0443 \u0438\u0437 \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
#endif // QT_CONFIG(tooltip)
        self.delButton.setText(QCoreApplication.translate("MainWindow", u"Del", None))
#if QT_CONFIG(tooltip)
        self.playButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0412\u043e\u0441\u043f\u0440\u043e\u0438\u0437\u0432\u0435\u0441\u0442\u0438 \u0444\u0430\u0439\u043b", None))
#endif // QT_CONFIG(tooltip)
        self.playButton.setText(QCoreApplication.translate("MainWindow", u"Play", None))
#if QT_CONFIG(tooltip)
        self.openButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043f\u0430\u043f\u043a\u0443 \u0441 \u0444\u0430\u0439\u043b\u043e\u043c", None))
#endif // QT_CONFIG(tooltip)
        self.openButton.setText(QCoreApplication.translate("MainWindow", u"Open", None))
#if QT_CONFIG(tooltip)
        self.r128DtctButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u0418\u0437\u043c\u0435\u0440\u0435\u043d\u0438\u0435 \u0443\u0440\u043e\u0432\u043d\u044f \u0433\u0440\u043e\u043c\u043a\u043e\u0441\u0442\u0438", None))
#endif // QT_CONFIG(tooltip)
        self.r128DtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.queueButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
#if QT_CONFIG(tooltip)
        self.blckDtctButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u0447\u0451\u0440\u043d\u043e\u0433\u043e \u043f\u043e\u043b\u044f", None))
#endif // QT_CONFIG(tooltip)
        self.blckDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
#if QT_CONFIG(tooltip)
        self.slncDtctButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u043f\u0443\u0441\u043a\u043e\u0432 \u0437\u0432\u0443\u043a\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.slncDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
#if QT_CONFIG(tooltip)
        self.frzDtctButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0438\u0435 \u0441\u0442\u043e\u043f-\u043a\u0430\u0434\u0440\u043e\u0432", None))
#endif // QT_CONFIG(tooltip)
        self.frzDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
#if QT_CONFIG(tooltip)
        self.fullDtctButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u043b\u043d\u043e\u0435 \u0441\u043a\u0430\u043d\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.fullDtctButton.setText(QCoreApplication.translate("MainWindow", u"Wave", None))
        self.migrateButton.setText(QCoreApplication.translate("MainWindow", u"Copy/Rename", None))
#if QT_CONFIG(shortcut)
        self.migrateButton.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+M", None))
#endif // QT_CONFIG(shortcut)
        self.exportButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
#if QT_CONFIG(tooltip)
        self.switchModeButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0440\u0435\u0436\u0438\u043c \u0442\u0430\u0431\u043b\u0438\u0446\u044b", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.switchModeButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.switchModeButton.setText(QCoreApplication.translate("MainWindow", u"Add", None))
#if QT_CONFIG(tooltip)
        self.settingsButton.setToolTip(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
#endif // QT_CONFIG(tooltip)
        self.settingsButton.setText(QCoreApplication.translate("MainWindow", u"Export", None))
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
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuScanners.setTitle(QCoreApplication.translate("MainWindow", u"Scanners", None))
        self.menuDataBase.setTitle(QCoreApplication.translate("MainWindow", u"DataBase", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

