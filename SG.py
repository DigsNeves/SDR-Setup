#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SG
# Author: Diego Neves
# Description: Implementation of a signal generator
# GNU Radio version: 3.10.5.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio import soapy
import SG_my_mod as my_mod  # embedded python module
import time
import threading



from gnuradio import qtgui

class SG(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "SG", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SG")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SG")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.receiver_SDR = receiver_SDR = 2
        self.raw_result_filename = raw_result_filename = "result.txt"
        self.fun_probe = fun_probe = 1
        self.full_path = full_path = "/home/diego/Downloads/hack_aut/hack_both/"
        self.frequency_stop = frequency_stop = 2.74e9
        self.frequency_step = frequency_step = 1e6
        self.frequency_start = frequency_start = 2.18e9
        self.auxiliar_filename = auxiliar_filename = "test.txt"
        self.SDR_2 = SDR_2 = "000000000000000057b068dc22214f63"
        self.SDR_1 = SDR_1 = "0000000000000000a06063c82535465f"
        self.samp_rate = samp_rate = 8000000
        self.receiver_config = receiver_config = my_mod.set_receiver_serial_number(SDR_1, SDR_2, receiver_SDR)

        self.frequency_config = frequency_config = my_mod.set_frequency(frequency_start, frequency_stop, frequency_step)
        self.freq = freq = my_mod.sweeper(fun_probe)
        self.filename_config = filename_config = my_mod.set_filenames(full_path, auxiliar_filename, raw_result_filename)

        ##################################################
        # Blocks
        ##################################################

        self.prob_block = blocks.probe_signal_f()
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, freq)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', False)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(30, 0.0), 47.0))
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _qtgui_levelgauge_0_lg_win = qtgui.GrLevelGauge('Frequency',"default","default","default",(frequency_start/1e6),(frequency_stop/1e6), 100, False,1,isFloat,scaleFactor,True,self)
        _qtgui_levelgauge_0_lg_win.setValue((freq/1e6))
        self.qtgui_levelgauge_0 = _qtgui_levelgauge_0_lg_win

        self.top_layout.addWidget(_qtgui_levelgauge_0_lg_win)
        def _fun_probe_probe():
          while True:

            val = self.prob_block.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_fun_probe,val))
              except AttributeError:
                self.set_fun_probe(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (1))
        _fun_probe_thread = threading.Thread(target=_fun_probe_probe)
        _fun_probe_thread.daemon = True
        _fun_probe_thread.start()
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_CONST_WAVE, 0, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0, 0), (self.prob_block, 0))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.soapy_hackrf_sink_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SG")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_receiver_SDR(self):
        return self.receiver_SDR

    def set_receiver_SDR(self, receiver_SDR):
        self.receiver_SDR = receiver_SDR
        self.set_receiver_config(my_mod.set_receiver_serial_number(self.SDR_1, self.SDR_2, self.receiver_SDR))

    def get_raw_result_filename(self):
        return self.raw_result_filename

    def set_raw_result_filename(self, raw_result_filename):
        self.raw_result_filename = raw_result_filename
        self.set_filename_config(my_mod.set_filenames(self.full_path, self.auxiliar_filename, self.raw_result_filename))

    def get_fun_probe(self):
        return self.fun_probe

    def set_fun_probe(self, fun_probe):
        self.fun_probe = fun_probe
        self.set_freq(my_mod.sweeper(self.fun_probe))

    def get_full_path(self):
        return self.full_path

    def set_full_path(self, full_path):
        self.full_path = full_path
        self.set_filename_config(my_mod.set_filenames(self.full_path, self.auxiliar_filename, self.raw_result_filename))

    def get_frequency_stop(self):
        return self.frequency_stop

    def set_frequency_stop(self, frequency_stop):
        self.frequency_stop = frequency_stop
        self.set_frequency_config(my_mod.set_frequency(self.frequency_start, self.frequency_stop, self.frequency_step))

    def get_frequency_step(self):
        return self.frequency_step

    def set_frequency_step(self, frequency_step):
        self.frequency_step = frequency_step
        self.set_frequency_config(my_mod.set_frequency(self.frequency_start, self.frequency_stop, self.frequency_step))

    def get_frequency_start(self):
        return self.frequency_start

    def set_frequency_start(self, frequency_start):
        self.frequency_start = frequency_start
        self.set_frequency_config(my_mod.set_frequency(self.frequency_start, self.frequency_stop, self.frequency_step))

    def get_auxiliar_filename(self):
        return self.auxiliar_filename

    def set_auxiliar_filename(self, auxiliar_filename):
        self.auxiliar_filename = auxiliar_filename
        self.set_filename_config(my_mod.set_filenames(self.full_path, self.auxiliar_filename, self.raw_result_filename))

    def get_SDR_2(self):
        return self.SDR_2

    def set_SDR_2(self, SDR_2):
        self.SDR_2 = SDR_2
        self.set_receiver_config(my_mod.set_receiver_serial_number(self.SDR_1, self.SDR_2, self.receiver_SDR))

    def get_SDR_1(self):
        return self.SDR_1

    def set_SDR_1(self, SDR_1):
        self.SDR_1 = SDR_1
        self.set_receiver_config(my_mod.set_receiver_serial_number(self.SDR_1, self.SDR_2, self.receiver_SDR))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.samp_rate)

    def get_receiver_config(self):
        return self.receiver_config

    def set_receiver_config(self, receiver_config):
        self.receiver_config = receiver_config

    def get_qtgui_levelgauge_0(self):
        return self.qtgui_levelgauge_0

    def set_qtgui_levelgauge_0(self, qtgui_levelgauge_0):
        self.qtgui_levelgauge_0 = qtgui_levelgauge_0
        self.qtgui_levelgauge_0.setValue((self.freq/1e6))

    def get_frequency_config(self):
        return self.frequency_config

    def set_frequency_config(self, frequency_config):
        self.frequency_config = frequency_config

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.qtgui_levelgauge_0.setValue((self.freq/1e6))
        self.analog_sig_source_x_0_1.set_frequency(self.freq)
        self.soapy_hackrf_sink_0.set_frequency(0, self.freq)

    def get_filename_config(self):
        return self.filename_config

    def set_filename_config(self, filename_config):
        self.filename_config = filename_config




def main(top_block_cls=SG, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
