import ast
import configparser
import os

from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QFileDialog

from forms.ui_settings import Ui_Settings

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QtWidgets.QDialog()
        self.ui_set = Ui_Settings()
        self.ui_set.setupUi(self.settings)
        self.ui_set.saveButton_main.clicked.connect(self.save_butt_settings)
        self.ui_set.cancelButton_main.clicked.connect(self.cancel_butt_settings)
        self.ui_set.blackCheckBox.clicked.connect(self.black_detect_update_settings)
        self.ui_set.silenceCheckBox.clicked.connect(self.silence_detect_update_settings)
        self.ui_set.freezeCheckBox.clicked.connect(self.freeze_detect_update_settings)
        self.ui_set.chck_con_posql_Button.clicked.connect(self.check_connection_posql_db)
        self.ui_set.chck_con_sqlite_Button.clicked.connect(self.check_connection_sqlite_db)
        self.ui_set.blck_tc_in.setInputMask('00:00:00')
        self.ui_set.blck_tc_out.setInputMask('00:00:00')
        self.ui_set.slnc_noize_txt.setInputMask('-000')
        self.ui_set.slnc_tc_in.setInputMask('00:00:00')
        self.ui_set.slnc_tc_out.setInputMask('00:00:00')
        self.ui_set.frz_noize_txt.setInputMask('-000')
        self.ui_set.frz_tc_in.setInputMask('00:00:00')
        self.ui_set.frz_tc_out.setInputMask('00:00:00')

        self.ui_set.db_posql_host.setInputMask('000.000.000.000')

        settings_directory = os.path.join(PARENT_DIRECTORY, 'config')
        self.settings_name = os.path.join(settings_directory, 'settings.ini')
        self.config = configparser.ConfigParser()
        self.config.read(self.settings_name)
        self.base_settings_main()
        self.base_settings_damage()
        self.base_settings_db()

    def open_settings_window(self):
        self.save_temp_settings_main()
        self.save_temp_settings_damage()
        self.save_temp_settings_db()
        self.settings.show()

    def values_damage(self):
        v_slnc_dur = self.ui_set.slnc_dur_txt.text()
        v_slnc_noize = self.ui_set.slnc_noize_txt.text()
        v_slnc_tc_in = self.ui_set.slnc_tc_in.text()
        v_slnc_tc_out = self.ui_set.slnc_tc_out.text()

        v_frz_dur = self.ui_set.frz_dur_txt.text()
        v_frz_noize = self.ui_set.frz_noize_txt.text()
        v_frz_tc_in = self.ui_set.frz_tc_in.text()
        v_frz_tc_out = self.ui_set.frz_tc_out.text()

    def black_detect_update_settings(self):
        if self.ui_set.blackCheckBox.isChecked():
            self.ui_set.blck_tc_in.setText('00:00:00')
            self.ui_set.blck_tc_in.setEnabled(False)
            self.ui_set.blck_tc_in.setStyleSheet('color:grey')
            self.ui_set.blck_out_label.setText('Until out')
        else:
            self.ui_set.blck_tc_in.setEnabled(True)
            self.ui_set.blck_tc_in.setStyleSheet('color:white')
            self.ui_set.blck_out_label.setText('Out')

    def silence_detect_update_settings(self):
        if self.ui_set.silenceCheckBox.isChecked():
            self.ui_set.slnc_tc_in.setText('00:00:00')
            self.ui_set.slnc_tc_in.setEnabled(False)
            self.ui_set.slnc_tc_in.setStyleSheet('color:grey')
            self.ui_set.slnc_out_label.setText('Until out')
        else:
            self.ui_set.slnc_tc_in.setEnabled(True)
            self.ui_set.slnc_tc_in.setStyleSheet('color:white')
            self.ui_set.slnc_out_label.setText('Out')

    def freeze_detect_update_settings(self):
        if self.ui_set.freezeCheckBox.isChecked():
            self.ui_set.frz_tc_in.setText('00:00:00')
            self.ui_set.frz_tc_in.setEnabled(False)
            self.ui_set.frz_tc_in.setStyleSheet('color:grey')
            self.ui_set.frz_out_label.setText('Until out')
        else:
            self.ui_set.frz_tc_in.setEnabled(True)
            self.ui_set.frz_tc_in.setStyleSheet('color:white')
            self.ui_set.frz_out_label.setText('Out')

    def check_connection_posql_db(self):
        self.save_temp_settings_db()
        # self.ui_set.chck_con_posql_label.setText(DataPos().check_connect())

    def check_connection_sqlite_db(self):
        self.save_temp_settings_db()
        # self.ui_set.chck_con_sqlite_label.setText(DataLite().check_connect())

    def save_butt_settings(self):
        self.save_temp_settings_main()
        self.save_temp_settings_damage()
        self.save_temp_settings_db()
        # VideoInfo().error_highlight()
        self.settings.close()

    def cancel_butt_settings(self):
        self.base_settings_main()
        self.base_settings_damage()
        self.base_settings_db()
        # self.call_temp_settings_main()
        # self.call_temp_settings_damage()
        # VideoInfo().error_highlight()
        self.settings.close()

    def base_settings_db(self):
        self.ui_set.db_posql_host.setText(self.config['Posql']['host'])
        self.ui_set.db_posql_dbname.setText(self.config['Posql']['database'])
        self.ui_set.db_posql_user.setText(self.config['Posql']['user'])
        self.ui_set.db_posql_password.setText(self.config['Posql']['password'])
        self.ui_set.db_posql_port.setText(self.config['Posql']['port'])
        self.ui_set.db_sqlite_dbname.setText(self.config['Sqlite']['database'])

    def save_temp_settings_db(self):
        self.config['Posql']['host'] = self.ui_set.db_posql_host.text()
        self.config['Posql']['database'] = self.ui_set.db_posql_dbname.text()
        self.config['Posql']['user'] = self.ui_set.db_posql_user.text()
        self.config['Posql']['password'] = self.ui_set.db_posql_password.text()
        self.config['Posql']['port'] = self.ui_set.db_posql_port.text()

        self.config['Sqlite']['database'] = self.ui_set.db_sqlite_dbname.text()
        self.write_config()

    def read_config(self, sect, key):
        return self.config[sect][key]

    def write_config(self):
        with open(self.settings_name, 'w') as configfile:
            self.config.write(configfile)

    def base_settings_main(self):
        self.ui_set.presetComboBox.addItems(ast.literal_eval(self.config['Presets']['name_combobox']))
        self.ui_set.presetComboBox.setCurrentText(self.config['Presets']['name'])
        self.ui_set.presetComboBox.setStyleSheet('color:grey')
        self.ui_set.codec_txt.setText(self.config['Video_standard']['codec'])
        self.ui_set.width_txt.setText(self.config['Video_standard']['width'])
        self.ui_set.height_txt.setText(self.config['Video_standard']['height'])
        self.ui_set.v_bit_rate_txt.setText(self.config['Video_standard']['v_bit_rate'])
        self.ui_set.frame_rate_comboBox.addItems(ast.literal_eval(self.config['Video_standard']['frame_rate_comboBox']))
        self.ui_set.frame_rate_comboBox.setCurrentText(self.config['Video_standard']['frame_rate'])
        self.ui_set.dar_comboBox.addItems(ast.literal_eval(self.config['Video_standard']['dar_combobox']))
        self.ui_set.dar_comboBox.setCurrentText(self.config['Video_standard']['dar'])
        self.ui_set.codec_aud_txt.setText(self.config['Audio_standard']['codec_aud'])
        self.ui_set.channels_txt.setText(self.config['Audio_standard']['channels'])
        self.ui_set.sample_rate_comboBox.addItems(ast.literal_eval(self.config['Audio_standard']['sample_rate_combobox']))
        self.ui_set.sample_rate_comboBox.setCurrentText(self.config['Audio_standard']['sample_rate'])
        self.ui_set.a_bit_rate_txt.setText(self.config['Audio_standard']['a_bit_rate'])

        self.ui_set.r128_i_txt.setText(self.config['Loudness_meter']['r128_i'])
        self.ui_set.r128_lra_txt.setText(self.config['Loudness_meter']['r128_lra'])
        self.ui_set.r128_tp_txt.setText(self.config['Loudness_meter']['r128_tp'])
        self.ui_set.r128_thr_txt.setText(self.config['Loudness_meter']['r128_thr'])

    def base_settings_damage(self):
        self.ui_set.blackCheckBox.setChecked(eval(self.config['Damage_test_black']['checkbox']))
        self.ui_set.blck_dur_txt.setText(self.config['Damage_test_black']['blck_dur'])
        self.ui_set.blck_thr_txt.setText(self.config['Damage_test_black']['blck_thr'])
        self.ui_set.blck_tc_in.setText(self.config['Damage_test_black']['blck_tc_in'])
        self.ui_set.blck_tc_out.setText(self.config['Damage_test_black']['blck_tc_out'])

        self.ui_set.silenceCheckBox.setChecked(eval(self.config['Damage_test_silence']['checkbox']))
        self.ui_set.slnc_dur_txt.setText(self.config['Damage_test_silence']['slnc_dur'])
        self.ui_set.slnc_noize_txt.setText(self.config['Damage_test_silence']['slnc_noize'])
        self.ui_set.slnc_tc_in.setText(self.config['Damage_test_silence']['slnc_tc_in'])
        self.ui_set.slnc_tc_out.setText(self.config['Damage_test_silence']['slnc_tc_out'])

        self.ui_set.freezeCheckBox.setChecked(eval(self.config['Damage_test_freeze']['checkbox']))
        self.ui_set.frz_dur_txt.setText(self.config['Damage_test_freeze']['frz_dur'])
        self.ui_set.frz_noize_txt.setText(self.config['Damage_test_freeze']['frz_noize'])
        self.ui_set.frz_tc_in.setText(self.config['Damage_test_freeze']['frz_tc_in'])
        self.ui_set.frz_tc_out.setText(self.config['Damage_test_freeze']['frz_tc_out'])

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
        self.ui_set.blackCheckBox.isChecked()
        self.ui_set.blck_dur_txt.text()
        self.ui_set.blck_thr_txt.text()
        self.ui_set.blck_tc_in.text()
        self.ui_set.blck_tc_out.text()

        self.ui_set.silenceCheckBox.isChecked()
        self.ui_set.slnc_dur_txt.text()
        self.ui_set.slnc_noize_txt.text()
        self.ui_set.slnc_tc_in.text()
        self.ui_set.slnc_tc_out.text()

        self.ui_set.freezeCheckBox.isChecked()
        self.ui_set.frz_dur_txt.text()
        self.ui_set.frz_noize_txt.text()
        self.ui_set.frz_tc_in.text()
        self.ui_set.frz_tc_out.text()
        self.settings.close()

    def save_temp_settings_main(self):
        self.config['Video_standard']['codec'] = self.ui_set.codec_txt.text()
        self.config['Video_standard']['width'] = self.ui_set.width_txt.text()
        self.config['Video_standard']['height'] = self.ui_set.height_txt.text()
        self.config['Video_standard']['v_bit_rate'] = self.ui_set.v_bit_rate_txt.text()
        self.config['Video_standard']['frame_rate'] = self.ui_set.frame_rate_comboBox.currentText()
        self.config['Video_standard']['dar'] = self.ui_set.dar_comboBox.currentText()
        self.config['Audio_standard']['codec_aud'] = self.ui_set.codec_aud_txt.text()
        self.config['Audio_standard']['channels'] = self.ui_set.channels_txt.text()
        self.config['Audio_standard']['sample_rate'] = self.ui_set.sample_rate_comboBox.currentText()
        self.config['Audio_standard']['a_bit_rate'] = self.ui_set.a_bit_rate_txt.text()

        self.config['Loudness_meter']['r128_i'] = self.ui_set.r128_i_txt.text()
        self.config['Loudness_meter']['r128_lra'] = self.ui_set.r128_lra_txt.text()
        self.config['Loudness_meter']['r128_tp'] = self.ui_set.r128_tp_txt.text()
        self.config['Loudness_meter']['r128_thr'] = self.ui_set.r128_thr_txt.text()

        self.write_config()

    def save_temp_settings_damage(self):
        self.config['Damage_test_black']['checkbox'] = str(self.ui_set.blackCheckBox.isChecked())
        self.config['Damage_test_black']['blck_dur'] = self.ui_set.blck_dur_txt.text()
        self.config['Damage_test_black']['blck_thr'] = self.ui_set.blck_thr_txt.text()
        self.config['Damage_test_black']['blck_tc_in'] = self.ui_set.blck_tc_in.text()
        self.config['Damage_test_black']['blck_tc_out'] = self.ui_set.blck_tc_out.text()

        self.config['Damage_test_silence']['checkbox'] = str(self.ui_set.silenceCheckBox.isChecked())
        self.config['Damage_test_silence']['slnc_dur'] = self.ui_set.slnc_dur_txt.text()
        self.config['Damage_test_silence']['slnc_noize'] = self.ui_set.slnc_noize_txt.text()
        self.config['Damage_test_silence']['slnc_tc_in'] = self.ui_set.slnc_tc_in.text()
        self.config['Damage_test_silence']['slnc_tc_out'] = self.ui_set.slnc_tc_out.text()

        self.config['Damage_test_freeze']['checkbox'] = str(self.ui_set.freezeCheckBox.isChecked())
        self.config['Damage_test_freeze']['frz_dur'] = self.ui_set.frz_dur_txt.text()
        self.config['Damage_test_freeze']['frz_noize'] = self.ui_set.frz_noize_txt.text()
        self.config['Damage_test_freeze']['frz_tc_in'] = self.ui_set.frz_tc_in.text()
        self.config['Damage_test_freeze']['frz_tc_out'] = self.ui_set.frz_tc_out.text()

        self.write_config()