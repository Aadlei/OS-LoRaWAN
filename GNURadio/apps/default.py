#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.10.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import uhd
import time
from gnuradio import zeromq
from xmlrpc.server import SimpleXMLRPCServer
import threading
import gnuradio.lora_sdr as lora_sdr
import sip



class default(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "default")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 2e6
        self.sink_freq = sink_freq = 8681e5
        self.sf2 = sf2 = 7
        self.sf = sf = 12
        self.low_pass_samp_rate = low_pass_samp_rate = samp_rate/2
        self.gain = gain = 120
        self.center_freq = center_freq = 8681e5
        self.bandwidth = bandwidth = 125e3

        ##################################################
        # Blocks
        ##################################################

        self.zeromq_push_sink_0_2 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5559', 100, False, (-1), True)
        self.zeromq_push_sink_0_1_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5561', 100, False, (-1), True)
        self.zeromq_push_sink_0_1 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5558', 100, False, (-1), True)
        self.zeromq_push_sink_0_0_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5560', 100, False, (-1), True)
        self.zeromq_push_sink_0_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5557', 100, False, (-1), True)
        self.zeromq_push_sink_0 = zeromq.push_sink(gr.sizeof_char, 1, 'tcp://127.0.0.1:5556', 100, False, (-1), True)
        self.zeromq_pull_source_0_0 = zeromq.pull_source(gr.sizeof_char, 1, 'tcp://127.0.0.1:5555', 100, False, (-1), False)
        self.zeromq_pull_source_0 = zeromq.pull_source(gr.sizeof_char, 1, 'tcp://127.0.0.1:5554', 100, False, (-1), False)
        self.xmlrpc_server_0 = SimpleXMLRPCServer(('localhost', 8089), allow_none=True)
        self.xmlrpc_server_0.register_instance(self)
        self.xmlrpc_server_0_thread = threading.Thread(target=self.xmlrpc_server_0.serve_forever)
        self.xmlrpc_server_0_thread.daemon = True
        self.xmlrpc_server_0_thread.start()
        self.uhd_usrp_source_0 = uhd.usrp_source(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
        )
        self.uhd_usrp_source_0.set_samp_rate(samp_rate)
        self.uhd_usrp_source_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_source_0.set_center_freq(868e6, 0)
        self.uhd_usrp_source_0.set_antenna("RX2", 0)
        self.uhd_usrp_source_0.set_bandwidth(125e3, 0)
        self.uhd_usrp_source_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0_0 = uhd.usrp_sink(
            ",".join(("", 'master_clock_rate=30.72e6')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0_0.set_samp_rate(2e6)
        self.uhd_usrp_sink_0_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0_0.set_center_freq(sink_freq, 0)
        self.uhd_usrp_sink_0_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(bandwidth, 0)
        self.uhd_usrp_sink_0_0.set_gain(gain, 0)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", 'master_clock_rate=30.72e6')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(2e6)
        self.uhd_usrp_sink_0.set_time_now(uhd.time_spec(time.time()), uhd.ALL_MBOARDS)

        self.uhd_usrp_sink_0.set_center_freq(sink_freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_bandwidth(bandwidth, 0)
        self.uhd_usrp_sink_0.set_gain(gain, 0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                low_pass_samp_rate,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_1.set_min_output_buffer(65568)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                low_pass_samp_rate,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0_0.set_min_output_buffer(65568)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                low_pass_samp_rate,
                77500,
                10000,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0.set_min_output_buffer(65568)
        self.lora_sdr_whitening_0_0 = lora_sdr.whitening(True,False,',','packet_len')
        self.lora_sdr_whitening_0 = lora_sdr.whitening(True,False,',','packet_len')
        self.lora_sdr_modulate_0_0 = lora_sdr.modulate(sf2, int(samp_rate), int(bandwidth), [0x34], (int(20*2**sf*samp_rate/bandwidth)),8)
        self.lora_sdr_modulate_0 = lora_sdr.modulate(sf, int(samp_rate), int(bandwidth), [0x34], (int(20*2**sf*samp_rate/bandwidth)),8)
        self.lora_sdr_interleaver_0_0 = lora_sdr.interleaver(1, sf2, 2, 125000)
        self.lora_sdr_interleaver_0 = lora_sdr.interleaver(1, sf, 2, 125000)
        self.lora_sdr_header_decoder_0_2 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0_1_0 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0_1 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0_0_0 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0_0 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_decoder_0 = lora_sdr.header_decoder(False, 3, 255, False, 2, True)
        self.lora_sdr_header_0_0 = lora_sdr.header(False, False, 1)
        self.lora_sdr_header_0 = lora_sdr.header(False, False, 1)
        self.lora_sdr_hamming_enc_0_0 = lora_sdr.hamming_enc(1, sf2)
        self.lora_sdr_hamming_enc_0 = lora_sdr.hamming_enc(1, sf)
        self.lora_sdr_hamming_dec_0_2 = lora_sdr.hamming_dec(True)
        self.lora_sdr_hamming_dec_0_1_0 = lora_sdr.hamming_dec(True)
        self.lora_sdr_hamming_dec_0_1 = lora_sdr.hamming_dec(True)
        self.lora_sdr_hamming_dec_0_0_0 = lora_sdr.hamming_dec(True)
        self.lora_sdr_hamming_dec_0_0 = lora_sdr.hamming_dec(True)
        self.lora_sdr_hamming_dec_0 = lora_sdr.hamming_dec(True)
        self.lora_sdr_gray_mapping_0_2 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_mapping_0_1_0 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_mapping_0_1 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_mapping_0_0_0 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_mapping_0_0 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_mapping_0 = lora_sdr.gray_mapping( True)
        self.lora_sdr_gray_demap_0_0 = lora_sdr.gray_demap(sf2)
        self.lora_sdr_gray_demap_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_frame_sync_0_2 = lora_sdr.frame_sync(int(868e6), 125000, sf2, False, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_1_0 = lora_sdr.frame_sync(int(868e6), 125000, sf2, False, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_1 = lora_sdr.frame_sync(int(868e6), 125000, sf, False, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0_0 = lora_sdr.frame_sync(int(868e6), 125000, sf2, False, [0x34], 16,8)
        self.lora_sdr_frame_sync_0_0 = lora_sdr.frame_sync(int(868e6), 125000, sf, False, [0x34], 16,8)
        self.lora_sdr_frame_sync_0 = lora_sdr.frame_sync(int(868e6), 125000, sf, False, [0x34], 16,8)
        self.lora_sdr_fft_demod_0_2 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_fft_demod_0_1_0 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_fft_demod_0_1 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_fft_demod_0_0_0 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_fft_demod_0_0 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_fft_demod_0 = lora_sdr.fft_demod( True, True)
        self.lora_sdr_dewhitening_0_2 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_1_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_1 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0_0 = lora_sdr.dewhitening()
        self.lora_sdr_dewhitening_0 = lora_sdr.dewhitening()
        self.lora_sdr_deinterleaver_0_2 = lora_sdr.deinterleaver( True)
        self.lora_sdr_deinterleaver_0_1_0 = lora_sdr.deinterleaver( True)
        self.lora_sdr_deinterleaver_0_1 = lora_sdr.deinterleaver( True)
        self.lora_sdr_deinterleaver_0_0_0 = lora_sdr.deinterleaver( True)
        self.lora_sdr_deinterleaver_0_0 = lora_sdr.deinterleaver( True)
        self.lora_sdr_deinterleaver_0 = lora_sdr.deinterleaver( True)
        self.lora_sdr_crc_verif_0_2 = lora_sdr.crc_verif( 2, False)
        self.lora_sdr_crc_verif_0_1_0 = lora_sdr.crc_verif( 2, False)
        self.lora_sdr_crc_verif_0_1 = lora_sdr.crc_verif( 2, False)
        self.lora_sdr_crc_verif_0_0_0 = lora_sdr.crc_verif( 2, False)
        self.lora_sdr_crc_verif_0_0 = lora_sdr.crc_verif( 2, False)
        self.lora_sdr_crc_verif_0 = lora_sdr.crc_verif( 2, False)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_conjugate_cc_0_0 = blocks.conjugate_cc()
        self.blocks_conjugate_cc_0 = blocks.conjugate_cc()
        self.analog_sig_source_x_0_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (-500000), 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (-300000), 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (-100000), 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_sdr_header_decoder_0, 'frame_info'), (self.lora_sdr_frame_sync_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0, 'frame_info'), (self.lora_sdr_frame_sync_0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_0_0, 'frame_info'), (self.lora_sdr_frame_sync_0_0_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_1, 'frame_info'), (self.lora_sdr_frame_sync_0_1, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_1_0, 'frame_info'), (self.lora_sdr_frame_sync_0_1_0, 'frame_info'))
        self.msg_connect((self.lora_sdr_header_decoder_0_2, 'frame_info'), (self.lora_sdr_frame_sync_0_2, 'frame_info'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_sig_source_x_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.blocks_conjugate_cc_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_conjugate_cc_0_0, 0), (self.uhd_usrp_sink_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0, 0), (self.zeromq_push_sink_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0, 0), (self.zeromq_push_sink_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_0_0, 0), (self.zeromq_push_sink_0_0_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_1, 0), (self.zeromq_push_sink_0_1, 0))
        self.connect((self.lora_sdr_crc_verif_0_1_0, 0), (self.zeromq_push_sink_0_1_0, 0))
        self.connect((self.lora_sdr_crc_verif_0_2, 0), (self.zeromq_push_sink_0_2, 0))
        self.connect((self.lora_sdr_deinterleaver_0, 0), (self.lora_sdr_hamming_dec_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0, 0), (self.lora_sdr_hamming_dec_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_0_0, 0), (self.lora_sdr_hamming_dec_0_0_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_1, 0), (self.lora_sdr_hamming_dec_0_1, 0))
        self.connect((self.lora_sdr_deinterleaver_0_1_0, 0), (self.lora_sdr_hamming_dec_0_1_0, 0))
        self.connect((self.lora_sdr_deinterleaver_0_2, 0), (self.lora_sdr_hamming_dec_0_2, 0))
        self.connect((self.lora_sdr_dewhitening_0, 0), (self.lora_sdr_crc_verif_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0, 0), (self.lora_sdr_crc_verif_0_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_0_0, 0), (self.lora_sdr_crc_verif_0_0_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_1, 0), (self.lora_sdr_crc_verif_0_1, 0))
        self.connect((self.lora_sdr_dewhitening_0_1_0, 0), (self.lora_sdr_crc_verif_0_1_0, 0))
        self.connect((self.lora_sdr_dewhitening_0_2, 0), (self.lora_sdr_crc_verif_0_2, 0))
        self.connect((self.lora_sdr_fft_demod_0, 0), (self.lora_sdr_gray_mapping_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0, 0), (self.lora_sdr_gray_mapping_0_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_0_0, 0), (self.lora_sdr_gray_mapping_0_0_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_1, 0), (self.lora_sdr_gray_mapping_0_1, 0))
        self.connect((self.lora_sdr_fft_demod_0_1_0, 0), (self.lora_sdr_gray_mapping_0_1_0, 0))
        self.connect((self.lora_sdr_fft_demod_0_2, 0), (self.lora_sdr_gray_mapping_0_2, 0))
        self.connect((self.lora_sdr_frame_sync_0, 0), (self.lora_sdr_fft_demod_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0, 0), (self.lora_sdr_fft_demod_0_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_0_0, 0), (self.lora_sdr_fft_demod_0_0_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_1, 0), (self.lora_sdr_fft_demod_0_1, 0))
        self.connect((self.lora_sdr_frame_sync_0_1_0, 0), (self.lora_sdr_fft_demod_0_1_0, 0))
        self.connect((self.lora_sdr_frame_sync_0_2, 0), (self.lora_sdr_fft_demod_0_2, 0))
        self.connect((self.lora_sdr_gray_demap_0, 0), (self.lora_sdr_modulate_0, 0))
        self.connect((self.lora_sdr_gray_demap_0_0, 0), (self.lora_sdr_modulate_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0, 0), (self.lora_sdr_deinterleaver_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0, 0), (self.lora_sdr_deinterleaver_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_0_0, 0), (self.lora_sdr_deinterleaver_0_0_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_1, 0), (self.lora_sdr_deinterleaver_0_1, 0))
        self.connect((self.lora_sdr_gray_mapping_0_1_0, 0), (self.lora_sdr_deinterleaver_0_1_0, 0))
        self.connect((self.lora_sdr_gray_mapping_0_2, 0), (self.lora_sdr_deinterleaver_0_2, 0))
        self.connect((self.lora_sdr_hamming_dec_0, 0), (self.lora_sdr_header_decoder_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0, 0), (self.lora_sdr_header_decoder_0_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_0_0, 0), (self.lora_sdr_header_decoder_0_0_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_1, 0), (self.lora_sdr_header_decoder_0_1, 0))
        self.connect((self.lora_sdr_hamming_dec_0_1_0, 0), (self.lora_sdr_header_decoder_0_1_0, 0))
        self.connect((self.lora_sdr_hamming_dec_0_2, 0), (self.lora_sdr_header_decoder_0_2, 0))
        self.connect((self.lora_sdr_hamming_enc_0, 0), (self.lora_sdr_interleaver_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0_0, 0), (self.lora_sdr_interleaver_0_0, 0))
        self.connect((self.lora_sdr_header_0, 0), (self.lora_sdr_hamming_enc_0, 0))
        self.connect((self.lora_sdr_header_0_0, 0), (self.lora_sdr_hamming_enc_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0, 0), (self.lora_sdr_dewhitening_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0, 0), (self.lora_sdr_dewhitening_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_0_0, 0), (self.lora_sdr_dewhitening_0_0_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_1, 0), (self.lora_sdr_dewhitening_0_1, 0))
        self.connect((self.lora_sdr_header_decoder_0_1_0, 0), (self.lora_sdr_dewhitening_0_1_0, 0))
        self.connect((self.lora_sdr_header_decoder_0_2, 0), (self.lora_sdr_dewhitening_0_2, 0))
        self.connect((self.lora_sdr_interleaver_0, 0), (self.lora_sdr_gray_demap_0, 0))
        self.connect((self.lora_sdr_interleaver_0_0, 0), (self.lora_sdr_gray_demap_0_0, 0))
        self.connect((self.lora_sdr_modulate_0, 0), (self.blocks_conjugate_cc_0, 0))
        self.connect((self.lora_sdr_modulate_0_0, 0), (self.blocks_conjugate_cc_0_0, 0))
        self.connect((self.lora_sdr_whitening_0, 0), (self.lora_sdr_header_0, 0))
        self.connect((self.lora_sdr_whitening_0_0, 0), (self.lora_sdr_header_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.lora_sdr_frame_sync_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.lora_sdr_frame_sync_0_2, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.lora_sdr_frame_sync_0_1, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.lora_sdr_frame_sync_0_1_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.lora_sdr_frame_sync_0_0, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.lora_sdr_frame_sync_0_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.uhd_usrp_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.zeromq_pull_source_0, 0), (self.lora_sdr_whitening_0, 0))
        self.connect((self.zeromq_pull_source_0_0, 0), (self.lora_sdr_whitening_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "default")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_low_pass_samp_rate(self.samp_rate/2)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_1.set_sampling_freq(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

    def get_sink_freq(self):
        return self.sink_freq

    def set_sink_freq(self, sink_freq):
        self.sink_freq = sink_freq
        self.uhd_usrp_sink_0.set_center_freq(self.sink_freq, 0)
        self.uhd_usrp_sink_0_0.set_center_freq(self.sink_freq, 0)

    def get_sf2(self):
        return self.sf2

    def set_sf2(self, sf2):
        self.sf2 = sf2
        self.lora_sdr_gray_demap_0_0.set_sf(self.sf2)
        self.lora_sdr_hamming_enc_0_0.set_sf(self.sf2)
        self.lora_sdr_interleaver_0_0.set_sf(self.sf2)
        self.lora_sdr_modulate_0_0.set_sf(self.sf2)

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_sdr_gray_demap_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0.set_sf(self.sf)
        self.lora_sdr_modulate_0.set_sf(self.sf)

    def get_low_pass_samp_rate(self):
        return self.low_pass_samp_rate

    def set_low_pass_samp_rate(self, low_pass_samp_rate):
        self.low_pass_samp_rate = low_pass_samp_rate
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.low_pass_samp_rate, 77500, 10000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.low_pass_samp_rate, 77500, 10000, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.low_pass_samp_rate, 77500, 10000, window.WIN_HAMMING, 6.76))

    def get_gain(self):
        return self.gain

    def set_gain(self, gain):
        self.gain = gain
        self.uhd_usrp_sink_0.set_gain(self.gain, 0)
        self.uhd_usrp_sink_0_0.set_gain(self.gain, 0)
        self.uhd_usrp_source_0.set_gain(self.gain, 0)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_freq, self.samp_rate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.uhd_usrp_sink_0.set_bandwidth(self.bandwidth, 0)
        self.uhd_usrp_sink_0_0.set_bandwidth(self.bandwidth, 0)




def main(top_block_cls=default, options=None):

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
