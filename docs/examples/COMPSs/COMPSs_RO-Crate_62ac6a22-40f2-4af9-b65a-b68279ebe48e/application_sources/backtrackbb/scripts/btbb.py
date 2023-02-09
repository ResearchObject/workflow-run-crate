# -*- coding: utf8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import time
import numpy as np
from glob import glob
from obspy import Stream
from collections import defaultdict

from pycompss.api.task import task
from pycompss.api.parameter import INOUT
from pycompss.api.parameter import FILE_OUT
from pycompss.api.parameter import COLLECTION_IN
from pycompss.api.parameter import COLLECTION_FILE_IN
from pycompss.api.parameter import Type, Depth
from pycompss.api.api import compss_wait_on
from pycompss.api.api import compss_barrier

from backtrackbb.mod_setup import configure
from backtrackbb.read_traces import read_traces
from backtrackbb.init_filter import init_filter
from backtrackbb.read_grids import read_grid  # notice read_grid instead read_grids
from backtrackbb.summary_cf import summary_cf, empty_cf
from backtrackbb.mod_utils import read_locationTremor, read_locationEQ
from backtrackbb.plot import plt_SummaryOut
from backtrackbb.rec_memory import init_recursive_memory
from backtrackbb.mod_btbb import run_btbb


DEBUG = True

@task(returns=3, config=INOUT, traces=COLLECTION_FILE_IN)
def reading_data(config, basepath, traces):
    #---Reading data---------------------------------------------------------
    #st = read_traces(config)  # old method - can cause issues with paths
    st = read_traces(config, basepath, traces)
    #------------------------------------------------------------------------
    t_bb = np.arange(config.start_t, config.end_t,
                     config.time_lag - config.t_overlap)
    # selecting the time windows that do not exceed the length of the data---
    t_ee = t_bb + config.time_lag
    data_length = st[0].stats.endtime - st[0].stats.starttime
    t_bb = t_ee[t_ee <= data_length] - config.time_lag
    print('Number of time windows = ', len(t_bb))
    #------------------------------------------------------------------------
    return st, t_bb, t_ee

@task(returns=1, st=INOUT)
def remove_mean_and_trend(st):
    #---remove mean and trend------------------------------------------------
    st.detrend(type='constant')
    st.detrend(type='linear')
    #------------------------------------------------------------------------


@task(returns=1, p_outputs=COLLECTION_IN)
def filter_outputs(p_outputs):
    #----filter outputs------------------------------------------------------
    triggers = list(filter(None, p_outputs))
    return triggers
    #------------------------------------------------------------------------


@task(file_out_triggers=FILE_OUT)
def write_outputs(file_out_triggers, triggers):
    #----------Outputs-------------------------------------------------------
    #writing output
    eventids = []
    with open(file_out_triggers, 'w') as f:
        for trigger in triggers:
            # check if eventid already exists
            while trigger.eventid in eventids:
                # increment the last letter by one
                evid = list(trigger.eventid)
                evid[-1] = chr(ord(evid[-1]) + 1)
                trigger.eventid = ''.join(evid)
            eventids.append(trigger.eventid)
            f.write(str(trigger) + '\n')
            # sort picks by station
            picks = sorted(trigger.picks, key=lambda x: x.station)
            for pick in picks:
                f.write(str(pick) + '\n')
    #------------------------------------------------------------------------


