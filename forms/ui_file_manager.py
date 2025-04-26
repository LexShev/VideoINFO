# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_file_manager.ui'
##
## Created by: Qt User Interface Compiler version 6.6.3
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QProgressBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QToolButton, QTreeView,
    QVBoxLayout, QWidget)
import icons_rc

class Ui_FileManager(object):
    def setupUi(self, FileManager):
        if not FileManager.objectName():
            FileManager.setObjectName(u"FileManager")
        FileManager.resize(1350, 900)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FileManager.sizePolicy().hasHeightForWidth())
        FileManager.setSizePolicy(sizePolicy)
        FileManager.setStyleSheet(u"background-color: rgb(40, 40, 45);\n"
"font-family: Noto Sans;\n"
"")
        self.gridLayout_2 = QGridLayout(FileManager)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_rename = QHBoxLayout()
        self.horizontalLayout_rename.setObjectName(u"horizontalLayout_rename")
        self.groupBox = QGroupBox(FileManager)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setStyleSheet(u"color: white")
        self.verticalLayout_9 = QVBoxLayout(self.groupBox)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.mask_full = QLineEdit(self.groupBox)
        self.mask_full.setObjectName(u"mask_full")

        self.verticalLayout_9.addWidget(self.mask_full)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.mask_name = QPushButton(self.groupBox)
        self.mask_name.setObjectName(u"mask_name")
        self.mask_name.setLayoutDirection(Qt.LeftToRight)
        self.mask_name.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout.addWidget(self.mask_name)

        self.mask_counter = QPushButton(self.groupBox)
        self.mask_counter.setObjectName(u"mask_counter")
        self.mask_counter.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout.addWidget(self.mask_counter)

        self.mask_date = QPushButton(self.groupBox)
        self.mask_date.setObjectName(u"mask_date")
        self.mask_date.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout.addWidget(self.mask_date)

        self.mask_time = QPushButton(self.groupBox)
        self.mask_time.setObjectName(u"mask_time")
        self.mask_time.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout.addWidget(self.mask_time)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_save_mask_preset = QPushButton(self.groupBox)
        self.btn_save_mask_preset.setObjectName(u"btn_save_mask_preset")
        self.btn_save_mask_preset.setLayoutDirection(Qt.LeftToRight)
        self.btn_save_mask_preset.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_2.addWidget(self.btn_save_mask_preset)

        self.btn_load_mask_preset = QPushButton(self.groupBox)
        self.btn_load_mask_preset.setObjectName(u"btn_load_mask_preset")
        self.btn_load_mask_preset.setLayoutDirection(Qt.LeftToRight)
        self.btn_load_mask_preset.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_2.addWidget(self.btn_load_mask_preset)

        self.comboBox_preset = QComboBox(self.groupBox)
        self.comboBox_preset.setObjectName(u"comboBox_preset")
        self.comboBox_preset.setMinimumSize(QSize(350, 0))

        self.horizontalLayout_2.addWidget(self.comboBox_preset)


        self.verticalLayout_9.addLayout(self.horizontalLayout_2)


        self.horizontalLayout_rename.addWidget(self.groupBox)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(FileManager)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setStyleSheet(u"color: white")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.mask_search = QLineEdit(self.groupBox_2)
        self.mask_search.setObjectName(u"mask_search")

        self.horizontalLayout_3.addWidget(self.mask_search)


        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.groupBox_2)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.mask_replace = QLineEdit(self.groupBox_2)
        self.mask_replace.setObjectName(u"mask_replace")

        self.horizontalLayout_4.addWidget(self.mask_replace)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)


        self.verticalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(FileManager)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setStyleSheet(u"color: white")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.comboBox_upper = QComboBox(self.groupBox_4)
        self.comboBox_upper.setObjectName(u"comboBox_upper")

        self.gridLayout_4.addWidget(self.comboBox_upper, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.groupBox_4)


        self.horizontalLayout_rename.addLayout(self.verticalLayout_2)

        self.define_counter_group = QGroupBox(FileManager)
        self.define_counter_group.setObjectName(u"define_counter_group")
        self.define_counter_group.setStyleSheet(u"color: white")
        self.verticalLayout_8 = QVBoxLayout(self.define_counter_group)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_5 = QLabel(self.define_counter_group)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_5.addWidget(self.label_5)

        self.spinBox_start = QSpinBox(self.define_counter_group)
        self.spinBox_start.setObjectName(u"spinBox_start")
        self.spinBox_start.setMinimum(1)
        self.spinBox_start.setMaximum(999999)

        self.horizontalLayout_5.addWidget(self.spinBox_start)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_6 = QLabel(self.define_counter_group)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_6.addWidget(self.label_6)

        self.spinBox_step = QSpinBox(self.define_counter_group)
        self.spinBox_step.setObjectName(u"spinBox_step")
        self.spinBox_step.setMinimum(0)
        self.spinBox_step.setValue(1)

        self.horizontalLayout_6.addWidget(self.spinBox_step)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_7 = QLabel(self.define_counter_group)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_7.addWidget(self.label_7)

        self.comboBox_digits = QComboBox(self.define_counter_group)
        self.comboBox_digits.setObjectName(u"comboBox_digits")

        self.horizontalLayout_7.addWidget(self.comboBox_digits)


        self.verticalLayout_8.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_rename.addWidget(self.define_counter_group)


        self.verticalLayout.addLayout(self.horizontalLayout_rename)

        self.horizontalLayout_work = QHBoxLayout()
        self.horizontalLayout_work.setObjectName(u"horizontalLayout_work")
        self.verticalLayout_source = QVBoxLayout()
        self.verticalLayout_source.setSpacing(0)
        self.verticalLayout_source.setObjectName(u"verticalLayout_source")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(1)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(1, -1, 1, -1)
        self.source_tub1 = QPushButton(FileManager)
        self.source_tub1.setObjectName(u"source_tub1")
        self.source_tub1.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_13.addWidget(self.source_tub1)

        self.source_tub2 = QPushButton(FileManager)
        self.source_tub2.setObjectName(u"source_tub2")
        self.source_tub2.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_13.addWidget(self.source_tub2)

        self.source_tub3 = QPushButton(FileManager)
        self.source_tub3.setObjectName(u"source_tub3")
        self.source_tub3.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_13.addWidget(self.source_tub3)

        self.source_tub4 = QPushButton(FileManager)
        self.source_tub4.setObjectName(u"source_tub4")
        self.source_tub4.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_13.addWidget(self.source_tub4)

        self.source_tub5 = QPushButton(FileManager)
        self.source_tub5.setObjectName(u"source_tub5")
        self.source_tub5.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_13.addWidget(self.source_tub5)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_2)


        self.verticalLayout_source.addLayout(self.horizontalLayout_13)

        self.listWidget_source = QListWidget(FileManager)
        self.listWidget_source.setObjectName(u"listWidget_source")
        self.listWidget_source.setAlternatingRowColors(True)
        self.listWidget_source.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.listWidget_source.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget_source.setLayoutMode(QListView.SinglePass)
        self.listWidget_source.setSortingEnabled(True)

        self.verticalLayout_source.addWidget(self.listWidget_source)

        self.treeView_source = QTreeView(FileManager)
        self.treeView_source.setObjectName(u"treeView_source")
        self.treeView_source.setSelectionMode(QAbstractItemView.ContiguousSelection)

        self.verticalLayout_source.addWidget(self.treeView_source)


        self.horizontalLayout_work.addLayout(self.verticalLayout_source)

        self.Buttons = QFrame(FileManager)
        self.Buttons.setObjectName(u"Buttons")
        self.Buttons.setStyleSheet(u"color: rgb(146, 146, 146);\n"
"border: 0px;")
        self.verticalLayout_buttons = QVBoxLayout(self.Buttons)
        self.verticalLayout_buttons.setObjectName(u"verticalLayout_buttons")
        self.verticalLayout_buttons.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_buttons.addItem(self.verticalSpacer_2)

        self.rename_Button = QToolButton(self.Buttons)
        self.rename_Button.setObjectName(u"rename_Button")
        self.rename_Button.setMinimumSize(QSize(40, 30))
        self.rename_Button.setMaximumSize(QSize(40, 30))
        self.rename_Button.setBaseSize(QSize(40, 30))
        self.rename_Button.setStyleSheet(u"QToolButton{\n"
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
        icon = QIcon()
        icon.addFile(u":/bl_img/icons/text_rotation_none_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.rename_Button.setIcon(icon)
        self.rename_Button.setIconSize(QSize(20, 35))
        self.rename_Button.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.rename_Button)

        self.undo_rename_Button = QToolButton(self.Buttons)
        self.undo_rename_Button.setObjectName(u"undo_rename_Button")
        self.undo_rename_Button.setMinimumSize(QSize(40, 30))
        self.undo_rename_Button.setMaximumSize(QSize(40, 30))
        self.undo_rename_Button.setBaseSize(QSize(40, 30))
        self.undo_rename_Button.setStyleSheet(u"QToolButton{\n"
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
        icon1.addFile(u":/bl_img/icons/repartition_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.undo_rename_Button.setIcon(icon1)
        self.undo_rename_Button.setIconSize(QSize(20, 35))
        self.undo_rename_Button.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.undo_rename_Button)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_buttons.addItem(self.verticalSpacer_3)

        self.copy_to_dbButton = QToolButton(self.Buttons)
        self.copy_to_dbButton.setObjectName(u"copy_to_dbButton")
        self.copy_to_dbButton.setMinimumSize(QSize(40, 30))
        self.copy_to_dbButton.setMaximumSize(QSize(40, 30))
        self.copy_to_dbButton.setBaseSize(QSize(40, 30))
        self.copy_to_dbButton.setStyleSheet(u"QToolButton{\n"
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
        icon2.addFile(u":/bl_img/icons/arrow_forward_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.copy_to_dbButton.setIcon(icon2)
        self.copy_to_dbButton.setIconSize(QSize(20, 35))
        self.copy_to_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.copy_to_dbButton)

        self.move_to_dbButton = QToolButton(self.Buttons)
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
        icon3 = QIcon()
        icon3.addFile(u":/bl_img/icons/keyboard_tab_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.move_to_dbButton.setIcon(icon3)
        self.move_to_dbButton.setIconSize(QSize(20, 35))
        self.move_to_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.move_to_dbButton)

        self.copy_from_dbButton = QToolButton(self.Buttons)
        self.copy_from_dbButton.setObjectName(u"copy_from_dbButton")
        self.copy_from_dbButton.setEnabled(True)
        self.copy_from_dbButton.setMinimumSize(QSize(40, 30))
        self.copy_from_dbButton.setMaximumSize(QSize(40, 30))
        self.copy_from_dbButton.setBaseSize(QSize(40, 30))
        self.copy_from_dbButton.setStyleSheet(u"QToolButton{\n"
"color: rgb(255, 255, 255);\n"
"background-color:rgba(255,255,255,30);\n"
"border: 1px solid rgba(255,255,255,40);\n"
"border-radius:3px;\n"
"}\n"
"QToolButton:hover{\n"
"background-color:rgba(255,255,255,50);\n"
"}\n"
"QToolButton:pressed{\n"
"background-color:rgba(255,255,255,70);\n"
"}")
        icon4 = QIcon()
        icon4.addFile(u":/bl_img/icons/arrow_back_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.copy_from_dbButton.setIcon(icon4)
        self.copy_from_dbButton.setIconSize(QSize(20, 35))
        self.copy_from_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.copy_from_dbButton)

        self.move_from_dbButton = QToolButton(self.Buttons)
        self.move_from_dbButton.setObjectName(u"move_from_dbButton")
        self.move_from_dbButton.setMinimumSize(QSize(40, 30))
        self.move_from_dbButton.setMaximumSize(QSize(40, 30))
        self.move_from_dbButton.setBaseSize(QSize(40, 30))
        self.move_from_dbButton.setStyleSheet(u"QToolButton{\n"
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
        icon5.addFile(u":/bl_img/icons/keyboard_tab_rtl_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.move_from_dbButton.setIcon(icon5)
        self.move_from_dbButton.setIconSize(QSize(20, 35))
        self.move_from_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)

        self.verticalLayout_buttons.addWidget(self.move_from_dbButton)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_buttons.addItem(self.verticalSpacer)


        self.horizontalLayout_work.addWidget(self.Buttons)

        self.verticalLayout_destination = QVBoxLayout()
        self.verticalLayout_destination.setSpacing(0)
        self.verticalLayout_destination.setObjectName(u"verticalLayout_destination")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(1, -1, 1, -1)
        self.destination_tub1 = QPushButton(FileManager)
        self.destination_tub1.setObjectName(u"destination_tub1")
        self.destination_tub1.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_8.addWidget(self.destination_tub1)

        self.destination_tub2 = QPushButton(FileManager)
        self.destination_tub2.setObjectName(u"destination_tub2")
        self.destination_tub2.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_8.addWidget(self.destination_tub2)

        self.destination_tub3 = QPushButton(FileManager)
        self.destination_tub3.setObjectName(u"destination_tub3")
        self.destination_tub3.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_8.addWidget(self.destination_tub3)

        self.destination_tub4 = QPushButton(FileManager)
        self.destination_tub4.setObjectName(u"destination_tub4")
        self.destination_tub4.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_8.addWidget(self.destination_tub4)

        self.destination_tub5 = QPushButton(FileManager)
        self.destination_tub5.setObjectName(u"destination_tub5")
        self.destination_tub5.setStyleSheet(u"QPushButton{\n"
"color: white;\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_8.addWidget(self.destination_tub5)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)


        self.verticalLayout_destination.addLayout(self.horizontalLayout_8)

        self.listWidget_destination = QListWidget(FileManager)
        self.listWidget_destination.setObjectName(u"listWidget_destination")
        self.listWidget_destination.setAlternatingRowColors(True)
        self.listWidget_destination.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.listWidget_destination.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listWidget_destination.setSortingEnabled(True)

        self.verticalLayout_destination.addWidget(self.listWidget_destination)

        self.treeView_destination = QTreeView(FileManager)
        self.treeView_destination.setObjectName(u"treeView_destination")
        self.treeView_destination.setSelectionMode(QAbstractItemView.ContiguousSelection)

        self.verticalLayout_destination.addWidget(self.treeView_destination)


        self.horizontalLayout_work.addLayout(self.verticalLayout_destination)


        self.verticalLayout.addLayout(self.horizontalLayout_work)

        self.progressBar = QProgressBar(FileManager)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimumSize(QSize(700, 0))
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)


        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)


        self.retranslateUi(FileManager)

        self.comboBox_digits.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(FileManager)
    # setupUi

    def retranslateUi(self, FileManager):
        FileManager.setWindowTitle(QCoreApplication.translate("FileManager", u"File manager", None))
        self.groupBox.setTitle(QCoreApplication.translate("FileManager", u"Mask for file name", None))
        self.mask_full.setText(QCoreApplication.translate("FileManager", u"[N]", None))
        self.mask_name.setText(QCoreApplication.translate("FileManager", u"[N] Name", None))
        self.mask_counter.setText(QCoreApplication.translate("FileManager", u"[C] Counter", None))
        self.mask_date.setText(QCoreApplication.translate("FileManager", u"[dd-mm-yy] Date", None))
        self.mask_time.setText(QCoreApplication.translate("FileManager", u"[hh:mm:ss] Time", None))
        self.btn_save_mask_preset.setText(QCoreApplication.translate("FileManager", u"Save", None))
        self.btn_load_mask_preset.setText(QCoreApplication.translate("FileManager", u"Load", None))
        self.comboBox_preset.setCurrentText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("FileManager", u"Search and replace", None))
        self.label_3.setText(QCoreApplication.translate("FileManager", u"Search:", None))
        self.mask_search.setText("")
        self.label_4.setText(QCoreApplication.translate("FileManager", u"Replace:", None))
        self.mask_replace.setText("")
        self.groupBox_4.setTitle(QCoreApplication.translate("FileManager", u"Upper/lowercase", None))
        self.define_counter_group.setTitle(QCoreApplication.translate("FileManager", u"Define counter [C]", None))
        self.label_5.setText(QCoreApplication.translate("FileManager", u"Start at:", None))
        self.label_6.setText(QCoreApplication.translate("FileManager", u"Step by:", None))
        self.label_7.setText(QCoreApplication.translate("FileManager", u"Digits:", None))
        self.source_tub1.setText(QCoreApplication.translate("FileManager", u"tub1", None))
        self.source_tub2.setText(QCoreApplication.translate("FileManager", u"tub2", None))
        self.source_tub3.setText(QCoreApplication.translate("FileManager", u"tub3", None))
        self.source_tub4.setText(QCoreApplication.translate("FileManager", u"tub4", None))
        self.source_tub5.setText(QCoreApplication.translate("FileManager", u"tub5", None))
#if QT_CONFIG(tooltip)
        self.rename_Button.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.rename_Button.setText(QCoreApplication.translate("FileManager", u"Open", None))
#if QT_CONFIG(tooltip)
        self.undo_rename_Button.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.undo_rename_Button.setText(QCoreApplication.translate("FileManager", u"Open", None))
#if QT_CONFIG(tooltip)
        self.copy_to_dbButton.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.copy_to_dbButton.setText(QCoreApplication.translate("FileManager", u"Open", None))
#if QT_CONFIG(tooltip)
        self.move_to_dbButton.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.move_to_dbButton.setText(QCoreApplication.translate("FileManager", u"Open", None))
#if QT_CONFIG(tooltip)
        self.copy_from_dbButton.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.copy_from_dbButton.setText(QCoreApplication.translate("FileManager", u"Open", None))
#if QT_CONFIG(tooltip)
        self.move_from_dbButton.setToolTip(QCoreApplication.translate("FileManager", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u0432 \u0442\u0430\u0431\u043b\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.move_from_dbButton.setText(QCoreApplication.translate("FileManager", u"Open", None))
        self.destination_tub1.setText(QCoreApplication.translate("FileManager", u"tub1", None))
        self.destination_tub2.setText(QCoreApplication.translate("FileManager", u"tub2", None))
        self.destination_tub3.setText(QCoreApplication.translate("FileManager", u"tub3", None))
        self.destination_tub4.setText(QCoreApplication.translate("FileManager", u"tub4", None))
        self.destination_tub5.setText(QCoreApplication.translate("FileManager", u"tub5", None))
    # retranslateUi

