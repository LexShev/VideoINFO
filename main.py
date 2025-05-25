from __future__ import annotations

import ast
import datetime
import hashlib
import shutil
import os
import sqlite3
import subprocess
import sys
import configparser
from fractions import Fraction
from math import isclose

# pip install pyqtdarktheme
import qdarktheme
# pip install pyside6
from PySide6 import QtWidgets, QtSql, QtGui
from PySide6.QtCore import Qt, QUrl, QSize, QThreadPool, QSortFilterProxyModel, QAbstractTableModel, QModelIndex, QDir, \
    QCoreApplication
from PySide6.QtGui import QColor, QPixmap, QIcon, qRgb, QKeySequence, QIntValidator, QFont
from PySide6.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QTableWidgetItem, QSlider, \
    QGraphicsColorizeEffect, QProgressDialog, \
    QDialog, QLabel, QComboBox, QToolBar, QLineEdit, QPushButton, QMessageBox, QDialogButtonBox, QVBoxLayout, QMenu, \
    QListWidget, QWidget, QProgressBar

from create_mongo_table import MongoTableModel
from ffmpeg_worker import FFmpegWorker
from ffprobe_single_scan import FFprobeMongo
from ffprobe_worker import FFprobeScan, R128Scan, BlackDetect, SilenceDetect, FreezeDetect
from mongo_connection import MongoDB
from settings import Settings
from sqlite_connection import DataLite
from posql_connection import DataPos
from ffprobe_main import Info
from forms.ui_db_settings import Ui_DB_Settings
from forms.ui_videoinfo import Ui_MainWindow
from forms.ui_confirm_action import Ui_ConfirmDialog
from forms.ui_file_manager import Ui_FileManager
from ffmpeg_mongo import R128
from video_player import VideoInfoPlayer

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))


def now():
    return datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def convert_fram_duration(file_info):
    try:
        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        format = file_info.get('format')
        f_duration = format.get('duration')

        v_frame_rate = video[0].get('r_frame_rate')
        f_frame_rate = format.get('r_frame_rate')

        # print(v_frame_rate, type(eval(v_frame_rate)), f_frame_rate, type(eval(f_frame_rate)), f_duration, type(float(f_duration)))
        if v_frame_rate:
            return float(f_duration) * float(Fraction(v_frame_rate))
        else:
            return float(f_duration) * float(Fraction(f_frame_rate))
    except Exception as e:
        print(e)
        return 1

def convert_fps(data):
    try:
        fps = eval(data)
        unit = 'fps'
        if fps % 1 == 0:
            data = f'{int(fps)} {unit}'
        else:
            data = f'{round(fps, 3)} {unit}'
    except ZeroDivisionError:
        data = '0'
    return data


def convert_khz(data):
    try:
        val = f'{float(data) / 1000} kHz'
        return val
    except Exception:
        pass


def convert_bytes(size, unit):
    try:
        # 2**10 = 1024
        size = int(size)
        power = (2 ** 10)
        n = 0
        labels = ['', 'K', 'M', 'G', 'T']
        while size > power:
            size /= power
            n += 1
        val = f'{round(size, 2)} {labels[n]}{unit}'
        return val
    except Exception as e:
        print(e)
        return size