def main():
    start_time = time.time()

    config = configure()

    var_twin = config.varWin_stationPair
    print('use of var time window for location:', var_twin)

    #---Reading data---------------------------------------------------------
    basepath = config.data_dir
    if config.data_day:
        basepath = os.path.join(basepath, config.data_day)
        if config.data_hours:
            basepath = os.path.join(basepath, config.data_hours)
    traces = glob(os.path.join(basepath, '*'))

    st, t_bb, t_ee = reading_data(config, basepath, traces)  # TASK

    loc_infile = None
    location_jma = None
    if config.catalog_dir:
        if config.data_day:
            loc_infile = os.path.join(config.catalog_dir,
                                      config.data_day + config.tremor_file)
        location_jma = os.path.join(config.catalog_dir, config.eq_file)
    #------------------------------------------------------------------------

    #--Read grids of theoretical travel-times--------------------------------
    GRD_sta = defaultdict(dict)
    coord_sta = {}
    for grid_type in config.grid_type:
        for station in config.stations:
            grid_bname = '.'.join(('*', grid_type, station, 'time.hdr'))
            grid_bname = os.path.join(config.grid_dir, grid_bname)
            grid_bname = glob(grid_bname)[0]
            GRD_sta[station][grid_type], coord_sta[station] = read_grid(grid_bname)  # TASK
    #------------------------------------------------------------------------

    #---remove mean and trend------------------------------------------------
    remove_mean_and_trend(st)  # TASK
    #------------------------------------------------------------------------

    #---init filtering parameters--------------------------------------------
    init_filter(config)  # TASK

    config = compss_wait_on(config)
    st = compss_wait_on(st)

    if config.recursive_memory:
        rec_memory = init_recursive_memory(config)  # TASK
        st_CF = empty_cf(config, st)  # TASK
        if DEBUG:
            st_CF2 = summary_cf(config, st)  # TASK
    else:
        rec_memory = None
        st_CF = summary_cf(config, st)  # TASK
    #------------------------------------------------------------------------

    #----geographical coordinates of the eq's epicenter----------------------
    coord_eq = None
    if loc_infile:
        coord_eq = read_locationTremor(loc_infile, config)  # TASK
    coord_jma = None
    if location_jma:
        coord_jma = read_locationEQ(location_jma, config)  # TASK
    #------------------------------------------------------------------------
    print('starting BPmodule')

    #-----Create out_dir, if it doesn't exist--------------------------------
    if not os.path.exists(config.out_dir):  # TODO: move to top
        os.mkdir(config.out_dir)

    datestr = st[0].stats.starttime.strftime('%y%m%d%H')
    fq_str = '%s_%s' % (np.round(config.frequencies[0]),
                        np.round(config.frequencies[-1]))
    ch_str = str(config.channel)[1:-1].replace("'", "")
    file_out_base = '_'.join((
        datestr,
        str(len(config.frequencies)) + 'fq' + fq_str + 'hz',
        str(config.decay_const) + str(config.sampl_rate_cf) +
        str(config.smooth_lcc) + str(config.t_overlap),
        config.ch_function,
        ch_str,
        ''.join(config.wave_type),
        'trig' + str(config.trigger)
        ))

    #------------------------------------------------------------------------

    t_bb = compss_wait_on(t_bb)
    for k in coord_sta.keys():
        coord_sta[k] = compss_wait_on(coord_sta[k])
    for x in GRD_sta.keys():
        for y in GRD_sta[x].keys():
            GRD_sta[x][y] = compss_wait_on(GRD_sta[x][y])

    #---Take the first grid as reference ------------------------------------
    grid1 = list(list(GRD_sta.values())[0].values())[0]
    #------------------------------------------------------------------------

    #---running program------------------------------------------------------
    p_outputs = []
    for t_begin in t_bb:

        fq_str = '%s_%s' % (str(np.round(config.frequencies[0])),
                            str(np.round(config.frequencies[-1])))
        datestr = st[0].stats.starttime.strftime('%y%m%d%H')

        file_out_fig =\
            datestr + '_t' + '%06.1f' % (config.cut_start+t_begin) +\
            's_' + fq_str + '_fig.' + config.plot_format
        file_out_fig = os.path.join(config.out_dir, file_out_fig)

        p_outputs.append(run_btbb(config,
                                  st,
                                  st_CF,
                                  t_begin,
                                  coord_eq,
                                  coord_sta,
                                  rec_memory,
                                  grid1,
                                  GRD_sta,
                                  file_out_fig))  # run_btbb TASK
    #------------------------------------------------------------------------

    #----filter outputs------------------------------------------------------
    triggers = filter_outputs(p_outputs)  # TASK
    #------------------------------------------------------------------------

    #----------Outputs-------------------------------------------------------
    file_out_triggers = file_out_base + '_OUT2.dat'
    file_out_triggers = os.path.join(config.out_dir, file_out_triggers)
    write_outputs(file_out_triggers, triggers)  # TASK
    #------------------------------------------------------------------------

    #-plot summary output----------------------------------------------------
    file_out_fig = file_out_base + '_FIG2.' + config.plot_format
    file_out_fig = os.path.join(config.out_dir, file_out_fig)
    plt_SummaryOut(config, grid1, st_CF, st, coord_sta,
                   triggers, t_bb, datestr,
                   coord_eq, coord_jma, file_out_fig)  # TASK
    #------------------------------------------------------------------------

    if DEBUG:
        import matplotlib.pyplot as plt
        st_CF = compss_wait_on(st_CF)
        st_CF2 = compss_wait_on(st_CF2)
        CF = st_CF.select(station=config.stations[0])[0]
        CF2 = st_CF2.select(station=config.stations[0])[0]
        fig = plt.figure()
        ax1 = fig.add_subplot(211)
        ax1.plot(CF, linewidth=2)
        ax1.plot(CF2[0:len(CF)])
        ax2 = fig.add_subplot(212, sharex=ax1)
        ax2.plot(CF - CF2[0:len(CF)])
        plt.show()

    compss_barrier()
    print("Elapsed time: " + str(time.time() - start_time))

if __name__ == '__main__':
    main()
