#!/usr/bin/env python

import os
import numpy as np
from tqdm import tqdm


from phylib.utils import Bunch
from phylib.io.model import load_model
from phy.apps.template.gui import TemplateController


def _get_waveforms_with_n_spikes(
        self, cluster_id, n_spikes_waveforms, current_filter=None):
    pos = self.model.channel_positions
    if self.model.spike_waveforms is not None:
        subset_spikes = self.model.spike_waveforms.spike_ids
        spike_ids = self.selector(
            n_spikes_waveforms, [cluster_id], subset_spikes=subset_spikes)
    else:
        spike_ids = self.selector(n_spikes_waveforms, [cluster_id], subset_chunks=True)

    channel_ids = self.get_best_channels(cluster_id)
    channel_labels = self._get_channel_labels(channel_ids)
    data = self.model.get_waveforms(spike_ids, channel_ids)
    if data is not None:
        data = data - np.median(data, axis=1)[:, np.newaxis, :]
    assert data.ndim == 3  # n_spikes, n_samples, n_channels
    if data is not None:
        data = self.raw_data_filter.apply(data, axis=1)
    return Bunch(
        data=data,
        channel_ids=channel_ids,
        channel_labels=channel_labels,
        channel_positions=pos[channel_ids],
    )

def get_waveforms(result, n_spikes_waveform=100):
    os.makedirs(result + '.log', exist_ok=True)
    model = load_model(result + 'params.py')
    controller = TemplateController(model=model, dir_path=result + '.log')
    
    ws = {}
    for i in tqdm(range(model.n_clusters)):
        try:
            w = _get_waveforms_with_n_spikes(controller, i, n_spikes_waveform)
            w = w.data[:,:,0]
            ws[i] = w
        except:
            pass

    return ws