def convert_duration(seconds, fps='25/1'):
    try:
        seconds = float(seconds)
        fps = eval(fps)
        hh = int(seconds // 3600)
        mm = int((seconds % 3600) // 60)
        ss = int((seconds % 3600) % 60 // 1)
        ff = int(seconds % 1 * fps)
        conv_data = f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'
        return conv_data
    except Exception as e:
        print(e)
        return ''

def convert_duration_sec(data, fps=25):
    hh = int(data // 3600)
    mm = int((data % 3600) // 60)
    ss = int((data % 3600) % 60 // 1)
    ff = int(data % 1 * fps)
    # data /= sec
    conv_data = f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'

    return conv_data


def convert_tf_to_sec(time):
    hh = int(time.split(':')[0])
    mm = int(time.split(':')[1])
    ss = int(time.split(':')[2])
    sec = (hh*3600)+(mm*60)+ss
    return sec

class SingleProgressDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Processing...")
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(650, 150)
        self.setStyleSheet(
            "QPushButton {color: white; background-color:rgba(255,255,255,30);"
            "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
            "QPushButton:hover {background-color:rgba(255,255,255,50);}"
            "QPushButton:pressed{background-color:rgba(255,255,255,70);}"
        )
        layout = QVBoxLayout(self)
        self.label = QLabel('Start scan')
        self.label.setAlignment(Qt.AlignCenter)

        self.single_progress_bar = QProgressBar()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(70, 30)

        layout.addWidget(self.label)
        layout.addWidget(self.single_progress_bar)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)


class DoubleProgressDialog(QDialog):
    def  __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Processing...")
        self.setWindowModality(Qt.WindowModal)
        self.setFixedSize(650, 200)
        self.setStyleSheet(
            "QPushButton {color: white; background-color:rgba(255,255,255,30);"
            "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
            "QPushButton:hover {background-color:rgba(255,255,255,50);}"
            "QPushButton:pressed{background-color:rgba(255,255,255,70);}"
        )

        # Создаем layout
        layout = QVBoxLayout(self)

        # Первый прогрессбар с меткой
        self.label_01 = QLabel("Current task:")
        self.label_01.setAlignment(Qt.AlignCenter)
        self.progress_01 = QProgressBar()

        # Второй прогрессбар с меткой
        self.label_02 = QLabel("Total progress:")
        self.label_02.setAlignment(Qt.AlignCenter)
        self.progress_02 = QProgressBar()

        # Кнопка отмены
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(70, 30)

        # self.cancel_button.clicked.connect(self.reject)

        # Добавляем виджеты в layout
        layout.addWidget(self.label_01)
        layout.addWidget(self.progress_01)
        layout.addWidget(self.label_02)
        layout.addWidget(self.progress_02)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

        # Настройка прогрессбаров
        self.progress_01.setRange(0, 100)
        self.progress_02.setRange(0, 100)

class VideoInfo(QMainWindow):

    def __init__(self):
        super(VideoInfo, self).__init__()

        self.progress_dialog = None
        self.close_progress_dialog_btn = None
        self.ffmpeg_scanners = []
        self.thread_pool = QThreadPool()
        self.thread_pool.setMaxThreadCount(1)
        self.double_progress_bar = DoubleProgressDialog(parent=self)
        self.double_progress_bar.setModal(False)
        self.double_progress_bar.cancel_button.clicked.connect(self.stop_processing)

        self.ffprobe_scanners = []
        self.thread_ffprobe = QThreadPool()
        self.thread_ffprobe.setMaxThreadCount(1)
        self.single_progress_dialog = SingleProgressDialog(parent=self)
        self.single_progress_dialog.cancel_button.clicked.connect(self.stop_single_processing)

        self.mongo = MongoDB()
        self.settings = Settings()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


        self.video_info_player = None

        self.table_mode = True
        self.switch_tool_flag = False

        self.init_table_widget()

        # colors
        self.red_light = QColor(205, 90, 80)
        self.red_dark = QColor(195, 75, 60)  # C34B3C
        self.yell_light = QColor(230, 165, 45)
        self.yell_dark = QColor(230, 145, 25)
        self.green_light = QColor(88, 145, 39)
        self.green_dark = QColor(79, 130, 35)
        self.white = QColor(255, 255, 255)

        self.ui.switchToolButton.clicked.connect(self.switch_tools)
        self.ui.switchToolButton.setToolTip('Подробнее')
        self.colorizeEffect_wt(self.ui.switchToolButton)

        self.ui.tableWidget_01.horizontalHeader().sectionClicked.connect(self.error_highlight)
        self.ui.tableWidget_01.clicked.connect(self.click_table_w)
        # self.ui.tableWidget_01.doubleClicked.connect(self.double_click_table)
        self.ui.tableWidget_01.doubleClicked.connect(self.double_click_video_player)

        self.ui.addButton.clicked.connect(self.prepare_table_01)

        self.ui.addButton.setToolTip('Добавить файлы')
        self.colorizeEffect_wt(self.ui.addButton)
        self.ui.delButton.clicked.connect(self.del_selected_rows)
        self.ui.delButton.setToolTip('Удалить выбранное')
        self.ui.delete_from_dbButton.hide()
        self.ui.delete_from_dbButton.clicked.connect(self.del_file_from_db)
        self.colorizeEffect_wt(self.ui.delete_from_dbButton)
        self.ui.move_to_dbButton.setToolTip('Удалить выбранное из базы данных')
        self.ui.move_to_dbButton.clicked.connect(self.move_to_db)
        # self.ui.move_to_dbButton.clicked.connect(self.del_file_from_db)
        self.ui.move_to_dbButton.hide()
        self.colorizeEffect_wt(self.ui.move_to_dbButton)
        self.ui.move_to_dbButton.setToolTip('Переместить выбранное в основную базу данных')
        self.ui.playButton.clicked.connect(self.play_selected)
        self.ui.playButton.setToolTip('Воспроизвести выбранное')
        self.ui.openButton.clicked.connect(self.open_folder)
        self.ui.openButton.setToolTip('Открыть папку с файлом')
        self.ui.move_to_tableButton.clicked.connect(self.move_to_table_01)
        self.ui.move_to_tableButton.setToolTip('Открыть в таблице')
        self.colorizeEffect_wt(self.ui.move_to_tableButton)
        self.ui.move_to_tableButton.hide()
        self.ui.exportButton.clicked.connect(self.export_db_xlsx)
        self.ui.exportButton.setToolTip('Экспорт базы данных в Excel')

        self.ui.r128DtctButton.clicked.connect(self.scan_loudnorm)
        self.ui.r128DtctButton.setToolTip('Сканировать выбранное R128')
        self.ui.blckDtctButton.clicked.connect(self.scan_black_detect)
        self.ui.blckDtctButton.setToolTip('Сканировать выбранное Black')
        self.ui.slncDtctButton.clicked.connect(self.scan_silence_detect)
        self.ui.slncDtctButton.setToolTip('Сканировать выбранное Silence')
        self.ui.frzDtctButton.clicked.connect(self.scan_freeze_detect)
        self.ui.frzDtctButton.setToolTip('Сканировать выбранное Freeze')
        self.ui.fullDtctButton.clicked.connect(self.full_detect)
        self.ui.fullDtctButton.setToolTip('Полное сканирование')
        self.ui.migrateButton.clicked.connect(self.file_manage)
        self.ui.migrateButton.setToolTip('Копирование и переименование')
        self.ui.settingsButton.clicked.connect(self.settings.open_settings_window)
        self.ui.settingsButton.setToolTip('Настройки')
        self.colorizeEffect_wt(self.ui.settingsButton)
        self.ui.switchModeButton.clicked.connect(self.switch_db_editor)
        self.ui.switchModeButton.setToolTip('Редактирование базы данных')
        self.colorizeEffect_wt(self.ui.switchModeButton)

        self.colorizeEffect_wt(self.ui.resizeButtonUp)
        self.colorizeEffect_wt(self.ui.resizeButtonDown)

        self.ui.delButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.delButton)
        self.ui.playButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.playButton)
        self.ui.openButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.openButton)
        self.ui.r128DtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.r128DtctButton)
        self.ui.queueButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.queueButton)
        self.ui.queueButton.hide()
        self.ui.blckDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.blckDtctButton)
        self.ui.slncDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.slncDtctButton)
        self.ui.frzDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.frzDtctButton)
        self.ui.fullDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.fullDtctButton)
        self.colorizeEffect_wt(self.ui.exportButton)
        # self.ui.migrateButton.setEnabled(False)
        self.colorizeEffect_wt(self.ui.migrateButton)

        self.grey_light = QColor(65, 65, 70)
        self.grey_dark = QColor(40, 40, 45)

        # Config settings
        settings_directory = os.path.join(PARENT_DIRECTORY, 'config')
        os.makedirs(settings_directory, exist_ok=True)
        self.settings_name = os.path.join(settings_directory, 'settings.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_name)

        # DB Edit Dialog
        self.db_sett = QDialog()
        self.db_settings = Ui_DB_Settings()
        self.db_settings.setupUi(self.db_sett)

        # DB_Editor

        self.ui.tableView_db.clicked.connect(self.click_table_db)
        self.tbl_name = 'films'

        db_directory = os.path.join(PARENT_DIRECTORY, 'db')
        os.makedirs(db_directory, exist_ok=True)
        self.sqlite_db_name = os.path.join(db_directory, 'sqlite_videoinfo.db')
        self.sqlite_db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.sqlite_db.setDatabaseName(self.sqlite_db_name)

        self.sqlite_model = QSqlTableModel(self)
        self.sqlite_model.setTable(self.tbl_name)
        self.sqlite_model.select()

        self.mongo_model = MongoTableModel()
        self.mongo_model.load_from_mongo()
        self.ui.tableView_db.setModel(self.mongo_model)
        self.ui.tableView_db.hide()
        self.ui.tableView_db.hideColumn(0)
        self.ui.tableView_db.setColumnWidth(1, 400)

        self.posql_model = TableModel([0, 0], [0, 0])

        # WaveView
        self.ui.wave_view.hide()
        self.ui.r128_loudness.hide()
        self.ui.resizeButtonDown.hide()
        # self.wave_flag = False
        self.ui.resizeButtonUp.clicked.connect(self.wave_view)
        self.ui.resizeButtonDown.clicked.connect(self.wave_hide)

        # MenuBar
        self.ui.actionAdd_files.triggered.connect(self.prepare_table_01)
        self.ui.actionDelete_selected_file.triggered.connect(self.del_selected_rows)
        self.ui.actionPlay_selected_file.triggered.connect(self.play_selected)

        self.ui.actionOpen_destination_folder.triggered.connect(self.open_folder)
        self.ui.actionSelected_files.triggered.connect(self.selected_db_file_list)

        self.ui.actionExport_table_to_Excel.triggered.connect(self.export_tbl_xlsx)
        self.ui.actionExport_all_db_to_Excel.triggered.connect(self.export_db_xlsx)
        self.ui.actionSettings.triggered.connect(self.settings.open_settings_window)
        # self.ui.actionOpen_VideoPlayer.triggered.connect(self.switch_db_editor)
        self.ui.actionOpen_VideoPlayer.setEnabled(False)
        self.ui.actionClear_table.triggered.connect(self.clear_table_01)
        self.ui.actionCheck_DB.triggered.connect(self.check_data_base)
        self.ui.actionShow_all_tables.triggered.connect(self.show_db_tables)
        # self.ui.actionUpdate_data_for_file.triggered.connect(self.update_ffprobe)
        self.ui.actionChoose_default_directory.triggered.connect(self.choose_default_dir)

        self.ui.actionRun_Loudness_selected_scan.triggered.connect(self.scan_loudnorm)
        self.ui.actionRun_SilenceDetect_selected_scan.triggered.connect(self.scan_silence_detect)
        # self.ui.actionRun_SilenceDetect_single_scan.triggered.connect(self.prepare_silence_detect_single)
        # self.ui.actionRun_SilenceDetect_multiple_scan.triggered.connect(self.prepare_silence_detect_multi)
        self.ui.actionRun_BlackDetect_selected_scan.triggered.connect(self.scan_black_detect)
        self.ui.actionRun_FreezeDetect_selected_scan.triggered.connect(self.scan_freeze_detect)
        # self.ui.actionRun_FreezeDetect_single_scan.triggered.connect(self.prepare_freeze_detect_single)
        # self.ui.actionRun_FreezeDetect_multiple_scan.triggered.connect(self.prepare_freeze_detect_multi)
        self.ui.actionRun_Full_selected_scan.triggered.connect(self.full_detect)
        # self.ui.actionRun_Full_single_scan.triggered.connect(self.prepare_full_detect_single)
        # self.ui.actionRun_Full_multiple_scan.triggered.connect(self.prepare_full_detect_multi)
        # self.ui.actionRun_Background_Loudness_scan.triggered.connect(self.prepare_background_loudnorm_scan)
        # self.ui.actionRun_Background_BlackDetect_scan.triggered.connect(self.prepare_background_blackdetect_scan)
        # self.ui.actionRun_Background_SilenceDetect_scan.triggered.connect(self.prepare_background_silencedetect_scan)
        # self.ui.actionRun_Background_FreezeDetect_scan.triggered.connect(self.prepare_background_freezedetect_scan)
        # self.ui.actionRun_Background_Full_scan.triggered.connect(self.prepare_background_fulldetect_scan)

        self.ui.actionOpen_db_editor.triggered.connect(self.switch_db_editor)

        self.ui.actionCreate_db.triggered.connect(self.create_new_db)
        self.ui.actionReset_scan_result_for_file.triggered.connect(self.reset_mediainfo_tbl_01)
        self.ui.actionDelete_from_db.triggered.connect(self.clear_mediainfo)
        self.ui.actionShow_Loudness.triggered.connect(self.show_loudness)
        self.ui.actionShow_Details.triggered.connect(self.show_details)

        self.choose_base_btn = QPushButton()
        self.choose_base_btn.setMinimumSize(QSize(60, 30))
        self.choose_base_btn.setMaximumSize(QSize(60, 30))
        self.choose_base_btn.setText('DB')
        self.choose_btn_style_wt = ('QPushButton{color: rgb(255, 255, 255);'
                                    'background-color:rgba(255,255,255,30);'
                                    'border: 1px solid rgba(255,255,255,40);'
                                    'border-radius:3px;}'
                                    'QPushButton:hover'
                                    '{background-color:rgba(255,255,255,50);}'
                                    'QPushButton:pressed{background-color:rgba(255,255,255,70);}')
        self.choose_btn_style_red = ('QPushButton{color: rgb(255, 28, 0);'
                                     'background-color:rgba(255, 28, 0, 30);'
                                     'border: 1px solid rgba(255, 28, 0, 40);'
                                     'border-radius:3px;}'
                                     'QPushButton:hover'
                                     '{background-color:rgba(255, 28, 0, 50);}'
                                     'QPushButton:pressed{background-color:rgba(255, 28, 0, 70);}')
        self.choose_base_btn.setStyleSheet(self.choose_btn_style_wt)
        self.choose_base_btn.clicked.connect(self.select_db)
        self.ui.toolBar.addWidget(self.choose_base_btn)
        self.ui.toolBar.setStyleSheet('padding-left: 10px;'
                                      'margin-right: 10px;'
                                      'margin-left: 10px;')
        self.choose_table_cmbx = QComboBox()
        self.choose_table_cmbx.addItems(ast.literal_eval(self.config['Toolbar']['table_name_combobox']))
        self.choose_table_cmbx.currentTextChanged.connect(self.update_db_table)
        self.choose_table_cmbx.setCurrentText(self.config['Toolbar']['table_name'])
        self.choose_table_cmbx.setMinimumSize(QSize(160, 0))
        self.ui.toolBar.addWidget(self.choose_table_cmbx)

        self.filter_table = QLineEdit()
        self.filter_table.setPlaceholderText("Filter...")
        self.ui.toolBar.addWidget(self.filter_table)

        self.selected_db = 'SQLITE'

        # progress_dialog
        # self.progress_dialog_label = QLabel()
        # self.progress_dialog_label.setAlignment(Qt.AlignCenter)
        # self.progress_dialog_label.setWordWrap(True)

        # Confirm action
        self.conf_action = QDialog()
        self.conf_dialog = Ui_ConfirmDialog()
        self.conf_dialog.setupUi(self.conf_action)

        self.posql_proxy_model = QSortFilterProxyModel()
        self.posql_proxy_model.setFilterKeyColumn(0)  # Search all columns.
        self.posql_proxy_model.sort(1, Qt.AscendingOrder)
        self.filter_table.textChanged.connect(self.posql_proxy_model.setFilterFixedString)

        self.sqlite_proxy_model = QSortFilterProxyModel()
        self.sqlite_proxy_model.setFilterKeyColumn(1)
        self.sqlite_proxy_model.setSourceModel(self.sqlite_model)
        self.sqlite_proxy_model.sort(1, Qt.AscendingOrder)

        self.ui.tableView_db.setModel(self.sqlite_proxy_model)
        self.filter_table.textChanged.connect(self.sqlite_proxy_model.setFilterFixedString)

        self.filter_table.textChanged.connect(self.search_main_table)

        # File manager

        self.fmanage = QWidget()
        self.file_manager = Ui_FileManager()
        self.file_manager.setupUi(self.fmanage)
        self.file_manager.treeView_source.setContextMenuPolicy(Qt.CustomContextMenu)
        self.file_manager.treeView_source.setSortingEnabled(True)
        self.file_manager.treeView_source.sortByColumn(0, Qt.AscendingOrder)

        self.treeView_source_model = QtWidgets.QFileSystemModel()
        self.treeView_source_model.setRootPath(QDir.rootPath())
        # self.treeView_source_model.sort(0, Qt.AscendingOrder)
        self.file_manager.treeView_source.setModel(self.treeView_source_model)
        self.file_manager.treeView_source.setColumnWidth(0, 300)
        self.file_manager.treeView_source.hide()

        self.treeView_destination_model = QtWidgets.QFileSystemModel()
        self.treeView_destination_model.setRootPath(QDir.rootPath())
        # self.treeView_destination_model.sort(0, Qt.AscendingOrder)
        self.file_manager.treeView_destination.setModel(self.treeView_destination_model)
        self.file_manager.treeView_destination.setColumnWidth(0, 300)
        self.file_manager.treeView_destination.setSortingEnabled(True)
        self.file_manager.treeView_destination.sortByColumn(0, Qt.AscendingOrder)
        self.file_manager.listWidget_destination.hide()
        self.colorizeEffect_wt(self.file_manager.rename_Button)
        self.colorizeEffect_wt(self.file_manager.undo_rename_Button)
        self.colorizeEffect_wt(self.file_manager.copy_to_dbButton)
        self.colorizeEffect_wt(self.file_manager.copy_from_dbButton)
        self.colorizeEffect_wt(self.file_manager.move_to_dbButton)
        self.colorizeEffect_wt(self.file_manager.move_from_dbButton)
        self.norm_tub_style = ('QPushButton{color: white}'
                               'QPushButton:hover{color: white; background-color: rgba(255,255,255,20)}'
                               'QPushButton:pressed{color: white; background-color: rgba(255,255,255,40)}')
        self.selected_tub_style = ('QPushButton{color: white; background-color: rgba(255,255,255,30)}'
                               'QPushButton:hover{color: white; background-color: rgba(255,255,255,20)}'
                               'QPushButton:pressed{color: white; background-color: rgba(255,255,255,40)}')

        self.file_manager.comboBox_preset.currentTextChanged.connect(self.set_mask_preset)
        self.file_manager.mask_full.setText(self.config['Mask_preset']['prst1'])
        self.mask_preset()
        self.file_manager.comboBox_digits.addItems(['1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.file_manager.comboBox_digits.setCurrentText('1')
        self.file_manager.comboBox_upper.addItems(['Unchanged', 'all lowercase', 'ALL UPPERCASE',
                                                   'First letter uppercase', 'First Of Each Word Uppercase'])
        self.file_manager.comboBox_upper.setCurrentText('Unchanged')

        self.file_manager.source_tub1.clicked.connect(self.source_file_list_manager_b1)
        self.file_manager.source_tub1.setText(self.config['Tubs_source']['tub1'])
        self.file_manager.source_tub2.clicked.connect(self.source_file_tree_manager_b2)
        self.file_manager.source_tub2.setText(self.config['Tubs_source']['tub2'])
        self.file_manager.source_tub3.clicked.connect(self.source_file_tree_manager_b3)
        self.file_manager.source_tub3.setText(self.config['Tubs_source']['tub3'])
        self.file_manager.source_tub4.clicked.connect(self.source_file_tree_manager_b4)
        self.file_manager.source_tub4.setText(self.config['Tubs_source']['tub4'])
        self.file_manager.source_tub5.clicked.connect(self.source_file_tree_manager_b5)
        self.file_manager.source_tub5.setText(self.config['Tubs_source']['tub5'])

        self.file_manager.destination_tub1.clicked.connect(self.destination_file_tree_manager_b1)
        self.file_manager.destination_tub1.setText(self.config['Tubs_destination']['tub1'])
        self.file_manager.destination_tub2.clicked.connect(self.destination_file_tree_manager_b2)
        self.file_manager.destination_tub2.setText(self.config['Tubs_destination']['tub2'])
        self.file_manager.destination_tub3.clicked.connect(self.destination_file_tree_manager_b3)
        self.file_manager.destination_tub3.setText(self.config['Tubs_destination']['tub3'])
        self.file_manager.destination_tub4.clicked.connect(self.destination_file_tree_manager_b4)
        self.file_manager.destination_tub4.setText(self.config['Tubs_destination']['tub4'])
        self.file_manager.destination_tub5.clicked.connect(self.destination_file_list_manager_b5)
        self.file_manager.destination_tub5.setText(self.config['Tubs_destination']['tub5'])

        self.file_manager.mask_name.clicked.connect(self.add_name)
        self.file_manager.mask_counter.clicked.connect(self.add_counter)
        self.file_manager.mask_date.clicked.connect(self.add_date)
        self.file_manager.mask_time.clicked.connect(self.add_time)
        self.file_manager.mask_full.textChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.comboBox_upper.currentTextChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.mask_search.textChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.mask_replace.textChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.spinBox_start.textChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.spinBox_step.textChanged.connect(self.destination_file_list_manager_b5)
        self.file_manager.comboBox_digits.currentTextChanged.connect(self.destination_file_list_manager_b5)

        self.file_manager.rename_Button.setToolTip('Rename all')
        self.file_manager.undo_rename_Button.setToolTip('Undo Rename all')
        self.file_manager.copy_to_dbButton.setToolTip('Copy to base')
        self.file_manager.copy_from_dbButton.setToolTip('Copy from base')
        self.file_manager.move_to_dbButton.setToolTip('Move to base')
        self.file_manager.move_from_dbButton.setToolTip('Move from base')

        self.file_manager.rename_Button.clicked.connect(self.file_list_rename)
        self.file_manager.undo_rename_Button.clicked.connect(self.undo_rename)
        self.file_manager.copy_to_dbButton.clicked.connect(self.file_list_copy_to)
        self.file_manager.copy_from_dbButton.clicked.connect(self.file_list_copy_from)
        self.file_manager.move_to_dbButton.clicked.connect(self.file_list_move_to)
        self.file_manager.move_from_dbButton.clicked.connect(self.file_list_move_from)

        # START PROGRAM
        self.db_connect()
        self.create_db_table()

    def init_table_widget(self):
        self.ui.tableWidget_01.keyPressEvent = self.table_key_press_event
        self.ui.tableWidget_01.mousePressEvent = self.table_mouse_key_press_event
        self.ui.tableView_db.keyPressEvent = self.table_db_key_press_event
        self.ui.tableView_db.mousePressEvent = self.table_db_mouse_key_press_event
        self.installEventFilter(self)
        # self.setFixedSize(self.ui.tableWidget_01.sizeHint())
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.setColumnCount(1)
        self.ui.tableWidget_01.setColumnCount(22)
        self.ui.tableWidget_01.setSortingEnabled(False)
        self.ui.tableWidget_01.setHorizontalHeaderLabels([
            'file_path', 'Name', 'Bit rate', 'Codec', 'Width', 'Height', 'SAR', 'DAR', 'Frame rate',
            'Duration', 'Audio map', 'Audio codec', 'Sample rate', 'Channels', 'Audio bit rate',
            'Integrated', 'True Peak', 'LRA', 'Threshold', 'Black Screen', 'Silence', 'Freeze'
        ])
        self.ui.tableWidget_01.hideColumn(0)

        self.ui.tableWidget_01.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.ui.tableWidget_01.setStyleSheet(u"QTableWidget::item:selected {background-color : rgba(255,255,255,50);}"
                                             u"QHeaderView::section{color: rgb(255,255,255);}")
        self.ui.splitter.setStyleSheet(u"QSplitter::handle:hover{background : rgba(255,255,255,50);}")

    def progress_dialog_init(self):
        if self.progress_dialog is None:
            self.progress_dialog = QProgressDialog()
            self.close_progress_dialog_btn = QPushButton('Cancel')
            self.progress_dialog.setCancelButton(self.close_progress_dialog_btn)
            self.close_progress_dialog_btn.clicked.connect(self.stop_processing)
            self.progress_dialog.setWindowModality(Qt.WindowModal)
            self.progress_dialog.setMinimumDuration(0)
            self.progress_dialog.setFixedSize(650, 150)
            self.progress_dialog.setStyleSheet(
                "QPushButton {color: white; background-color:rgba(255,255,255,30);"
                "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                "QPushButton:pressed{background-color:rgba(255,255,255,70);}"
            )

    def stop_single_processing(self):
        for scanner in self.ffprobe_scanners:
            if hasattr(scanner, 'stop'):
                scanner.stop()
        self.ffmpeg_scanners.clear()
        self.single_progress_dialog.close()

    def stop_processing(self):
        for scanner in self.ffmpeg_scanners:
            if hasattr(scanner, 'stop'):
                scanner.stop()
        self.ffmpeg_scanners.clear()
        self.double_progress_bar.close()

        self.ui.r128DtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.r128DtctButton)
        self.ui.blckDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.blckDtctButton)
        self.ui.slncDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.slncDtctButton)
        self.ui.frzDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.frzDtctButton)
        self.ui.fullDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.fullDtctButton)

    def on_started(self, params):
        self.ui.r128DtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.r128DtctButton)
        self.ui.blckDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.blckDtctButton)
        self.ui.slncDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.slncDtctButton)
        self.ui.frzDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.frzDtctButton)
        self.ui.fullDtctButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.fullDtctButton)

        num = params.get('num')
        self.double_progress_bar.progress_01.setValue(0)
        if num == 1:
            self.double_progress_bar.progress_02.setValue(0)

    # def on_progress(self, file_path, num):
    #     self.double_progress_bar.progress_01.hide()
    #     self.double_progress_bar.label_01.setText(file_path)
    #     self.double_progress_bar.progress_02.setValue(num)

    def on_progress(self, params):
        file_path = params.get('file_path')
        num = params.get('num')
        total_files = params.get('total_files')
        scan_type = params.get('scan_type')
        percent = params.get('percent')
        # total_progress = int(num / total_files * 100)
        total_progress = int((num - 1) * 100 / total_files + percent / total_files)

        self.double_progress_bar.label_01.setText(f'{num}/{total_files} {scan_type}\n{os.path.basename(file_path)}')
        self.double_progress_bar.progress_01.setValue(percent)
        self.double_progress_bar.progress_02.setValue(total_progress)
        self.double_progress_bar.show()

    def on_finished(self, params):
        file_path = params.get('file_path')
        num = params.get('num')
        total_files = params.get('total_files')
        total_progress = int(num / total_files * 100)

        self.double_progress_bar.progress_01.setValue(100)
        self.double_progress_bar.progress_02.setValue(total_progress)
        # self.add_table_r128()
        # self.add_table_black()
        # self.add_table_silence()
        # self.add_table_freeze()

        if all(not scanner._is_running for scanner in self.ffmpeg_scanners):
            self.double_progress_bar.close()
            dlg = AttentionDialog("INFO", f'Scanning for file\n{file_path}\nwas finished')
            dlg.exec()
            self.ffmpeg_scanners.clear()

            self.ui.r128DtctButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.r128DtctButton)
            self.ui.blckDtctButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.blckDtctButton)
            self.ui.slncDtctButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.slncDtctButton)
            self.ui.frzDtctButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.frzDtctButton)
            self.ui.fullDtctButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.fullDtctButton)

    def on_error(self, file_path, error):
        print(f"Ошибка в {file_path}: {error}")
        dlg = AttentionDialog("ERROR", f"Ошибка в {file_path}: {error}")
        dlg.exec()
        self.ui.r128DtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.r128DtctButton)
        self.ui.blckDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.blckDtctButton)
        self.ui.slncDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.slncDtctButton)
        self.ui.frzDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.frzDtctButton)
        self.ui.fullDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.fullDtctButton)

    def on_started_ffprobe(self, params):
        if params.get('num') == 1:
            self.single_progress_dialog.single_progress_bar.setValue(0)
        # pass
        self.single_progress_dialog.show()
        # self.progress_dialog_init()
        # self.single_progress_bar.setValue(0)

    def on_finished_ffprobe(self, params):
        file_path = params.get('file_path')
        num = params.get('num')
        total_files = params.get('total_files')
        total_progress = int(num / total_files * 100)
        self.single_progress_dialog.label.setText(f'{num}/{total_files}  FFprobe Scan\n{os.path.basename(file_path)}')
        self.single_progress_dialog.single_progress_bar.setValue(total_progress)
        if all(not scanner._is_running for scanner in self.ffprobe_scanners):
            self.single_progress_dialog.close()

    def on_error_ffprobe(self, file_path, error):
        dlg = AttentionDialog("ERROR", f"Ошибка в {file_path}: {error}")
        dlg.exec()

    def db_connect(self):
        try:
            print(now())
            print('Подключение к базе данных')
            DataPos().create_table(self.read_tbl_name())
        except Exception:
            dlg = AttentionDialog("Error!", 'Подключение к базе данных не удалось. Проверьте настройки.')
            dlg.exec()


    def create_db_table(self):
        DataLite().create_table(self.read_tbl_name())

    def write_log(self, log_path, log_info):
        f = open(log_path, 'w')
        f.write(log_info)
        f.close()

    def read_log(self, log_path):
        f = open(log_path, 'r')
        log = f.read()
        f.close()
        return log

    def mask_preset(self):
        prst1_name = self.config['Mask_preset']['prst1']
        prst2_name = self.config['Mask_preset']['prst2']
        prst3_name = self.config['Mask_preset']['prst3']
        prst4_name = self.config['Mask_preset']['prst4']
        self.file_manager.comboBox_preset.addItems([prst1_name, prst2_name, prst3_name, prst4_name])
        self.file_manager.comboBox_preset.setCurrentText(prst1_name)

    def set_mask_preset(self):
        current_prst = self.file_manager.comboBox_preset.currentText()
        self.file_manager.mask_full.setText(current_prst)

    def tree_source_explorer(self):
        path = ""
        self.file_manager.treeView_source.setRootIndex(self.treeView_source_model.index(path))

    def file_manage(self):
        self.fmanage.show()
        self.source_file_list_manager_b1()
        self.destination_file_tree_manager_b1()

    def source_file_list_manager_b1(self):
        self.file_manager.source_tub1.setStyleSheet(self.selected_tub_style)
        self.file_manager.source_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub5.setStyleSheet(self.norm_tub_style)
        self.prepare_export_task()

    def source_file_tree_manager_b2(self):
        self.file_manager.source_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub2.setStyleSheet(self.selected_tub_style)
        self.file_manager.source_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub5.setStyleSheet(self.norm_tub_style)
        source_explorer_path = self.config['Tubs_source']['tub2_path']
        self.file_manager.treeView_source.setRootIndex(self.treeView_source_model.index(source_explorer_path))
        self.treeView_source_model.setRootPath('')
        self.treeView_source_model.setRootPath(source_explorer_path)
        self.file_manager.treeView_source.setSortingEnabled(True)
        if self.file_manager.listWidget_source.isVisible():
            self.file_manager.listWidget_source.hide()
            self.file_manager.treeView_source.show()

    def source_file_tree_manager_b3(self):
        self.file_manager.source_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub3.setStyleSheet(self.selected_tub_style)
        self.file_manager.source_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub5.setStyleSheet(self.norm_tub_style)
        source_explorer_path = self.config['Tubs_source']['tub3_path']
        self.file_manager.treeView_source.setRootIndex(self.treeView_source_model.index(source_explorer_path))
        self.treeView_source_model.setRootPath('')
        self.treeView_source_model.setRootPath(source_explorer_path)
        self.file_manager.treeView_source.setSortingEnabled(True)
        if self.file_manager.listWidget_source.isVisible():
            self.file_manager.listWidget_source.hide()
            self.file_manager.treeView_source.show()

    def source_file_tree_manager_b4(self):
        self.file_manager.source_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub4.setStyleSheet(self.selected_tub_style)
        self.file_manager.source_tub5.setStyleSheet(self.norm_tub_style)
        source_explorer_path = self.config['Tubs_source']['tub4_path']
        self.file_manager.treeView_source.setRootIndex(self.treeView_source_model.index(source_explorer_path))
        self.treeView_source_model.setRootPath('')
        self.treeView_source_model.setRootPath(source_explorer_path)
        self.file_manager.treeView_source.setSortingEnabled(True)
        if self.file_manager.listWidget_source.isVisible():
            self.file_manager.listWidget_source.hide()
            self.file_manager.treeView_source.show()

    def source_file_tree_manager_b5(self):
        self.file_manager.source_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.source_tub5.setStyleSheet(self.selected_tub_style)
        source_explorer_path = self.config['Tubs_source']['tub5_path']
        self.file_manager.treeView_source.setRootIndex(self.treeView_source_model.index(source_explorer_path))
        self.treeView_source_model.setRootPath('')
        self.treeView_source_model.setRootPath(source_explorer_path)
        self.file_manager.treeView_source.setSortingEnabled(True)
        if self.file_manager.listWidget_source.isVisible():
            self.file_manager.listWidget_source.hide()
            self.file_manager.treeView_source.show()

    def destination_file_tree_manager_b1(self):
        self.file_manager.destination_tub1.setStyleSheet(self.selected_tub_style)
        self.file_manager.destination_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub5.setStyleSheet(self.norm_tub_style)
        dest_explorer_path = self.config['Tubs_destination']['tub1_path']
        self.file_manager.treeView_destination.setRootIndex(self.treeView_destination_model.index(dest_explorer_path))
        self.treeView_destination_model.setRootPath('')
        self.treeView_destination_model.setRootPath(dest_explorer_path)
        if self.file_manager.listWidget_destination.isVisible():
            self.file_manager.listWidget_destination.hide()
            self.file_manager.treeView_destination.show()

    def destination_file_tree_manager_b2(self):
        self.file_manager.destination_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub2.setStyleSheet(self.selected_tub_style)
        self.file_manager.destination_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub5.setStyleSheet(self.norm_tub_style)
        dest_explorer_path = self.config['Tubs_destination']['tub2_path']
        self.file_manager.treeView_destination.setRootIndex(self.treeView_destination_model.index(dest_explorer_path))
        self.treeView_destination_model.setRootPath('')
        self.treeView_destination_model.setRootPath(dest_explorer_path)
        self.file_manager.treeView_destination.setSortingEnabled(True)
        if self.file_manager.listWidget_destination.isVisible():
            self.file_manager.listWidget_destination.hide()
            self.file_manager.treeView_destination.show()

    def destination_file_tree_manager_b3(self):
        self.file_manager.destination_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub3.setStyleSheet(self.selected_tub_style)
        self.file_manager.destination_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub5.setStyleSheet(self.norm_tub_style)
        dest_explorer_path = self.config['Tubs_destination']['tub3_path']
        self.file_manager.treeView_destination.setRootIndex(self.treeView_destination_model.index(dest_explorer_path))
        self.treeView_destination_model.setRootPath('')
        self.treeView_destination_model.setRootPath(dest_explorer_path)
        self.file_manager.treeView_destination.setSortingEnabled(True)
        if self.file_manager.listWidget_destination.isVisible():
            self.file_manager.listWidget_destination.hide()
            self.file_manager.treeView_destination.show()

    def destination_file_tree_manager_b4(self):
        self.file_manager.destination_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub4.setStyleSheet(self.selected_tub_style)
        self.file_manager.destination_tub5.setStyleSheet(self.norm_tub_style)
        dest_explorer_path = self.config['Tubs_destination']['tub4_path']
        self.file_manager.treeView_destination.setRootIndex(self.treeView_destination_model.index(dest_explorer_path))
        self.treeView_destination_model.setRootPath('')
        self.treeView_destination_model.setRootPath(dest_explorer_path)
        self.file_manager.treeView_destination.setSortingEnabled(True)
        if self.file_manager.listWidget_destination.isVisible():
            self.file_manager.listWidget_destination.hide()
            self.file_manager.treeView_destination.show()

    def destination_file_list_manager_b5(self):
        self.file_manager.destination_tub1.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub2.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub3.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub4.setStyleSheet(self.norm_tub_style)
        self.file_manager.destination_tub5.setStyleSheet(self.selected_tub_style)
        rename_list = self.file_list_rename_view()[1]
        self.file_manager.listWidget_destination.clear()
        self.file_manager.listWidget_destination.addItems(rename_list)
        if self.file_manager.treeView_destination.isVisible():
            self.file_manager.listWidget_destination.show()
            self.file_manager.treeView_destination.hide()


    def add_name(self):
        mask = self.file_manager.mask_full.text()
        self.file_manager.mask_full.setText(mask+'[N]')

    def add_counter(self):
        counter = self.file_manager.mask_full.text()
        self.file_manager.mask_full.setText(counter+'[C]')

    def add_date(self):
        date = self.file_manager.mask_full.text()
        self.file_manager.mask_full.setText(date+'[dd-mm-yy]')

    def add_time(self):
        time_ = self.file_manager.mask_full.text()
        self.file_manager.mask_full.setText(time_+'[hh:mm:ss]')

    def file_list_rename_view(self):
        items = self.file_manager.listWidget_source
        old_full_name_list = [items.item(x).text() for x in range(items.count())]
        new_name_list = []
        new_full_name_list = []
        mask = self.file_manager.mask_full.text()
        counter = self.file_manager.spinBox_start.text()
        step = self.file_manager.spinBox_step.text()
        dig = int(self.file_manager.comboBox_digits.currentText())
        search = self.file_manager.mask_search.text()
        replace = self.file_manager.mask_replace.text()
        upper = self.file_manager.comboBox_upper.currentText()
        for old_name in old_full_name_list:
            old_name_path = os.path.dirname(old_name)
            old_name_body = os.path.splitext(os.path.basename(old_name))[0]
            old_name_ext = os.path.splitext(old_name)[1]
            new_name = mask.replace('[N]', old_name_body)
            if '[N' in mask:
                mask_slice = '['+mask.split('[')[1].split(']')[0]+']'
                if mask_slice[2].isdigit() and not mask_slice[-2].isdigit():
                    try:
                        strt = int(mask_slice.split(']')[0].split('-')[0][2:])-1
                        new_name = new_name.replace(mask_slice, old_name_body[strt:])
                    except Exception:
                        pass
                if not mask_slice[2].isdigit() and mask_slice[-2].isdigit():
                    try:
                        fnsh = int(mask_slice.split(']')[0].split('-')[1])
                        new_name = new_name.replace(mask_slice, old_name_body[:fnsh])
                    except Exception:
                        pass
                if mask_slice[2].isdigit() and mask_slice[-2].isdigit():
                    try:
                        strt = int(mask_slice.split(']')[0].split('-')[0][2:])-1
                        fnsh = int(mask_slice.split(']')[0].split('-')[1])
                        new_name = new_name.replace(mask_slice, old_name_body[strt:fnsh])
                    except Exception:
                        pass

            new_name = new_name.replace('[C]', f'{int(counter):0{dig}}')
            new_name = new_name.replace('[dd-mm-yy]', str(datetime.date.today().strftime('%d-%m-%Y')))
            new_name = new_name.replace('[dd-mm]', str(datetime.date.today().strftime('%d-%m')))
            new_name = new_name.replace('[mm-yy]', str(datetime.date.today().strftime('%m-%Y')))
            new_name = new_name.replace('[hh:mm:ss]', str(datetime.datetime.now().strftime('%H:%M:%S')))
            new_name = new_name.replace('[hh:mm]', str(datetime.datetime.now().strftime('%H:%M')))
            if search != '':
                new_name = new_name.replace(search, replace)
            if upper == 'all lowercase':
                new_name = new_name.lower()
            if upper == 'ALL UPPERCASE':
                new_name = new_name.upper()
            if upper == 'First letter uppercase':
                new_name = new_name.capitalize()
            if upper == 'First Of Each Word Uppercase':
                new_name = new_name.title()
            new_name_full = old_name_path+'/'+new_name+old_name_ext
            new_full_name_list.append(new_name_full)
            new_name = new_name + old_name_ext
            new_name_list.append(new_name)
            counter = int(counter) + int(step)
        return old_full_name_list, new_name_list, new_full_name_list

    def file_list_rename(self):
        tbl_name = self.read_tbl_name()
        old_full_name_list = self.file_list_rename_view()[0]
        new_full_name_list = self.file_list_rename_view()[2]
        log = f'{old_full_name_list}, {new_full_name_list}'
        log_path = os.path.join(PARENT_DIRECTORY, 'logs', 'rename_list.txt')
        self.write_log(log_path, log)
        if 'Not selected' not in old_full_name_list:
            for i in range(len(old_full_name_list)):
                old_file_path = old_full_name_list[i]
                new_file_path = new_full_name_list[i]
                try:
                    os.rename(old_file_path, new_file_path)
                    if self.selected_db == 'SQLITE':
                        DataLite().update_data(tbl_name, old_file_path, new_file_path)
                    else:
                        DataPos().update_data(tbl_name, old_file_path, new_file_path)
                    self.file_manager.listWidget_source.item(i).setText(new_file_path)
                    row_count = self.ui.tableWidget_01.rowCount()
                    for row in range(row_count):
                        if self.ui.tableWidget_01.item(row, 0).text() == old_file_path:
                            item = QTableWidgetItem()
                            item.setData(Qt.EditRole, new_file_path)
                            self.ui.tableWidget_01.setItem(row, 0, item)
                except Exception:
                    message_text = (f'Error, could not rename\n'
                                    f'{old_file_path} -> {old_file_path}')
                    dlg = AttentionDialog("Error!", message_text)
                    dlg.exec()
                    break

    def undo_rename(self):
        log_path = os.path.join(PARENT_DIRECTORY, 'logs', 'rename_list.txt')
        rename_list = ast.literal_eval(self.read_log(log_path))
        old_full_name_list = rename_list[1]
        new_full_name_list = rename_list[0]
        tbl_name = self.read_tbl_name()
        for i in range(len(old_full_name_list)):
            old_file_path = old_full_name_list[i]
            new_file_path = new_full_name_list[i]
            try:
                os.rename(old_file_path, new_file_path)
                if self.selected_db == 'SQLITE':
                    DataLite().update_data(tbl_name, old_file_path, new_file_path)
                else:
                    DataPos().update_data(tbl_name, old_file_path, new_file_path)
                self.file_manager.listWidget_source.item(i).setText(new_file_path)
                row_count = self.ui.tableWidget_01.rowCount()
                for row in range(row_count):
                    if self.ui.tableWidget_01.item(row, 0).text() == old_file_path:
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, new_file_path)
                        self.ui.tableWidget_01.setItem(row, 0, item)
            except Exception:
                message_text = (f'Error, could not undo rename\n'
                                f'{old_file_path} -> {old_file_path}')
                dlg = AttentionDialog("Error!", message_text)
                dlg.exec()
                break

    def file_list_copy_to(self):
        tbl_name = self.read_tbl_name()
        self.file_manager.progressBar.setValue(0)
        if self.file_manager.listWidget_source.isVisible():
            items = self.file_manager.listWidget_source
            file_list = [items.item(x).text() for x in range(items.count())]
        else:
            indexes = self.file_manager.treeView_source.selectedIndexes()
            file_list = [self.treeView_source_model.filePath(index) for index in indexes if index.column() == 0]
        destination_file_path = self.treeView_destination_model.rootPath()
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            self.file_manager.progressBar.setValue((i+1)/total_files*100)
            QApplication.processEvents()
            shutil.copy(file_path, destination_file_path)
            new_file_path = os.path.join(destination_file_path, os.path.basename(file_path))
            if self.selected_db == 'SQLITE':
                DataLite().update_data(tbl_name, file_path, new_file_path)
            else:
                DataPos().update_data(tbl_name, file_path, new_file_path)
            # self.file_manager.listWidget_source.selectedItems()
            self.file_manager.listWidget_source.takeItem(0)
            row_count = self.ui.tableWidget_01.rowCount()
            for row in range(row_count):
                if self.ui.tableWidget_01.item(row, 0).text() == file_path:
                    self.ui.tableWidget_01.removeRow(row)
                    break
            print(file_path, 'copied')
        self.file_manager.progressBar.setValue(100)

    def file_list_copy_from(self):
        tbl_name = self.read_tbl_name()
        self.file_manager.progressBar.setValue(0)
        indexes = self.file_manager.treeView_destination.selectedIndexes()
        file_list = [self.treeView_destination_model.filePath(index) for index in indexes if index.column() == 0]
        destination_file_path = self.treeView_source_model.rootPath()
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            self.file_manager.progressBar.setValue((i+1)/total_files*100)
            QApplication.processEvents()
            shutil.copy(file_path, destination_file_path)
            new_file_path = os.path.join(destination_file_path, os.path.basename(file_path))
            if self.selected_db == 'SQLITE':
                DataLite().update_data(tbl_name, file_path, new_file_path)
            else:
                DataPos().update_data(tbl_name, file_path, new_file_path)
            # self.file_manager.listWidget_source.selectedItems()
            # self.file_manager.listWidget_source.takeItem(0)
            print(file_path, 'copied')
        self.file_manager.progressBar.setValue(100)

    def file_list_move_to(self):
        tbl_name = self.read_tbl_name()
        self.file_manager.progressBar.setValue(0)
        if self.file_manager.listWidget_source.isVisible():
            items = self.file_manager.listWidget_source
            file_list = [items.item(x).text() for x in range(items.count())]
        else:
            indexes = self.file_manager.treeView_source.selectedIndexes()
            file_list = [self.treeView_source_model.filePath(index) for index in indexes if index.column() == 0]
        destination_file_path = self.treeView_destination_model.rootPath()
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            self.file_manager.progressBar.setValue((i+1)/total_files*100)
            QApplication.processEvents()
            shutil.move(file_path, destination_file_path)
            new_file_path = os.path.join(destination_file_path, os.path.basename(file_path))
            if self.selected_db == 'SQLITE':
                DataLite().update_data(tbl_name, file_path, new_file_path)
            else:
                DataPos().update_data(tbl_name, file_path, new_file_path)
            # self.file_manager.listWidget_source.selectedItems()
            self.file_manager.listWidget_source.takeItem(0)
            row_count = self.ui.tableWidget_01.rowCount()
            for row in range(row_count):
                if self.ui.tableWidget_01.item(row, 0).text() == file_path:
                    self.ui.tableWidget_01.removeRow(row)
                    break
            print(file_path, 'moved')
        self.file_manager.progressBar.setValue(100)

    def file_list_move_from(self):
        tbl_name = self.read_tbl_name()
        self.file_manager.progressBar.setValue(0)
        indexes = self.file_manager.treeView_destination.selectedIndexes()
        file_list = [self.treeView_destination_model.filePath(index) for index in indexes if index.column() == 0]
        destination_file_path = self.treeView_source_model.rootPath()
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            self.file_manager.progressBar.setValue((i+1)/total_files*100)
            QApplication.processEvents()
            shutil.move(file_path, destination_file_path)
            new_file_path = os.path.join(destination_file_path, os.path.basename(file_path))
            if self.selected_db == 'SQLITE':
                DataLite().update_data(tbl_name, file_path, new_file_path)
            else:
                DataPos().update_data(tbl_name, file_path, new_file_path)
            print(file_path, 'moved')
        self.file_manager.progressBar.setValue(100)

    def prepare_export_task(self):
        tbl_file_list = self.selected_file_list()
        self.file_manager.listWidget_source.clear()
        self.file_manager.listWidget_source.addItems(tbl_file_list)
        if self.file_manager.treeView_source.isVisible():
            self.file_manager.listWidget_source.show()
            self.file_manager.treeView_source.hide()
        if not self.file_manager.listWidget_source.item(0):
            self.file_manager.listWidget_source.clear()
            self.file_manager.listWidget_source.addItem('Not selected')
            self.file_manager.listWidget_source.setEnabled(False)
            self.file_manager.listWidget_source.setStyleSheet('color: grey; font: italic')
            self.file_manager.listWidget_destination.setEnabled(False)
            self.file_manager.listWidget_destination.setStyleSheet('color: grey; font: italic')
        else:
            self.file_manager.listWidget_source.setEnabled(True)
            self.file_manager.listWidget_source.setStyleSheet('color: white; font: regular')
            self.file_manager.listWidget_destination.setEnabled(True)
            self.file_manager.listWidget_destination.setStyleSheet('color: white; font: regular')

    def search_main_table(self, s):
        self.ui.tableWidget_01.setCurrentItem(None)
        if not s:
            return
        matching_items = self.ui.tableWidget_01.findItems(s, Qt.MatchContains)
        if matching_items:
            for match in matching_items:
                if match.column() == 1:
                    match.setSelected(True)


    def read_config(self, sect, key):
        return self.config[sect][key]

    def write_config(self):
        with open(self.settings_name, 'w') as configfile:
            self.config.write(configfile)

    def select_db(self):
        if self.selected_db == 'SQLITE':
            self.ui.move_to_dbButton.hide()
            headers = DataPos().read_all_headers(self.read_tbl_name())
            data = DataPos().read_all_data(self.read_tbl_name())
            self.posql_model = TableModel(headers, data)
            self.posql_proxy_model.setSourceModel(self.posql_model)
            self.ui.tableView_db.setModel(self.posql_proxy_model)

            self.ui.tableView_db.hideColumn(0)
            self.ui.tableView_db.setColumnWidth(1, 400)

            self.selected_db = 'POSQL'
            self.choose_base_btn.setStyleSheet(self.choose_btn_style_red)
        else:
            self.ui.move_to_dbButton.show()
            self.ui.tableView_db.setModel(self.mongo_model)

            self.sqlite_model.setTable(self.read_tbl_name())
            self.sqlite_model.select()
            self.ui.tableView_db.hideColumn(0)
            self.ui.tableView_db.setColumnWidth(1, 400)

            self.selected_db = 'SQLITE'
            self.choose_base_btn.setStyleSheet(self.choose_btn_style_wt)

    def update_db_table(self):
        if self.selected_db == 'SQLITE':
            self.sqlite_model.setTable(self.read_tbl_name())
            self.sqlite_model.select()
            self.create_db_table()

            self.ui.tableView_db.hideColumn(0)
            self.ui.tableView_db.setColumnWidth(1, 400)
            self.check_table_bd()
        else:
            headers = DataPos().read_all_headers(self.read_tbl_name())
            data = DataPos().read_all_data(self.read_tbl_name())
            self.posql_model = TableModel(headers, data)
            self.posql_proxy_model.setSourceModel(self.posql_model)
            self.ui.tableView_db.setModel(self.posql_proxy_model)

            self.ui.tableView_db.hideColumn(0)
            self.ui.tableView_db.setColumnWidth(1, 400)
            self.check_table_bd()


    def read_tbl_name(self):
        tbl_name = self.choose_table_cmbx.currentText()
        return tbl_name

    def reset_mediainfo_tbl_01(self):
        file_list = self.selected_file_list()
        for file_path in file_list:
            self.mongo.update_file_info(file_path, {'ffmpeg_scanners': {}})
            self.add_table_r128(file_path, {})
            self.add_table_black(file_path, {})
            self.add_table_silence(file_path, {})
            self.add_table_freeze(file_path, {})

    def reset_mediainfo_db(self):
        file_list = self.selected_db_file_list()
        for file_path in file_list:
            self.mongo.update_file_info(file_path, {'ffmpeg_scanners': {}})
        self.update_db_table()

    def clear_mediainfo(self):
        file_list = self.selected_file_list()
        for file_path in file_list:
            self.mongo.drop_file(file_path)
        self.del_selected_rows()

    def del_file_from_db(self):
        file_list = self.selected_db_file_list()
        for file_path in file_list:
            self.confirm_the_action(file_path)


    def confirm_the_action(self, file_path):
        message_text = (f'Are you sure you want to delete the file\n{file_path} ?')
        dlg = CustomDialog(message_text)
        if dlg.exec():
            self.mongo.drop_file(file_path)
            index = self.ui.tableView_db.selectionModel().currentIndex()
            self.ui.tableView_db.selectRow(index.row())
            self.update_db_table()
        else:
            print("Cancel!")
        self.check_table_bd()

    def switch_tools(self):
        button_style_min = ("QToolButton{color: rgb(255, 255, 255);"
                            "background-color:rgba(255,255,255,30);"
                            "border: 1px solid rgba(255,255,255,40);"
                            "border-radius:3px;}"
                            "QToolButton:hover{background-color:rgba(255,255,255,50);}"
                            "QToolButton:pressed{background-color:rgba(255,255,255,70);}")

        button_style_max = ("QToolButton{color: rgb(255, 255, 255);"
                            "background-color:rgba(255,255,255,0);"
                            "border: 0px solid rgba(255,255,255,40);"
                            "border-radius:3px;}"
                            "QToolButton:hover{background-color:rgba(255,255,255,50);}"
                            "QToolButton:pressed{background-color:rgba(255,255,255,70);}")
        max_icon = QIcon()
        max_icon.addFile(u":/bl_img/icons/menu_open_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        min_icon = QIcon()
        min_icon.addFile(u":/bl_img/icons/menu_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
        if not self.switch_tool_flag:
            self.ui.buttons.setMinimumSize(185, 0)

            self.ui.move_to_tableButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.move_to_tableButton.setMinimumSize(180, 30)
            self.ui.move_to_tableButton.setToolTip('')
            self.ui.move_to_tableButton.setText('  Move to table')
            self.ui.move_to_tableButton.setStyleSheet(button_style_max)

            self.ui.delete_from_dbButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.delete_from_dbButton.setMinimumSize(180, 30)
            self.ui.delete_from_dbButton.setToolTip('')
            self.ui.delete_from_dbButton.setText('  Delete from DB')
            self.ui.delete_from_dbButton.setStyleSheet(button_style_max)

            self.ui.move_to_dbButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.move_to_dbButton.setMinimumSize(180, 30)
            self.ui.move_to_dbButton.setToolTip('')
            self.ui.move_to_dbButton.setText('  Move to DB')
            self.ui.move_to_dbButton.setStyleSheet(button_style_max)

            self.ui.addButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.addButton.setMinimumSize(180, 30)
            self.ui.addButton.setToolTip('')
            self.ui.addButton.setText('  Add files')
            self.ui.addButton.setStyleSheet(button_style_max)

            self.ui.delButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.delButton.setMinimumSize(180, 30)
            self.ui.delButton.setToolTip('')
            self.ui.delButton.setText('  Delete file from table')
            self.ui.delButton.setStyleSheet(button_style_max)

            self.ui.playButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.playButton.setMinimumSize(180, 30)
            self.ui.playButton.setToolTip('')
            self.ui.playButton.setText('  Play selected')
            self.ui.playButton.setStyleSheet(button_style_max)

            self.ui.openButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.openButton.setMinimumSize(180, 30)
            self.ui.openButton.setToolTip('')
            self.ui.openButton.setText('  Open folder with file')
            self.ui.openButton.setStyleSheet(button_style_max)

            self.ui.r128DtctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.r128DtctButton.setMinimumSize(180, 30)
            self.ui.r128DtctButton.setToolTip('')
            self.ui.r128DtctButton.setText('  Start Loudnorm scan')
            self.ui.r128DtctButton.setStyleSheet(button_style_max)

            self.ui.blckDtctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.blckDtctButton.setMinimumSize(180, 30)
            self.ui.blckDtctButton.setToolTip('')
            self.ui.blckDtctButton.setText('  Start BlackDetect scan')
            self.ui.blckDtctButton.setStyleSheet(button_style_max)

            self.ui.slncDtctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.slncDtctButton.setMinimumSize(180, 30)
            self.ui.slncDtctButton.setToolTip('')
            self.ui.slncDtctButton.setText('  Start SilenceDetect scan')
            self.ui.slncDtctButton.setStyleSheet(button_style_max)

            self.ui.frzDtctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.frzDtctButton.setMinimumSize(180, 30)
            self.ui.frzDtctButton.setToolTip('')
            self.ui.frzDtctButton.setText('  Start FreezeDetect scan')
            self.ui.frzDtctButton.setStyleSheet(button_style_max)

            self.ui.fullDtctButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.fullDtctButton.setMinimumSize(180, 30)
            self.ui.fullDtctButton.setToolTip('')
            self.ui.fullDtctButton.setText('  Start Full scan')
            self.ui.fullDtctButton.setStyleSheet(button_style_max)

            self.ui.migrateButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.migrateButton.setMinimumSize(180, 30)
            self.ui.migrateButton.setToolTip('')
            self.ui.migrateButton.setText('  Copy and Rename')
            self.ui.migrateButton.setStyleSheet(button_style_max)

            self.ui.exportButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.exportButton.setMinimumSize(180, 30)
            self.ui.exportButton.setToolTip('')
            self.ui.exportButton.setText('  Export DB to Excel')
            self.ui.exportButton.setStyleSheet(button_style_max)

            self.ui.switchModeButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.switchModeButton.setMinimumSize(180, 30)
            self.ui.switchModeButton.setToolTip('')
            self.ui.switchModeButton.setText('  Switch ViewMode')
            self.ui.switchModeButton.setStyleSheet(button_style_max)

            self.ui.settingsButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
            self.ui.settingsButton.setMinimumSize(180, 30)
            self.ui.settingsButton.setToolTip('')
            self.ui.settingsButton.setText('  Show Settings')
            self.ui.settingsButton.setStyleSheet(button_style_max)

            self.ui.switchToolButton.setStyleSheet(button_style_max)
            self.ui.switchToolButton.setIcon(max_icon)
            self.switch_tool_flag = True
        else:
            self.ui.buttons.setMinimumSize(46, 0)
            self.ui.move_to_tableButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.move_to_tableButton.setMinimumSize(40, 30)
            self.ui.move_to_tableButton.setToolTip('Добавить файл в таблицу')
            self.ui.move_to_tableButton.setStyleSheet(button_style_min)

            self.ui.delete_from_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.delete_from_dbButton.setMinimumSize(40, 30)
            self.ui.delete_from_dbButton.setToolTip('Переместить выбранное в основную базу данных')
            self.ui.delete_from_dbButton.setStyleSheet(button_style_min)

            self.ui.move_to_dbButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.move_to_dbButton.setMinimumSize(40, 30)
            self.ui.move_to_dbButton.setToolTip('Удалить файл из базы')
            self.ui.move_to_dbButton.setStyleSheet(button_style_min)

            self.ui.buttons.setMinimumSize(46, 0)
            self.ui.addButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.addButton.setMinimumSize(40, 30)
            self.ui.addButton.setToolTip('Добавить файл')
            self.ui.addButton.setStyleSheet(button_style_min)

            self.ui.delButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.delButton.setMinimumSize(40, 30)
            self.ui.delButton.setToolTip('Удалить строку из таблицы')
            self.ui.delButton.setStyleSheet(button_style_min)

            self.ui.playButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.playButton.setMinimumSize(40, 30)
            self.ui.playButton.setToolTip('Воспроизвести файл')
            self.ui.playButton.setStyleSheet(button_style_min)

            self.ui.openButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.openButton.setMinimumSize(40, 30)
            self.ui.openButton.setToolTip('Открыть папку с файлом')
            self.ui.openButton.setStyleSheet(button_style_min)

            self.ui.r128DtctButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.r128DtctButton.setMinimumSize(40, 30)
            self.ui.r128DtctButton.setToolTip('Измерение уровня громкости')
            self.ui.r128DtctButton.setStyleSheet(button_style_min)

            self.ui.blckDtctButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.blckDtctButton.setMinimumSize(40, 30)
            self.ui.blckDtctButton.setToolTip('Обнаружение чёрного поля')
            self.ui.blckDtctButton.setStyleSheet(button_style_min)

            self.ui.slncDtctButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.slncDtctButton.setMinimumSize(40, 30)
            self.ui.slncDtctButton.setToolTip('Обнаружение пропусков звука')
            self.ui.slncDtctButton.setStyleSheet(button_style_min)

            self.ui.frzDtctButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.frzDtctButton.setMinimumSize(40, 30)
            self.ui.frzDtctButton.setToolTip('Обнаружение стоп-кадров')
            self.ui.frzDtctButton.setStyleSheet(button_style_min)

            self.ui.fullDtctButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.fullDtctButton.setMinimumSize(40, 30)
            self.ui.fullDtctButton.setToolTip('Полное сканирование')
            self.ui.fullDtctButton.setStyleSheet(button_style_min)

            self.ui.migrateButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.migrateButton.setMinimumSize(40, 30)
            self.ui.migrateButton.setToolTip('Копирование и переименование')
            self.ui.migrateButton.setStyleSheet(button_style_min)

            self.ui.exportButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.exportButton.setMinimumSize(40, 30)
            self.ui.exportButton.setToolTip('Экспорт базы данных в Excel')
            self.ui.exportButton.setStyleSheet(button_style_min)

            self.ui.switchModeButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.switchModeButton.setMinimumSize(40, 30)
            self.ui.switchModeButton.setToolTip('Переключить режим таблицы')
            self.ui.switchModeButton.setStyleSheet(button_style_min)

            self.ui.settingsButton.setToolButtonStyle(Qt.ToolButtonIconOnly)
            self.ui.settingsButton.setMinimumSize(40, 30)
            self.ui.settingsButton.setToolTip('Настройки')
            self.ui.settingsButton.setStyleSheet(button_style_min)

            self.ui.switchToolButton.setStyleSheet(button_style_min)
            self.ui.switchToolButton.setIcon(min_icon)
            self.switch_tool_flag = False

    def colorizeEffect_wt(self, button):
        color = QGraphicsColorizeEffect(self)
        color.setColor(Qt.white)
        button.setGraphicsEffect(color)

    def colorizeEffect_gr(self, button):
        color = QGraphicsColorizeEffect(self)
        color.setColor(qRgb(80, 80, 80))
        button.setGraphicsEffect(color)

    def colorizeEffect_dgr(self, button):
        color = QGraphicsColorizeEffect(self)
        color.setColor(qRgb(35, 35, 35))
        button.setGraphicsEffect(color)

    def colorizeEffect_rd(self, button):
        color = QGraphicsColorizeEffect(self)
        color.setColor(Qt.red)
        button.setGraphicsEffect(color)

    def show_details(self):
        if self.ui.main_frame_tbl_02.isVisible():
            self.ui.main_frame_tbl_02.hide()
            self.ui.actionShow_Details.setText('Show Details')
        else:
            self.ui.main_frame_tbl_02.show()
            self.ui.actionShow_Details.setText('Hide Details')

    def show_loudness(self):
        if self.ui.frame_wave.isVisible():
            self.ui.frame_wave.hide()
            self.ui.actionShow_Loudness.setText('Show Loudness meter')

        else:
            self.ui.frame_wave.show()
            self.ui.actionShow_Loudness.setText('Hide Loudness meter')


    def table_key_press_event(self, event):
        QtWidgets.QTableWidget.keyPressEvent(self.ui.tableWidget_01, event)

        if event.key() == Qt.Key_Up:
            try:
                self.click_table_w()
            except Exception:
                pass
        elif event.key() == Qt.Key_Down:
            try:
                self.click_table_w()
            except Exception:
                pass
        elif event.key() == Qt.Key_Escape:
            try:
                self.ui.tableWidget_01.clearSelection()
            except Exception:
                pass



    def table_mouse_key_press_event(self, event):
        QtWidgets.QTableWidget.mousePressEvent(self.ui.tableWidget_01, event)

        if event.button() == Qt.LeftButton:
            pass

        elif event.button() == Qt.RightButton:
            if self.ui.tableWidget_01.rowCount() == 0:
                self.table_01_right_click_min()
            else:
                self.table_01_right_click_max()

    def table_db_key_press_event(self, event):
        QtWidgets.QTableView.keyPressEvent(self.ui.tableView_db, event)

        if event.key() == Qt.Key_Up:
            try:
                self.click_table_db()
            except Exception:
                pass
            # print('up')
        elif event.key() == Qt.Key_Down:
            try:
                self.click_table_db()
            except Exception:
                pass
        elif event.key() == Qt.Key_Escape:
            try:
                self.ui.tableView_db.clearSelection()
            except Exception:
                pass

    def table_db_mouse_key_press_event(self, event):
        QtWidgets.QTableView.mousePressEvent(self.ui.tableView_db, event)
        if event.button() == Qt.LeftButton:
            pass
            # print("Left Button Clicked")

        elif event.button() == Qt.RightButton:
            if self.sqlite_model.rowCount() == 0:
                self.table_db_right_click_min()
            else:
                self.table_db_right_click_max()

    def switch_db_editor(self):
        self.update_db_table()
        if self.ui.tableWidget_01.isVisible():
            self.check_table_bd()
            self.ui.tableWidget_01.hide()
            self.ui.tableView_db.show()
            self.ui.move_to_tableButton.show()
            self.ui.delete_from_dbButton.show()
            self.ui.move_to_dbButton.show()

            self.ui.addButton.hide()
            self.ui.delButton.hide()

            self.ui.r128DtctButton.hide()
            self.ui.blckDtctButton.hide()
            self.ui.slncDtctButton.hide()
            self.ui.frzDtctButton.hide()
            self.ui.fullDtctButton.hide()
            self.filter_table.setPlaceholderText("Search...")
            # self.ui.toolBar.show()

        else:
            self.ui.tableWidget_01.show()
            self.ui.tableView_db.hide()
            self.ui.addButton.show()
            self.ui.delButton.show()
            self.ui.move_to_tableButton.hide()
            self.ui.delete_from_dbButton.hide()
            self.ui.move_to_dbButton.hide()

            self.ui.r128DtctButton.show()
            self.ui.blckDtctButton.show()
            self.ui.slncDtctButton.show()
            self.ui.frzDtctButton.show()
            self.ui.fullDtctButton.show()
            self.filter_table.setPlaceholderText("Filter...")
            # self.ui.toolBar.hide()


    def update_db_editor(self):
        tbl_name = self.db_settings.db_list.currentText()
        # tbl_name = 'Video'
        self.sqlite_model.setTable(self.read_tbl_name())
        # self.model.select()

    def open_db(self):
        connection = sqlite3.connect('videoinfo.db')
        connection.commit()
        print('Соединение установлено')

    def close_db(self):
        connection = sqlite3.connect('videoinfo.db')
        connection.close()
        print('Соединение закрыто')

    def export_db_xlsx(self):
        if self.selected_db == 'SQLITE':
            DataLite().export_db_to_xlsx()
        else:
            DataPos().export_xlsx()

    def export_tbl_xlsx(self):
        if self.selected_db == 'SQLITE':
            DataLite().export_tbl_to_xlsx(self.read_tbl_name())
        else:
            DataPos().export_tbl_to_xlsx(self.read_tbl_name())


    def show_db_tables(self):
        self.db_settings.db_list.clear()
        # self.db_tables = QtWidgets.QDialog()
        if self.selected_db == 'SQLITE':
            tbl_list = DataLite().show_all_tbl()
        else:
            tbl_list = DataPos().show_all_tbl()

        self.db_settings.db_list.setEditable(True)
        self.db_settings.db_list.addItems(tbl_list)
        self.db_settings.connectButton.clicked.connect(self.save_db_settings)
        self.db_settings.cancelButton.clicked.connect(self.cancel_db_settings)

        self.db_sett.show()

    def save_db_settings(self):
        # tbl = self.db_settings.db_list.currentText()
        self.update_db_editor()
        self.db_sett.close()

    def temp_db_settings(self):
        self.temp_tbl = self.db_settings.db_list.currentText()
        self.temp_tbl_list = self.db_settings.db_list.currentIndex()
        print(self.temp_tbl_list)

    def call_temp_db_settings(self):
        self.db_settings.db_list.addItems(self.temp_tbl_list)
        self.db_settings.db_list.setCurrentText(str(self.temp_tbl))

    def cancel_db_settings(self):
        self.db_sett.close()

    def create_new_db(self):
        db_name, check = QFileDialog.getSaveFileName(None, "Create Base", "new_database.db", "Docu Base (*.db)")
        if check:
            if self.selected_db == 'SQLITE':
                DataLite().create_table(self.read_tbl_name())
            else:
                DataPos().create_table(self.read_tbl_name())

    def selected_db_file_list(self):
        items = self.ui.tableView_db.selectionModel().selectedRows()
        file_list = [item.data() for item in items]
        return tuple(file_list)

    def selected_db_file_path(self):
        index = self.ui.tableView_db.selectionModel().currentIndex()
        index_item = index.sibling(index.row(), index.column()).data()
        file_path = index.sibling(index.row(), 0).data()
        return file_path

    def click_table_db(self):
        file_path = self.selected_db_file_path()
        self.create_table_02(file_path)
        self.create_tags(file_path)
        self.show_waves(file_path)

    def move_to_table_01(self):
        file_list = self.selected_db_file_list()
        if len(file_list) != 0:
            self.ui.tableWidget_01.setRowCount(0)
            self.switch_db_editor()


    def move_to_db(self):
        tbl_name = self.read_tbl_name()
        DataPos().create_table(tbl_name)
        file_list = self.selected_db_file_list()
        for file_path in file_list:
            headers = DataLite().read_all_headers(tbl_name)
            DataPos().add_columns(tbl_name, headers)
            data = DataLite().read_all_data_for_file(tbl_name, file_path)
            DataPos().move_video(tbl_name, file_path, headers, tuple(data))


    def selected_rows(self):
        items = self.ui.tableWidget_01.selectionModel().selectedRows()
        selected_rows = [item.row() for item in items]
        return selected_rows

    def selected_file_list(self):
        items = self.ui.tableWidget_01.selectionModel().selectedRows()
        return [item.data() for item in items]

    def choose_default_dir(self):
        directory = r'\\slave\storage\ContentX'
        file_path = QFileDialog.getExistingDirectory(self, caption="Choose directory", dir=directory)
        if file_path:
            self.config['path']['default_path'] = file_path
            self.write_config()
        return file_path

    def get_file_list(self):
        directory = self.config['path']['default_path']
        file_list = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select files',
            dir=directory,
            filter='Video files (*.mp4 *.mkv *.mov *.m4v *.avi *.mpeg *.mts *.m2ts *.mxf *.ts *.webm *.wmv);;'
                   'Audio files (*.aac *.ac3 *.mp2 *.mp3 *.aif *.dts *.flac *.m4a *.ogg *.opus *.wav *.wma);;'
                   'All files (*.*)'
        )
        return file_list[0]

    def start_ffprobe(self):
        file_list = self.get_file_list()
        complited = False
        total_files = len(file_list)
        for num, file_path in enumerate(file_list, 1):
            file_info = self.mongo.find_file(file_path)
            if not file_info:
                params = {
                    'file_path': file_path, 'num': num, 'total_files': total_files
                }
                print(now())
                print('Сбор данных для файла', file_path)
                scanner = FFprobeScan(**params)
                scanner.signals.started.connect(self.on_started)
                scanner.signals.progress.connect(self.on_progress)
                scanner.signals.finished.connect(self.on_finished)
                scanner.signals.error.connect(self.on_error)
                scanner.signals.scan_result.connect(self.create_table_01)
                self.ffprobe_scanners.append(scanner)
                self.thread_pool.start(scanner)
                print(now())
                print('Сбор данных завершён')
            else:
                self.create_table_01(file_path, file_info)
            complited = True
        return complited

    def prepare_table_01(self):
        file_list = self.get_file_list()
        total_files = len(file_list)
        for num, file_path in enumerate(file_list, 1):
            if not os.path.exists(file_path):
                print('files offline')
                continue
            row_count = self.ui.tableWidget_01.rowCount()
            tbl_file_list = []
            for row in range(row_count):
                tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
                tbl_file_list.append(tbl_file_path)
            if file_path not in tbl_file_list:
                print(now())
                print('Построение:', file_path)
                file_info = self.mongo.find_file(file_path)
                if not file_info:
                    print('Scanning')
                    params = {
                        'scan_type': 'creating_table', 'file_path': file_path, 'num': num, 'total_files': total_files
                    }
                    scanner = FFprobeScan(**params)
                    scanner.signals.started.connect(self.on_started_ffprobe)
                    scanner.signals.finished.connect(self.on_finished_ffprobe)
                    scanner.signals.error.connect(self.on_error_ffprobe)
                    scanner.signals.scan_result.connect(self.create_table_01)
                    self.ffprobe_scanners.append(scanner)
                    self.thread_pool.start(scanner)
                else:
                    print('Use DB')
                    self.create_table_01(file_path, file_info)
            else:
                print('Вы пытаетесь добавить дубликат')


    def init_header(self, header_name):
        head = QTableWidgetItem()
        head.setData(Qt.EditRole, header_name)
        return head

    def init_item(self, val):
        item = QTableWidgetItem()
        # if val:
        item.setData(Qt.EditRole, val)
        # else:
        #     item.setData(Qt.EditRole, 'N/A')
        return item

    def prepare_data(self, file_path, file_info):

        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        audio = list(filter(lambda x: x.get('codec_type') == 'audio', streams))
        subtitle = list(filter(lambda x: x.get('codec_type') == 'subtitle', streams))
        cover = list(filter(lambda x: x.get('codec_type') == 'video' and x.get('level') == -99, streams))
        format = file_info.get('format')
        ffmpeg_scanners = file_info.get('ffmpeg_scanners')

        file_name = os.path.basename(file_path)
        a_audio_map = len(audio)
        v_codec_type = video[0].get('codec_type')
        v_codec_name = video[0].get('codec_name')
        v_width = video[0].get('width')
        v_height = video[0].get('height')
        v_sample_aspect_ratio = video[0].get('sample_aspect_ratio')
        v_display_aspect_ratio = video[0].get('display_aspect_ratio')
        v_frame_rate = video[0].get('r_frame_rate')

        a_codec_name = audio[0].get('codec_name')
        a_sample_rate = audio[0].get('sample_rate')
        a_channels = audio[0].get('channels')
        a_bit_rate = audio[0].get('bit_rate')

        f_bit_rate = format.get('bit_rate')
        f_duration = format.get('duration')
        f_size = format.get('size')
        f_frame_rate = format.get('r_frame_rate')

        r128 = ffmpeg_scanners.get('r128')
        if r128:
            input_i = r128.get('input_i')
            input_tp = r128.get('input_tp')
            input_lra = r128.get('input_lra')
            input_thresh = r128.get('input_thresh')
        else:
            input_i, input_tp, input_lra, input_thresh = '', '', '', ''

        black_screen = ffmpeg_scanners.get('black_screen')
        silence = ffmpeg_scanners.get('silence')
        freeze = ffmpeg_scanners.get('freeze')

        return (file_path, file_name, convert_bytes(f_bit_rate, "bit/s"), v_codec_name, v_width, v_height,
                v_sample_aspect_ratio, v_display_aspect_ratio, convert_fps(v_frame_rate),
                convert_duration(f_duration, v_frame_rate), a_audio_map, a_codec_name, convert_khz(a_sample_rate),
                a_channels, convert_bytes(a_bit_rate, "bit/s"), input_i, input_tp, input_lra, input_thresh,
                black_screen, silence, freeze)

    def create_table_01(self, file_path, file_info):
        # print(file_info)
        print(now())
        print('Построение таблицы')
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        row_position = self.ui.tableWidget_01.rowCount()
        # self.ui.tableWidget_01.setRowCount(row_position)
        self.ui.tableWidget_01.insertRow(row_position)

        for col, val in enumerate(self.prepare_data(file_path, file_info)):
            self.ui.tableWidget_01.setItem(row_position, col, self.init_item(val))

            if row_position % 2 != 0:
                self.ui.tableWidget_01.item(row_position, col).setBackground(self.grey_light)
            else:
                self.ui.tableWidget_01.item(row_position, col).setBackground(self.grey_dark)
        self.ui.tableWidget_01.selectRow(row_position)
        self.error_highlight()
        self.enable_ui_buttons()

    def enable_ui_buttons(self):
        self.ui.delButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.delButton)
        self.ui.playButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.playButton)
        self.ui.openButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.openButton)
        self.ui.r128DtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.r128DtctButton)
        self.ui.queueButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.queueButton)
        self.ui.blckDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.blckDtctButton)
        self.ui.slncDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.slncDtctButton)
        self.ui.exportButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.exportButton)
        self.ui.frzDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.frzDtctButton)
        self.ui.fullDtctButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.fullDtctButton)
        # self.ui.migrateButton.setEnabled(True)
        self.colorizeEffect_wt(self.ui.migrateButton)
        self.ui.tableWidget_01.setSortingEnabled(True)
        self.table_mode = True

    def filter_table_01(self):
        search_query = self.filter_table.text()
        file_list_tbl = self.file_queue()
        if search_query in file_list_tbl:
            print('Find')
        else:
            print('No')

    def create_table_02(self, file_path):
        file_info = self.mongo.find_file(file_path)
        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        audio = list(filter(lambda x: x.get('codec_type') == 'audio', streams))
        subtitle = list(filter(lambda x: x.get('codec_type') == 'subtitle', streams))
        format = [file_info.get('format')]

        self.ui.tableWidget_02.setRowCount(0)
        for type_info in (video, audio, subtitle, format):
            for stream_info in type_info:
                self.block_table_02(stream_info)

    def block_table_02(self, stream_info):
        for head, value in stream_info.items():
            row_position = self.ui.tableWidget_02.rowCount()
            self.ui.tableWidget_02.insertRow(row_position)
            self.ui.tableWidget_02.setColumnWidth(0, 120)
            self.ui.tableWidget_02.setColumnWidth(1, 220)
            self.ui.tableWidget_02.setItem(row_position, 0, QtWidgets.QTableWidgetItem(head))
            self.ui.tableWidget_02.item(row_position, 0).setForeground(QColor(146, 146, 146))
            self.ui.tableWidget_02.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(value)))
            self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(30, 30, 30))
        self.ui.tableWidget_02.insertRow(self.ui.tableWidget_02.rowCount())

    def check_value(self, head_val):
        head, value = head_val
        if 'size' in head:
            value = convert_bytes(int(value), "b")
        if 'bit_rate' in head:
            value = convert_bytes(int(value), "bit/s")
        if 'duration' in head:
            fps = convert_fps(value).split(' ')[0]
            value = str(convert_duration(value, fps))
        if 'frame_rate' in head:
            value = convert_fps(value)
        if 'sample_rate' in head:
            value = convert_khz(value)
        if 'level' in head:
            value = int(value) / 10
        return value

    def click_table_w(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        self.create_table_02(file_path)
        self.create_tags(file_path)
        self.show_waves(file_path)
        self.check_file_path()
        return file_path

    def double_click_video_player(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        if self.video_info_player is None:
            self.video_info_player = VideoInfoPlayer(file_path)

    def table_01_right_click_min(self):
        top_menu = QMenu()

        menu = top_menu.addMenu("Menu")

        add_files = menu.addAction("Add files ...\t")
        menu.addSeparator()
        switch_mode = menu.addAction("Switch ViewMode\t")

        action = menu.exec(QtGui.QCursor.pos())

        if action == add_files:
            self.start_ffprobe()
        elif action == switch_mode:
            self.switch_db_editor()


    def table_01_right_click_max(self):
        top_menu = QMenu()

        menu = top_menu.addMenu("Menu")
        file = menu.addMenu("File ...\t")

        add_files = file.addAction("Add files ...\t")
        del_selected = file.addAction("Delete seleted\t")

        file.addSeparator()

        play_selected = file.addAction("Play selected")
        open_folder = file.addAction("Open folder")

        scanners = menu.addMenu("Scanners ...\t")
        loudnorm_scan = scanners.addAction("Run Loudnorm scan selected\t")
        blackdetect_scan = scanners.addAction("Run Blackdetect scan selected\t")
        silencedetect_scan = scanners.addAction("Run Silencedetect scan selected\t")
        freezedetect_scan = scanners.addAction("Run Freezedetect scan selected\t")
        menu.addSeparator()
        switch_mode = menu.addAction("Switch ViewMode\t")
        action = menu.exec(QtGui.QCursor.pos())

        if action == add_files:
            self.start_ffprobe()
        elif action == del_selected:
            self.del_selected_rows()
        elif action == play_selected:
            self.play_selected()
        elif action == open_folder:
            self.open_folder()
        elif action == loudnorm_scan:
            self.scan_loudnorm()
        elif action == silencedetect_scan:
            self.scan_silence_detect()
        elif action == blackdetect_scan:
            self.scan_black_detect()
        elif action == freezedetect_scan:
            self.scan_freeze_detect()
        elif action == switch_mode:
            self.switch_db_editor()

    def table_db_right_click_min(self):
        top_menu = QMenu()

        menu = top_menu.addMenu("Menu")

        export_excel = menu.addAction("Export table to Excel\t")
        menu.addSeparator()
        switch_mode = menu.addAction("Switch ViewMode\t")

        action = menu.exec(QtGui.QCursor.pos())

        if action == export_excel:
            self.export_tbl_xlsx()
        elif action == switch_mode:
            self.switch_db_editor()

    def table_db_right_click_max(self):
        # bar = self.parent.menuBar()
        top_menu = QMenu()

        menu = top_menu.addMenu("Menu")
        file = menu.addMenu("File ...\t")

        move_to_tbl = file.addAction("Move to table ...\t")
        del_frm_db = file.addAction("Delete from db\t")
        move_to_db = file.addAction("Move to server db\t")

        file.addSeparator()

        play_selected = file.addAction("Play selected")
        open_folder = file.addAction("Open folder")

        scanners = menu.addMenu("DataBase ...\t")
        reset_scan_results = scanners.addAction("Reset scan results\t")
        menu.addSeparator()
        switch_mode = menu.addAction("Switch ViewMode\t")

        action = menu.exec(QtGui.QCursor.pos())

        if action == move_to_tbl:
            self.move_to_table_01()
        elif action == del_frm_db:
            self.del_file_from_db()
        elif action == play_selected:
            self.play_selected()
        elif action == open_folder:
            self.open_folder()
        elif action == move_to_db:
            self.move_to_db()
        elif action == reset_scan_results:
            self.reset_mediainfo_db()
        elif action == switch_mode:
            self.switch_db_editor()


    def create_tags(self, file_path):
        file_name = os.path.basename(file_path)
        file_info = self.mongo.find_file(file_path)

        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        audio = list(filter(lambda x: x.get('codec_type') == 'audio', streams))
        subtitle = list(filter(lambda x: x.get('codec_type') == 'subtitle', streams))
        format = file_info.get('format')

        if len(video) > 0:
            video1 = video[0]
        else:
            video1 = {}

        if len(audio) == 1:
            audio1 = audio[0]
            audio2 = {}
        elif len(audio) > 1:
            audio1 = audio[0]
            audio2 = audio[1]
        else:
            audio1 = {}
            audio2 = {}

        if len(subtitle) == 1:
            sub1 = subtitle[0].get('tags')
            sub2 = {}
        elif len(subtitle) > 1:
            sub1 = subtitle[0].get('tags')
            sub2 = subtitle[1].get('tags')
        else:
            sub1 = {}
            sub2 = {}

        width = video1.get('width')
        height = video1.get('height')
        if width and height:
            self.ui.tag_resolution.setText(f'{width} x {height}')
        else:
            self.ui.tag_resolution.setText('')
        prof = video1.get('profile')
        lev = video1.get('level')
        if prof and lev:
            self.ui.tag_v1_profile.setText(f'{prof} {int(lev) / 10}')
        else:
            self.ui.tag_v1_profile.setText('')

        self.ui.tag_file_name.setText(file_name)
        self.ui.tag_file_path.setText(os.path.split(file_path)[0])
        self.ui.tag_v1_codec_name.setText(video1.get('codec_name'))
        self.ui.tag_a1_codec_name.setText(audio1.get('codec_name'))
        self.ui.tag_a2_codec_name.setText(audio2.get('codec_name'))
        self.ui.tag_a1_sample_rate.setText(convert_khz(audio1.get('sample_rate')))
        self.ui.tag_a2_sample_rate.setText(convert_khz(audio2.get('sample_rate')))
        self.ui.tag_a1_channel_layout.setText(audio1.get('channel_layout'))
        self.ui.tag_a2_channel_layout.setText(audio2.get('channel_layout'))
        self.ui.tag_s1_title.setText(sub1.get('title'))
        self.ui.tag_s2_title.setText(sub2.get('title'))
        self.ui.tag_s1_language.setText(sub1.get('language'))
        self.ui.tag_s2_language.setText(sub2.get('language'))
        self.ui.tag_v1_r_frame_rate.setText(convert_fps(video1.get('r_frame_rate')))
        self.ui.tag_duration.setText(convert_duration(format.get('duration'), video1.get('r_frame_rate')))

    def alternating_rows(self, row, col):
        if row % 2 != 0:
            self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
        else:
            self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)

    def error_highlight(self):

        codec = self.config['Video_standard']['codec']
        width = self.config['Video_standard']['width']
        height = self.config['Video_standard']['height']
        v_bit_rate = float(self.config['Video_standard']['v_bit_rate'])
        frame_rate = self.config['Video_standard']['frame_rate']
        dar = self.config['Video_standard']['dar']
        codec_aud = self.config['Audio_standard']['codec_aud']
        channels = self.config['Audio_standard']['channels']
        sample_rate = str(self.config['Audio_standard']['sample_rate'])
        a_bit_rate = float(self.config['Audio_standard']['a_bit_rate'])

        r128_i = self.config['Loudness_meter']['r128_i']
        r128_lra = self.config['Loudness_meter']['r128_lra']
        r128_tp = self.config['Loudness_meter']['r128_tp']
        r128_thr = self.config['Loudness_meter']['r128_thr']

        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()

        for row in range(rows):
            for col in range(columns):
                self.alternating_rows(row, col)

            item = self.ui.tableWidget_01.item(row, 2)
            if item.text() and not isclose(float(item.text().split(' ')[0]), v_bit_rate, abs_tol=1):
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 3)
            if item.text() != codec:
                item.setBackground(self.red_dark)

            item = self.ui.tableWidget_01.item(row, 4)
            if item.text() != width:
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 5)
            if item.text() != height:
                item.setBackground(self.red_dark)

            item = self.ui.tableWidget_01.item(row, 7)
            if item.text() != dar:
                item.setBackground(self.red_dark)

            item = self.ui.tableWidget_01.item(row, 8)
            if item.text().split(' ')[0] != str(frame_rate):
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 10)
            if item.text() != 1:
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 11)
            if item.text() != codec_aud:
                item.setBackground(self.red_dark)

            item = self.ui.tableWidget_01.item(row, 12)
            if item.text().split(' ')[0] != str(sample_rate):
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 13)
            if item.text() != channels:
                item.setBackground(self.red_dark)

            item = self.ui.tableWidget_01.item(row, 14)
            if item.text() and not isclose(float(item.text().split(' ')[0]), a_bit_rate, abs_tol=60):
                item.setBackground(self.red_light)

            item = self.ui.tableWidget_01.item(row, 15)
            if item.text() == '-Inf':
                item.setBackground(self.red_dark)
            elif item.text() and not isclose(float(item.text()), float(r128_i), abs_tol=0.5):
                item.setBackground(self.yell_dark)

            item = self.ui.tableWidget_01.item(row, 16)
            if item.text() == '-Inf':
                item.setBackground(self.red_light)
            elif item.text() and not isclose(float(item.text()), float(r128_tp), abs_tol=0.5):
                item.setBackground(self.yell_light)

            item = self.ui.tableWidget_01.item(row, 17)
            if item.text() and not isclose(float(item.text()), float(r128_lra), abs_tol=5):
                item.setBackground(self.yell_dark)

            item = self.ui.tableWidget_01.item(row, 18)
            if item.text() and not isclose(float(item.text()), float(r128_thr), abs_tol=0.5):
                item.setBackground(self.yell_light)
                #
                # if self.header_rename('black_start') in header:
                #     if data == 'найден':
                #         self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                # if self.header_rename('silence_start') in header:
                #     if data == 'найден':
                #         self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                # if self.header_rename('freeze_start') in header:
                #     if data == 'найден':
                #         self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
        self.check_file_path()

    def check_file_path(self):
        rows = self.ui.tableWidget_01.rowCount()
        for row in range(rows):
            file_path = self.ui.tableWidget_01.item(row, 0).text()
            columns = self.ui.tableWidget_01.columnCount()
            if not os.path.exists(file_path):
                self.ui.tableWidget_01.item(row, 1).setText('OFFLINE_' + os.path.basename(file_path))
                for col in range(columns):
                    self.ui.tableWidget_01.item(row, col).setForeground(self.yell_dark)
                # print('file offline')
            else:
                self.ui.tableWidget_01.item(row, 1).setText(os.path.basename(file_path))
                for col in range(columns):
                    self.ui.tableWidget_01.item(row, col).setForeground(self.white)
                # self.update_table_01(file_path, row)

    def check_data_base(self):
        self.list_widget_offline = QListWidget()
        self.list_widget_offline.setWindowTitle('Offline files')
        self.list_widget_offline.setMinimumWidth(700)
        tbl_name = self.read_tbl_name()
        offline_list = []

        if self.selected_db == 'SQLITE':
            db_file_list = DataLite().read_all_files(tbl_name)
            print(db_file_list)
        else:
            db_file_list = DataPos().read_all_files(tbl_name)
        for file_path in db_file_list:
            if not os.path.exists(file_path):
                offline_list.append(file_path)
                print(file_path, 'offline')
        if not offline_list:
            self.list_widget_offline.addItem("No offline. It's OK!")
        else:
            self.list_widget_offline.addItems(offline_list)
        self.list_widget_offline.show()


    def del_row(self):
        row_position = self.ui.tableWidget_01.currentRow()
        self.ui.tableWidget_01.removeRow(row_position)
        if self.ui.tableWidget_01.rowCount() == 0:
            self.ui.delButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.delButton)
            self.ui.playButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.playButton)
            self.ui.openButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.openButton)
            self.ui.r128DtctButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.r128DtctButton)
            self.ui.queueButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.queueButton)
            self.ui.queueButton.hide()
            self.ui.blckDtctButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.blckDtctButton)
            self.ui.slncDtctButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.slncDtctButton)
            self.ui.frzDtctButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.frzDtctButton)
            self.ui.fullDtctButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.fullDtctButton)
            self.ui.tableWidget_02.setRowCount(0)
            self.ui.wave_view.setPixmap(QPixmap(u":/imgs/img/WaveForm_04.png"))
            self.ui.r128_loudness.setText('LOUDNESS METER')


    def del_selected_rows(self):
        rows = self.selected_rows()
        for row in sorted(rows, reverse=True):
            self.ui.tableWidget_01.removeRow(row)
            if row == 0:
                self.ui.tableWidget_01.selectRow(row)
            else:
                self.ui.tableWidget_01.selectRow(row-1)
            if self.ui.tableWidget_01.rowCount() == 0:
                self.ui.delButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.delButton)
                self.ui.playButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.playButton)
                self.ui.openButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.openButton)
                self.ui.r128DtctButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.r128DtctButton)
                self.ui.queueButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.queueButton)
                self.ui.queueButton.hide()
                self.ui.blckDtctButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.blckDtctButton)
                self.ui.slncDtctButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.slncDtctButton)
                self.ui.frzDtctButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.frzDtctButton)
                self.ui.fullDtctButton.setEnabled(False)
                self.colorizeEffect_gr(self.ui.fullDtctButton)
                self.ui.tableWidget_02.setRowCount(0)
                self.ui.wave_view.setPixmap(QPixmap(u":/imgs/img/WaveForm_04.png"))
                self.ui.r128_loudness.setText('LOUDNESS METER')
        self.error_highlight()

    def check_table_bd(self):
        self.sqlite_model.select()
        if self.posql_model.rowCount() == 0:
            self.ui.move_to_tableButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.move_to_tableButton)
            self.ui.delete_from_dbButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.delete_from_dbButton)
            self.ui.move_to_dbButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.move_to_dbButton)
            self.ui.playButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.playButton)
            self.ui.openButton.setEnabled(False)
            self.colorizeEffect_gr(self.ui.openButton)
        if self.sqlite_model.rowCount() != 0 and self.ui.tableWidget_01.rowCount() != 0:
            self.ui.move_to_tableButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.move_to_tableButton)
            self.ui.delete_from_dbButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.delete_from_dbButton)
            self.ui.move_to_dbButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.move_to_dbButton)
            self.ui.playButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.playButton)
            self.ui.openButton.setEnabled(True)
            self.colorizeEffect_wt(self.ui.openButton)

    def clear_table_01(self):
        self.ui.tableWidget_01.setRowCount(0)

    def file_queue(self):
        row_count = self.ui.tableWidget_01.rowCount()
        queue_list = []
        if row_count != 0:
            for row in range(row_count):
                file_path = self.ui.tableWidget_01.item(row, 0).text()
                queue_list.append(file_path)
            return queue_list

    def play_selected(self):
        if self.ui.tableWidget_01.isVisible():
            row_position = self.ui.tableWidget_01.currentRow()
            if row_position > 0:
                file_path = self.ui.tableWidget_01.item(row_position, 0).text()
                os.startfile(os.path.normpath(file_path))
        else:
            file_path = self.selected_db_file_path()
            os.startfile(os.path.normpath(file_path))



    def open_folder(self):
        try:
            if self.ui.tableWidget_01.isVisible():
                row_position = self.ui.tableWidget_01.currentRow()
                file_path = self.ui.tableWidget_01.item(row_position, 0).text()
            else:
                file_path = self.selected_db_file_path()
            subprocess.Popen(fr'explorer /select,"{os.path.abspath(file_path)}"')
        except Exception:
            print('Файл не выделен')

    def scan_loudnorm(self):
        file_list = self.selected_file_list()

        r128_i = self.config['Loudness_meter']['r128_i']
        r128_lra = self.config['Loudness_meter']['r128_lra']
        r128_tp = self.config['Loudness_meter']['r128_tp']
        r128_thr = self.config['Loudness_meter']['r128_thr']

        total_files = len(file_list)
        for num, file_path in enumerate(file_list, 1):
            params = {
                'file_path': file_path,
                'scan_type': 'loudness_scan', 'num': num, 'total_files': total_files,
                'r128_i': r128_i, 'r128_lra': r128_lra, 'r128_tp': r128_tp, 'r128_thr': r128_thr
            }
            file_info = self.mongo.find_file(file_path)
            dur = convert_fram_duration(file_info)
            # if self.progress_dialog.wasCanceled():
            #     break
            ffmpeg_scanners = file_info.get('ffmpeg_scanners')
            if not ffmpeg_scanners.get('r128'):
                print(now())
                print('Запуск анализа уровня громкости файла', file_path)
                scanner = R128Scan(**params)
                scanner.signals.started.connect(self.on_started)
                scanner.signals.progress.connect(self.on_progress)
                scanner.signals.finished.connect(self.on_finished)
                scanner.signals.scan_result.connect(self.add_table_r128)
                scanner.signals.error.connect(self.on_error)
                self.ffmpeg_scanners.append(scanner)
                self.thread_pool.start(scanner)
            else:
                print(now())
                print('Сканирование R128 файла', file_path, 'уже проводилось')

    def scan_black_detect(self):
        tbl_file_list = self.selected_file_list()
        total_files = len(tbl_file_list)
        blck_dur = self.config['Damage_test_black']['blck_dur']
        blck_thr = self.config['Damage_test_black']['blck_thr']
        blck_tc_in = self.config['Damage_test_black']['blck_tc_in']
        blck_tc_out = self.config['Damage_test_black']['blck_tc_out']
        for num, tbl_file_path in enumerate(tbl_file_list, 1):
            file_info = self.mongo.find_file(tbl_file_path)
            ffmpeg_scanners = file_info.get('ffmpeg_scanners')
            if not ffmpeg_scanners.get('black_detect'):
                params = {
                    'file_path': tbl_file_path,
                    'scan_type': 'black_detect_scan', 'num': num, 'total_files': total_files,
                    'black_check': self.config['Damage_test_black']['checkbox'],
                    'blck_dur': blck_dur, 'blck_thr': blck_thr, 'blck_tc_in': blck_tc_in, 'blck_tc_out': blck_tc_out
                }
                print(now())
                print('Анализ чёрного поля файла', tbl_file_path)
                scanner = BlackDetect(**params)
                scanner.signals.started.connect(self.on_started)
                scanner.signals.progress.connect(self.on_progress)
                scanner.signals.finished.connect(self.on_finished)
                scanner.signals.scan_result.connect(self.add_table_black)
                scanner.signals.error.connect(self.on_error)
                self.ffprobe_scanners.append(scanner)
                self.thread_pool.start(scanner)
            else:
                print('Сканирование чёрного поля файла', tbl_file_path, 'уже проводилось')

    def scan_silence_detect(self):
        tbl_file_list = self.selected_file_list()
        total_files = len(tbl_file_list)
        slnc_dur = self.config['Damage_test_silence']['slnc_dur']
        slnc_noize = self.config['Damage_test_silence']['slnc_noize']
        slnc_tc_in = self.config['Damage_test_silence']['slnc_tc_in']
        slnc_tc_out = self.config['Damage_test_silence']['slnc_tc_out']
        for num, tbl_file_path in enumerate(tbl_file_list, 1):
            # if progress_dialog_slnc.wasCanceled():
            #     break
            file_info = self.mongo.find_file(tbl_file_path)
            ffmpeg_scanners = file_info.get('ffmpeg_scanners')
            if not ffmpeg_scanners.get('silence_detect'):
                params = {
                    'file_path': tbl_file_path,
                    'scan_type': 'silence_detect_scan', 'num': num, 'total_files': total_files,
                    'silence_check': self.config['Damage_test_silence']['checkbox'],
                    'slnc_dur': slnc_dur, 'slnc_noize': slnc_noize, 'slnc_tc_in': slnc_tc_in, 'slnc_tc_out': slnc_tc_out
                }
                print(now())
                print('Анализ пропусков звука в', tbl_file_path)
                scanner = SilenceDetect(**params)
                scanner.signals.started.connect(self.on_started)
                scanner.signals.progress.connect(self.on_progress)
                scanner.signals.finished.connect(self.on_finished)
                scanner.signals.scan_result.connect(self.add_table_silence)
                scanner.signals.error.connect(self.on_error)
                self.ffmpeg_scanners.append(scanner)
                self.thread_pool.start(scanner)
            else:
                print('Сканирование пропусков звука в', tbl_file_path, 'уже проводилось')

    def scan_freeze_detect(self):
        tbl_file_list = self.selected_file_list()
        total_files = len(tbl_file_list)
        frz_dur = self.config['Damage_test_freeze']['frz_dur']
        frz_noize = self.config['Damage_test_freeze']['frz_noize']
        frz_tc_in = self.config['Damage_test_freeze']['frz_tc_in']
        frz_tc_out = self.config['Damage_test_freeze']['frz_tc_out']
        for num, tbl_file_path in enumerate(tbl_file_list, 1):
            file_info = self.mongo.find_file(tbl_file_path)
            ffmpeg_scanners = file_info.get('ffmpeg_scanners')
            if not ffmpeg_scanners.get('freeze_detect'):
                print(now())
                print('Анализ стоп-кадров в', tbl_file_path)
                params = {
                    'file_path': tbl_file_path,
                    'scan_type': 'freeze_detect_scan', 'num': num, 'total_files': total_files,
                    'freeze_check': self.config['Damage_test_freeze']['checkbox'],
                    'frz_dur': frz_dur, 'frz_noize': frz_noize, 'frz_tc_in': frz_tc_in,
                    'frz_tc_out': frz_tc_out
                }
                scanner = FreezeDetect(**params)
                scanner.signals.started.connect(self.on_started)
                scanner.signals.progress.connect(self.on_progress)
                scanner.signals.finished.connect(self.on_finished)
                scanner.signals.scan_result.connect(self.add_table_freeze)
                scanner.signals.error.connect(self.on_error)
                self.ffmpeg_scanners.append(scanner)
                self.thread_pool.start(scanner)
            else:
                print('Анализ стоп-кадров в', tbl_file_path, 'уже проводился')


    def full_detect(self):
        self.scan_loudnorm()
        self.scan_black_detect()
        self.scan_silence_detect()
        self.scan_freeze_detect()

    def add_table_r128(self, file_path, scan_result):
        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()
        for row in range(rows):
            tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
            print(file_path, tbl_file_path)
            for col in range(columns):
                if tbl_file_path == file_path:
                    item = self.ui.tableWidget_01.item(row, 15)
                    item.setText(scan_result.get('input_i', 'not scanned'))
                    item = self.ui.tableWidget_01.item(row, 16)
                    item.setText(scan_result.get('input_tp', 'not scanned'))
                    item = self.ui.tableWidget_01.item(row, 17)
                    item.setText(scan_result.get('input_lra', 'not scanned'))
                    item = self.ui.tableWidget_01.item(row, 18)
                    item.setText(scan_result.get('input_thresh', 'not scanned'))
        self.error_highlight()

    def add_table_black(self, file_path, scan_result):
        rows = self.ui.tableWidget_01.rowCount()
        if scan_result and scan_result != 'N/A':
            item_text = 'found'
        elif not scan_result:
            item_text = 'not scanned'
        else:
            item_text = 'N/A'
        for row in range(rows):
            tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
            if tbl_file_path == file_path:
                item = self.ui.tableWidget_01.item(row, 19)
                item.setText(item_text)
        self.error_highlight()

    def add_table_silence(self, file_path, scan_result):
        rows = self.ui.tableWidget_01.rowCount()
        if scan_result and scan_result != 'N/A':
            item_text = 'found'
        elif not scan_result:
            item_text = 'not scanned'
        else:
            item_text = 'N/A'
        for row in range(rows):
            tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
            if tbl_file_path == file_path:
                item = self.ui.tableWidget_01.item(row, 20)
                item.setText(item_text)
        self.error_highlight()

    def add_table_freeze(self, file_path, scan_result):
        rows = self.ui.tableWidget_01.rowCount()
        if scan_result and scan_result != 'N/A':
            item_text = 'found'
        elif not scan_result:
            item_text = 'not scanned'
        else:
            item_text = 'N/A'
        for row in range(rows):
            tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
            if tbl_file_path == file_path:
                item = self.ui.tableWidget_01.item(row, 21)
                item.setText(item_text)
        self.error_highlight()

    def wave_view(self):
        self.ui.wave_view.show()
        self.ui.resizeButtonUp.hide()
        self.ui.resizeButtonDown.show()
        self.ui.r128_loudness.show()

    def wave_hide(self):
        self.ui.wave_view.hide()
        self.ui.r128_loudness.hide()
        self.ui.resizeButtonDown.hide()
        self.ui.resizeButtonUp.show()
        self.ui.frame_wave.setStyleSheet(u"QFrame#frame_wave{\nborder: 0px solid rgb(63,64,66);\n}")

    def show_waves(self, file_path):
        self.ui.frame_wave.setStyleSheet(u"QFrame#frame_wave{\nborder: 1px solid rgb(63,64,66);\n}")
        file_info = self.mongo.find_file(file_path)
        ffmpeg_scanners = file_info.get('ffmpeg_scanners')

        r128 = ffmpeg_scanners.get('r128')
        wave_directory = os.path.join(PARENT_DIRECTORY, 'waveforms')
        wave_file_path = os.path.join(wave_directory, hashlib.md5(file_path.encode('utf-8')).hexdigest() + '.png')
        if r128 and os.path.exists(wave_file_path):
            self.ui.wave_view.setPixmap(QPixmap(wave_file_path))
            input_i = r128.get('input_i')
            input_tp = r128.get('input_tp')
            input_lra = r128.get('input_lra')
            input_thresh = r128.get('input_thresh')
            text_info = f'  I = {input_i}  |  LRA = {input_lra}  |  TP = {input_tp}  |  THRESHOLD = {input_thresh}  '
            self.ui.r128_loudness.setText(text_info)
        else:
            self.ui.wave_view.setPixmap(QPixmap(u":/imgs/img/WaveForm_04.png"))
            # self.ui.r128_loudness.hide()
            self.ui.r128_loudness.setText('LOUDNESS METER')

    def closeEvent(self, event):
        print('Завершение')


class CustomDialog(QDialog):
    def __init__(self, message_text):
        super().__init__()

        self.setWindowTitle("Attention!")

        qbtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(message_text)
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class AttentionDialog(QDialog):
    def __init__(self, title, message_text):
        super().__init__()

        self.setWindowTitle(title)
        qbtn = QDialogButtonBox.StandardButton.Ok
        self.buttonBox = QDialogButtonBox(qbtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(message_text)
        message.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox, alignment=Qt.AlignCenter)
        self.setLayout(self.layout)


class TableModel(QAbstractTableModel):
    def __init__(self, headers, data):
        super().__init__()
        self._data = data
        self._headers = headers

    def headerData(self, section, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self._headers[section]
        if role == Qt.DisplayRole and orientation == Qt.Vertical:
            return section+1

    def data(self, index, role: int = Qt.DisplayRole):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index: QModelIndex = ...):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index: QModelIndex = ...):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        try:
            col = len(self._data[0])
        except Exception:
            col = 1
        return col


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    # qdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"})
    window = VideoInfo()
    window.show()
    sys.exit(app.exec())
