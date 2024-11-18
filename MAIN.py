from __future__ import annotations

import ast
import datetime
import os
import sqlite3
import subprocess
import sys
from math import isclose

# pip install pyqtdarktheme
# pip install pyqtdarktheme==2.1.0 --ignore-requires-python
import qdarktheme
# pip install pyside6
from PySide6 import QtWidgets, QtSql
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QColor, QPixmap, QIcon, qRgb
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtSql import QSqlTableModel
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QHeaderView, QTableWidgetItem, QSlider, \
    QGraphicsColorizeEffect, QProgressDialog, \
    QDialog

from db_connection import Data
from ffmpeg_main import R128, BlackDetect, SilenceDetect, FreezeDetect
from ffprobe_main import Info
from forms.ui_db_settings import Ui_DB_Settings
from forms.ui_settings import Ui_Settings
from forms.ui_videoinfo import Ui_MainWindow
from forms.ui_videoinfo_player import Ui_VideoINFO_Player


def now():
    now_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return now_time


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
    # 2**10 = 1024
    power = (2 ** 10)
    n = 0
    labels = ['', 'K', 'M', 'G', 'T']
    while size > power:
        size /= power
        n += 1
    val = f'{round(size, 2)} {labels[n]}{unit}'
    return val


def convert_duration_sec(data, fps):
    # print('dur:', data, type(data))
    # conv_data = datetime.timedelta(seconds=(round(float(data), 0)))
    # while data > sec:
    hh = int(data // 3600)
    mm = int((data % 3600) // 60)
    ss = int((data % 3600) % 60 // 1)
    ff = int(data % 1 * fps)
    # data /= sec
    conv_data = f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'
    # print(data)
    # print(fps)
    # print(ff)
    # print(conv_data)
    return conv_data


# def convert_duration_frames(data, fps):
#     val = data
#     sec = float(data) // fps
#     frames = float(data) % fps
#     convert = datetime.timedelta(seconds=sec)
#     val = str(convert) + str(round(frames, 0))
#     return val


class VideoInfo(QMainWindow):

    def __init__(self):
        super(VideoInfo, self).__init__()

        print(now())
        print('Создание базы данных')
        Data().create_database()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.table_mode = True
        self.switch_tool_flag = False

        self.ui.tableWidget_01.keyPressEvent = self.table_key_press_event
        # self.setFixedSize(self.ui.tableWidget_01.sizeHint())
        self.ui.tableWidget_01.horizontalHeader().setVisible(False)
        self.ui.tableWidget_01.setColumnCount(1)
        self.ui.tableWidget_01.hideColumn(0)
        # self.ui.tableWidget_01.hideColumn(15)
        # self.ui.tableWidget_01.hideColumn(16)
        # self.ui.tableWidget_01.hideColumn(17)
        # self.ui.tableWidget_01.hideColumn(18)
        self.ui.tableWidget_01.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.ui.tableWidget_01.setStyleSheet(u"QTableWidget::item:selected {background-color : rgba(255,255,255,50);}"
                                             u"QHeaderView::section{color: rgb(255,255,255);}")
        self.ui.splitter.setStyleSheet(u"QSplitter::handle:hover{background : rgba(255,255,255,50);}")

        # colors

        self.red_light = QColor(205, 90, 80)
        self.red_dark = QColor(195, 75, 60)  # C34B3C
        self.yell_light = QColor(230, 165, 45)
        self.yell_dark = QColor(230, 145, 25)
        self.green_light = QColor(88, 145, 39)
        self.green_dark = QColor(79, 130, 35)

        # self.ui.tableWidget_01.setMaximumWidth(2500)
        # self.ui.tableWidget_01.setMaximumHeight(1500)

        # self.layout = QVBoxLayout(self)
        # self.sublayout = QHBoxLayout(self)

        self.ui.switchToolButton.clicked.connect(self.switch_tools)
        self.ui.switchToolButton.setToolTip('Подробнее')
        self.colorizeEffect_wt(self.ui.switchToolButton)

        self.ui.tableWidget_01.horizontalHeader().sectionClicked.connect(self.error_highlight)
        self.ui.tableWidget_01.clicked.connect(self.click_table)
        # self.ui.tableWidget_01.doubleClicked.connect(self.double_click_table)
        self.ui.tableWidget_01.doubleClicked.connect(self.double_click_video_player)

        self.ui.addButton.clicked.connect(self.prepare_ffprobe)

        self.ui.addButton.setToolTip('Добавить файлы')
        self.colorizeEffect_wt(self.ui.addButton)
        self.ui.delButton.clicked.connect(self.del_row)
        self.ui.delButton.setToolTip('Удалить выбранное')
        self.ui.playButton.clicked.connect(self.play_selected)
        self.ui.playButton.setToolTip('Воспроизвести выбранное')
        self.ui.openButton.clicked.connect(self.open_folder)
        self.ui.openButton.setToolTip('Открыть папку с файлом')
        self.ui.exportButton.clicked.connect(self.export_db_xlsx)
        self.ui.exportButton.setToolTip('Экспорт базы данных в Excel')

        self.ui.r128DtctButton.clicked.connect(self.prepare_loudnorm_single)
        self.ui.r128DtctButton.setToolTip('Сканировать выбранное R128')
        self.ui.queueButton.clicked.connect(self.prepare_loudnorm_multi)
        self.ui.queueButton.setToolTip('Сканировать весь список R128')
        self.ui.blckDtctButton.clicked.connect(self.prepare_black_detect_single)
        self.ui.blckDtctButton.setToolTip('Сканировать выбранное Black')
        self.ui.slncDtctButton.clicked.connect(self.prepare_silence_detect_single)
        self.ui.slncDtctButton.setToolTip('Сканировать выбранное Silence')
        self.ui.frzDtctButton.clicked.connect(self.prepare_freeze_detect_single)
        self.ui.frzDtctButton.setToolTip('Сканировать выбранное Freeze')
        self.ui.fullDtctButton.clicked.connect(self.prepare_full_detect_single)
        self.ui.fullDtctButton.setToolTip('Полное сканирование')
        self.ui.settingsButton.clicked.connect(self.open_settings_window)
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
        self.ui.exportButton.setEnabled(False)
        self.colorizeEffect_gr(self.ui.exportButton)

        # self.last_pressed = None
        # self.timer = QTimer()
        # self.timer.setSingleShot(True)
        # self.timer.timeout.connect(self.clear_pressed)

        self.grey_light = QColor(65, 65, 70)
        self.grey_dark = QColor(40, 40, 45)

        # SettingsWin
        self.settings = QtWidgets.QDialog()
        self.ui_set = Ui_Settings()
        self.ui_set.setupUi(self.settings)
        self.ui_set.saveButton_main.clicked.connect(self.save_butt_settings)
        self.ui_set.cancelButton_main.clicked.connect(self.cancel_butt_settings)
        self.ui_set.saveButton_damage.clicked.connect(self.save_butt_settings)
        self.ui_set.cancelButton_damage.clicked.connect(self.cancel_butt_settings)
        self.base_settings_main()
        self.base_settings_damage()

        # DB Edit Dialog
        self.db_sett = QDialog()
        self.db_settings = Ui_DB_Settings()
        self.db_settings.setupUi(self.db_sett)

        # DB_Editor
        # self.ui_db_editor = QtWidgets.QDialog()
        # self.db_editor = Ui_DB_editor()
        # self.db_editor.setupUi(self.ui_db_editor)
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('videoinfo.db')
        # db.query("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE")
        # tbl_name = self.choose_db_tables()
        # tbl_name = self.db_settings.db_list.currentText()
        tbl_name = 'Video'
        self.model = QSqlTableModel(self)
        self.model.setTable(f'{tbl_name}')
        self.model.select()
        self.ui.tableView_db.setModel(self.model)
        self.ui.tableView_db.hide()
        self.ui.tableView_db.hideRow(0)
        self.ui.tableView_db.hideColumn(1)

        # self.ui.tableView_db.openDB.clicked.connect(self.open_db)
        # self.ui.tableView_db.closeDB.clicked.connect(self.close_db)

        # InfoWin
        # self.alert = QtWidgets.QDialog()
        # self.alert.info_win = Ui_AlertDialog()
        # self.alert.info_win.setupUi(self.alert)
        # self.alert.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.alert.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # self.alert.setWindowFlags(Qt.FramelessWindowHint)

        # WaveView
        self.ui.wave_view.hide()
        self.ui.r128_loudness.hide()
        self.ui.resizeButtonDown.hide()
        # self.wave_flag = False
        self.ui.resizeButtonUp.clicked.connect(self.wave_view)
        self.ui.resizeButtonDown.clicked.connect(self.wave_hide)

        # VideoINFO_Player
        self.vinfo_player = QtWidgets.QDialog()
        self.dialog = Ui_VideoINFO_Player()
        self.dialog.setupUi(self.vinfo_player)

        # self.color_effect = QPalette()
        # self.color_effect.setColor('white')

        self.dialog.player_openButton.clicked.connect(self.open_folder_video_player)
        self.dialog.player_prev_fr_Button.clicked.connect(self.prev_frame)
        self.dialog.player_prev_mark_Button.clicked.connect(self.prev_mark)
        self.dialog.player_playButton.clicked.connect(self.play_pause)
        # self.dialog.player_pauseButton.clicked.connect(self.pause_video)
        self.dialog.player_next_mark_Button.clicked.connect(self.next_mark)
        self.dialog.player_next_fr_Button.clicked.connect(self.next_frame)
        self.dialog.player_fullButton.clicked.connect(self.full_screen)
        self.dialog.player_fullButton.setEnabled(False)
        self.dialog.player_muteButton.clicked.connect(self.vol_mute)
        self.colorizeEffect_wt(self.dialog.player_openButton)
        self.colorizeEffect_wt(self.dialog.player_prev_fr_Button)
        self.colorizeEffect_wt(self.dialog.player_prev_mark_Button)
        self.colorizeEffect_wt(self.dialog.player_playButton)
        self.colorizeEffect_wt(self.dialog.player_next_mark_Button)
        self.colorizeEffect_wt(self.dialog.player_next_fr_Button)
        self.colorizeEffect_wt(self.dialog.player_muteButton)
        self.colorizeEffect_gr(self.dialog.player_fullButton)

        self.dialog.player_add_mark.clicked.connect(self.add_marks)
        self.dialog.player_dell_mark.clicked.connect(self.del_mark)
        self.dialog.player_save_marks.clicked.connect(self.add_marks_db)

        self.dialog.blck_table.clicked.connect(self.click_table_blck_detect)
        self.dialog.slnc_table.clicked.connect(self.click_table_slnc_detect)
        self.dialog.frz_table.clicked.connect(self.click_table_frz_detect)

        self.player = QMediaPlayer()
        self.videoOutput = QVideoWidget(self.dialog.video_player_img)
        self.videoOutput.resize(960, 540)
        self.player.setVideoOutput(self.videoOutput)
        self.audioOutput = QAudioOutput()
        self.positionSlider = QSlider(Qt.Orientation.Horizontal, self.dialog.videoSlider)
        self.positionSlider.resize(960, 25)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(5)

        self.player.positionChanged.connect(self.positionChanged)
        self.player.durationChanged.connect(self.durationChanged)

        self.volumeslider = QSlider(Qt.Orientation.Horizontal, self.dialog.volumeSlider)
        self.volumeslider.setSingleStep(1)
        self.volumeslider.setRange(0, 100)
        self.volumeslider.resize(157, 25)
        self.audioOutput.setVolume(0.5)
        self.volumeslider.setValue(50)
        self.player.setAudioOutput(self.audioOutput)
        self.volumeslider.valueChanged.connect(self.volumeChanged)

        # MenuBar
        self.ui.actionAdd_files.triggered.connect(self.prepare_ffprobe)
        self.ui.actionDelete_selected_file.triggered.connect(self.del_row)
        self.ui.actionPlay_selected_file.triggered.connect(self.play_selected)

        self.ui.actionOpen_destination_folder.triggered.connect(self.open_folder)

        self.ui.actionExport_table_to_Excel.triggered.connect(self.export_db_xlsx)
        self.ui.actionSettings.triggered.connect(self.open_settings_window)
        # self.ui.actionOpen_VideoPlayer.triggered.connect(self.switch_db_editor)
        self.ui.actionOpen_VideoPlayer.setEnabled(False)
        self.ui.actionClear_table.triggered.connect(self.clear_table_01)
        self.ui.actionShow_all_tables.triggered.connect(self.show_db_tables)

        self.ui.actionRun_Loudness_single_scan.triggered.connect(self.prepare_loudnorm_single)
        self.ui.actionRun_Loudness_multiple_scan.triggered.connect(self.prepare_loudnorm_multi)
        self.ui.actionRun_BlackDetect_single_scan.triggered.connect(self.prepare_black_detect_single)
        self.ui.actionRun_BlackDetect_multiple_scan.triggered.connect(self.prepare_black_detect_multi)
        self.ui.actionRun_FreezeDetect_single_scan.triggered.connect(self.prepare_freeze_detect_single)
        self.ui.actionRun_FreezeDetect_multiple_scan.triggered.connect(self.prepare_freeze_detect_multi)
        self.ui.actionRun_Full_single_scan.triggered.connect(self.prepare_full_detect_single)
        self.ui.actionRun_Full_multiple_scan.triggered.connect(self.prepare_full_detect_multi)
        self.ui.actionRun_Background_Loudness_scan.triggered.connect(self.prepare_background_loudnorm_scan)
        self.ui.actionRun_Background_BlackDetect_scan.triggered.connect(self.prepare_background_blackdetect_scan)
        self.ui.actionRun_Background_SilenceDetect_scan.triggered.connect(self.prepare_background_silencedetect_scan)
        self.ui.actionRun_Background_FreezeDetect_scan.triggered.connect(self.prepare_background_freezedetect_scan)
        self.ui.actionRun_Background_Full_scan.triggered.connect(self.prepare_background_fulldetect_scan)

        self.ui.actionOpen_db_editor.triggered.connect(self.switch_db_editor)

        self.ui.actionCreate_db.triggered.connect(self.create_new_db)
        self.ui.actionShow_Loudness.triggered.connect(self.show_loudness)
        self.ui.actionShow_Details.triggered.connect(self.show_details)

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
            # self.ui.frame_wave.setStyleSheet("{border: 0px solid rgb(63, 64, 66);}")

        else:
            self.ui.frame_wave.show()
            self.ui.actionShow_Loudness.setText('Hide Loudness meter')

    # def closeEvent(self, event):  # When the form is closed
    #     # The playback cannot be stopped automatically when the window is closed, it needs to be stopped manually
    #     if (self.player.state() == QMediaPlayer.PlayingState):
    #         self.player.stop()

    # self.volumeslider.setToolTip("Volume")
    # self.hbuttonbox.addWidget(self.volumeslider)
    # self.volumeslider.valueChanged.connect(self.set_volume)

    # self.info_win.setObjectName("info_win")
    # self.info_win.setGeometry(QRect(500, 500, 300, 100))
    # self.info_win.setWindowTitle('Внимание!')

    # self.info_label = QLabel(self.info_win)
    # self.info_label.setObjectName("info_label")
    # self.info_label.setText('Запущено сканирование')

    # self.info_label.setGeometry(QRect(50, 10, 121, 21))

    # def clear_pressed(self):
    #     self.last_pressed = None
    #
    # def keyPressEvent(self, event):
    #     self.pressedKeys[event.key()] = True
    #     if self.timer.isActive():
    #         if self.last_pressed == event.key():
    #             self.timer.stop()
    #     else:
    #         self.timer.start(200)
    #     self.last_pressed = event.key()
    #     self.keyAction()
    #
    # def keyReleaseEvent(self, event):
    #     self.pressedKeys[event.key()] = False
    #     self.keyAction()
    #
    # def keyAction(self):
    #     if self.pressedKeys[Qt.Key_Left]:
    #         print('left')
    #     if self.pressedKeys[Qt.Key_Right]:
    #         print('right')
    #     if self.pressedKeys[Qt.Key_Up]:
    #         print('up')
    #     if self.pressedKeys[Qt.Key_Down]:
    #         print('down')
    # def menu_bar(self):
    #     self.menuFile

    def table_key_press_event(self, event):
        QtWidgets.QTableWidget.keyPressEvent(self.ui.tableWidget_01, event)
        # if event.key() == Qt.Key_Left:
        #     print('left')
        # elif event.key() == Qt.Key_Right:
        #     print('right')
        if event.key() == Qt.Key_Up:
            try:
                self.click_table()
            except Exception:
                pass
            # print('up')
        elif event.key() == Qt.Key_Down:
            try:
                self.click_table()
            except Exception:
                pass
        elif event.key() == Qt.Key_Escape:
            try:
                self.ui.tableWidget_01.clearSelection()
            except Exception:
                pass

    # def vido_player_press_event(self, event):
    #     QtWidgets.QDialog.keyPressEvent(self.vinfo_player, event)
    #     # if event.key() == Qt.Key_Left:
    #     #     print('left')
    #     # elif event.key() == Qt.Key_Right:
    #     #     print('right')
    #     if event.key() == Qt.Key_Up:
    #         try:
    #             print('test')
    #         except Exception:
    #             print('test_error')
    #             pass

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Escape:
    #         self.videoOutput.setFullScreen(False)
    #         print('Esc')
    #     event.accept()
    def open_settings_window(self):
        self.save_temp_settings_main()
        self.save_temp_settings_damage()
        self.settings.show()

    def switch_db_editor(self):
        # self.update_db_editor()
        if self.ui.tableWidget_01.isVisible():
            self.model.select()
            self.ui.tableWidget_01.hide()
            self.ui.tableView_db.show()

            self.ui.r128DtctButton.hide()
            self.ui.blckDtctButton.hide()
            self.ui.slncDtctButton.hide()
            self.ui.frzDtctButton.hide()
            self.ui.fullDtctButton.hide()

        else:
            self.ui.tableWidget_01.show()
            self.ui.tableView_db.hide()

            self.ui.r128DtctButton.show()
            self.ui.blckDtctButton.show()
            self.ui.slncDtctButton.show()
            self.ui.frzDtctButton.show()
            self.ui.fullDtctButton.show()

    def update_db_editor(self):
        tbl_name = self.db_settings.db_list.currentText()
        # tbl_name = 'Video'
        self.model.setTable(f'{tbl_name}')
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
        Data().export_xlsx()

    # def close_settings_window(self):
    #     self.settings.close()
    def show_db_tables(self):
        self.db_settings.db_list.clear()
        # self.db_tables = QtWidgets.QDialog()
        tbl_list = Data().show_all_tbl()
        # self.db_tables.resize(400, 200)

        # self.save_button = QPushButton(self.db_tables)
        # self.save_button.setText('Choose')
        # self.frame_tables = QFrame(self.save_button)
        # self.horizontalLayout = QHBoxLayout(self.save_button)
        # self.cancel_button = QPushButton(self.db_tables)
        # self.save_button.setText('Cancel')

        self.db_settings.db_list.setEditable(True)
        self.db_settings.db_list.addItems(tbl_list)
        self.db_settings.connectButton.clicked.connect(self.save_db_settings)
        self.db_settings.cancelButton.clicked.connect(self.cancel_db_settings)

        self.db_sett.show()
        # self.db_tables.show()

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
            Data().create_database(db_name)

    def save_butt_settings(self):
        self.save_temp_settings_main()
        self.save_temp_settings_damage()
        self.error_highlight()
        self.settings.close()

    def cancel_butt_settings(self):
        self.call_temp_settings_main()
        self.call_temp_settings_damage()
        self.error_highlight()
        self.settings.close()

    def base_settings_main(self):
        self.ui_set.codec_txt.setText('h264')
        self.ui_set.width_txt.setText('1920')
        self.ui_set.height_txt.setText('1080')
        self.ui_set.v_bit_rate_txt.setText('6')
        self.ui_set.frame_rate_comboBox.addItems(['23.976', '24', '25', '29.97', '30'])
        self.ui_set.frame_rate_comboBox.setCurrentText('25')
        self.ui_set.dar_comboBox.addItems(['4:3', '16:9'])
        self.ui_set.dar_comboBox.setCurrentText('16:9')
        self.ui_set.codec_aud_txt.setText('aac')
        self.ui_set.channels_txt.setText('2')
        self.ui_set.sample_rate_comboBox.addItems(['44.1', '48.0', '96.0'])
        self.ui_set.sample_rate_comboBox.setCurrentText('48.0')
        self.ui_set.a_bit_rate_txt.setText('320')

        self.ui_set.r128_i_txt.setText('-23')
        self.ui_set.r128_lra_txt.setText('11')
        self.ui_set.r128_tp_txt.setText('-2')
        self.ui_set.r128_thr_txt.setText('0')

    def base_settings_damage(self):
        self.ui_set.blck_dur_txt.setText('2')
        self.ui_set.blck_thr_txt.setText('0.1')
        self.ui_set.blck_tc_in.setText('00:00:00')
        self.ui_set.blck_tc_out.setText('00:00:00')

        self.ui_set.slnc_dur_txt.setText('2')
        self.ui_set.slnc_noize_txt.setText('-40')
        self.ui_set.slnc_tc_in.setText('00:00:00')
        self.ui_set.slnc_tc_out.setText('00:00:00')

        self.ui_set.frz_dur_txt.setText('2')
        self.ui_set.frz_noize_txt.setText('-40')
        self.ui_set.frz_tc_in.setText('00:00:00')
        self.ui_set.frz_tc_out.setText('00:00:00')

    def save_settings_main(self):
        self.ui_set.codec_txt.text()
        self.ui_set.width_txt.text()
        self.ui_set.height_txt.text()
        self.ui_set.v_bit_rate_txt.text()
        self.ui_set.frame_rate_comboBox.currentText()
        self.ui_set.dar_comboBox.currentText()
        self.ui_set.codec_aud_txt.text()
        self.ui_set.channels_txt.text()
        self.ui_set.sample_rate_comboBox.currentText()
        self.ui_set.a_bit_rate_txt.text()

        self.ui_set.r128_i_txt.text()
        self.ui_set.r128_lra_txt.text()
        self.ui_set.r128_tp_txt.text()
        self.ui_set.r128_thr_txt.text()

        self.settings.close()

    def save_settings_damage(self):
        self.ui_set.blck_dur_txt.text()
        self.ui_set.blck_thr_txt.text()
        self.ui_set.blck_tc_in.text()
        self.ui_set.blck_tc_out.text()

        self.ui_set.slnc_dur_txt.text()
        self.ui_set.slnc_noize_txt.text()
        self.ui_set.slnc_tc_in.text()
        self.ui_set.slnc_tc_out.text()

        self.ui_set.frz_dur_txt.text()
        self.ui_set.frz_noize_txt.text()
        self.ui_set.frz_tc_in.text()
        self.ui_set.frz_tc_out.text()
        self.settings.close()

    def save_temp_settings_main(self):
        self.temp_codec = self.ui_set.codec_txt.text()
        self.temp_width = self.ui_set.width_txt.text()
        self.temp_height = self.ui_set.height_txt.text()
        self.temp_v_bit_rate = self.ui_set.v_bit_rate_txt.text()
        self.temp_frame_rate = self.ui_set.frame_rate_comboBox.currentText()
        self.temp_dar = self.ui_set.dar_comboBox.currentText()
        self.temp_codec_aud = self.ui_set.codec_aud_txt.text()
        self.temp_channels = self.ui_set.channels_txt.text()
        self.temp_sample_rate = self.ui_set.sample_rate_comboBox.currentText()
        self.temp_a_bit_rate = self.ui_set.a_bit_rate_txt.text()

        self.temp_r128_i = self.ui_set.r128_i_txt.text()
        self.temp_r128_lra = self.ui_set.r128_lra_txt.text()
        self.temp_r128_tp = self.ui_set.r128_tp_txt.text()
        self.temp_r128_thr = self.ui_set.r128_thr_txt.text()

    def save_temp_settings_damage(self):
        self.blck_dur_temp = self.ui_set.blck_dur_txt.text()
        self.blck_thr_temp = self.ui_set.blck_thr_txt.text()
        self.blck_tc_in_temp = self.ui_set.blck_tc_in.text()
        self.blck_tc_out_temp = self.ui_set.blck_tc_out.text()

        self.slnc_dur_temp = self.ui_set.slnc_dur_txt.text()
        self.slnc_noize_temp = self.ui_set.slnc_noize_txt.text()
        self.slnc_tc_in_temp = self.ui_set.slnc_tc_in.text()
        self.slnc_tc_out_temp = self.ui_set.slnc_tc_out.text()

        self.frz_dur_temp = self.ui_set.frz_dur_txt.text()
        self.frz_noize_temp = self.ui_set.frz_noize_txt.text()
        self.frz_tc_in_temp = self.ui_set.frz_tc_in.text()
        self.frz_tc_out_temp = self.ui_set.frz_tc_out.text()

    def call_temp_settings_main(self):
        self.ui_set.codec_txt.setText(self.temp_codec)
        self.ui_set.width_txt.setText(self.temp_width)
        self.ui_set.height_txt.setText(self.temp_height)
        self.ui_set.v_bit_rate_txt.setText(str(self.temp_v_bit_rate))
        # self.ui_set.frame_rate_comboBox.addItems(list(str(self.temp_frame_rate)))
        self.ui_set.frame_rate_comboBox.setCurrentText(str(self.temp_frame_rate))
        # self.ui_set.dar_comboBox.addItems(list(str(self.temp_dar)))
        self.ui_set.dar_comboBox.setCurrentText(str(self.temp_dar))
        self.ui_set.codec_aud_txt.setText(self.temp_codec_aud)
        self.ui_set.channels_txt.setText(self.temp_channels)
        # self.ui_set.sample_rate_comboBox.addItems(list(str(self.temp_sample_rate)))
        # print(self.temp_sample_rate)
        self.ui_set.sample_rate_comboBox.setCurrentText(str(self.temp_sample_rate))
        self.ui_set.a_bit_rate_txt.setText(str(self.temp_a_bit_rate))

        self.ui_set.r128_i_txt.setText(str(self.temp_r128_i))
        self.ui_set.r128_lra_txt.setText(str(self.temp_r128_lra))
        self.ui_set.r128_tp_txt.setText(str(self.temp_r128_tp))
        self.ui_set.r128_thr_txt.setText(str(self.temp_r128_thr))

    def call_temp_settings_damage(self):
        self.ui_set.blck_dur_txt.setText(self.blck_dur_temp)
        self.ui_set.blck_thr_txt.setText(self.blck_thr_temp)
        self.ui_set.blck_tc_in.setText(self.blck_tc_in_temp)
        self.ui_set.blck_tc_out.setText(self.blck_tc_out_temp)

        self.ui_set.slnc_dur_txt.setText(self.slnc_dur_temp)
        self.ui_set.slnc_noize_txt.setText(self.slnc_noize_temp)
        self.ui_set.slnc_tc_in.setText(self.slnc_tc_in_temp)
        self.ui_set.slnc_tc_out.setText(self.slnc_tc_out_temp)

        self.ui_set.frz_dur_txt.setText(self.frz_dur_temp)
        self.ui_set.frz_noize_txt.setText(self.frz_noize_temp)
        self.ui_set.frz_tc_in.setText(self.frz_tc_in_temp)
        self.ui_set.frz_tc_out.setText(self.frz_tc_out_temp)

    def header_rename(self, header):
        header = header.replace('file_name', 'Name')
        header = header.replace('F_bit_rate', 'Bit rate')
        header = header.replace('V01_codec_name', 'Codec')
        header = header.replace('V01_width', 'Width')
        header = header.replace('V01_height', 'Height')
        header = header.replace('V01_sample_aspect_ratio', 'SAR')
        header = header.replace('V01_display_aspect_ratio', 'DAR')
        header = header.replace('V01_r_frame_rate', 'Frame rate')
        header = header.replace('F_duration', 'Duration')

        header = header.replace('audio_streams', 'Audio map')
        header = header.replace('A01_codec_name', 'Audio codec')
        header = header.replace('A01_sample_rate', 'Sample rate')
        header = header.replace('A01_channels', 'Channels')
        header = header.replace('A01_bit_rate', 'Audio bit rate')
        header = header.replace('input_i', 'Integrated')
        header = header.replace('input_tp', 'True Peak')
        header = header.replace('input_lra', 'LRA')
        header = header.replace('input_thresh', 'Threshold')

        header = header.replace('black_start', 'Black Screen')
        header = header.replace('silence_start', 'Silence')
        header = header.replace('freeze_start', 'Freeze')

        return header

    def tbl2_header_rename(self, header):
        header = header.replace('V01_codec_name', 'Codec')
        header = header.replace('V01_profile', 'Profile')
        header = header.replace('V01_codec_type', 'Codec type')
        header = header.replace('V01_width', 'Width')
        header = header.replace('V01_height', 'Height')
        header = header.replace('V01_sample_aspect_ratio', 'SAR')
        header = header.replace('V01_display_aspect_ratio', 'DAR')
        header = header.replace('V01_pix_fmt', 'Pixel format')
        header = header.replace('V01_level', 'Level')
        header = header.replace('V01_color_range', 'Color range')
        header = header.replace('V01_color_space', 'Color space')
        header = header.replace('V01_field_order', 'Field order')
        header = header.replace('V01_r_frame_rate', 'Frame rate')
        header = header.replace('V01_language', 'Language')
        header = header.replace('V01_title', 'Handler name')
        header = header.replace('V01_handler_name', 'Handler name')
        header = header.replace('V01_encoder', 'Encoder')
        header = header.replace('F_filename', 'File name')
        header = header.replace('F_format_name', 'Format name')
        header = header.replace('F_duration', 'Duration')
        header = header.replace('F_size', 'Size')
        header = header.replace('F_bit_rate', 'Bit rate')
        header = header.replace('F_title', 'Title')
        header = header.replace('F_encoder', 'Encoder')

        # header = header.replace('codec_name', 'Audio codec')
        # header = header.replace('sample_rate', 'Sample rate')
        # header = header.replace('channels', 'Channels')
        # header = header.replace('bit_rate', 'Audio bit rate')
        # header = header.replace('input_i', 'Integrated')
        # header = header.replace('input_tp', 'True Peak')
        # header = header.replace('input_lra', 'LRA')
        # header = header.replace('input_thresh', 'Threshold')
        header = header.replace('_', ' ')
        return header

    def get_file_list(self):
        directory = r'\\slave\storage\ContentX\FILMS'
        # print(self.ui.tableView_db.selectedIndexes())
        file_list = QFileDialog.getOpenFileNames(
            parent=self,
            caption='Select files',
            dir=directory,
            filter='Video files (*.mp4 *.mkv *.mov *.m4v *.avi *.mpeg *.mts *.m2ts *.mxf *.ts *.webm *.wmv);;'
                   'Audio files (*.aac *.ac3 *.mp2 *.mp3 *.aif *.dts *.flac *.m4a *.ogg *.opus *.wav *.wma);;'
                   'All files (*.*)'
        )
        return tuple(file_list[0])

    def prepare_background_loudnorm_scan(self):
        file_list = self.get_file_list()
        if file_list != ():
            progress_dialog_ffpr = QProgressDialog("FFprobe Scan", "Cancel", 0, 100, self)
            progress_dialog_ffpr.setWindowTitle("Processing...")
            progress_dialog_ffpr.setWindowModality(Qt.WindowModal)
            progress_dialog_ffpr.setMinimumDuration(0)
            progress_dialog_ffpr.setMinimumSize(400, 150)
            progress_dialog_ffpr.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                               "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                               "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                               "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

            start_scan = self.start_ffprobe(file_list, progress_dialog_ffpr)
            if start_scan:
                progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
                progress_dialog_r128.setWindowTitle("Processing...")
                progress_dialog_r128.setWindowModality(Qt.WindowModal)
                progress_dialog_r128.setMinimumDuration(0)
                progress_dialog_r128.setMinimumSize(400, 150)
                progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                                   "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                                   "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                                   "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

                self.backgound_scan_loudnorm(file_list, progress_dialog_r128)
                # process = multiprocessing.Process(target=self.scan_loudnorm(tuple(tbl_file_list), progress_dialog_r128))
                # process.start()
                progress_dialog_r128.setValue(100)
            # progress_dialog_r128.repaint()

    def prepare_background_blackdetect_scan(self):
        file_list = self.get_file_list()
        if file_list != ():
            progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
            progress_dialog_blck.setWindowTitle("Processing...")
            progress_dialog_blck.setWindowModality(Qt.WindowModal)
            progress_dialog_blck.setMinimumDuration(0)
            progress_dialog_blck.setMinimumSize(400, 150)
            progress_dialog_blck.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                               "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                               "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                               "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

            self.backgound_scan_blackdetect(file_list, progress_dialog_blck)
            progress_dialog_blck.setValue(100)
            progress_dialog_blck.repaint()

    def prepare_background_silencedetect_scan(self):
        file_list = self.get_file_list()
        if file_list != ():
            progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
            progress_dialog_slnc.setWindowTitle("Processing...")
            progress_dialog_slnc.setWindowModality(Qt.WindowModal)
            progress_dialog_slnc.setMinimumDuration(0)
            progress_dialog_slnc.setMinimumSize(400, 150)
            progress_dialog_slnc.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                               "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                               "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                               "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

            self.backgound_scan_silencedetect(file_list, progress_dialog_slnc)
            progress_dialog_slnc.setValue(100)
            progress_dialog_slnc.repaint()

    def prepare_background_freezedetect_scan(self):
        file_list = self.get_file_list()
        if file_list != ():
            progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
            progress_dialog_frz.setWindowTitle("Processing...")
            progress_dialog_frz.setWindowModality(Qt.WindowModal)
            progress_dialog_frz.setMinimumDuration(0)
            progress_dialog_frz.setMinimumSize(400, 150)
            progress_dialog_frz.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                              "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                              "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                              "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

            self.backgound_scan_freezedetect(file_list, progress_dialog_frz)
            progress_dialog_frz.setValue(100)
            progress_dialog_frz.repaint()
            # print(tuple(file_list[0]))

    def prepare_background_fulldetect_scan(self):
        file_list = self.get_file_list()
        if file_list != ():
            progress_dialog_ffpr = QProgressDialog("FFprobe Scan", "Cancel", 0, 100, self)
            progress_dialog_ffpr.setWindowTitle("Processing...")
            progress_dialog_ffpr.setWindowModality(Qt.WindowModal)
            progress_dialog_ffpr.setMinimumDuration(0)
            progress_dialog_ffpr.setMinimumSize(400, 150)
            progress_dialog_ffpr.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                               "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                               "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                               "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

            self.ui.tableWidget_01.setRowCount(0)
            if self.start_ffprobe_bg(file_list, progress_dialog_ffpr):
                progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
                progress_dialog_r128.setWindowTitle("Processing...")
                progress_dialog_r128.setWindowModality(Qt.WindowModal)
                progress_dialog_r128.setMinimumDuration(0)
                progress_dialog_r128.setMinimumSize(400, 150)
                progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                                   "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                                   "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                                   "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

                if self.backgound_scan_loudnorm(file_list, progress_dialog_r128):
                    # process = multiprocessing.Process(target=self.scan_loudnorm(tuple(tbl_file_list), progress_dialog_r128))
                    # process.start()
                    progress_dialog_r128.setValue(100)

                    self.ui.tableWidget_01.setColumnCount(4)
                    headers = ['File path', 'Name', 'Loudnorm', 'BlackDetect', 'SilenceDetect', 'FreezeDetect']
                    self.ui.tableWidget_01.setHorizontalHeaderLabels(headers)
                    progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
                    progress_dialog_blck.setWindowTitle("Processing...")
                    progress_dialog_blck.setWindowModality(Qt.WindowModal)
                    progress_dialog_blck.setMinimumDuration(0)
                    progress_dialog_blck.setMinimumSize(400, 150)
                    progress_dialog_blck.setStyleSheet(
                        "QPushButton {color: white; background-color:rgba(255,255,255,30);"
                        "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                        "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                        "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

                    if self.backgound_fullscan_blackdetect(file_list, progress_dialog_blck):
                        progress_dialog_blck.setValue(100)
                        progress_dialog_blck.repaint()

                        progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
                        progress_dialog_slnc.setWindowTitle("Processing...")
                        progress_dialog_slnc.setWindowModality(Qt.WindowModal)
                        progress_dialog_slnc.setMinimumDuration(0)
                        progress_dialog_slnc.setMinimumSize(400, 150)
                        progress_dialog_slnc.setStyleSheet(
                            "QPushButton {color: white; background-color:rgba(255,255,255,30);"
                            "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                            "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                            "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

                        self.ui.tableWidget_01.setColumnCount(5)
                        headers = ['File path', 'Name', 'Loudnorm', 'BlackDetect', 'SilenceDetect', 'FreezeDetect']
                        self.ui.tableWidget_01.setHorizontalHeaderLabels(headers)
                        if self.backgound_fullscan_silencedetect(file_list, progress_dialog_slnc):
                            progress_dialog_slnc.setValue(100)
                            progress_dialog_slnc.repaint()

                            progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
                            progress_dialog_frz.setWindowTitle("Processing...")
                            progress_dialog_frz.setWindowModality(Qt.WindowModal)
                            progress_dialog_frz.setMinimumDuration(0)
                            progress_dialog_frz.setMinimumSize(400, 150)
                            progress_dialog_frz.setStyleSheet(
                                "QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

                            self.ui.tableWidget_01.setColumnCount(6)
                            headers = ['File path', 'Name', 'Loudnorm', 'BlackDetect', 'SilenceDetect', 'FreezeDetect']
                            self.ui.tableWidget_01.setHorizontalHeaderLabels(headers)
                            if self.backgound_fullscan_freezedetect(file_list, progress_dialog_frz):
                                progress_dialog_frz.setValue(100)
                                progress_dialog_frz.repaint()

        # process = multiprocessing.Process(target=self.start_ffprobe(tuple(file_list[0])))
        # process.start()
        # task_thread = threading.Thread(target=self.start_ffprobe(tuple(file_list[0])))
        # task_thread.start()
        # lock = threading.Lock()

    # def add_file_list(self):
    #     add_file = QFileDialog.getOpenFileNames(
    #         parent=self,
    #         caption='Select files',
    #         dir=r'C:/Users/Алексей/Videos',
    #         filter='Video files (*.mp4 *.mkv);; All files (*.*)'
    #     )
    # print(file_list[0])
    # new_file_list = self.get_file_list() + add_file
    # print(self.file_list)
    # print(self.add_file[0])
    # self.start_ffprobe(new_file_list)
    def prepare_ffprobe(self):
        file_list = self.get_file_list()
        if file_list != ():
            self.progress_dialog_ffpr_start(file_list)

    def progress_dialog_ffpr_start(self, file_list):
        progress_dialog_ffpr = QProgressDialog("FFprobe Scan", "Cancel", 0, 100, self)
        progress_dialog_ffpr.setWindowTitle("Processing...")
        progress_dialog_ffpr.setWindowModality(Qt.WindowModal)
        progress_dialog_ffpr.setMinimumDuration(0)
        progress_dialog_ffpr.setMinimumSize(400, 150)
        progress_dialog_ffpr.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        if self.start_ffprobe(file_list, progress_dialog_ffpr):
            self.progress_dialog_tbl_start(file_list)

    def progress_dialog_tbl_start(self, file_list):
        progress_dialog_tbl = QProgressDialog("Creating Table", "Cancel", 0, 100, self)
        progress_dialog_tbl.setWindowTitle("Processing...")
        progress_dialog_tbl.setWindowModality(Qt.WindowModal)
        progress_dialog_tbl.setMinimumDuration(0)
        progress_dialog_tbl.setMinimumSize(400, 150)
        progress_dialog_tbl.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                          "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                          "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                          "QPushButton:pressed{background-color:rgba(255,255,255,70);}")
        self.prepare_table_01(file_list, progress_dialog_tbl)
        progress_dialog_tbl.setValue(100)

    def start_ffprobe(self, file_list, progress_dialog_ffpr):
        complited = False
        # db_file_list = Data().read_bd_multi('file_path')
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            # self.prepare_table_bg(file_path)
            progress_dialog_ffpr.setLabelText(f'{i + 1}/{total_files}  FFprobe Scan\n{file_path}')
            if progress_dialog_ffpr.wasCanceled():
                complited = False
                self.progress_dialog_tbl_start(file_list[:i])
                break
            db_file_path = Data().read_bd('file_path', file_path)
            if file_path != db_file_path:
                print(now())
                print('Сбор данных для файла', file_path)
                try:
                    Info(file_path)
                    print(now())
                    print('Сбор данных завершён')
                except Exception:
                    print(now())
                    print('Ошибка сбора данных')
                    pass
            progress = int((i + 1) / total_files * 100)
            progress_dialog_ffpr.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def start_ffprobe_bg(self, file_list, progress_dialog_ffpr):
        complited = False
        # db_file_list = Data().read_bd_multi('file_path')
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            self.prepare_table_bg(file_path)
            progress_dialog_ffpr.setLabelText(f'{i + 1}/{total_files}  FFprobe Scan\n{file_path}')
            if progress_dialog_ffpr.wasCanceled():
                complited = False
                # self.progress_dialog_tbl_start(file_list[:i])
                break
            db_file_path = Data().read_bd('file_path', file_path)
            if file_path != db_file_path:
                print(now())
                print('Сбор данных для файла', file_path)
                try:
                    Info(file_path)
                    print(now())
                    print('Сбор данных завершён')
                except Exception:
                    print(now())
                    print('Ошибка сбора данных')
                    pass
            progress = int((i + 1) / total_files * 100)
            progress_dialog_ffpr.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def prepare_table_bg(self, file_path):
        headers = ['File path', 'Name']
        self.ui.tableWidget_01.setHorizontalHeaderLabels(headers)
        file_name = os.path.basename(file_path)
        row_position = self.ui.tableWidget_01.rowCount()
        self.ui.tableWidget_01.insertRow(row_position)
        self.ui.tableWidget_01.setItem(row_position, 0, QtWidgets.QTableWidgetItem(file_path))
        self.ui.tableWidget_01.setItem(row_position, 1, QtWidgets.QTableWidgetItem(file_name))
        self.ui.tableWidget_01.repaint()
        self.table_mode = False

    def create_table_bg(self, file_path, header, status):
        file_name = os.path.basename(file_path)
        row_position = self.ui.tableWidget_01.rowCount()
        head1 = QTableWidgetItem()
        head1.setData(Qt.EditRole, 'Name')
        self.ui.tableWidget_01.setHorizontalHeaderItem(1, head1)
        head2 = QTableWidgetItem()
        head2.setData(Qt.EditRole, header)
        self.ui.tableWidget_01.setHorizontalHeaderItem(2, head2)
        self.ui.tableWidget_01.insertRow(row_position)
        self.ui.tableWidget_01.setItem(row_position, 0, QtWidgets.QTableWidgetItem(file_path))
        self.ui.tableWidget_01.setItem(row_position, 1, QtWidgets.QTableWidgetItem(file_name))
        # self.ui.tableWidget_02.item(row_position, 0).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
        self.ui.tableWidget_01.setItem(row_position, 2, QtWidgets.QTableWidgetItem(str(status)))
        if status == 'Выполнено':
            self.ui.tableWidget_01.item(row_position, 2).setBackground(self.green_dark)
        if status == 'Ошибка':
            self.ui.tableWidget_01.item(row_position, 2).setBackground(self.red_dark)
        if status == 'Сканирование проводилось':
            self.ui.tableWidget_01.item(row_position, 2).setBackground(self.yell_dark)
        self.ui.tableWidget_01.repaint()
        self.table_mode = False

    def create_table_bg_full(self, file_path, row, header, status):
        if header == 'Loudnorm':
            col = 2
        elif header == 'BlackDetect':
            col = 3
        elif header == 'SilenceDetect':
            col = 4
        elif header == 'FreezeDetect':
            col = 5
        else:
            col = 2
        # file_name = os.path.basename(file_path)
        # row_position = self.ui.tableWidget_01.rowCount()
        # file_path = self.ui.tableWidget_01.item(row, 0).text()
        # self.ui.tableWidget_01.insertRow(row_position)

        # self.ui.tableWidget_01.setItem(row, 0, QtWidgets.QTableWidgetItem(file_path))
        # self.ui.tableWidget_01.setItem(row, 1, QtWidgets.QTableWidgetItem(file_name))
        self.ui.tableWidget_01.setItem(row, col, QtWidgets.QTableWidgetItem(str(status)))
        if status == 'Выполнено':
            self.ui.tableWidget_01.item(row, col).setBackground(self.green_dark)
        if status == 'Ошибка' or status == 'Отменено':
            self.ui.tableWidget_01.item(row, col).setBackground(self.red_dark)
        if status == 'Сканирование проводилось':
            self.ui.tableWidget_01.item(row, col).setBackground(self.yell_dark)
        self.ui.tableWidget_01.repaint()
        self.table_mode = False

    def prepare_table_01(self, file_list, progress_dialog_tbl):
        total_files = len(file_list)
        for i, file_path in enumerate(file_list):
            print(i, file_path)
            progress_dialog_tbl.setLabelText(f'{i + 1}/{total_files}  Creating Table\n{file_path}')
            if progress_dialog_tbl.wasCanceled():
                break
            row_count = self.ui.tableWidget_01.rowCount()
            print(row_count)
            if row_count == 0:
                print(now())
                print('Построение:', file_path)
                self.create_table_01(file_path)
            else:
                tbl_file_list = []
                for row in range(row_count):
                    tbl_file_path = self.ui.tableWidget_01.item(row, 0).text()
                    tbl_file_list.append(tbl_file_path)
                tbl_file_list = tuple(tbl_file_list)
                print(tbl_file_list)
                if file_path not in tbl_file_list:
                    print(now())
                    print('Построение:', file_path)
                    self.create_table_01(file_path)
                else:
                    print('Вы пытаетесь добавить дубликат')

            progress = int((i + 1) / total_files * 100)
            progress_dialog_tbl.setValue(progress)
            QApplication.processEvents()

    # Info(file_path)
    # print(now())
    # print('Сбор данных для файла', file_path, 'завершён')

    # def write_base(self, file_path):
    #     data = Info(file_path).res_ffprobe(file_path)
    #     all_headers = list(map(lambda key: key, data))
    #     Data().add_columns(all_headers)
    #     Data().add_headers(all_headers)
    #     Data().add_video(file_path)
    #     Data().add_param(file_path, all_headers, data)
    #     # self.ui.statusBar.setText('Построение таблицы')
    #     self.create_table_01(file_path)

    # def open_
    def create_table_01(self, file_path):
        self.ui.tableWidget_01.setColumnCount(22)
        if not self.table_mode:
            self.ui.tableWidget_01.setRowCount(0)
        self.ui.tableWidget_01.setSortingEnabled(False)
        print(now())
        print('Построение таблицы')
        # self.ui.tableWidget_01.setStyleSheet(
        #     "QTableWidget::section {background-color: rgb(100, 100, 100); color: rgb(200, 200, 200);}")
        # file_name = os.path.basename(file_path)

        # self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        headers = ('file_path', 'file_name', 'F_bit_rate', 'V01_codec_name', 'V01_width', 'V01_height',
                   'V01_sample_aspect_ratio', 'V01_display_aspect_ratio', 'V01_r_frame_rate', 'F_duration',
                   'audio_streams', 'A01_codec_name', 'A01_sample_rate', 'A01_channels', 'A01_bit_rate',
                   'input_i', 'input_tp', 'input_lra', 'input_thresh', 'black_start', 'silence_start', 'freeze_start')
        row_position = self.ui.tableWidget_01.rowCount()
        print('row_position', row_position)
        self.ui.tableWidget_01.setRowCount(row_position)
        self.ui.tableWidget_01.insertRow(row_position)

        # self.ui.tableWidget_01.setVerticalHeaderItem(row_position, QtWidgets.QTableWidgetItem(file_name))
        # self.ui.tableWidget_01.verticalHeader().frameGeometry()

        col = 0
        # all_headers = Data().read_all_data('file_path')
        # all_data = Data().read_all_data(file_path)
        # all_dict = dict(zip(all_headers, all_data))
        # print('all_dict', all_dict)
        for header in headers:
            db_data = Data().read_bd(header, file_path)
            # db_data = all_dict[header]
            # print('header', header)
            # print('db_data', db_data)
            if 'frame_rate' in header and db_data != 'нет данных':
                db_data = convert_fps(db_data)
            if 'size' in header and db_data != 'нет данных':
                db_data = convert_bytes(int(db_data), "b")
            if 'bit_rate' in header and db_data != 'нет данных':
                db_data = convert_bytes(int(db_data), "bit/s")
            if 'duration' in header and db_data != 'нет данных':
                fps = Data().read_bd('V01_r_frame_rate', file_path)
                fps = convert_fps(fps).split(' ')[0]
                db_data = str(convert_duration_sec(float(db_data), float(fps)))
            if 'sample_rate' in header and db_data != 'нет данных':
                db_data = convert_khz(db_data)
            if 'black_start' in header:
                if db_data != 'нет данных' and db_data != 'не найдено':
                    db_data = 'найден'

            if 'silence_start' in header:
                if db_data != 'нет данных' and db_data != 'не найдено':
                    db_data = 'найден'

            if 'freeze_start' in header:
                if db_data != 'нет данных' and db_data != 'не найдено':
                    db_data = 'найден'

            header = self.header_rename(header)
            head = QTableWidgetItem()
            head.setData(Qt.EditRole, header)
            self.ui.tableWidget_01.setHorizontalHeaderItem(col, head)
            self.ui.tableWidget_01.horizontalHeader().setVisible(True)

            item = QTableWidgetItem()
            item.setData(Qt.EditRole, db_data)
            self.ui.tableWidget_01.setItem(row_position, col, item)

            if row_position % 2 != 0:
                self.ui.tableWidget_01.item(row_position, col).setBackground(self.grey_light)
            else:
                self.ui.tableWidget_01.item(row_position, col).setBackground(self.grey_dark)

            # green QColor(90, 180, 90)
            # self.ui.tableWidget_01.setItem(row_position, col, QTableWidgetItem().setData(Qt.EditRole, db_data))
            col += 1
        self.error_highlight()
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
        self.ui.tableWidget_01.selectRow(row_position)
        self.ui.tableWidget_01.repaint()  # !!!!
        self.ui.tableWidget_01.setSortingEnabled(True)
        self.table_mode = True

        # task_thread = threading.Thread(target=self.ui.tableWidget_01.repaint())
        # task_thread.start()
        # process = multiprocessing.Process(target=self.ui.tableWidget_01.repaint())
        # process.start()

        # self.ui.tableWidget_01.selectedItems(QTableWidgetItem())
        # self.ui.playButton.clicked.connect(self.play_selected())
        # col_position = self.ui.tableWidget_01.columnCount()
        # print('col_position:', col_position)
        # row_position = self.ui.tableWidget_01.rowCount()
        # print('row_position:', row_position)

    def create_table_02(self, file_path):
        # all_headers = Data().read_all_data('file_path')
        self.ui.tableWidget_02.setRowCount(0)
        self.block_table_02(file_path, 'V')
        self.block_table_02(file_path, 'A')
        self.block_table_02(file_path, 'S')
        self.block_table_02(file_path, 'C')
        self.block_table_02(file_path, 'F')

    def block_table_02(self, file_path, type_material):
        all_headers = Data().read_all_data('file_path')
        all_data = Data().read_all_data(file_path)
        all_dict = dict(zip(all_headers, all_data))
        data_target = False
        for header in all_headers:
            row_position = self.ui.tableWidget_02.rowCount()
            data = all_dict[header]
            # data = Data().read_bd(header, file_path)  # !!!
            # print('all_dict', all_dict)
            if header[:1] == f'{type_material}' and data != None and data != 'нет данных':
                # print('header', header[:1])
                # print('data', data)
                if 'size' in header:
                    data = convert_bytes(int(data), "b")
                if 'bit_rate' in header:
                    data = convert_bytes(int(data), "bit/s")
                if 'duration' in header:
                    fps = Data().read_bd('V01_r_frame_rate', file_path)
                    fps = convert_fps(fps).split(' ')[0]
                    data = str(convert_duration_sec(float(data), float(fps)))
                if 'frame_rate' in header:
                    data = convert_fps(data)
                if 'sample_rate' in header:
                    data = convert_khz(data)
                if 'level' in header:
                    data = int(data) / 10

                data_target = True
                header = self.tbl2_header_rename(header)

                self.ui.tableWidget_02.insertRow(row_position)
                self.ui.tableWidget_02.setColumnWidth(0, 120)
                self.ui.tableWidget_02.setColumnWidth(1, 220)
                self.ui.tableWidget_02.setItem(row_position, 0, QtWidgets.QTableWidgetItem(header))
                # self.ui.tableWidget_02.item(row_position, 0).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
                self.ui.tableWidget_02.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(data)))
                if header[1:3].isdigit():
                    if int(header[1:3]) % 2 != 0:
                        self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(30, 30, 30))
                        # self.ui.tableWidget_02.item(row_position, 0).setForeground(QColor(146, 146, 146))
                    else:
                        self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(30, 30, 30))
                        self.ui.tableWidget_02.item(row_position, 0).setForeground(QColor(146, 146, 146))
                else:
                    self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(30, 30, 30))
                # if header[1:3].isdigit is True and int(header[1:3]) % 2 != 0:
                #     self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(30, 30, 30))
                # else:
                #     self.ui.tableWidget_02.item(row_position, 1).setBackground(QColor(35, 35, 35))
                # QColor(self.grey_light)
        if data_target:
            row_position = self.ui.tableWidget_02.rowCount()
            self.ui.tableWidget_02.insertRow(row_position)

    def click_table(self):
        row_position = self.ui.tableWidget_01.currentRow()
        # name_01 = self.ui.tableWidget_01.horizontalHeader().sectionClicked.connect(self.click_handler)
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        # # print(self.ui.tableWidget_01.verticalHeaderItem(row_position).text())
        self.create_table_02(file_path)
        self.create_tags(file_path)
        self.show_waves(file_path)
        return file_path

    def double_click_table(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path_video = self.ui.tableWidget_01.item(row_position, 0).text()
        file_path_image = Data().read_bd('waveform_path', file_path_video)
        os.startfile(os.path.normpath(file_path_image))

    def double_click_video_player(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        # print('test')
        self.dialog.file_path.setText(file_path)
        self.show_video_info_player(file_path)
        self.video_player()

    def create_tags(self, file_path):
        width = Data().read_bd('V01_width', file_path)
        height = Data().read_bd('V01_height', file_path)
        if width != 'нет данных' and height != 'нет данных':
            self.ui.tag_resolution.setText(f'{width} x {height}')
        else:
            self.ui.tag_resolution.setText('')
        prof = Data().read_bd('V01_profile', file_path)
        lev = Data().read_bd('V01_level', file_path)
        if prof != 'нет данных' and lev != 'нет данных':
            self.ui.tag_v1_profile.setText(f'{prof} {int(lev) / 10}')
        else:
            self.ui.tag_v1_profile.setText('')

        self.ui.tag_file_name.setText(self.prepare_tag('file_name', file_path))
        self.ui.tag_file_path.setText(self.prepare_tag('file_path', file_path))
        self.ui.tag_v1_codec_name.setText(self.prepare_tag('V01_codec_name', file_path))
        self.ui.tag_a1_codec_name.setText(self.prepare_tag('A01_codec_name', file_path))
        self.ui.tag_a2_codec_name.setText(self.prepare_tag('A02_codec_name', file_path))
        self.ui.tag_a1_sample_rate.setText(self.prepare_tag('A01_sample_rate', file_path))
        self.ui.tag_a2_sample_rate.setText(self.prepare_tag('A02_sample_rate', file_path))
        self.ui.tag_a1_channel_layout.setText(self.prepare_tag('A01_channel_layout', file_path))
        self.ui.tag_a2_channel_layout.setText(self.prepare_tag('A02_channel_layout', file_path))
        self.ui.tag_s1_title.setText(self.prepare_tag('S01_title', file_path))
        self.ui.tag_s2_title.setText(self.prepare_tag('S02_title', file_path))
        self.ui.tag_s1_language.setText(self.prepare_tag('S01_language', file_path))
        self.ui.tag_s2_language.setText(self.prepare_tag('S02_language', file_path))
        self.ui.tag_v1_r_frame_rate.setText(str(self.prepare_tag('V01_r_frame_rate', file_path)))
        self.ui.tag_duration.setText(str(self.prepare_tag('F_duration', file_path)))

    def prepare_tag(self, header_tag, file_path):
        # all_headers = Data().read_all_data('file_path')
        # all_data = Data().read_all_data(file_path)
        # all_dict = dict(zip(all_headers, all_data))
        # tag = all_dict[header_tag]
        tag = Data().read_bd(header_tag, file_path)
        if tag is None or tag == 'нет данных':
            tag = ''
        elif 'frame_rate' in header_tag:
            tag = convert_fps(tag)
        elif 'file_path' in header_tag:
            tag = os.path.split(tag)[0]
        elif 'sample_rate' in header_tag:
            tag = convert_khz(tag)
        elif 'F_duration' in header_tag:
            fps = Data().read_bd('V01_r_frame_rate', file_path)
            fps = convert_fps(fps).split(' ')[0]
            tag = str(convert_duration_sec(float(tag), float(fps)))
            # tag = datetime.timedelta(seconds=(round(float(tag), 0)))
        return tag

    def error_highlight(self):

        codec = self.ui_set.codec_txt.text()
        width = self.ui_set.width_txt.text()
        height = self.ui_set.height_txt.text()
        v_bit_rate = float(self.ui_set.v_bit_rate_txt.text())
        frame_rate = self.ui_set.frame_rate_comboBox.currentText()
        dar = self.ui_set.dar_comboBox.currentText()
        codec_aud = self.ui_set.codec_aud_txt.text()
        channels = self.ui_set.channels_txt.text()
        sample_rate = str(self.ui_set.sample_rate_comboBox.currentText())
        a_bit_rate = float(self.ui_set.a_bit_rate_txt.text())

        r128_i = self.ui_set.r128_i_txt.text()
        r128_lra = self.ui_set.r128_lra_txt.text()
        r128_tp = self.ui_set.r128_tp_txt.text()
        r128_thr = self.ui_set.r128_thr_txt.text()

        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()

        for row in range(rows):
            for col in range(columns):
                if row % 2 != 0:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
                else:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)

                if col % 2 != 0:
                    error_red_color = self.red_light
                    error_yell_color = self.yell_light
                else:
                    error_red_color = self.red_dark
                    error_yell_color = self.yell_dark
                header = self.ui.tableWidget_01.horizontalHeaderItem(col).text()
                data = self.ui.tableWidget_01.item(row, col).text()
                if data != 'нет данных':
                    if self.header_rename('F_bit_rate') in header and not isclose(float(data.split(' ')[0]), v_bit_rate,
                                                                                  abs_tol=1):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('V01_codec_name') in header and data != codec:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('V01_width') in header and data != width:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('V01_height') in header and data != height:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('V01_display_aspect_ratio') in header and data != dar:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('V01_r_frame_rate') in header and str(data.split(' ')[0]) != str(frame_rate):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('A01_sample_rate') in header and str(data.split(' ')[0]) != str(sample_rate):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('A01_codec_name') in header and data != codec_aud:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('A01_channels') in header and data != channels:
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('A01_bit_rate') in header and data != 'нет данных' and not isclose(
                            float(data.split(' ')[0]), a_bit_rate, abs_tol=60):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if self.header_rename('audio_streams') in header and data != '1':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)

                if self.header_rename('input_i') in header:
                    if data == '-Inf':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if data == 'нет данных':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                    elif not isclose(float(data), float(r128_i), abs_tol=0.5):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                if self.header_rename('input_tp') in header:
                    if data == '-Inf':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                    if data == 'нет данных':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                    elif not isclose(float(data), float(r128_tp), abs_tol=0.5):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                if self.header_rename('input_lra') in header:
                    if data == 'нет данных':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                    elif not isclose(float(data), float(r128_lra), abs_tol=5):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                if self.header_rename('input_thresh') in header:
                    if data == 'нет данных':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)
                    elif not isclose(float(data), float(r128_thr), abs_tol=0.5):
                        self.ui.tableWidget_01.item(row, col).setBackground(error_yell_color)

                if self.header_rename('black_start') in header:
                    if data == 'найден':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                if self.header_rename('silence_start') in header:
                    if data == 'найден':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
                if self.header_rename('freeze_start') in header:
                    if data == 'найден':
                        self.ui.tableWidget_01.item(row, col).setBackground(error_red_color)
        # duration = Data().read_bd('F_duration', file_path)
        # self.ui.tag_duration.setText(duration)

    def del_row(self):
        row_position = self.ui.tableWidget_01.currentRow()
        self.ui.tableWidget_01.removeRow(row_position)
        # self.ui.tableWidget_01.focusPreviousChild()
        # a1_ch = Data().read_bd('A1_channel_layout', file_path)
        # self.ui.tag_file_path.setText(a1_ch)

    def clear_table_01(self):
        self.ui.tableWidget_01.setRowCount(0)

    # def file_queue(self):
    #     row_count = self.ui.tableWidget_01.rowCount()
    #     queue_list = []
    #     if row_count != 0:
    #         for row in range(row_count):
    #             file_path = self.ui.tableWidget_01.item(row, 0).text()
    #             db_wf_file_path = Data().read_bd('waveform_path', file_path)
    #             if db_wf_file_path == 'нет данных':
    #                 queue_list.append(file_path)
    #                 self.create_image_files(file_path)
    #             else:
    #                 print('Сканирование R128 уже проводилось')
    #     return queue_list

    def file_queue(self):
        row_count = self.ui.tableWidget_01.rowCount()
        queue_list = []
        if row_count != 0:
            for row in range(row_count):
                file_path = self.ui.tableWidget_01.item(row, 0).text()
                queue_list.append(file_path)
            return queue_list

    def play_selected(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        os.startfile(os.path.normpath(file_path))

    def open_folder(self):
        try:
            row_position = self.ui.tableWidget_01.currentRow()
            file_path = self.ui.tableWidget_01.item(row_position, 0).text()
            subprocess.Popen(fr'explorer /select,"{os.path.abspath(file_path)}"')
        except Exception:
            print('Файл не выделен')
            pass

    def open_folder_video_player(self):
        file_path = self.dialog.file_path.text()
        subprocess.Popen(fr'explorer /select,"{os.path.abspath(file_path)}"')

    def prepare_loudnorm_single(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
        progress_dialog_r128.setWindowTitle("Processing...")
        progress_dialog_r128.setWindowModality(Qt.WindowModal)
        progress_dialog_r128.setMinimumDuration(0)
        progress_dialog_r128.setMinimumSize(400, 150)
        progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")
        self.scan_loudnorm((file_path,), progress_dialog_r128)
        progress_dialog_r128.setValue(100)

    def prepare_loudnorm_multi(self):
        tbl_file_list = self.file_queue()
        progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
        progress_dialog_r128.setWindowTitle("Processing...")
        progress_dialog_r128.setWindowModality(Qt.WindowModal)
        progress_dialog_r128.setMinimumDuration(0)
        progress_dialog_r128.setMinimumSize(400, 150)
        progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_loudnorm(tuple(tbl_file_list), progress_dialog_r128)
        # process = multiprocessing.Process(target=self.scan_loudnorm(tuple(tbl_file_list), progress_dialog_r128))
        # process.start()
        progress_dialog_r128.setValue(100)
        progress_dialog_r128.repaint()

    # def create_image_file(self):
    #     row_position = self.ui.tableWidget_01.currentRow()
    #     file_path = self.ui.tableWidget_01.item(row_position, 0).text()
    #     WaveformSingle(file_path)

    def backgound_scan_loudnorm(self, file_list, progress_dialog_r128):
        completed = False
        r128_i = self.ui_set.r128_i_txt.text()
        r128_lra = self.ui_set.r128_lra_txt.text()
        r128_tp = self.ui_set.r128_tp_txt.text()
        r128_thr = self.ui_set.r128_thr_txt.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_01.setRowCount(0)
        self.ui.tableWidget_01.setColumnCount(3)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_r128.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_r128.setLabelText(f'{i + 1}/{total_files}  Loudness scan\n{file_path}')
            if progress_dialog_r128.wasCanceled():
                completed = False
                break
            db_wf_file_path = Data().read_bd('waveform_path', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Запуск анализа уровня громкости файла', file_path)
                    R128(file_path, r128_i, r128_lra, r128_tp)
                    print(now())
                    print('Анализ уровня громкости файла', file_path, 'завершён')
                    self.create_table_bg(file_path, 'Loudnorm', 'Выполнено')
                except Exception:
                    print(now())
                    print('Ошибка анализа уровня громкости')
                    self.create_table_bg(file_path, 'Loudnorm', 'Ошибка')
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование R128 файла', file_path, 'уже проводилось')
                self.create_table_bg(file_path, 'Loudnorm', 'Сканирование проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_r128.setValue(progress)
            QApplication.processEvents()
            completed = True
        return completed

    def backgound_scan_blackdetect(self, file_list, progress_dialog_blck):
        blck_dur = self.ui_set.blck_dur_txt.text()
        blck_thr = self.ui_set.blck_thr_txt.text()
        blck_tc_in = self.ui_set.blck_tc_in.text()
        blck_tc_out = self.ui_set.blck_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_01.setRowCount(0)
        self.ui.tableWidget_01.setColumnCount(3)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_blck.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_blck.setLabelText(f'{i + 1}/{total_files}  BlackDetect scan\n{file_path}')
            if progress_dialog_blck.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('black_duration', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ чёрного поля файла', file_path)
                    BlackDetect(file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out)
                    print(now())
                    print('Анализ завершён')
                    self.create_table_bg(file_path, 'BlackDetect', 'Выполнено')
                except Exception:
                    print(now())
                    print('Ошибка анализа чёрного поля')
                    self.create_table_bg(file_path, 'BlackDetect', 'Ошибка')
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование чёрного поля файла', file_path, 'уже проводилось')
                self.create_table_bg(file_path, 'BlackDetect', 'Сканирование проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_blck.setValue(progress)
            QApplication.processEvents()

    def backgound_scan_silencedetect(self, file_list, progress_dialog_slnc):
        slnc_dur = self.ui_set.slnc_dur_txt.text()
        slnc_noize = self.ui_set.slnc_noize_txt.text()
        slnc_tc_in = self.ui_set.slnc_tc_in.text()
        slnc_tc_out = self.ui_set.slnc_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_01.setRowCount(0)
        self.ui.tableWidget_01.setColumnCount(3)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_slnc.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_slnc.setLabelText(f'{i + 1}/{total_files}  SilenceDetect scan\n{file_path}')
            if progress_dialog_slnc.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('silence_duration', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ пропусков звука в', file_path)
                    SilenceDetect(file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out)
                    print(now())
                    print('Анализ завершён')
                    self.create_table_bg(file_path, 'SilenceDetect', 'Выполнено')
                except Exception:
                    print(now())
                    print('Ошибка анализа пропусков звука')
                    self.create_table_bg(file_path, 'SilenceDetect', 'Ошибка')
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование пропусков звука в', file_path, 'уже проводилось')
                self.create_table_bg(file_path, 'SilenceDetect', 'Сканирование проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_slnc.setValue(progress)
            QApplication.processEvents()

    def backgound_scan_freezedetect(self, file_list, progress_dialog_frz):
        frz_dur = self.ui_set.frz_dur_txt.text()
        frz_noize = self.ui_set.frz_noize_txt.text()
        frz_tc_in = self.ui_set.frz_tc_in.text()
        frz_tc_out = self.ui_set.frz_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.tableWidget_01.setRowCount(0)
        self.ui.tableWidget_01.setColumnCount(3)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_frz.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_frz.setLabelText(f'{i + 1}/{total_files}  FreezeDetect scan\n{file_path}')
            if progress_dialog_frz.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('freeze_duration', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ стоп-кадров в', file_path)
                    FreezeDetect(file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out)
                    print(now())
                    print('Анализ завершён')
                    self.create_table_bg(file_path, 'FreezeDetect', 'Выполнено')
                except Exception:
                    print(now())
                    print('Ошибка анализа стоп-кадров')
                    self.create_table_bg(file_path, 'FreezeDetect', 'Ошибка')
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Анализ стоп-кадров в', file_path, 'уже проводился')
                self.create_table_bg(file_path, 'FreezeDetect', 'Сканирование проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_frz.setValue(progress)
            QApplication.processEvents()

    def backgound_fullscan_loudnorm(self, file_list, progress_dialog_r128):
        complited = False
        r128_i = self.ui_set.r128_i_txt.text()
        r128_lra = self.ui_set.r128_lra_txt.text()
        r128_tp = self.ui_set.r128_tp_txt.text()
        r128_thr = self.ui_set.r128_thr_txt.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_r128.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_r128.setLabelText(f'{i + 1}/{total_files}  Loudness scan\n{file_path}')
            if progress_dialog_r128.wasCanceled():
                complited = False
                break
            db_wf_file_path = Data().read_bd('waveform_path', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Запуск анализа уровня громкости файла', file_path)
                    R128(file_path, r128_i, r128_lra, r128_tp)
                    print(now())
                    print('Анализ уровня громкости файла', file_path, 'завершён')
                    self.create_table_bg_full(file_path, 'Loudness', 'Выполнено')
                except Exception:
                    print(now())
                    print('Ошибка анализа уровня громкости')
                    self.create_table_bg_full(file_path, 'Loudness', 'Ошибка')
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование R128 файла', file_path, 'уже проводилось')
                self.create_table_bg_full(file_path, 'Loudness', 'Сканирование проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_r128.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def backgound_fullscan_blackdetect(self, file_list, progress_dialog_blck):
        complited = False
        blck_dur = self.ui_set.blck_dur_txt.text()
        blck_thr = self.ui_set.blck_thr_txt.text()
        blck_tc_in = self.ui_set.blck_tc_in.text()
        blck_tc_out = self.ui_set.blck_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_blck.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_blck.setLabelText(f'{i + 1}/{total_files}  BlackDetect scan\n{file_path}')
            if progress_dialog_blck.wasCanceled():
                status = 'Отменено'
                complited = False
                self.create_table_bg_full(file_path, i, 'BlackDetect', status)
                break
            db_wf_file_path = Data().read_bd('black_duration', file_path)
            if db_wf_file_path == 'нет данных':
                try:
                    print(now())
                    print('Анализ чёрного поля файла', file_path)
                    BlackDetect(file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out)
                    print(now())
                    print('Анализ завершён')
                    status = 'Выполнено'
                except Exception:
                    print(now())
                    print('Ошибка анализа чёрного поля')
                    status = 'Ошибка'
                    pass
            else:
                print(now())
                print('Сканирование чёрного поля файла', file_path, 'уже проводилось')
                status = 'Сканирование проводилось'
            self.create_table_bg_full(file_path, i, 'BlackDetect', status)
            progress = int((i + 1) / total_files * 100)
            progress_dialog_blck.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def backgound_fullscan_silencedetect(self, file_list, progress_dialog_r128):
        complited = False
        slnc_dur = self.ui_set.slnc_dur_txt.text()
        slnc_noize = self.ui_set.slnc_noize_txt.text()
        slnc_tc_in = self.ui_set.slnc_tc_in.text()
        slnc_tc_out = self.ui_set.slnc_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_r128.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_r128.setLabelText(f'{i + 1}/{total_files}  SilenceDetect scan\n{file_path}')
            if progress_dialog_r128.wasCanceled():
                complited = False
                status = 'Отменено'
                self.create_table_bg_full(file_path, i, 'SilenceDetect', status)
                break
            db_wf_file_path = Data().read_bd('silence_duration', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ пропусков звука в', file_path)
                    SilenceDetect(file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out)
                    print(now())
                    print('Анализ завершён')
                    status = 'Выполнено'
                except Exception:
                    print(now())
                    print('Ошибка анализа пропусков звука')
                    status = 'Ошибка'
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование пропусков звука в', file_path, 'уже проводилось')
                status = 'Сканирование проводилось'
            self.create_table_bg_full(file_path, i, 'SilenceDetect', status)
            progress = int((i + 1) / total_files * 100)
            progress_dialog_r128.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def backgound_fullscan_freezedetect(self, file_list, progress_dialog_frz):
        complited = False
        frz_dur = self.ui_set.frz_dur_txt.text()
        frz_noize = self.ui_set.frz_noize_txt.text()
        frz_tc_in = self.ui_set.frz_tc_in.text()
        frz_tc_out = self.ui_set.frz_tc_out.text()
        self.ui.tableWidget_01.horizontalHeader().setVisible(True)
        # self.ui.tableWidget_01.horizontalHeader().setMinimumHeight(300)
        # self.ui.tableWidget_01.horizontalHeader().setMaximumHeight(500)
        self.ui.tableWidget_01.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        total_files = len(file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_frz.setValue(progress)
        QApplication.processEvents()
        for i, file_path in enumerate(file_list):
            progress_dialog_frz.setLabelText(f'{i + 1}/{total_files}  FreezeDetect scan\n{file_path}')
            if progress_dialog_frz.wasCanceled():
                complited = False
                status = 'Отменено'
                for _ in range(i, total_files):
                    self.create_table_bg_full(file_path, i, 'FreezeDetect', status)
                break
            db_wf_file_path = Data().read_bd('freeze_duration', file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ стоп-кадров в', file_path)
                    FreezeDetect(file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out)
                    print(now())
                    print('Анализ завершён')
                    status = 'Выполнено'
                except Exception:
                    print(now())
                    print('Ошибка анализа стоп-кадров')
                    status = 'Ошибка'
                    pass
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Анализ стоп-кадров в', file_path, 'уже проводился')
                status = 'Сканирование проводилось'
            self.create_table_bg_full(file_path, i, 'FreezeDetect', status)
            progress = int((i + 1) / total_files * 100)
            progress_dialog_frz.setValue(progress)
            QApplication.processEvents()
            complited = True
        return complited

    def scan_loudnorm(self, tbl_file_list, progress_dialog_r128):
        r128_i = self.ui_set.r128_i_txt.text()
        r128_lra = self.ui_set.r128_lra_txt.text()
        r128_tp = self.ui_set.r128_tp_txt.text()
        r128_thr = self.ui_set.r128_thr_txt.text()
        total_files = len(tbl_file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_r128.setValue(progress)
        QApplication.processEvents()
        for i, tbl_file_path in enumerate(tbl_file_list):
            progress_dialog_r128.setLabelText(f'{i + 1}/{total_files}  Loudness scan\n{tbl_file_path}')
            if progress_dialog_r128.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('waveform_path', tbl_file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Запуск анализа уровня громкости файла', tbl_file_path)
                    R128(tbl_file_path, r128_i, r128_lra, r128_tp)
                    print(now())
                    print('Анализ уровня громкости файла', tbl_file_path, 'завершён')
                except Exception:
                    print(now())
                    print('Ошибка анализа уровня громкости')
                    pass
                self.add_table_r128()
                # self.error_highlight()
                # self.alert.close()
            else:
                print(now())
                print('Сканирование R128 файла', tbl_file_path, 'уже проводилось')
            progress = int((i + 1) / total_files * 100)
            progress_dialog_r128.setValue(progress)
            QApplication.processEvents()

    def values_damage(self):
        v_slnc_dur = self.ui_set.slnc_dur_txt.text()
        v_slnc_noize = self.ui_set.slnc_noize_txt.text()
        v_slnc_tc_in = self.ui_set.slnc_tc_in.text()
        v_slnc_tc_out = self.ui_set.slnc_tc_out.text()

        v_frz_dur = self.ui_set.frz_dur_txt.text()
        v_frz_noize = self.ui_set.frz_noize_txt.text()
        v_frz_tc_in = self.ui_set.frz_tc_in.text()
        v_frz_tc_out = self.ui_set.frz_tc_out.text()

    def prepare_black_detect_single(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
        progress_dialog_blck.setWindowTitle("Processing...")
        progress_dialog_blck.setWindowModality(Qt.WindowModal)
        progress_dialog_blck.setMinimumDuration(0)
        progress_dialog_blck.setMinimumSize(400, 150)
        progress_dialog_blck.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_black_detect((file_path,), progress_dialog_blck)
        progress_dialog_blck.setValue(100)

    def prepare_black_detect_multi(self):
        tbl_file_list = self.file_queue()
        progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
        progress_dialog_blck.setWindowTitle("Processing...")
        progress_dialog_blck.setWindowModality(Qt.WindowModal)
        progress_dialog_blck.setMinimumDuration(0)
        progress_dialog_blck.setMinimumSize(400, 150)
        progress_dialog_blck.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_black_detect(tuple(tbl_file_list), progress_dialog_blck)
        progress_dialog_blck.setValue(100)

    def scan_black_detect(self, tbl_file_list, progress_dialog_blck):
        total_files = len(tbl_file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_blck.setValue(progress)
        QApplication.processEvents()
        blck_dur = self.ui_set.blck_dur_txt.text()
        blck_thr = self.ui_set.blck_thr_txt.text()
        blck_tc_in = self.ui_set.blck_tc_in.text()
        blck_tc_out = self.ui_set.blck_tc_out.text()
        for i, tbl_file_path in enumerate(tbl_file_list):
            progress_dialog_blck.setLabelText(f'{i + 1}/{total_files}  BlackDetect scan\n{tbl_file_path}')
            if progress_dialog_blck.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('black_duration', tbl_file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ чёрного поля файла', tbl_file_path)
                    BlackDetect(tbl_file_path, blck_dur, blck_thr, blck_tc_in, blck_tc_out)
                except Exception:
                    print(now())
                    print('Ошибка анализа чёрного поля')
                    pass
                self.add_table_black()
                # self.error_highlight()
                # self.alert.close()
            else:
                print('Сканирование чёрного поля файла', tbl_file_path, 'уже проводилось')

            progress = int((i + 1) / total_files * 100)
            progress_dialog_blck.setValue(progress)
            QApplication.processEvents()

    def prepare_silence_detect_single(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
        progress_dialog_slnc.setWindowTitle("Processing...")
        progress_dialog_slnc.setWindowModality(Qt.WindowModal)
        progress_dialog_slnc.setMinimumDuration(0)
        progress_dialog_slnc.setMinimumSize(400, 150)
        progress_dialog_slnc.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_silence_detect((file_path,), progress_dialog_slnc)
        progress_dialog_slnc.setValue(100)

    def prepare_silence_detect_multi(self):
        tbl_file_list = self.file_queue()
        progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
        progress_dialog_slnc.setWindowTitle("Processing...")
        progress_dialog_slnc.setWindowModality(Qt.WindowModal)
        progress_dialog_slnc.setMinimumDuration(0)
        progress_dialog_slnc.setMinimumSize(400, 150)
        progress_dialog_slnc.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_silence_detect(tuple(tbl_file_list), progress_dialog_slnc)
        progress_dialog_slnc.setValue(100)

    def scan_silence_detect(self, tbl_file_list, progress_dialog_slnc):
        slnc_dur = self.ui_set.slnc_dur_txt.text()
        slnc_noize = self.ui_set.slnc_noize_txt.text()
        slnc_tc_in = self.ui_set.slnc_tc_in.text()
        slnc_tc_out = self.ui_set.slnc_tc_out.text()
        total_files = len(tbl_file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_slnc.setValue(progress)
        QApplication.processEvents()
        for i, tbl_file_path in enumerate(tbl_file_list):
            progress_dialog_slnc.setLabelText(f'{i + 1}/{total_files}  SilenceDetect scan\n{tbl_file_path}')
            if progress_dialog_slnc.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('silence_duration', tbl_file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ пропусков звука в', tbl_file_path)
                    SilenceDetect(tbl_file_path, slnc_dur, slnc_noize, slnc_tc_in, slnc_tc_out)
                except Exception:
                    print(now())
                    print('Ошибка анализа пропусков звука')
                    pass
                self.add_table_silence()
                # self.error_highlight()
                # self.alert.close()
            else:
                print('Сканирование пропусков звука в', tbl_file_path, 'уже проводилось')

            progress = int((i + 1) / total_files * 100)
            progress_dialog_slnc.setValue(progress)
            QApplication.processEvents()

    def prepare_freeze_detect_single(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
        progress_dialog_frz.setWindowTitle("Processing...")
        progress_dialog_frz.setWindowModality(Qt.WindowModal)
        progress_dialog_frz.setMinimumDuration(0)
        progress_dialog_frz.setMinimumSize(400, 150)
        progress_dialog_frz.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                          "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                          "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                          "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_freeze_detect((file_path,), progress_dialog_frz)
        progress_dialog_frz.setValue(100)

    def prepare_freeze_detect_multi(self):
        tbl_file_list = self.file_queue()
        progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
        progress_dialog_frz.setWindowTitle("Processing...")
        progress_dialog_frz.setWindowModality(Qt.WindowModal)
        progress_dialog_frz.setMinimumDuration(0)
        progress_dialog_frz.setMinimumSize(400, 150)
        progress_dialog_frz.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                          "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                          "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                          "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_freeze_detect(tuple(tbl_file_list), progress_dialog_frz)
        progress_dialog_frz.setValue(100)

    def scan_freeze_detect(self, tbl_file_list, progress_dialog_frz):
        frz_dur = self.ui_set.frz_dur_txt.text()
        frz_noize = self.ui_set.frz_noize_txt.text()
        frz_tc_in = self.ui_set.frz_tc_in.text()
        frz_tc_out = self.ui_set.frz_tc_out.text()
        total_files = len(tbl_file_list)
        progress = int(1 / total_files * 100)
        progress_dialog_frz.setValue(progress)
        QApplication.processEvents()
        for i, tbl_file_path in enumerate(tbl_file_list):
            progress_dialog_frz.setLabelText(f'{i + 1}/{total_files}  FreezeDetect scan\n{tbl_file_path}')
            if progress_dialog_frz.wasCanceled():
                break
            db_wf_file_path = Data().read_bd('freeze_duration', tbl_file_path)
            if db_wf_file_path == 'нет данных':
                # self.alert.show()
                try:
                    print(now())
                    print('Анализ стоп-кадров в', tbl_file_path)
                    FreezeDetect(tbl_file_path, frz_dur, frz_noize, frz_tc_in, frz_tc_out)
                except Exception:
                    print(now())
                    print('Ошибка анализа стоп-кадров')
                    pass
                self.add_table_freeze()
                # self.error_highlight()
                # self.alert.close()
            else:
                print('Анализ стоп-кадров в', tbl_file_path, 'уже проводился')

            progress = int((i + 1) / total_files * 100)
            progress_dialog_frz.setValue(progress)
            QApplication.processEvents()

    def prepare_full_detect_single(self):
        row_position = self.ui.tableWidget_01.currentRow()
        file_path = self.ui.tableWidget_01.item(row_position, 0).text()
        progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
        progress_dialog_r128.setWindowTitle("Processing...")
        progress_dialog_r128.setWindowModality(Qt.WindowModal)
        progress_dialog_r128.setMinimumDuration(0)
        progress_dialog_r128.setMinimumSize(400, 150)
        progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_loudnorm((file_path,), progress_dialog_r128)
        progress_dialog_r128.setValue(100)

        progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
        progress_dialog_blck.setWindowTitle("Processing...")
        progress_dialog_blck.setWindowModality(Qt.WindowModal)
        progress_dialog_blck.setMinimumDuration(0)
        progress_dialog_blck.setMinimumSize(400, 150)
        progress_dialog_blck.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_black_detect((file_path,), progress_dialog_blck)
        progress_dialog_blck.setValue(100)

        progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
        progress_dialog_slnc.setWindowTitle("Processing...")
        progress_dialog_slnc.setWindowModality(Qt.WindowModal)
        progress_dialog_slnc.setMinimumDuration(0)
        progress_dialog_slnc.setMinimumSize(400, 150)
        progress_dialog_slnc.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_silence_detect((file_path,), progress_dialog_slnc)
        progress_dialog_slnc.setValue(100)

        progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
        progress_dialog_frz.setWindowTitle("Processing...")
        progress_dialog_frz.setWindowModality(Qt.WindowModal)
        progress_dialog_frz.setMinimumDuration(0)
        progress_dialog_frz.setMinimumSize(400, 150)
        progress_dialog_frz.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                          "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                          "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                          "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_freeze_detect((file_path,), progress_dialog_frz)
        progress_dialog_frz.setValue(100)

    def prepare_full_detect_multi(self):
        tbl_file_list = self.file_queue()
        progress_dialog_r128 = QProgressDialog("Loudness scan", "Cancel", 0, 100, self)
        progress_dialog_r128.setWindowTitle("Processing...")
        progress_dialog_r128.setWindowModality(Qt.WindowModal)
        progress_dialog_r128.setMinimumDuration(0)
        progress_dialog_r128.setMinimumSize(400, 150)
        progress_dialog_r128.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_loudnorm(tuple(tbl_file_list), progress_dialog_r128)
        progress_dialog_r128.setValue(100)

        progress_dialog_blck = QProgressDialog("BlackDetect scan", "Cancel", 0, 100, self)
        progress_dialog_blck.setWindowTitle("Processing...")
        progress_dialog_blck.setWindowModality(Qt.WindowModal)
        progress_dialog_blck.setMinimumDuration(0)
        progress_dialog_blck.setMinimumSize(400, 150)
        progress_dialog_blck.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_black_detect(tuple(tbl_file_list), progress_dialog_blck)
        progress_dialog_blck.setValue(100)

        progress_dialog_slnc = QProgressDialog("SilenceDetect scan", "Cancel", 0, 100, self)
        progress_dialog_slnc.setWindowTitle("Processing...")
        progress_dialog_slnc.setWindowModality(Qt.WindowModal)
        progress_dialog_slnc.setMinimumDuration(0)
        progress_dialog_slnc.setMinimumSize(400, 150)
        progress_dialog_slnc.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                           "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                           "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                           "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_silence_detect(tuple(tbl_file_list), progress_dialog_slnc)
        progress_dialog_slnc.setValue(100)

        progress_dialog_frz = QProgressDialog("FreezeDetect scan", "Cancel", 0, 100, self)
        progress_dialog_frz.setWindowTitle("Processing...")
        progress_dialog_frz.setWindowModality(Qt.WindowModal)
        progress_dialog_frz.setMinimumDuration(0)
        progress_dialog_frz.setMinimumSize(400, 150)
        progress_dialog_frz.setStyleSheet("QPushButton {color: white; background-color:rgba(255,255,255,30);"
                                          "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
                                          "QPushButton:hover {background-color:rgba(255,255,255,50);}"
                                          "QPushButton:pressed{background-color:rgba(255,255,255,70);}")

        self.scan_freeze_detect(tuple(tbl_file_list), progress_dialog_frz)
        progress_dialog_frz.setValue(100)

    def add_table_r128(self):
        # self.ui.tableWidget_01.repaint()
        # rows = self.ui.tableWidget_01.rowCount()
        # for row in range(rows):
        #     file_path = self.ui.tableWidget_01.item(row, 0).text()
        #     self.create_table_01(file_path)
        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()
        for row in range(rows):
            # self.ui.tableWidget_01.repaint()
            file_path = self.ui.tableWidget_01.item(row, 0).text()
            for col in range(columns):
                header = self.ui.tableWidget_01.horizontalHeaderItem(col).text()

                if self.header_rename('input_i') in header:
                    db_data = Data().read_bd('input_i', file_path)
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, db_data)
                    self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if self.header_rename('input_tp') in header:
                    db_data = Data().read_bd('input_tp', file_path)
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, db_data)
                    self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if self.header_rename('input_lra') in header:
                    db_data = Data().read_bd('input_lra', file_path)
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, db_data)
                    self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if self.header_rename('input_thresh') in header:
                    db_data = Data().read_bd('input_thresh', file_path)
                    item = QTableWidgetItem()
                    item.setData(Qt.EditRole, db_data)
                    self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if row % 2 != 0:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
                else:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)
        self.error_highlight()
        self.ui.tableWidget_01.repaint()

    def add_table_black(self):
        # self.ui.tableWidget_01.repaint()
        # rows = self.ui.tableWidget_01.rowCount()
        # for row in range(rows):
        #     file_path = self.ui.tableWidget_01.item(row, 0).text()
        #     self.create_table_01(file_path)
        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()
        for row in range(rows):
            # self.ui.tableWidget_01.repaint()
            file_path = self.ui.tableWidget_01.item(row, 0).text()
            for col in range(columns):
                header = self.ui.tableWidget_01.horizontalHeaderItem(col).text()
                db_data = Data().read_bd('black_start', file_path)
                if self.header_rename('black_start') in header:
                    if db_data != 'нет данных' and db_data != 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'найден')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    if db_data == 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'не найдено')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if row % 2 != 0:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
                else:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)
        self.error_highlight()

    def add_table_silence(self):
        # self.ui.tableWidget_01.repaint()
        # rows = self.ui.tableWidget_01.rowCount()
        # for row in range(rows):
        #     file_path = self.ui.tableWidget_01.item(row, 0).text()
        #     self.create_table_01(file_path)
        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()
        for row in range(rows):
            # self.ui.tableWidget_01.repaint()
            file_path = self.ui.tableWidget_01.item(row, 0).text()
            for col in range(columns):
                header = self.ui.tableWidget_01.horizontalHeaderItem(col).text()
                db_data = Data().read_bd('silence_start', file_path)
                if self.header_rename('silence_start') in header:
                    if db_data != 'нет данных' and db_data != 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'найден')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    if db_data == 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'не найдено')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if row % 2 != 0:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
                else:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)
        self.error_highlight()

    def add_table_freeze(self):
        # self.ui.tableWidget_01.repaint()
        # rows = self.ui.tableWidget_01.rowCount()
        # for row in range(rows):
        #     file_path = self.ui.tableWidget_01.item(row, 0).text()
        #     self.create_table_01(file_path)
        rows = self.ui.tableWidget_01.rowCount()
        columns = self.ui.tableWidget_01.columnCount()
        for row in range(rows):
            # self.ui.tableWidget_01.repaint()
            file_path = self.ui.tableWidget_01.item(row, 0).text()
            for col in range(columns):
                header = self.ui.tableWidget_01.horizontalHeaderItem(col).text()
                db_data = Data().read_bd('freeze_start', file_path)
                if self.header_rename('freeze_start') in header:
                    if db_data != 'нет данных' and db_data != 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'найден')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    if db_data == 'не найдено':
                        item = QTableWidgetItem()
                        item.setData(Qt.EditRole, 'не найдено')
                        self.ui.tableWidget_01.setItem(row, col, item)
                    # self.ui.tableWidget_01.showColumn(col)
                if row % 2 != 0:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_light)
                else:
                    self.ui.tableWidget_01.item(row, col).setBackground(self.grey_dark)
        self.error_highlight()

    def wave_view(self):
        self.ui.wave_view.show()
        self.ui.resizeButtonUp.hide()
        self.ui.resizeButtonDown.show()
        self.ui.r128_loudness.show()

        # self.ui.resizeButton.setText('Up')
        # # sender = self.sender()
        # print(sender.text())
        # if sender.text() == 'Up':
        #     self.ui.wave_view.show()
        #     self.ui.resizeButton.setText('Down')
        #     print(sender.text())
        # elif sender.text() == 'Down':
        #     self.ui.wave_view.hide()
        #     self.ui.resizeButton.setText('Up')
        #     print(sender.text())

    def wave_hide(self):
        self.ui.wave_view.hide()
        self.ui.r128_loudness.hide()
        self.ui.resizeButtonDown.hide()
        self.ui.resizeButtonUp.show()
        self.ui.frame_wave.setStyleSheet(u"QFrame#frame_wave{\nborder: 0px solid rgb(63,64,66);\n}")

    def show_waves(self, file_path):
        self.ui.frame_wave.setStyleSheet(u"QFrame#frame_wave{\nborder: 1px solid rgb(63,64,66);\n}")
        wave_file = Data().read_bd('waveform_path', file_path)
        if wave_file != 'нет данных':
            self.ui.wave_view.setPixmap(QPixmap(wave_file))

            input_i = Data().read_bd('input_i', file_path)
            input_tp = Data().read_bd('input_tp', file_path)
            input_lra = Data().read_bd('input_lra', file_path)
            input_thresh = Data().read_bd('input_thresh', file_path)
            text_info = f'  I = {input_i}  |  LRA = {input_lra}  |  TP = {input_tp}  |  THRESHOLD = {input_thresh}  '

            self.ui.r128_loudness.setText(text_info)
        else:
            self.ui.wave_view.setPixmap(QPixmap(u":/imgs/img/WaveForm_04.png"))
            # self.ui.r128_loudness.hide()
            self.ui.r128_loudness.setText('')

    def show_video_info_player(self, file_path):
        self.vinfo_player.show()
        # print('test2')
        black_start = Data().read_bd('black_start', file_path)
        silence_start = Data().read_bd('silence_start', file_path)
        freeze_start = Data().read_bd('freeze_start', file_path)
        if black_start != None and black_start != 'нет данных' and black_start != 'не найдено':
            self.create_blck_table(file_path)
        elif black_start == 'не найдено':
            self.dialog.blck_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.blck_table.setRowCount(0)
            self.dialog.blck_table.insertRow(0)
            self.dialog.blck_table.setItem(0, 0, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.blck_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.blck_table.setRowCount(0)
            self.dialog.blck_table.insertRow(0)
            self.dialog.blck_table.setItem(0, 0, QtWidgets.QTableWidgetItem('нет данных'))

        if silence_start != None and silence_start != 'нет данных' and silence_start != 'не найдено':
            self.create_slnc_table(file_path)
        elif silence_start == 'не найдено':
            self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.slnc_table.setRowCount(0)
            self.dialog.slnc_table.insertRow(0)
            self.dialog.slnc_table.setItem(0, 0, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.slnc_table.setRowCount(0)
            self.dialog.slnc_table.insertRow(0)
            self.dialog.slnc_table.setItem(0, 0, QtWidgets.QTableWidgetItem('нет данных'))
        if freeze_start != None and freeze_start != 'нет данных' and freeze_start != 'не найдено':
            self.create_freeze_table(file_path)
        elif freeze_start == 'не найдено':
            self.dialog.frz_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.frz_table.setRowCount(0)
            self.dialog.frz_table.insertRow(0)
            self.dialog.frz_table.setItem(0, 0, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.frz_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
            self.dialog.frz_table.setRowCount(0)
            self.dialog.frz_table.insertRow(0)
            self.dialog.frz_table.setItem(0, 0, QtWidgets.QTableWidgetItem('нет данных'))

    def create_blck_table(self, file_path):
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        black_start = Data().read_bd('black_start', file_path)
        black_start_list = ast.literal_eval(black_start)
        black_end = Data().read_bd('black_end', file_path)
        black_end_list = ast.literal_eval(black_end)
        black_duration = Data().read_bd('black_duration', file_path)
        black_duration_list = ast.literal_eval(black_duration)
        self.dialog.blck_table.setRowCount(0)
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = convert_fps(fps).split(' ')[0]
        for row in range(len(black_start_list)):
            self.dialog.blck_table.insertRow(row)
            black_start_item_tc = convert_duration_sec(float(black_start_list[row]), float(fps))
            black_end_item_tc = convert_duration_sec(float(black_end_list[row]), float(fps))
            black_duration_item_tc = convert_duration_sec(float(black_duration_list[row]), float(fps))
            black_start_item_ms = str(black_start_list[row])
            black_end_item_ms = str(black_end_list[row])

            self.dialog.blck_table.setItem(row, 0, QtWidgets.QTableWidgetItem(black_start_item_ms))
            self.dialog.blck_table.hideColumn(0)
            self.dialog.blck_table.setItem(row, 1, QtWidgets.QTableWidgetItem(black_start_item_tc))
            self.dialog.blck_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.blck_table.setColumnWidth(2, 5)
            self.dialog.blck_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.blck_table.setItem(row, 3, QtWidgets.QTableWidgetItem(black_end_item_ms))
            self.dialog.blck_table.hideColumn(3)
            self.dialog.blck_table.setItem(row, 4, QtWidgets.QTableWidgetItem(black_end_item_tc))
            self.dialog.blck_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.blck_table.setColumnWidth(5, 10)
            self.dialog.blck_table.setItem(row, 6, QtWidgets.QTableWidgetItem(black_duration_item_tc[-8:]))

    def create_slnc_table(self, file_path):
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        silence_start = Data().read_bd('silence_start', file_path)
        silence_start_list = ast.literal_eval(silence_start)
        silence_end = Data().read_bd('silence_end', file_path)
        silence_end_list = ast.literal_eval(silence_end)
        silence_duration = Data().read_bd('silence_duration', file_path)
        silence_duration_list = ast.literal_eval(silence_duration)
        self.dialog.slnc_table.setRowCount(0)
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = convert_fps(fps).split(' ')[0]
        # self.dialog.slnc_table.clearContents()
        for row in range(len(silence_start_list)):
            self.dialog.slnc_table.insertRow(row)
            silence_start_item_tc = convert_duration_sec(float(silence_start_list[row]), float(fps))
            silence_end_item_tc = convert_duration_sec(float(silence_end_list[row]), float(fps))
            silence_duration_item_tc = convert_duration_sec(float(silence_duration_list[row]), float(fps))
            silence_start_item_ms = str(silence_start_list[row])
            silence_end_item_ms = str(silence_end_list[row])
            self.dialog.slnc_table.setItem(row, 0, QtWidgets.QTableWidgetItem(silence_start_item_ms))
            self.dialog.slnc_table.hideColumn(0)
            self.dialog.slnc_table.setItem(row, 1, QtWidgets.QTableWidgetItem(silence_start_item_tc))
            self.dialog.slnc_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.slnc_table.setColumnWidth(2, 5)
            self.dialog.slnc_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.slnc_table.setItem(row, 3, QtWidgets.QTableWidgetItem(silence_end_item_ms))
            self.dialog.slnc_table.hideColumn(3)
            self.dialog.slnc_table.setItem(row, 4, QtWidgets.QTableWidgetItem(silence_end_item_tc))
            self.dialog.slnc_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.slnc_table.setColumnWidth(5, 10)
            self.dialog.slnc_table.setItem(row, 6, QtWidgets.QTableWidgetItem(silence_duration_item_tc[-8:]))

    def create_freeze_table(self, file_path):
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        freeze_start = Data().read_bd('freeze_start', file_path)
        freeze_start_list = ast.literal_eval(freeze_start)
        freeze_end = Data().read_bd('freeze_end', file_path)
        freeze_end_list = ast.literal_eval(freeze_end)
        freeze_duration = Data().read_bd('freeze_duration', file_path)
        freeze_duration_list = ast.literal_eval(freeze_duration)
        self.dialog.frz_table.setRowCount(0)
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = convert_fps(fps).split(' ')[0]
        # self.dialog.slnc_table.clearContents()
        for row in range(len(freeze_start_list) - 1):
            self.dialog.frz_table.insertRow(row)
            freeze_start_item_tc = convert_duration_sec(float(freeze_start_list[row]), float(fps))
            freeze_end_item_tc = convert_duration_sec(float(freeze_end_list[row]), float(fps))
            freeze_duration_item_tc = convert_duration_sec(float(freeze_duration_list[row]), float(fps))
            freeze_start_item_ms = str(freeze_start_list[row])
            freeze_end_item_ms = str(freeze_end_list[row])
            self.dialog.frz_table.setItem(row, 0, QtWidgets.QTableWidgetItem(freeze_start_item_ms))
            self.dialog.frz_table.hideColumn(0)
            self.dialog.frz_table.setItem(row, 1, QtWidgets.QTableWidgetItem(freeze_start_item_tc))
            self.dialog.frz_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.frz_table.setColumnWidth(2, 5)
            self.dialog.frz_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.frz_table.setItem(row, 3, QtWidgets.QTableWidgetItem(freeze_end_item_ms))
            self.dialog.frz_table.hideColumn(3)
            self.dialog.frz_table.setItem(row, 4, QtWidgets.QTableWidgetItem(freeze_end_item_tc))
            self.dialog.frz_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.frz_table.setColumnWidth(5, 10)
            self.dialog.frz_table.setItem(row, 6, QtWidgets.QTableWidgetItem(freeze_duration_item_tc[-8:]))

    def click_table_blck_detect(self):
        row_pos_blck_table = self.dialog.blck_table.currentRow()
        col_pos_blck_table = self.dialog.blck_table.currentColumn()
        try:
            value = self.dialog.blck_table.item(row_pos_blck_table, col_pos_blck_table - 1).text()
        except Exception:
            value = ''
        if value == ' ' or value == '-':
            tc = float(self.dialog.blck_table.item(row_pos_blck_table, 0).text()) * 1000
            self.play_video_tc(int(tc))
        if value == '':
            pass
        else:
            try:
                tc = float(value) * 1000
                self.play_video_tc(int(tc))

            except Exception:
                pass

    def click_table_slnc_detect(self):
        row_pos_slnc_table = self.dialog.slnc_table.currentRow()
        col_pos_slnc_table = self.dialog.slnc_table.currentColumn()
        try:
            value = self.dialog.slnc_table.item(row_pos_slnc_table, col_pos_slnc_table - 1).text()
        except Exception:
            value = ''
        if value == ' ' or value == '-':
            tc = float(self.dialog.slnc_table.item(row_pos_slnc_table, 0).text()) * 1000
            self.play_video_tc(int(tc))
        if value == '':
            pass
        else:
            try:
                tc = float(value) * 1000
                self.play_video_tc(int(tc))
            except Exception:
                pass

    def click_table_frz_detect(self):
        row_pos_frz_table = self.dialog.frz_table.currentRow()
        col_pos_frz_table = self.dialog.frz_table.currentColumn()
        try:
            value = self.dialog.frz_table.item(row_pos_frz_table, col_pos_frz_table - 1).text()
        except Exception:
            value = ''
        if value == ' ' or value == '-':
            tc = float(self.dialog.frz_table.item(row_pos_frz_table, 0).text()) * 1000
            self.play_video_tc(int(tc))
        if value == '':
            pass
        else:
            try:
                tc = float(value) * 1000
                self.play_video_tc(int(tc))
            except Exception:
                pass

    # def ffplay_ss(self, file_path, ss='00:00:00'):
    #     cmd = ['ffplay', '-ss', ss, '-i', file_path, '-x', '640', '-y', '360']
    #     print('cmd', cmd)
    #     subprocess.run(cmd)

    def video_player(self):
        self.videoOutput = QVideoWidget(self.dialog.video_player_img)
        self.videoOutput.resize(960, 540)
        self.player.setVideoOutput(self.videoOutput)
        self.videoOutput.show()
        self.positionSlider.show()
        self.positionSlider.updateGeometry()
        file_path = self.dialog.file_path.text()
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.read_marks()

    def play_video(self):
        self.player.play()

    def pause_video(self):
        pos = self.find_position()
        self.player.setPosition(pos)
        self.player.pause()

    def play_pause(self):
        # self.videoOutput.setFullScreen(True)
        # print(self.player.isPlaying())
        if not self.player.isPlaying():
            self.player.play()
            pause_icon = QIcon()
            pause_icon.addFile(u":/bl_img/icons/pause_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
            self.dialog.player_playButton.setIcon(pause_icon)
        else:
            self.player.pause()
            play_icon = QIcon()
            play_icon.addFile(u":/bl_img/icons/play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                              QIcon.Off)
            self.dialog.player_playButton.setIcon(play_icon)

    def play_pause_check(self):
        if self.player.isPlaying():
            pause_icon = QIcon()
            pause_icon.addFile(u":/bl_img/icons/pause_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal, QIcon.Off)
            self.dialog.player_playButton.setIcon(pause_icon)
        else:
            play_icon = QIcon()
            play_icon.addFile(u":/bl_img/icons/play_arrow_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                              QIcon.Off)
            self.dialog.player_playButton.setIcon(play_icon)

    def vol_mute(self):
        volume = self.audioOutput.volume()
        if volume > 0:
            self.audioOutput.setVolume(0)
            mute_icon = QIcon()
            mute_icon.addFile(u":/bl_img/icons/no_sound_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                              QIcon.Off)
            self.dialog.player_muteButton.setIcon(mute_icon)
        else:
            self.audioOutput.setVolume(0.5)
            vol_icon = QIcon()
            vol_icon.addFile(u":/bl_img/icons/volume_up_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                             QIcon.Off)
            self.dialog.player_muteButton.setIcon(vol_icon)

    def vol_mute_check(self):
        volume = self.audioOutput.volume()
        if not volume > 0:
            mute_icon = QIcon()
            mute_icon.addFile(u":/bl_img/icons/no_sound_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                              QIcon.Off)
            self.dialog.player_muteButton.setIcon(mute_icon)
        else:
            vol_icon = QIcon()
            vol_icon.addFile(u":/bl_img/icons/volume_up_FILL0_wght400_GRAD0_opsz24.svg", QSize(), QIcon.Normal,
                             QIcon.Off)
            self.dialog.player_muteButton.setIcon(vol_icon)

    def find_position(self):
        pos = self.player.position()
        return pos

    def play_video_tc(self, tc=0):
        self.player.play()
        self.player.setPosition(tc)
        self.play_pause_check()
        # self.videoOutput.setFullScreen(True)
        # print(self.player.isPlaying())
        # if self.player.isPlaying() == True:
        #     self.player.pause()
        #     self.is_paused = True
        #     print('playing')
        # else:
        #     # if self.mediaplayer.play() == -1:
        #     self.player.play()
        #     self.is_paused = False
        #     print('paused')

    # def play_pause(self):
    #     val = self.player.isPlaying()
    #     print('val', val)
    #     return val

    def full_screen(self):
        if self.videoOutput.isFullScreen():
            self.videoOutput.setFullScreen(False)
        else:
            self.videoOutput.setFullScreen(True)

    def prev_frame(self):
        file_path = self.dialog.file_path.text()
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = float(convert_fps(fps).split(' ')[0])
        pos = int(self.player.position())
        frame = int(1000 / fps)
        self.player.setPosition(pos - frame)
        self.player.pause()
        self.play_pause_check()

    def next_frame(self):
        file_path = self.dialog.file_path.text()
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = float(convert_fps(fps).split(' ')[0])
        pos = int(self.player.position())
        frame = int(1000 / fps)
        self.player.setPosition(pos + frame)
        self.player.pause()
        self.play_pause_check()

    def add_marks(self):
        row_position = self.dialog.tableMarks.rowCount()
        # self.dialog.tableMarks.setRowCount(row_position)
        self.dialog.tableMarks.insertRow(row_position)
        num = f'Mark {row_position + 1}'
        num_item = QTableWidgetItem()
        num_item.setData(Qt.EditRole, num)

        file_path = self.dialog.file_path.text()
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = float(convert_fps(fps).split(' ')[0])
        pos = self.player.position()

        pos_item = QTableWidgetItem()
        pos_item.setData(Qt.EditRole, pos)

        pos_tc = convert_duration_sec(pos / 1000, fps)
        pos_tc_item = QTableWidgetItem()
        pos_tc_item.setData(Qt.EditRole, pos_tc)

        mark = 'Введите описание'
        mark_item = QTableWidgetItem()
        mark_item.setData(Qt.EditRole, mark)

        # db_data = (num, tc, mark),
        # print(db_data)
        self.dialog.tableMarks.setItem(row_position, 0, pos_item)
        self.dialog.tableMarks.hideColumn(0)
        self.dialog.tableMarks.setItem(row_position, 1, pos_tc_item)
        self.dialog.tableMarks.setItem(row_position, 2, mark_item)
        self.dialog.tableMarks.setColumnWidth(1, 85)
        self.dialog.tableMarks.setColumnWidth(2, 690)
        self.dialog.tableMarks.sortByColumn(0, Qt.AscendingOrder)

    def read_marks(self):
        self.dialog.tableMarks.setRowCount(0)
        file_path = self.dialog.file_path.text()
        db_marks = Data().read_bd('marks', file_path)
        if db_marks != 'нет данных':
            for data in ast.literal_eval(db_marks):
                row_position = self.dialog.tableMarks.rowCount()
                self.dialog.tableMarks.insertRow(row_position)
                pos = int(data[0])
                pos_item = QTableWidgetItem()
                pos_item.setData(Qt.EditRole, pos)
                pos_tc = data[1]
                pos_tc_item = QTableWidgetItem()
                pos_tc_item.setData(Qt.EditRole, pos_tc)
                mark = data[2]
                mark_item = QTableWidgetItem()
                mark_item.setData(Qt.EditRole, mark)

                self.dialog.tableMarks.setItem(row_position, 0, pos_item)
                self.dialog.tableMarks.hideColumn(0)
                self.dialog.tableMarks.setItem(row_position, 1, pos_tc_item)
                self.dialog.tableMarks.setItem(row_position, 2, mark_item)
                self.dialog.tableMarks.setColumnWidth(1, 85)
                self.dialog.tableMarks.setColumnWidth(2, 690)
                self.dialog.tableMarks.sortByColumn(0, Qt.AscendingOrder)

        # row_pos_blck_table = self.dialog.blck_table.currentRow()
        # col_pos_blck_table = self.dialog.blck_table.currentColumn()

    def add_marks_db(self):
        rows = self.dialog.tableMarks.rowCount()
        db_data = ()
        for row in range(rows):
            pos = self.dialog.tableMarks.item(row, 0).text()
            pos_tc = self.dialog.tableMarks.item(row, 1).text()
            mark = self.dialog.tableMarks.item(row, 2).text()
            data = (pos, pos_tc, mark),
            db_data += data
        file_path = self.dialog.file_path.text()
        Data().add_data('marks', db_data, file_path)

    def del_mark(self):
        row = self.dialog.tableMarks.currentRow()
        self.dialog.tableMarks.removeRow(row)

    def prev_mark(self):
        row = self.dialog.tableMarks.currentRow()
        self.dialog.tableMarks.selectRow(row - 1)
        sel_row = self.dialog.tableMarks.currentRow()
        mrk_pos = self.dialog.tableMarks.item(sel_row, 0).text()
        self.player.setPosition(int(mrk_pos))

    def next_mark(self):
        row = self.dialog.tableMarks.currentRow()
        self.dialog.tableMarks.selectRow(row + 1)
        sel_row = self.dialog.tableMarks.currentRow()
        mrk_pos = self.dialog.tableMarks.item(sel_row, 0).text()
        self.player.setPosition(int(mrk_pos))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

        file_path = self.dialog.file_path.text()
        fps = Data().read_bd('V01_r_frame_rate', file_path)
        fps = float(convert_fps(fps).split(' ')[0])

        pos = convert_duration_sec(float(self.player.position() / 1000), float(fps))
        dur = convert_duration_sec(float(self.player.duration() / 1000), float(fps))
        pos_dur = f'{pos} / {dur}'
        self.dialog.pos_dur_tc.setText(pos_dur)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.player.setPosition(position)

    def volumeChanged(self, volume):
        # volume = self.volumeslider.value()
        self.audioOutput.setVolume(volume / 100)
        self.vol_mute_check()

    # def set_volume(self, volume):
    #     self.mediaplayer.audio_set_volume(volume)

    # headers = ['Start', 'End', 'Duration']
    # headers = ['silence_start', 'silence_end', 'silence_duration']
    # # self.dialog.blck_table.insertRow(row_position)
    # col = 0
    # insert = True
    # for header in headers:
    #     # print('row_position', row_position)
    #     # self.dialog.blck_table.setRowCount(row_position)
    #     # print(header)
    #     row_position = 0
    #     db_data = Data().read_bd(header, file_path)
    #     if db_data != None and db_data != 'нет данных':
    #         data_list = ast.literal_eval(db_data)
    #         for data in data_list:
    #             # print(data_list)
    #             # print('header:', header)
    #             # print('data:', data)
    #             if insert is True:
    #                 self.dialog.slnc_table.insertRow(row_position)
    #             # self.dialog.blck_table.setColumnWidth(0, 120)
    #             # self.dialog.blck_table.setColumnWidth(1, 220)
    #             # self.dialog.blck_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(header))
    #             # self.ui.tableWidget_02.item(row_position, 0).setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
    #             self.dialog.slnc_table.setItem(row_position, col, QtWidgets.QTableWidgetItem(data))
    #             # self.dialog.slnc_table.item(row_position, col).setBackground(QColor(30, 30, 30))
    #             row_position += 1
    #             # print('row_position:', row_position)
    #     insert = False
    #     col += 1
    # print('col:', col)

    # file_name = os.path.basename(file_path)
    # image_file = f'{file_name}_WAVE.png'
    # # os.path.splitext()
    # cmd = [
    #     'ffmpeg',
    #     '-i', file_path,
    #     '-filter_complex', 'showwavespic=s=1500x800:scale=cbrt:draw=full',
    #     '-frames:v', '1',
    #     '-y',
    #     image_file
    # ]
    # subprocess.run(cmd)
    # print('Создание', image_file, 'успешно завершено')

    def click(self):
        print('click')

    # def search(self, s):
    #     """
    #     Поиск документов в таблице.
    #     :param s: Вводимый текст в строке поиска.
    #     """
    #     self.ui.docTable.setCurrentItem(None)
    #     if not s:
    #         return
    #     matching_items = self.ui.docTable.findItems(s, Qt.MatchContains)
    #     if matching_items:
    #         for item in matching_items:
    #             item.setSelected(True)
    # def mouseDoubleClickEvent(self, event):
    #     QMediaPlayer(self.videoOutput)
    #     if self.videoOutput.isFullScreen():
    #         print('test')

    def closeEvent(self, event):
        print('Завершение')
        # Переопределить colseEvent
        # message = QMessageBox()
        # reply = QMessageBox.question(self, 'Закрытие приложения', "Вы уверены, что хотите уйти?",
        #                              QMessageBox.Yes, QMessageBox.No)
        #
        # # QMessageBox.setStyleSheet(self, "QPushButton {color: white; background-color: rgba(255,255,255,30);"
        # #                                    "border: 1px solid rgba(255,255,255,40); border-radius:3px;}"
        # #                                    "QPushButton:hover {background-color:rgba(255,255,255,50);}"
        # #                                    "QPushButton:pressed {background-color:rgba(255,255,255,70);}")
        # # effect = QGraphicsDropShadowEffect()
        # # effect.setOffset(20, 20)
        #
        # if reply == QMessageBox.Yes:
        #     event.accept()
        # else:
        #     event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    # qdarktheme.setup_theme(custom_colors={"primary": "#D0BCFF"})
    window = VideoInfo()
    window.show()
    sys.exit(app.exec())
