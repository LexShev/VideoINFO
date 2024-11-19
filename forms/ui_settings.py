# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_settings.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QToolBox, QVBoxLayout, QWidget)

class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName(u"Settings")
        Settings.resize(680, 805)
        Settings.setStyleSheet(u"background-color: rgb(40, 40, 46);\n"
"font-family: Noto Sans;")
        self.verticalLayout = QVBoxLayout(Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.toolBox = QToolBox(Settings)
        self.toolBox.setObjectName(u"toolBox")
        self.toolBox.setStyleSheet(u"color: white;")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setGeometry(QRect(0, 0, 662, 647))
        self.gridLayout_9 = QGridLayout(self.page_1)
        self.gridLayout_9.setObjectName(u"gridLayout_9")
        self.main_frame_p1 = QFrame(self.page_1)
        self.main_frame_p1.setObjectName(u"main_frame_p1")
        self.main_frame_p1.setMinimumSize(QSize(500, 0))
        self.main_frame_p1.setStyleSheet(u"QFrame#main_frame_p1{\n"
"     border: none;\n"
"}")
        self.main_frame_p1.setFrameShape(QFrame.StyledPanel)
        self.main_frame_p1.setFrameShadow(QFrame.Raised)
        self.gridLayout_7 = QGridLayout(self.main_frame_p1)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.frame_3 = QFrame(self.main_frame_p1)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setStyleSheet(u"QFrame#frame_3{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.horizontalSpacer = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 2, 1, 1)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setVerticalSpacing(4)
        self.gridLayout_3.setContentsMargins(-1, -1, -1, 6)
        self.r128_i_txt = QLineEdit(self.frame_3)
        self.r128_i_txt.setObjectName(u"r128_i_txt")
        self.r128_i_txt.setEnabled(True)
        self.r128_i_txt.setMinimumSize(QSize(60, 0))
        self.r128_i_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.r128_i_txt, 0, 1, 1, 1)

        self.ebu_TP = QLabel(self.frame_3)
        self.ebu_TP.setObjectName(u"ebu_TP")
        self.ebu_TP.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_3.addWidget(self.ebu_TP, 2, 0, 1, 1, Qt.AlignRight)

        self.ebu_I = QLabel(self.frame_3)
        self.ebu_I.setObjectName(u"ebu_I")
        self.ebu_I.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_3.addWidget(self.ebu_I, 0, 0, 1, 1, Qt.AlignRight)

        self.r128_tp_txt = QLineEdit(self.frame_3)
        self.r128_tp_txt.setObjectName(u"r128_tp_txt")
        self.r128_tp_txt.setEnabled(True)
        self.r128_tp_txt.setMinimumSize(QSize(60, 0))
        self.r128_tp_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.r128_tp_txt, 2, 1, 1, 1)

        self.ebu_LRA = QLabel(self.frame_3)
        self.ebu_LRA.setObjectName(u"ebu_LRA")
        self.ebu_LRA.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_3.addWidget(self.ebu_LRA, 1, 0, 1, 1, Qt.AlignRight)

        self.r128_lra_txt = QLineEdit(self.frame_3)
        self.r128_lra_txt.setObjectName(u"r128_lra_txt")
        self.r128_lra_txt.setEnabled(True)
        self.r128_lra_txt.setMinimumSize(QSize(60, 0))
        self.r128_lra_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.r128_lra_txt, 1, 1, 1, 1)

        self.ebu_THR = QLabel(self.frame_3)
        self.ebu_THR.setObjectName(u"ebu_THR")
        self.ebu_THR.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_3.addWidget(self.ebu_THR, 3, 0, 1, 1, Qt.AlignRight)

        self.r128_thr_txt = QLineEdit(self.frame_3)
        self.r128_thr_txt.setObjectName(u"r128_thr_txt")
        self.r128_thr_txt.setEnabled(True)
        self.r128_thr_txt.setMinimumSize(QSize(60, 0))
        self.r128_thr_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_3.addWidget(self.r128_thr_txt, 3, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 1, 1, 1)

        self.label_16 = QLabel(self.frame_3)
        self.label_16.setObjectName(u"label_16")
        font = QFont()
        font.setFamilies([u"Noto Sans"])
        font.setBold(False)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet(u"color: white")

        self.gridLayout_4.addWidget(self.label_16, 0, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_3, 4, 0, 1, 1)

        self.frame_4 = QFrame(self.main_frame_p1)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setStyleSheet(u"QFrame#frame_4{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_5.addItem(self.horizontalSpacer_2, 1, 1, 1, 1)

        self.label_15 = QLabel(self.frame_4)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setFont(font)
        self.label_15.setStyleSheet(u"color: white")

        self.gridLayout_5.addWidget(self.label_15, 0, 0, 1, 1)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(4)
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 6)
        self.Bitrate_2 = QLabel(self.frame_4)
        self.Bitrate_2.setObjectName(u"Bitrate_2")
        self.Bitrate_2.setMinimumSize(QSize(0, 0))
        self.Bitrate_2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.Bitrate_2, 3, 0, 1, 1, Qt.AlignRight)

        self.Channels = QLabel(self.frame_4)
        self.Channels.setObjectName(u"Channels")
        self.Channels.setMinimumSize(QSize(0, 0))
        self.Channels.setBaseSize(QSize(110, 0))
        self.Channels.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.Channels, 1, 0, 1, 1, Qt.AlignRight)

        self.channels_txt = QLineEdit(self.frame_4)
        self.channels_txt.setObjectName(u"channels_txt")
        self.channels_txt.setMinimumSize(QSize(60, 0))
        self.channels_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.channels_txt, 1, 1, 1, 1)

        self.label_21 = QLabel(self.frame_4)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setStyleSheet(u"color: rgb(146, 146, 146)\n"
"")

        self.gridLayout_2.addWidget(self.label_21, 2, 2, 1, 1)

        self.label_22 = QLabel(self.frame_4)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setStyleSheet(u"color: rgb(146, 146, 146)\n"
"")

        self.gridLayout_2.addWidget(self.label_22, 3, 2, 1, 1)

        self.label_9 = QLabel(self.frame_4)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(0, 0))
        self.label_9.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.label_9, 2, 0, 1, 1, Qt.AlignRight)

        self.a_bit_rate_txt = QLineEdit(self.frame_4)
        self.a_bit_rate_txt.setObjectName(u"a_bit_rate_txt")
        self.a_bit_rate_txt.setMinimumSize(QSize(60, 0))
        self.a_bit_rate_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.a_bit_rate_txt, 3, 1, 1, 1)

        self.sample_rate_comboBox = QComboBox(self.frame_4)
        self.sample_rate_comboBox.setObjectName(u"sample_rate_comboBox")
        self.sample_rate_comboBox.setMinimumSize(QSize(60, 0))
        self.sample_rate_comboBox.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.sample_rate_comboBox, 2, 1, 1, 1)

        self.Codec_aud = QLabel(self.frame_4)
        self.Codec_aud.setObjectName(u"Codec_aud")
        self.Codec_aud.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_2.addWidget(self.Codec_aud, 0, 0, 1, 1, Qt.AlignRight)

        self.codec_aud_txt = QLineEdit(self.frame_4)
        self.codec_aud_txt.setObjectName(u"codec_aud_txt")
        self.codec_aud_txt.setMinimumSize(QSize(60, 0))
        self.codec_aud_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_2.addWidget(self.codec_aud_txt, 0, 1, 1, 1)


        self.gridLayout_5.addLayout(self.gridLayout_2, 1, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_4, 3, 0, 1, 1)

        self.gridLayout_10 = QGridLayout()
        self.gridLayout_10.setObjectName(u"gridLayout_10")
        self.gridLayout_10.setContentsMargins(-1, -1, -1, 20)
        self.label_17 = QLabel(self.main_frame_p1)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setEnabled(False)
        self.label_17.setMaximumSize(QSize(16777215, 20))
        self.label_17.setBaseSize(QSize(0, 20))
        self.label_17.setFont(font)
        self.label_17.setStyleSheet(u"color: white")

        self.gridLayout_10.addWidget(self.label_17, 1, 0, 1, 1, Qt.AlignRight)

        self.presetComboBox = QComboBox(self.main_frame_p1)
        self.presetComboBox.setObjectName(u"presetComboBox")
        self.presetComboBox.setEnabled(False)
        self.presetComboBox.setMaximumSize(QSize(16777215, 20))
        self.presetComboBox.setBaseSize(QSize(0, 20))

        self.gridLayout_10.addWidget(self.presetComboBox, 1, 1, 1, 1)

        self.label_18 = QLabel(self.main_frame_p1)
        self.label_18.setObjectName(u"label_18")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setMinimumSize(QSize(0, 20))
        self.label_18.setMaximumSize(QSize(16777215, 20))
        self.label_18.setBaseSize(QSize(0, 20))
        self.label_18.setFont(font)
        self.label_18.setStyleSheet(u"color: rgb(76, 76, 76)")

        self.gridLayout_10.addWidget(self.label_18, 0, 1, 1, 1, Qt.AlignRight)

        self.gridLayout_10.setColumnStretch(0, 1)
        self.gridLayout_10.setColumnStretch(1, 4)

        self.gridLayout_7.addLayout(self.gridLayout_10, 0, 0, 1, 1)

        self.frame_5 = QFrame(self.main_frame_p1)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"QFrame#frame_5{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.gridLayout_6 = QGridLayout(self.frame_5)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.label_2 = QLabel(self.frame_5)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: white")

        self.gridLayout_6.addWidget(self.label_2, 1, 0, 1, 1)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_6.addItem(self.horizontalSpacer_3, 2, 1, 1, 1)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(4)
        self.gridLayout.setContentsMargins(-1, -1, -1, 6)
        self.frame_rate_comboBox = QComboBox(self.frame_5)
        self.frame_rate_comboBox.setObjectName(u"frame_rate_comboBox")
        self.frame_rate_comboBox.setMinimumSize(QSize(60, 0))
        self.frame_rate_comboBox.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.frame_rate_comboBox, 3, 1, 1, 1)

        self.Codec = QLabel(self.frame_5)
        self.Codec.setObjectName(u"Codec")
        self.Codec.setStyleSheet(u"color: rgb(146, 146, 146)")
        self.Codec.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.Codec, 0, 0, 1, 1, Qt.AlignRight)

        self.Framerate = QLabel(self.frame_5)
        self.Framerate.setObjectName(u"Framerate")
        self.Framerate.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout.addWidget(self.Framerate, 3, 0, 1, 1, Qt.AlignRight)

        self.Resolution = QLabel(self.frame_5)
        self.Resolution.setObjectName(u"Resolution")
        self.Resolution.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout.addWidget(self.Resolution, 1, 0, 1, 1, Qt.AlignRight)

        self.v_bit_rate_txt = QLineEdit(self.frame_5)
        self.v_bit_rate_txt.setObjectName(u"v_bit_rate_txt")
        self.v_bit_rate_txt.setMinimumSize(QSize(60, 0))
        self.v_bit_rate_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.v_bit_rate_txt, 2, 1, 1, 1)

        self.label_20 = QLabel(self.frame_5)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setStyleSheet(u"color: rgb(146, 146, 146)\n"
"")

        self.gridLayout.addWidget(self.label_20, 3, 2, 1, 2)

        self.label_4 = QLabel(self.frame_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)

        self.Bitrate = QLabel(self.frame_5)
        self.Bitrate.setObjectName(u"Bitrate")
        self.Bitrate.setStyleSheet(u"color: rgb(146, 146, 146)\n"
"")

        self.gridLayout.addWidget(self.Bitrate, 2, 0, 1, 1, Qt.AlignRight)

        self.width_txt = QLineEdit(self.frame_5)
        self.width_txt.setObjectName(u"width_txt")
        self.width_txt.setMinimumSize(QSize(60, 0))
        self.width_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.width_txt, 1, 1, 1, 1)

        self.label_7 = QLabel(self.frame_5)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout.addWidget(self.label_7, 4, 0, 1, 1, Qt.AlignRight)

        self.label_19 = QLabel(self.frame_5)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setStyleSheet(u"color: rgb(146, 146, 146)\n"
"")

        self.gridLayout.addWidget(self.label_19, 2, 2, 1, 2)

        self.codec_txt = QLineEdit(self.frame_5)
        self.codec_txt.setObjectName(u"codec_txt")
        self.codec_txt.setMinimumSize(QSize(60, 0))
        self.codec_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.codec_txt, 0, 1, 1, 1)

        self.height_txt = QLineEdit(self.frame_5)
        self.height_txt.setObjectName(u"height_txt")
        self.height_txt.setMinimumSize(QSize(60, 0))
        self.height_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.height_txt, 1, 3, 1, 1)

        self.dar_comboBox = QComboBox(self.frame_5)
        self.dar_comboBox.setObjectName(u"dar_comboBox")
        self.dar_comboBox.setMinimumSize(QSize(60, 0))
        self.dar_comboBox.setMaximumSize(QSize(100, 16777215))

        self.gridLayout.addWidget(self.dar_comboBox, 4, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout, 2, 0, 1, 1)


        self.gridLayout_7.addWidget(self.frame_5, 2, 0, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 60, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer_3, 5, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_7.addItem(self.verticalSpacer, 1, 0, 1, 1)


        self.gridLayout_9.addWidget(self.main_frame_p1, 0, 1, 1, 1)

        self.horizontalSpacer_4 = QSpacerItem(200, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_9.addItem(self.horizontalSpacer_4, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_1, u"Main preset")
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setGeometry(QRect(0, 0, 662, 647))
        self.gridLayout_16 = QGridLayout(self.page_2)
        self.gridLayout_16.setObjectName(u"gridLayout_16")
        self.main_frame_blckslnc = QFrame(self.page_2)
        self.main_frame_blckslnc.setObjectName(u"main_frame_blckslnc")
        self.main_frame_blckslnc.setMinimumSize(QSize(500, 0))
        self.gridLayout_8 = QGridLayout(self.main_frame_blckslnc)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.slnc_frame = QFrame(self.main_frame_blckslnc)
        self.slnc_frame.setObjectName(u"slnc_frame")
        self.slnc_frame.setStyleSheet(u"QFrame#slnc_frame{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_14 = QGridLayout(self.slnc_frame)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.horizontalSpacer_8 = QSpacerItem(150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_14.addItem(self.horizontalSpacer_8, 1, 2, 1, 1)

        self.Silence_sett = QLabel(self.slnc_frame)
        self.Silence_sett.setObjectName(u"Silence_sett")
        self.Silence_sett.setMinimumSize(QSize(20, 0))
        self.Silence_sett.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_14.addWidget(self.Silence_sett, 0, 0, 1, 1)

        self.gridLayout_12 = QGridLayout()
        self.gridLayout_12.setObjectName(u"gridLayout_12")
        self.slnc_dur_txt = QLineEdit(self.slnc_frame)
        self.slnc_dur_txt.setObjectName(u"slnc_dur_txt")
        self.slnc_dur_txt.setMinimumSize(QSize(60, 0))
        self.slnc_dur_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_12.addWidget(self.slnc_dur_txt, 0, 1, 1, 1)

        self.NoiseTolerance_slnc = QLabel(self.slnc_frame)
        self.NoiseTolerance_slnc.setObjectName(u"NoiseTolerance_slnc")
        self.NoiseTolerance_slnc.setMinimumSize(QSize(0, 0))
        self.NoiseTolerance_slnc.setBaseSize(QSize(110, 0))
        self.NoiseTolerance_slnc.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.NoiseTolerance_slnc, 1, 0, 1, 1, Qt.AlignRight)

        self.Duration_slnc = QLabel(self.slnc_frame)
        self.Duration_slnc.setObjectName(u"Duration_slnc")
        self.Duration_slnc.setMinimumSize(QSize(0, 0))
        self.Duration_slnc.setBaseSize(QSize(110, 0))
        self.Duration_slnc.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.Duration_slnc, 0, 0, 1, 1, Qt.AlignRight)

        self.slnc_in_label = QLabel(self.slnc_frame)
        self.slnc_in_label.setObjectName(u"slnc_in_label")
        self.slnc_in_label.setMinimumSize(QSize(0, 0))
        self.slnc_in_label.setBaseSize(QSize(110, 0))
        self.slnc_in_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.slnc_in_label, 2, 0, 1, 1, Qt.AlignRight)

        self.Channels_10 = QLabel(self.slnc_frame)
        self.Channels_10.setObjectName(u"Channels_10")
        self.Channels_10.setMinimumSize(QSize(0, 0))
        self.Channels_10.setBaseSize(QSize(110, 0))
        self.Channels_10.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.Channels_10, 1, 2, 1, 1)

        self.Channels_9 = QLabel(self.slnc_frame)
        self.Channels_9.setObjectName(u"Channels_9")
        self.Channels_9.setMinimumSize(QSize(0, 0))
        self.Channels_9.setBaseSize(QSize(110, 0))
        self.Channels_9.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.Channels_9, 0, 2, 1, 1)

        self.slnc_noize_txt = QLineEdit(self.slnc_frame)
        self.slnc_noize_txt.setObjectName(u"slnc_noize_txt")
        self.slnc_noize_txt.setMinimumSize(QSize(60, 0))
        self.slnc_noize_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_12.addWidget(self.slnc_noize_txt, 1, 1, 1, 1)

        self.slnc_out_label = QLabel(self.slnc_frame)
        self.slnc_out_label.setObjectName(u"slnc_out_label")
        self.slnc_out_label.setMinimumSize(QSize(0, 0))
        self.slnc_out_label.setBaseSize(QSize(110, 0))
        self.slnc_out_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_12.addWidget(self.slnc_out_label, 3, 0, 1, 1, Qt.AlignRight)

        self.slnc_tc_in = QLineEdit(self.slnc_frame)
        self.slnc_tc_in.setObjectName(u"slnc_tc_in")
        self.slnc_tc_in.setMinimumSize(QSize(60, 0))
        self.slnc_tc_in.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_12.addWidget(self.slnc_tc_in, 2, 1, 1, 1)

        self.slnc_tc_out = QLineEdit(self.slnc_frame)
        self.slnc_tc_out.setObjectName(u"slnc_tc_out")
        self.slnc_tc_out.setMinimumSize(QSize(60, 0))
        self.slnc_tc_out.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_12.addWidget(self.slnc_tc_out, 3, 1, 1, 1)

        self.silenceCheckBox = QCheckBox(self.slnc_frame)
        self.silenceCheckBox.setObjectName(u"silenceCheckBox")

        self.gridLayout_12.addWidget(self.silenceCheckBox, 2, 2, 2, 1)


        self.gridLayout_14.addLayout(self.gridLayout_12, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.slnc_frame, 1, 0, 1, 2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_8.addItem(self.verticalSpacer_2, 3, 1, 1, 1)

        self.freeze_frame = QFrame(self.main_frame_blckslnc)
        self.freeze_frame.setObjectName(u"freeze_frame")
        self.freeze_frame.setStyleSheet(u"QFrame#freeze_frame{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_17 = QGridLayout(self.freeze_frame)
        self.gridLayout_17.setObjectName(u"gridLayout_17")
        self.horizontalSpacer_9 = QSpacerItem(150, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_17.addItem(self.horizontalSpacer_9, 1, 2, 1, 1)

        self.Silence_sett_2 = QLabel(self.freeze_frame)
        self.Silence_sett_2.setObjectName(u"Silence_sett_2")
        self.Silence_sett_2.setMinimumSize(QSize(20, 0))
        self.Silence_sett_2.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_17.addWidget(self.Silence_sett_2, 0, 0, 1, 1)

        self.gridLayout_18 = QGridLayout()
        self.gridLayout_18.setObjectName(u"gridLayout_18")
        self.frz_dur_txt = QLineEdit(self.freeze_frame)
        self.frz_dur_txt.setObjectName(u"frz_dur_txt")
        self.frz_dur_txt.setMinimumSize(QSize(60, 0))
        self.frz_dur_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_18.addWidget(self.frz_dur_txt, 0, 1, 1, 1)

        self.NoiseTolerance_slnc_6 = QLabel(self.freeze_frame)
        self.NoiseTolerance_slnc_6.setObjectName(u"NoiseTolerance_slnc_6")
        self.NoiseTolerance_slnc_6.setMinimumSize(QSize(0, 0))
        self.NoiseTolerance_slnc_6.setBaseSize(QSize(110, 0))
        self.NoiseTolerance_slnc_6.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.NoiseTolerance_slnc_6, 1, 0, 1, 1, Qt.AlignRight)

        self.Duration_slnc_2 = QLabel(self.freeze_frame)
        self.Duration_slnc_2.setObjectName(u"Duration_slnc_2")
        self.Duration_slnc_2.setMinimumSize(QSize(0, 0))
        self.Duration_slnc_2.setBaseSize(QSize(110, 0))
        self.Duration_slnc_2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.Duration_slnc_2, 0, 0, 1, 1, Qt.AlignRight)

        self.frz_in_label = QLabel(self.freeze_frame)
        self.frz_in_label.setObjectName(u"frz_in_label")
        self.frz_in_label.setMinimumSize(QSize(0, 0))
        self.frz_in_label.setBaseSize(QSize(110, 0))
        self.frz_in_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.frz_in_label, 2, 0, 1, 1, Qt.AlignRight)

        self.Channels_11 = QLabel(self.freeze_frame)
        self.Channels_11.setObjectName(u"Channels_11")
        self.Channels_11.setMinimumSize(QSize(0, 0))
        self.Channels_11.setBaseSize(QSize(110, 0))
        self.Channels_11.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.Channels_11, 1, 2, 1, 1)

        self.Channels_12 = QLabel(self.freeze_frame)
        self.Channels_12.setObjectName(u"Channels_12")
        self.Channels_12.setMinimumSize(QSize(0, 0))
        self.Channels_12.setBaseSize(QSize(110, 0))
        self.Channels_12.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.Channels_12, 0, 2, 1, 1)

        self.frz_noize_txt = QLineEdit(self.freeze_frame)
        self.frz_noize_txt.setObjectName(u"frz_noize_txt")
        self.frz_noize_txt.setMinimumSize(QSize(60, 0))
        self.frz_noize_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_18.addWidget(self.frz_noize_txt, 1, 1, 1, 1)

        self.frz_out_label = QLabel(self.freeze_frame)
        self.frz_out_label.setObjectName(u"frz_out_label")
        self.frz_out_label.setMinimumSize(QSize(0, 0))
        self.frz_out_label.setBaseSize(QSize(110, 0))
        self.frz_out_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_18.addWidget(self.frz_out_label, 3, 0, 1, 1, Qt.AlignRight)

        self.frz_tc_in = QLineEdit(self.freeze_frame)
        self.frz_tc_in.setObjectName(u"frz_tc_in")
        self.frz_tc_in.setMinimumSize(QSize(60, 0))
        self.frz_tc_in.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_18.addWidget(self.frz_tc_in, 2, 1, 1, 1)

        self.frz_tc_out = QLineEdit(self.freeze_frame)
        self.frz_tc_out.setObjectName(u"frz_tc_out")
        self.frz_tc_out.setMinimumSize(QSize(60, 0))
        self.frz_tc_out.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_18.addWidget(self.frz_tc_out, 3, 1, 1, 1)

        self.freezeCheckBox = QCheckBox(self.freeze_frame)
        self.freezeCheckBox.setObjectName(u"freezeCheckBox")

        self.gridLayout_18.addWidget(self.freezeCheckBox, 2, 2, 2, 1)


        self.gridLayout_17.addLayout(self.gridLayout_18, 1, 1, 1, 1)


        self.gridLayout_8.addWidget(self.freeze_frame, 2, 0, 1, 2)

        self.blck_frame = QFrame(self.main_frame_blckslnc)
        self.blck_frame.setObjectName(u"blck_frame")
        self.blck_frame.setStyleSheet(u"QFrame#blck_frame{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_13 = QGridLayout(self.blck_frame)
        self.gridLayout_13.setObjectName(u"gridLayout_13")
        self.Black_sett = QLabel(self.blck_frame)
        self.Black_sett.setObjectName(u"Black_sett")
        self.Black_sett.setMinimumSize(QSize(0, 20))
        self.Black_sett.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_13.addWidget(self.Black_sett, 0, 0, 1, 1)

        self.gridLayout_11 = QGridLayout()
        self.gridLayout_11.setObjectName(u"gridLayout_11")
        self.blck_dur_txt = QLineEdit(self.blck_frame)
        self.blck_dur_txt.setObjectName(u"blck_dur_txt")
        self.blck_dur_txt.setMinimumSize(QSize(60, 0))
        self.blck_dur_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_11.addWidget(self.blck_dur_txt, 0, 1, 1, 1)

        self.blck_tc_in = QLineEdit(self.blck_frame)
        self.blck_tc_in.setObjectName(u"blck_tc_in")
        self.blck_tc_in.setMinimumSize(QSize(60, 0))
        self.blck_tc_in.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_11.addWidget(self.blck_tc_in, 2, 1, 1, 1)

        self.Threshold_blck = QLabel(self.blck_frame)
        self.Threshold_blck.setObjectName(u"Threshold_blck")
        self.Threshold_blck.setMinimumSize(QSize(0, 0))
        self.Threshold_blck.setBaseSize(QSize(110, 0))
        self.Threshold_blck.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_11.addWidget(self.Threshold_blck, 1, 0, 1, 1, Qt.AlignRight)

        self.blck_tc_out = QLineEdit(self.blck_frame)
        self.blck_tc_out.setObjectName(u"blck_tc_out")
        self.blck_tc_out.setMinimumSize(QSize(60, 0))
        self.blck_tc_out.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_11.addWidget(self.blck_tc_out, 3, 1, 1, 1)

        self.blck_thr_txt = QLineEdit(self.blck_frame)
        self.blck_thr_txt.setObjectName(u"blck_thr_txt")
        self.blck_thr_txt.setMinimumSize(QSize(60, 0))
        self.blck_thr_txt.setMaximumSize(QSize(100, 16777215))

        self.gridLayout_11.addWidget(self.blck_thr_txt, 1, 1, 1, 1)

        self.Duration_blck = QLabel(self.blck_frame)
        self.Duration_blck.setObjectName(u"Duration_blck")
        self.Duration_blck.setMinimumSize(QSize(0, 0))
        self.Duration_blck.setBaseSize(QSize(110, 0))
        self.Duration_blck.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_11.addWidget(self.Duration_blck, 0, 0, 1, 1, Qt.AlignRight)

        self.blck_out_label = QLabel(self.blck_frame)
        self.blck_out_label.setObjectName(u"blck_out_label")
        self.blck_out_label.setMinimumSize(QSize(0, 0))
        self.blck_out_label.setBaseSize(QSize(110, 0))
        self.blck_out_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_11.addWidget(self.blck_out_label, 3, 0, 1, 1, Qt.AlignRight)

        self.Channels_8 = QLabel(self.blck_frame)
        self.Channels_8.setObjectName(u"Channels_8")
        self.Channels_8.setMinimumSize(QSize(0, 0))
        self.Channels_8.setBaseSize(QSize(110, 0))
        self.Channels_8.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_11.addWidget(self.Channels_8, 0, 2, 1, 1)

        self.blck_in_label = QLabel(self.blck_frame)
        self.blck_in_label.setObjectName(u"blck_in_label")
        self.blck_in_label.setMinimumSize(QSize(0, 0))
        self.blck_in_label.setBaseSize(QSize(110, 0))
        self.blck_in_label.setStyleSheet(u"color: rgb(146, 146, 146)")
        self.blck_in_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_11.addWidget(self.blck_in_label, 2, 0, 1, 1, Qt.AlignRight)

        self.blackCheckBox = QCheckBox(self.blck_frame)
        self.blackCheckBox.setObjectName(u"blackCheckBox")

        self.gridLayout_11.addWidget(self.blackCheckBox, 2, 2, 2, 1)


        self.gridLayout_13.addLayout(self.gridLayout_11, 1, 1, 1, 1)

        self.horizontalSpacer_6 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_13.addItem(self.horizontalSpacer_6, 1, 2, 1, 1)


        self.gridLayout_8.addWidget(self.blck_frame, 0, 0, 1, 2)


        self.gridLayout_16.addWidget(self.main_frame_blckslnc, 0, 1, 1, 1)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_16.addItem(self.horizontalSpacer_5, 0, 0, 1, 1)

        self.toolBox.addItem(self.page_2, u"Damage test")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setGeometry(QRect(0, 0, 662, 647))
        self.gridLayout_15 = QGridLayout(self.page_3)
        self.gridLayout_15.setObjectName(u"gridLayout_15")
        self.horizontalSpacer_12 = QSpacerItem(135, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_15.addItem(self.horizontalSpacer_12, 0, 0, 1, 1)

        self.main_frame_db_2 = QFrame(self.page_3)
        self.main_frame_db_2.setObjectName(u"main_frame_db_2")
        self.gridLayout_22 = QGridLayout(self.main_frame_db_2)
        self.gridLayout_22.setObjectName(u"gridLayout_22")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_22.addItem(self.verticalSpacer_5, 2, 0, 1, 1)

        self.db_frame_2 = QFrame(self.main_frame_db_2)
        self.db_frame_2.setObjectName(u"db_frame_2")
        self.db_frame_2.setStyleSheet(u"QFrame#db_frame_2{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_23 = QGridLayout(self.db_frame_2)
        self.gridLayout_23.setObjectName(u"gridLayout_23")
        self.gridLayout_24 = QGridLayout()
        self.gridLayout_24.setObjectName(u"gridLayout_24")
        self.Duration_blck_3 = QLabel(self.db_frame_2)
        self.Duration_blck_3.setObjectName(u"Duration_blck_3")
        self.Duration_blck_3.setMinimumSize(QSize(0, 0))
        self.Duration_blck_3.setBaseSize(QSize(110, 0))
        self.Duration_blck_3.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_24.addWidget(self.Duration_blck_3, 0, 0, 1, 1, Qt.AlignRight)

        self.db_sqlite_dbname = QLineEdit(self.db_frame_2)
        self.db_sqlite_dbname.setObjectName(u"db_sqlite_dbname")
        self.db_sqlite_dbname.setMinimumSize(QSize(150, 0))
        self.db_sqlite_dbname.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_24.addWidget(self.db_sqlite_dbname, 0, 1, 1, 1)


        self.gridLayout_23.addLayout(self.gridLayout_24, 1, 1, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.chck_con_sqlite_label = QLabel(self.db_frame_2)
        self.chck_con_sqlite_label.setObjectName(u"chck_con_sqlite_label")
        self.chck_con_sqlite_label.setMinimumSize(QSize(0, 20))
        self.chck_con_sqlite_label.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout_4.addWidget(self.chck_con_sqlite_label)

        self.chck_con_sqlite_Button = QPushButton(self.db_frame_2)
        self.chck_con_sqlite_Button.setObjectName(u"chck_con_sqlite_Button")
        self.chck_con_sqlite_Button.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"	 background-color:rgba(255,255,255,10)\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_4.addWidget(self.chck_con_sqlite_Button)


        self.gridLayout_23.addLayout(self.horizontalLayout_4, 3, 1, 1, 2)

        self.db_sett_2 = QLabel(self.db_frame_2)
        self.db_sett_2.setObjectName(u"db_sett_2")
        self.db_sett_2.setMinimumSize(QSize(0, 20))
        self.db_sett_2.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_23.addWidget(self.db_sett_2, 0, 0, 1, 1)

        self.horizontalSpacer_13 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_23.addItem(self.horizontalSpacer_13, 1, 2, 1, 1)

        self.verticalSpacer_7 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_23.addItem(self.verticalSpacer_7, 2, 1, 1, 1)


        self.gridLayout_22.addWidget(self.db_frame_2, 0, 0, 1, 1)


        self.gridLayout_15.addWidget(self.main_frame_db_2, 1, 1, 1, 1)

        self.main_frame_db = QFrame(self.page_3)
        self.main_frame_db.setObjectName(u"main_frame_db")
        self.main_frame_db.setMinimumSize(QSize(500, 0))
        self.gridLayout_19 = QGridLayout(self.main_frame_db)
        self.gridLayout_19.setObjectName(u"gridLayout_19")
        self.db_frame = QFrame(self.main_frame_db)
        self.db_frame.setObjectName(u"db_frame")
        self.db_frame.setStyleSheet(u"QFrame#db_frame{\n"
"     border: 1px solid rgb(63,64,66);\n"
"}")
        self.gridLayout_20 = QGridLayout(self.db_frame)
        self.gridLayout_20.setObjectName(u"gridLayout_20")
        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_20.addItem(self.verticalSpacer_6, 2, 1, 1, 1)

        self.gridLayout_21 = QGridLayout()
        self.gridLayout_21.setObjectName(u"gridLayout_21")
        self.db_posql_password = QLineEdit(self.db_frame)
        self.db_posql_password.setObjectName(u"db_posql_password")
        self.db_posql_password.setMinimumSize(QSize(150, 0))
        self.db_posql_password.setMaximumSize(QSize(200, 16777215))
        self.db_posql_password.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.gridLayout_21.addWidget(self.db_posql_password, 3, 1, 1, 1)

        self.db_posql_user = QLineEdit(self.db_frame)
        self.db_posql_user.setObjectName(u"db_posql_user")
        self.db_posql_user.setMinimumSize(QSize(150, 0))
        self.db_posql_user.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_21.addWidget(self.db_posql_user, 2, 1, 1, 1)

        self.blck_in_label_2 = QLabel(self.db_frame)
        self.blck_in_label_2.setObjectName(u"blck_in_label_2")
        self.blck_in_label_2.setMinimumSize(QSize(0, 0))
        self.blck_in_label_2.setBaseSize(QSize(110, 0))
        self.blck_in_label_2.setStyleSheet(u"color: rgb(146, 146, 146)")
        self.blck_in_label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_21.addWidget(self.blck_in_label_2, 2, 0, 1, 1, Qt.AlignRight)

        self.blck_out_label_2 = QLabel(self.db_frame)
        self.blck_out_label_2.setObjectName(u"blck_out_label_2")
        self.blck_out_label_2.setMinimumSize(QSize(0, 0))
        self.blck_out_label_2.setBaseSize(QSize(110, 0))
        self.blck_out_label_2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_21.addWidget(self.blck_out_label_2, 3, 0, 1, 1, Qt.AlignRight)

        self.db_port_label = QLabel(self.db_frame)
        self.db_port_label.setObjectName(u"db_port_label")
        self.db_port_label.setMinimumSize(QSize(0, 0))
        self.db_port_label.setBaseSize(QSize(110, 0))
        self.db_port_label.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_21.addWidget(self.db_port_label, 4, 0, 1, 1, Qt.AlignRight)

        self.Duration_blck_2 = QLabel(self.db_frame)
        self.Duration_blck_2.setObjectName(u"Duration_blck_2")
        self.Duration_blck_2.setMinimumSize(QSize(0, 0))
        self.Duration_blck_2.setBaseSize(QSize(110, 0))
        self.Duration_blck_2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_21.addWidget(self.Duration_blck_2, 0, 0, 1, 1, Qt.AlignRight)

        self.db_posql_host = QLineEdit(self.db_frame)
        self.db_posql_host.setObjectName(u"db_posql_host")
        self.db_posql_host.setMinimumSize(QSize(150, 0))
        self.db_posql_host.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_21.addWidget(self.db_posql_host, 0, 1, 1, 1)

        self.Threshold_blck_2 = QLabel(self.db_frame)
        self.Threshold_blck_2.setObjectName(u"Threshold_blck_2")
        self.Threshold_blck_2.setMinimumSize(QSize(0, 0))
        self.Threshold_blck_2.setBaseSize(QSize(110, 0))
        self.Threshold_blck_2.setStyleSheet(u"color: rgb(146, 146, 146)")

        self.gridLayout_21.addWidget(self.Threshold_blck_2, 1, 0, 1, 1, Qt.AlignRight)

        self.db_posql_port = QLineEdit(self.db_frame)
        self.db_posql_port.setObjectName(u"db_posql_port")
        self.db_posql_port.setMinimumSize(QSize(150, 0))
        self.db_posql_port.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_21.addWidget(self.db_posql_port, 4, 1, 1, 1)

        self.db_posql_dbname = QLineEdit(self.db_frame)
        self.db_posql_dbname.setObjectName(u"db_posql_dbname")
        self.db_posql_dbname.setMinimumSize(QSize(150, 0))
        self.db_posql_dbname.setMaximumSize(QSize(200, 16777215))

        self.gridLayout_21.addWidget(self.db_posql_dbname, 1, 1, 1, 1)


        self.gridLayout_20.addLayout(self.gridLayout_21, 1, 1, 1, 1)

        self.db_sett = QLabel(self.db_frame)
        self.db_sett.setObjectName(u"db_sett")
        self.db_sett.setMinimumSize(QSize(0, 20))
        self.db_sett.setMaximumSize(QSize(16777215, 20))

        self.gridLayout_20.addWidget(self.db_sett, 0, 0, 1, 1)

        self.horizontalSpacer_11 = QSpacerItem(60, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_20.addItem(self.horizontalSpacer_11, 1, 2, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.chck_con_posql_label = QLabel(self.db_frame)
        self.chck_con_posql_label.setObjectName(u"chck_con_posql_label")
        self.chck_con_posql_label.setMinimumSize(QSize(0, 20))
        self.chck_con_posql_label.setMaximumSize(QSize(16777215, 20))

        self.horizontalLayout.addWidget(self.chck_con_posql_label)

        self.chck_con_posql_Button = QPushButton(self.db_frame)
        self.chck_con_posql_Button.setObjectName(u"chck_con_posql_Button")
        self.chck_con_posql_Button.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"	 background-color:rgba(255,255,255,10)\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout.addWidget(self.chck_con_posql_Button)


        self.gridLayout_20.addLayout(self.horizontalLayout, 3, 1, 1, 2)


        self.gridLayout_19.addWidget(self.db_frame, 0, 0, 1, 1)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_19.addItem(self.verticalSpacer_4, 1, 0, 1, 1)


        self.gridLayout_15.addWidget(self.main_frame_db, 0, 1, 1, 1)

        self.toolBox.addItem(self.page_3, u"Database settings")

        self.verticalLayout.addWidget(self.toolBox)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 15, -1, -1)
        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_7)

        self.saveButton_main = QPushButton(Settings)
        self.saveButton_main.setObjectName(u"saveButton_main")
        self.saveButton_main.setMinimumSize(QSize(75, 25))
        self.saveButton_main.setMaximumSize(QSize(75, 25))
        self.saveButton_main.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"     background-color:rgba(255,255,255,10);\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_2.addWidget(self.saveButton_main)

        self.cancelButton_main = QPushButton(Settings)
        self.cancelButton_main.setObjectName(u"cancelButton_main")
        self.cancelButton_main.setMinimumSize(QSize(75, 25))
        self.cancelButton_main.setMaximumSize(QSize(75, 25))
        self.cancelButton_main.setStyleSheet(u"QPushButton{\n"
"	 color: white;\n"
"     background-color:rgba(255,255,255,10);\n"
"}\n"
"QPushButton:hover{\n"
"color: white;\n"
"background-color:rgba(255,255,255,20);\n"
"}\n"
"QPushButton:pressed{\n"
"color: white;\n"
"background-color:rgba(255,255,255,30);\n"
"}")

        self.horizontalLayout_2.addWidget(self.cancelButton_main)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Settings)

        self.toolBox.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(Settings)
    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", u"Test configuration", None))
        self.ebu_TP.setText(QCoreApplication.translate("Settings", u"TP", None))
        self.ebu_I.setText(QCoreApplication.translate("Settings", u"I", None))
        self.ebu_LRA.setText(QCoreApplication.translate("Settings", u"LRA", None))
        self.ebu_THR.setText(QCoreApplication.translate("Settings", u"THR", None))
        self.label_16.setText(QCoreApplication.translate("Settings", u"Loudness meter", None))
        self.label_15.setText(QCoreApplication.translate("Settings", u"Audio standard", None))
        self.Bitrate_2.setText(QCoreApplication.translate("Settings", u"Bitrate", None))
        self.Channels.setText(QCoreApplication.translate("Settings", u"Channels", None))
        self.label_21.setText(QCoreApplication.translate("Settings", u"Hz", None))
        self.label_22.setText(QCoreApplication.translate("Settings", u"Kbit/s", None))
        self.label_9.setText(QCoreApplication.translate("Settings", u"Sample rate", None))
        self.Codec_aud.setText(QCoreApplication.translate("Settings", u"Codec", None))
        self.label_17.setText(QCoreApplication.translate("Settings", u"Preset", None))
        self.label_18.setText(QCoreApplication.translate("Settings", u"\u0424\u0443\u043d\u043a\u0446\u0438\u044f \u0432 \u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0435", None))
        self.label_2.setText(QCoreApplication.translate("Settings", u"Video standard", None))
        self.Codec.setText(QCoreApplication.translate("Settings", u"Codec", None))
        self.Framerate.setText(QCoreApplication.translate("Settings", u"Framerate", None))
        self.Resolution.setText(QCoreApplication.translate("Settings", u"Resolution", None))
        self.label_20.setText(QCoreApplication.translate("Settings", u"fps", None))
        self.label_4.setText(QCoreApplication.translate("Settings", u"x", None))
        self.Bitrate.setText(QCoreApplication.translate("Settings", u"Bitrate", None))
        self.label_7.setText(QCoreApplication.translate("Settings", u"Display aspect ratio", None))
        self.label_19.setText(QCoreApplication.translate("Settings", u"Mbit/s", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_1), QCoreApplication.translate("Settings", u"Main preset", None))
        self.Silence_sett.setText(QCoreApplication.translate("Settings", u"Silence", None))
        self.NoiseTolerance_slnc.setText(QCoreApplication.translate("Settings", u"Noise tolerance", None))
        self.Duration_slnc.setText(QCoreApplication.translate("Settings", u"Duration", None))
        self.slnc_in_label.setText(QCoreApplication.translate("Settings", u"In", None))
        self.Channels_10.setText(QCoreApplication.translate("Settings", u"dB", None))
        self.Channels_9.setText(QCoreApplication.translate("Settings", u"sec", None))
        self.slnc_out_label.setText(QCoreApplication.translate("Settings", u"Out", None))
        self.silenceCheckBox.setText("")
        self.Silence_sett_2.setText(QCoreApplication.translate("Settings", u"Freeze", None))
        self.NoiseTolerance_slnc_6.setText(QCoreApplication.translate("Settings", u"Noise tolerance", None))
        self.Duration_slnc_2.setText(QCoreApplication.translate("Settings", u"Duration", None))
        self.frz_in_label.setText(QCoreApplication.translate("Settings", u"In", None))
        self.Channels_11.setText(QCoreApplication.translate("Settings", u"dB", None))
        self.Channels_12.setText(QCoreApplication.translate("Settings", u"sec", None))
        self.frz_out_label.setText(QCoreApplication.translate("Settings", u"Out", None))
        self.freezeCheckBox.setText("")
        self.Black_sett.setText(QCoreApplication.translate("Settings", u"Black", None))
        self.Threshold_blck.setText(QCoreApplication.translate("Settings", u"Threshold", None))
        self.Duration_blck.setText(QCoreApplication.translate("Settings", u"Duration", None))
        self.blck_out_label.setText(QCoreApplication.translate("Settings", u"Out", None))
        self.Channels_8.setText(QCoreApplication.translate("Settings", u"sec", None))
        self.blck_in_label.setText(QCoreApplication.translate("Settings", u"In", None))
        self.blackCheckBox.setText("")
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QCoreApplication.translate("Settings", u"Damage test", None))
        self.Duration_blck_3.setText(QCoreApplication.translate("Settings", u"DB name", None))
        self.chck_con_sqlite_label.setText(QCoreApplication.translate("Settings", u"Not connect", None))
        self.chck_con_sqlite_Button.setText(QCoreApplication.translate("Settings", u"Check connection", None))
        self.db_sett_2.setText(QCoreApplication.translate("Settings", u"SQLite settings", None))
        self.blck_in_label_2.setText(QCoreApplication.translate("Settings", u"User", None))
        self.blck_out_label_2.setText(QCoreApplication.translate("Settings", u"Password", None))
        self.db_port_label.setText(QCoreApplication.translate("Settings", u"Port", None))
        self.Duration_blck_2.setText(QCoreApplication.translate("Settings", u"Host", None))
        self.Threshold_blck_2.setText(QCoreApplication.translate("Settings", u"DB name", None))
        self.db_sett.setText(QCoreApplication.translate("Settings", u"PoSQL settings", None))
        self.chck_con_posql_label.setText(QCoreApplication.translate("Settings", u"Not connect", None))
        self.chck_con_posql_Button.setText(QCoreApplication.translate("Settings", u"Check connection", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), QCoreApplication.translate("Settings", u"Database settings", None))
        self.saveButton_main.setText(QCoreApplication.translate("Settings", u"Save", None))
        self.cancelButton_main.setText(QCoreApplication.translate("Settings", u"Cancel", None))
    # retranslateUi

