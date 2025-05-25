import os
import subprocess

from PySide6.QtGui import QIcon, qRgb
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QSlider, QHeaderView, QTableWidgetItem, QGraphicsColorizeEffect, QWidget
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, QUrl

from forms.ui_videoinfo_player import Ui_VideoINFO_Player
from mongo_connection import MongoDB


def convert_duration_sec(data, fps=25):
    print('data', type(data), data)
    hh = int(data // 3600)
    mm = int((data % 3600) // 60)
    ss = int((data % 3600) % 60 // 1)
    ff = int(data % 1 * fps)
    return f'{hh:02}:{mm:02}:{ss:02}.{ff:02}'

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


class VideoInfoPlayer(QWidget):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.vinfo_player = QtWidgets.QDialog()
        self.dialog = Ui_VideoINFO_Player()
        self.dialog.setupUi(self.vinfo_player)
        self.dialog.file_path.setText(file_path)

        self.mongo = MongoDB()


        self.dialog.player_openButton.clicked.connect(self.open_folder_video_player)
        self.dialog.player_prev_fr_Button.clicked.connect(self.prev_frame)
        self.dialog.player_prev_mark_Button.clicked.connect(self.prev_mark)
        self.dialog.player_playButton.clicked.connect(self.play_pause)
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
        self.show_tables()
        self.video_player()

    def scanners_info(self):
        file_info = self.mongo.find_file(self.file_path)
        ffmpeg_scanners = file_info.get('ffmpeg_scanners')
        black_screen = ffmpeg_scanners.get('black_screen')
        silence = ffmpeg_scanners.get('silence')
        freeze = ffmpeg_scanners.get('freeze')
        return black_screen, silence, freeze

    def fps_info(self):
        file_info = self.mongo.find_file(self.file_path)
        streams = file_info.get('streams')
        video = list(filter(lambda x: x.get('codec_type') == 'video', streams))
        format = file_info.get('format')
        v_frame_rate = video[0].get('r_frame_rate')
        f_frame_rate = format.get('r_frame_rate')
        if f_frame_rate:
            return f_frame_rate
        else:
            return v_frame_rate

    def markers_info(self):
        file_info = self.mongo.find_file(self.file_path)
        return file_info.get('markers')

    def colorizeEffect_wt(self, button):
        pass
        # color = QGraphicsColorizeEffect(self)
        # color.setColor(Qt.white)
        # button.setGraphicsEffect(color)

    def colorizeEffect_gr(self, button):
        pass
        # color = QGraphicsColorizeEffect(self)
        # color.setColor(qRgb(80, 80, 80))
        # button.setGraphicsEffect(color)

    def show_tables(self):
        self.vinfo_player.show()
        black_screen, silence, freeze = self.scanners_info()
        if black_screen:
            self.create_blck_table()
        elif black_screen == 'не найдено':
            self.dialog.blck_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.blck_table.setRowCount(0)
            self.dialog.blck_table.insertRow(0)
            self.dialog.blck_table.setItem(0, 1, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.blck_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.blck_table.setRowCount(0)
            self.dialog.blck_table.insertRow(0)
            self.dialog.blck_table.setItem(0, 1, QtWidgets.QTableWidgetItem('нет данных'))

        if silence:
            self.create_slnc_table()
        elif silence == 'не найдено':
            self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.slnc_table.setRowCount(0)
            self.dialog.slnc_table.insertRow(0)
            self.dialog.slnc_table.setItem(0, 1, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.slnc_table.setRowCount(0)
            self.dialog.slnc_table.insertRow(0)
            self.dialog.slnc_table.setItem(0, 1, QtWidgets.QTableWidgetItem('нет данных'))
        if freeze:
            self.create_freeze_table()
        elif freeze == 'не найдено':
            self.dialog.frz_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.frz_table.setRowCount(0)
            self.dialog.frz_table.insertRow(0)
            self.dialog.frz_table.setItem(0, 1, QtWidgets.QTableWidgetItem('не найдено'))
        else:
            self.dialog.frz_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
            self.dialog.frz_table.setRowCount(0)
            self.dialog.frz_table.insertRow(0)
            self.dialog.frz_table.setItem(0, 1, QtWidgets.QTableWidgetItem('нет данных'))

    def open_folder_video_player(self):
        file_path = self.dialog.file_path.text()
        subprocess.Popen(fr'explorer /select,"{os.path.abspath(file_path)}"')

    def create_blck_table(self):
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.blck_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        black_screen, silence, freeze = self.scanners_info()
        # if self.selected_db == 'SQLITE':
        #     black_start = DataLite().read_bd(tbl_name, 'black_start', self.file_path)
        #     black_start_list = ast.literal_eval(black_start)
        #     black_end = DataLite().read_bd(tbl_name, 'black_end', self.file_path)
        #     black_end_list = ast.literal_eval(black_end)
        #     black_duration = DataLite().read_bd(tbl_name, 'black_duration', self.file_path)
        #     black_duration_list = ast.literal_eval(black_duration)
        #     fps = DataLite().read_bd(tbl_name, 'V01_r_frame_rate', self.file_path)
        # else:
        #     black_start = DataPos().read_bd(tbl_name, 'black_start', self.file_path)
        #     black_start_list = ast.literal_eval(black_start)
        #     black_end = DataPos().read_bd(tbl_name, 'black_end', self.file_path)
        #     black_end_list = ast.literal_eval(black_end)
        #     black_duration = DataPos().read_bd(tbl_name, 'black_duration', self.file_path)
        #     black_duration_list = ast.literal_eval(black_duration)
        #     fps = DataPos().read_bd(tbl_name, 'V01_r_frame_rate', self.file_path)
        fps = convert_fps(self.fps_info())
        self.dialog.blck_table.setRowCount(0)
        for row, black_tc in enumerate(black_screen):
            self.dialog.blck_table.insertRow(row)
            # black_start_item_tc = convert_duration(float(black_start_list[row]), float(fps))
            # black_end_item_tc = convert_duration(float(black_end_list[row]), float(fps))
            # black_duration_item_tc = convert_duration(float(black_duration_list[row]), float(fps))
            # black_start_item_ms = str(black_start_list[row])
            # black_end_item_ms = str(black_end_list[row])

            self.dialog.blck_table.setItem(row, 0, QtWidgets.QTableWidgetItem(black_tc.get('start'))) #ms
            self.dialog.blck_table.hideColumn(0)
            self.dialog.blck_table.setItem(row, 1, QtWidgets.QTableWidgetItem(black_tc.get('start'))) #tc
            self.dialog.blck_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.blck_table.setColumnWidth(2, 5)
            self.dialog.blck_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.blck_table.setItem(row, 3, QtWidgets.QTableWidgetItem(black_tc.get('end'))) #ms
            self.dialog.blck_table.hideColumn(3)
            self.dialog.blck_table.setItem(row, 4, QtWidgets.QTableWidgetItem(black_tc.get('end'))) #tc
            self.dialog.blck_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.blck_table.setColumnWidth(5, 10)
            self.dialog.blck_table.setItem(row, 6, QtWidgets.QTableWidgetItem(black_tc.get('duration')))

    def create_slnc_table(self):
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.slnc_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        black_screen, silence, freeze = self.scanners_info()
        # if self.selected_db == 'SQLITE':
        #     silence_start = DataLite().read_bd(tbl_name, 'silence_start', self.file_path)
        #     silence_start_list = ast.literal_eval(silence_start)
        #     silence_end = DataLite().read_bd(tbl_name, 'silence_end', self.file_path)
        #     silence_end_list = ast.literal_eval(silence_end)
        #     silence_duration = DataLite().read_bd(tbl_name, 'silence_duration', self.file_path)
        #     silence_duration_list = ast.literal_eval(silence_duration)
        #     fps = DataLite().read_bd(tbl_name, 'v01_r_frame_rate', self.file_path)
        # else:
        #     silence_start = DataPos().read_bd(tbl_name, 'silence_start', self.file_path)
        #     silence_start_list = ast.literal_eval(silence_start)
        #     silence_end = DataPos().read_bd(tbl_name, 'silence_end', self.file_path)
        #     silence_end_list = ast.literal_eval(silence_end)
        #     silence_duration = DataPos().read_bd(tbl_name, 'silence_duration', self.file_path)
        #     silence_duration_list = ast.literal_eval(silence_duration)
        #     fps = DataPos().read_bd(tbl_name, 'v01_r_frame_rate', self.file_path)
        fps = convert_fps(self.fps_info())
        self.dialog.slnc_table.setRowCount(0)
        # self.dialog.slnc_table.clearContents()
        for row, silence_tc in enumerate(silence):
            self.dialog.slnc_table.insertRow(row)
            # silence_start_item_tc = convert_duration(float(silence_start_list[row]), float(fps))
            # silence_end_item_tc = convert_duration(float(silence_end_list[row]), float(fps))
            # silence_duration_item_tc = convert_duration(float(silence_duration_list[row]), float(fps))
            # silence_start_item_ms = str(silence_start_list[row])
            # silence_end_item_ms = str(silence_end_list[row])
            self.dialog.slnc_table.setItem(row, 0, QtWidgets.QTableWidgetItem(silence_tc.get('start')))
            self.dialog.slnc_table.hideColumn(0)
            self.dialog.slnc_table.setItem(row, 1, QtWidgets.QTableWidgetItem(silence_tc.get('start')))
            self.dialog.slnc_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.slnc_table.setColumnWidth(2, 5)
            self.dialog.slnc_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.slnc_table.setItem(row, 3, QtWidgets.QTableWidgetItem(silence_tc.get('end')))
            self.dialog.slnc_table.hideColumn(3)
            self.dialog.slnc_table.setItem(row, 4, QtWidgets.QTableWidgetItem(silence_tc.get('end')))
            self.dialog.slnc_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.slnc_table.setColumnWidth(5, 10)
            self.dialog.slnc_table.setItem(row, 6, QtWidgets.QTableWidgetItem(silence_tc.get('duration')))

    def create_freeze_table(self):
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.dialog.frz_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        black_screen, silence, freeze = self.scanners_info()
        # if self.selected_db == 'SQLITE':
        #     freeze_start = DataLite().read_bd(tbl_name, 'freeze_start', self.file_path)
        #     freeze_start_list = ast.literal_eval(freeze_start)
        #     freeze_end = DataLite().read_bd(tbl_name, 'freeze_end', self.file_path)
        #     freeze_end_list = ast.literal_eval(freeze_end)
        #     freeze_duration = DataLite().read_bd(tbl_name, 'freeze_duration', self.file_path)
        #     freeze_duration_list = ast.literal_eval(freeze_duration)
        #     fps = DataLite().read_bd(tbl_name, 'v01_r_frame_rate', self.file_path)
        # else:
        #     freeze_start = DataPos().read_bd(tbl_name, 'freeze_start', self.file_path)
        #     freeze_start_list = ast.literal_eval(freeze_start)
        #     freeze_end = DataPos().read_bd(tbl_name, 'freeze_end', self.file_path)
        #     freeze_end_list = ast.literal_eval(freeze_end)
        #     freeze_duration = DataPos().read_bd(tbl_name, 'freeze_duration', self.file_path)
        #     freeze_duration_list = ast.literal_eval(freeze_duration)
        #     fps = DataPos().read_bd(tbl_name, 'v01_r_frame_rate', self.file_path)
        fps = convert_fps(self.fps_info())
        self.dialog.frz_table.setRowCount(0)
        # self.dialog.slnc_table.clearContents()
        for row, freeze_tc in enumerate(freeze):
            self.dialog.frz_table.insertRow(row)
            # freeze_start_item_tc = convert_duration(float(freeze_start_list[row]), float(fps))
            # freeze_end_item_tc = convert_duration(float(freeze_end_list[row]), float(fps))
            # freeze_duration_item_tc = convert_duration(float(freeze_duration_list[row]), float(fps))
            # freeze_start_item_ms = str(freeze_start_list[row])
            # freeze_end_item_ms = str(freeze_end_list[row])
            self.dialog.frz_table.setItem(row, 0, QtWidgets.QTableWidgetItem(freeze_tc.get('start')))
            self.dialog.frz_table.hideColumn(0)
            self.dialog.frz_table.setItem(row, 1, QtWidgets.QTableWidgetItem(freeze_tc.get('start')))
            self.dialog.frz_table.setItem(row, 2, QtWidgets.QTableWidgetItem('-'))
            self.dialog.frz_table.setColumnWidth(2, 5)
            self.dialog.frz_table.item(row, 2).setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
            self.dialog.frz_table.setItem(row, 3, QtWidgets.QTableWidgetItem(freeze_tc.get('end')))
            self.dialog.frz_table.hideColumn(3)
            self.dialog.frz_table.setItem(row, 4, QtWidgets.QTableWidgetItem(freeze_tc.get('end')))
            self.dialog.frz_table.setItem(row, 5, QtWidgets.QTableWidgetItem(' '))
            self.dialog.frz_table.setColumnWidth(5, 10)
            self.dialog.frz_table.setItem(row, 6, QtWidgets.QTableWidgetItem(freeze_tc.get('duration')))

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

    def video_player(self):
        self.videoOutput = QVideoWidget(self.dialog.video_player_img)
        self.videoOutput.resize(960, 540)
        self.play_pause_check()
        self.player.setVideoOutput(self.videoOutput)
        self.player.setSource(QUrl.fromLocalFile(self.file_path))
        self.videoOutput.show()
        self.positionSlider.show()
        self.positionSlider.updateGeometry()
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

    def full_screen(self):
        if self.videoOutput.isFullScreen():
            self.videoOutput.setFullScreen(False)
        else:
            self.videoOutput.setFullScreen(True)

    def prev_frame(self):
        fps = self.fps_info()
        pos = int(self.player.position())
        frame = int(1000 / fps)
        self.player.setPosition(pos - frame)
        self.player.pause()
        self.play_pause_check()

    def next_frame(self):
        try:
            fps = eval(self.fps_info())
            pos = int(self.player.position())
            frame = int(1000 / fps)
            self.player.setPosition(pos + frame)
            self.player.pause()
            self.play_pause_check()
        except Exception as e:
            print(e)

    def add_marks(self):
        row_position = self.dialog.tableMarks.rowCount()
        # self.dialog.tableMarks.setRowCount(row_position)
        self.dialog.tableMarks.insertRow(row_position)
        num = f'Mark {row_position + 1}'
        num_item = QTableWidgetItem()
        num_item.setData(Qt.EditRole, num)

        fps = self.fps_info()
        pos = self.player.position()

        pos_item = QTableWidgetItem()
        pos_item.setData(Qt.EditRole, pos)

        pos_tc = convert_duration(pos / 1000, fps)
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
        # if self.selected_db == 'SQLITE':
        #     db_marks = DataLite().read_bd(self.read_tbl_name(), 'marks', self.file_path)
        # else:
        #     db_marks = DataPos().read_bd(self.read_tbl_name(), 'marks', self.file_path)
        db_marks = self.markers_info()
        # db_marks = {[sec, tc, mark],}
        if db_marks:
            for sec, tc, mark in db_marks:
                row_position = self.dialog.tableMarks.rowCount()
                self.dialog.tableMarks.insertRow(row_position)
                sec_item = QTableWidgetItem()
                sec_item.setData(Qt.EditRole, sec)
                tc_item = QTableWidgetItem()
                tc_item.setData(Qt.EditRole, tc)
                mark_item = QTableWidgetItem()
                mark_item.setData(Qt.EditRole, mark)

                self.dialog.tableMarks.setItem(row_position, 0, sec_item)
                self.dialog.tableMarks.hideColumn(0)
                self.dialog.tableMarks.setItem(row_position, 1, tc_item)
                self.dialog.tableMarks.setItem(row_position, 2, mark_item)
                self.dialog.tableMarks.setColumnWidth(1, 85)
                self.dialog.tableMarks.setColumnWidth(2, 690)
                self.dialog.tableMarks.sortByColumn(0, Qt.AscendingOrder)


    def add_marks_db(self):
        rows = self.dialog.tableMarks.rowCount()
        markers = []
        for row in range(rows):
            sec = self.dialog.tableMarks.item(row, 0).text()
            tc = self.dialog.tableMarks.item(row, 1).text()
            mark = self.dialog.tableMarks.item(row, 2).text()
            markers.append([sec, tc, mark])
        self.mongo.update_file_info(self.file_path, {'markers': markers})

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

        fps = self.fps_info()

        pos = convert_duration(float(self.player.position() / 1000), fps)
        dur = convert_duration(float(self.player.duration() / 1000), fps)
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

    def closeEvent(self, event):
        self.player.stop()
        print('Stop')
        event.accept()