import pathlib
import pickle

import matplotlib.pyplot as plt
import numpy as np
from labrad.units import GHz
from lqcs.utils.config_analysis import map2brand

DEBUG_PATH = pathlib.Path.home() / '.lqcs' / 'debug'
DEFULT_SAVE_PATH = DEBUG_PATH / 'device2runtime'

SAMPLING_RATE = {
    'Beijing': 2 * GHz,
    'UCSB': 1 * GHz,
    'MF': 2 * GHz,
    'LQ': 1 * GHz,
}

DAC_RESOLUTION = {b: 1 / SAMPLING_RATE[b] for b in SAMPLING_RATE}

plt.ion()


class debugger:
    """
    可视化 device2runtime_cmd

    """

    def __init__(self, path=None, auto_reload=True):
        if path is None:
            path = DEFULT_SAVE_PATH
        self.path = path
        self.auto_reload = auto_reload

        self.load()

    def load(self):
        with open(self.path, 'rb') as f:
            self.data = pickle.load(f)

    def plot_wave(self, device_name, channels, fig=1, ax=None, **kwargs):
        """
        画出特定板卡通道的波形，支持同时绘制多通道数据

        device_name: str
            例: 'DAC_Beijing 1', 'ADC_Beijing 1'
        channels: iterable
            例：['A', 'B'] or 'AB'

        """
        if self.auto_reload:
            self.load()

        data = self.data
        tlists_ns = data['tlists_ns']
        tlist_resolution_ns = tlists_ns[0][1] - tlists_ns[0][0]

        # plt.figure(fig, figsize=(16, 8))
        if 'dac' in device_name.lower():
            channel_runtime = data[device_name]['runtime_state']['channel_runtime']
            # dac resolution
            dac_resolution_ns = DAC_RESOLUTION[map2brand(device_name)]['ns']
            idx_interval = int(dac_resolution_ns / tlist_resolution_ns)
            for ch in channels:
                if 'wave' not in channel_runtime[ch]:  # 例：其中一个比特没有读取波形
                    continue
                for t, w in zip(tlists_ns, channel_runtime[ch]['wave']):
                    ax.plot(t[::idx_interval], w, label=f'{device_name} {ch}')
            plt.title(
                f'sequence length = {(tlists_ns[-1][-1] - tlists_ns[0][0] + 0.5) / 1000} us',
                fontsize=15,
            )  # 0.5是DAC分辨率
        elif 'adc' in device_name.lower():
            device_runtime = data[device_name]['runtime_state']
            if len(device_runtime['demod_qubits']):
                adc_start_delay = device_runtime['adc_start_delay']
                record_delays = device_runtime['record_delays']
                record_lengths = device_runtime['record_lengths']
                for d, l in zip(record_delays, record_lengths):
                    if l != 0:
                        d += tlists_ns[0][0]
                        for _ in [adc_start_delay + d, adc_start_delay + d + l]:
                            plt.vlines(
                                _,
                                ymin=-1,
                                ymax=1,
                                linestyles='--',
                                linewidth=2,
                                color='k',
                            )

        plt.xlabel('Time (ns)', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.tick_params(labelsize=10)
        plt.legend(fontsize=15)
        # plt.xlim(0, 2500)
        plt.show()

    def plot_device(self, device_name='all', fig=1, **kwargs):
        """
        画出特定 device (qubit, coupler...) 的波形

        params:
            device_name (str): 'q1', 'all'

        """
        if self.auto_reload:
            self.load()

        data = self.data

        if device_name == 'all':
            device_name = list(data['qubit2board_channel'].keys())
        elif not isinstance(device_name, (list, tuple, np.ndarray)):
            device_name = [device_name]

        _device_name = [_ for _ in device_name if _.startswith('q') or _.startswith('c')]
        _device_num = len(_device_name)

        # fig = plt.figure(fig,figsize=(16, 8))
        plt.subplots(len(_device_name), 1, sharex=True, sharey=False, figsize=(16, 8))
        for idx, dn in enumerate(_device_name):
            assert dn in data['qubit2board_channel'], f'No such device: {dn}'

            ax = plt.subplot(_device_num, 1, idx + 1)

            qubit2board_channel = data['qubit2board_channel'][dn]

            for board_type, info in qubit2board_channel.items():
                if board_type in ['meas', 'uwave', 'readout uwave', 'mark']:
                    board_name, channels = info['dac_name'], info['dac_channel']
                elif board_type in ['readout ADC']:
                    board_name, channels = info['adc_name'], None
                else:
                    continue

                self.plot_wave(board_name, channels, fig=fig, ax=ax, **kwargs)
            if idx < (len(device_name) - 1):
                plt.xlabel('')
            plt.legend(loc='upper left')
            plt.title(dn, fontsize=12)
        plt.tight_layout()
