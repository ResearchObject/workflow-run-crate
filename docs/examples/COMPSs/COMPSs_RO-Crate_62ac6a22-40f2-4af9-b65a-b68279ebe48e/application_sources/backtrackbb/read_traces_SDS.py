# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import sys
import os
import numpy as np
from glob import glob
from obspy.clients.filesystem.sds import Client
from obspy.core import read, Stream, UTCDateTime


# def read_traces_real_data(config, basepath, traces):
#     kwargs = {}
#     if config.data_format:
#         kwargs["format"] = config.data_format
#         print("Data format: %s" % config.data_format)
#
#     tmpst = Stream()
#
#     # ---Here we expect that start_time and end_time are always provided
#     start_t = UTCDateTime(config.start_time)
#     end_t = UTCDateTime(config.end_time)
#     time_lag = config.time_lag
#     t_overlap = config.t_overlap
#     # ---
#     # --- Making list of time-windows
#     t_bb = np.arange(
#         start_t - start_t + config.start_t,
#         end_t - start_t + config.start_t,
#         time_lag - t_overlap,
#     )
#     t_end = t_bb + time_lag
#     time_length = abs(end_t - start_t)
#     t_bb = t_end[t_end <= time_length] - time_lag
#     t_end = t_bb + time_lag
#     # -----------------------------------------------------------
#
#     if config.dataarchive_type == "SDS":
#         print("SDS Data Archive type")
#         client = Client(basepath)
#         tmpst = client.get_waveforms(
#             config.data_network, "*", "*", "*", start_t, end_t
#         )
#     else:
#         for filename in traces:
#             try:
#                 if config.start_time:
#                     tmpst += read(
#                         filename,
#                         starttime=start_t,
#                         endtime=end_t,
#                         **kwargs
#                     )
#                 else:
#                     tmpst += read(filename, **kwargs)
#             except Exception:
#                 continue
#
#     # Get the intersection between the list of available stations
#     # and the list of requested stations:
#     tmpst_select = Stream()
#     for ch in config.channel:
#         tmpst_select += tmpst.select(channel=ch)
#     tmpst_stations = [tr.stats.station for tr in tmpst_select]
#     stations = sorted(set(tmpst_stations) & set(config.stations))
#
#     # Retain only requested channel and stations:
#     print("Attempting to create stream.")
#     sys.stdout.write("Attempting to create stream.\n")
#     sys.stdout.write(str(tmpst_select) + "\n")
#     sys.stdout.write(str(stations) + "\n")
#     sys.stdout.flush()
#     st = Stream(tr for tr in tmpst_select if tr.stats.station in stations)
#     if not st:
#         print("Could not read any trace!")
#         sys.exit(1)
#     st.sort()
#
#     # --- Check for gaps and time-window adjustment:
#     gaps_sta = {}
#     sta_nodata = []
#     stagaps = []
#     for ssta in stations:
#         gaps_sta[ssta] = []
#         tmpst = st.select(station=ssta)
#         #
#         # --- Checking start-end of the trace
#         tr_start = abs(tmpst[0].stats.starttime - start_t)
#         tr_end = abs(tmpst[-1].stats.endtime - start_t)
#         lendat_sec = tr_end - tr_start
#         if lendat_sec < (end_t - start_t) / 3:
#             # print(ssta, 'short data')
#             if station not in sta_nodata:
#                 sta_nodata.append(station)
#         #
#         gaps_tmp = tmpst.get_gaps()
#         # print(tmpst, len(tmpst.get_gaps()))
#         #
#         # -- list of gap starts&ends in seconds from start_t
#         sta_gapbeg = [gg[4] - start_t for gg in gaps_tmp]
#         sta_gapend = [gg[5] - start_t for gg in gaps_tmp]
#         for idg in range(len(gaps_tmp)):
#             gstart = sta_gapbeg[idg]
#             gend = sta_gapend[idg]
#             idx1 = (np.abs(t_bb - gstart)).argmin()
#             idx2 = (np.abs(t_bb - gend)).argmin()
#             dte = min(t_bb - gend)
#             # print(gstart, idx1, gend, idx2)
#             gaps_sta[ssta].append([idx1, idx2])
#         idx1 = (np.abs(t_bb - tr_start)).argmin()
#         idx2 = (np.abs(t_bb - tr_end)).argmin()
#         # print(station, idx1, idx2, len(t_bb[idx1:idx2+1]), len(t_bb))
#         if len(t_bb[idx1 : idx2 + 1]) < len(t_bb):
#             if idx1 > 0:
#                 gst1 = [0, idx1]
#                 gaps_sta[ssta].append(gst1)
#             if idx2 < len(t_bb) - 1:
#                 gst2 = [idx2 + 1, len(t_bb) - 1]
#                 gaps_sta[ssta].append(gst2)
#
#         if len(gaps_sta[ssta]) > 0 and ssta not in stagaps and ssta not in sta_nodata:
#             stagaps.append(ssta)
#
#     # Remove stations with too short data
#     for sta in sta_nodata:
#         for tr in st.select(station=sta):
#             st.remove(tr)
#
#     persta = np.round(100.0 / len(stations) * len(stagaps), 0)
#     if persta < 10.0:
#         for sta in stagaps:
#             for tr in st.select(station=sta):
#                 st.remove(tr)
#         tbb_adj = t_bb
#         tend_adj = np.array(tbb_adj) + time_lag
#     else:
#         st.merge(method=1, fill_value="interpolate")
#         idwin_not = []
#         for kk in gaps_sta.keys():
#             #
#             for gg in gaps_sta[kk]:
#                 ids = [i for i in range(gg[0], gg[1] + 1) if i not in idwin_not]
#                 for ii in ids:
#                     idwin_not.append(ii)
#         if len(idwin_not) > 0:
#             #
#             tbb_adj = [t_bb[i] for i in range(len(t_bb)) if i not in idwin_not]
#             tend_adj = np.array(tbb_adj) + time_lag
#         else:
#             # print('No gaps in data')
#             tbb_adj = t_bb
#             tend_adj = np.array(tbb_adj) + time_lag
#     # -------------------------------------------------------------------------
#
#     # Check sampling rate
#     config.delta = None
#     for tr in st:
#         tr.detrend(type="constant")
#         tr.taper(type="hann", max_percentage=0.005, side="left")
#         sampling_rate = tr.stats.sampling_rate
#         # Resample data, if requested
#         if config.sampl_rate_data:
#             if sampling_rate >= config.sampl_rate_data:
#                 dec_ct = int(sampling_rate / config.sampl_rate_data)
#                 tr.decimate(dec_ct, strict_length=False, no_filter=True)
#             else:
#                 raise ValueError(
#                     "Sampling frequency for trace %s is lower than %s"
#                     % (tr.id, config.sampl_rate_data)
#                 )
#         delta = tr.stats.delta
#         if config.delta is None:
#             config.delta = delta
#         else:
#             if delta != config.delta:
#                 raise ValueError(
#                     "Trace %s has different delta: %s (expected: %s)"
#                     % (tr.id, delta, config.delta)
#                 )
#     # Recompute sampling rate after resampling
#     config.sampl_rate_data = st[0].stats.sampling_rate
#
#     # ---Will not actually need it with Gap check  --- Check if true!!!
#     # Check for common starttime and endtime of the traces
#     # st_starttime = max([tr.stats.starttime for tr in st])
#     # st_endtime = min([tr.stats.endtime for tr in st])
#     # if config.start_time:
#     #     st.trim(max(st_starttime, UTCDateTime(config.start_time)),
#     #             min(st_endtime, UTCDateTime(config.end_time)))
#     # else:
#     #     st.trim(st_starttime, st_endtime)
#
#     # --- cut the data to the selected length dt------------------------------
#     if config.cut_data:
#         st.trim(
#             st[0].stats.starttime + config.cut_start,
#             st[0].stats.starttime + config.cut_start + config.cut_delta,
#         )
#     else:
#         config.cut_start = 0.0
#
#     # config.starttime = st[0].stats.starttime
#     config.starttime = start_t
#
#     # attach station list and trace ids to config file
#     config.stations = [tr.stats.station for tr in st]
#     config.trids = [tr.id for tr in st]
#
#     print("Number of traces in stream = ", len(st))
#     # st.plot()
#     return st, tbb_adj

def read_traces_SDS(config, basepath):
    kwargs = {}
    if config.data_format:
        kwargs["format"] = config.data_format
        print("Data format: %s" % config.data_format)

    tmpst = Stream()

    # ---Here we expect that start_time and end_time are always provided
    start_t = UTCDateTime(config.start_time)
    end_t = UTCDateTime(config.end_time)
    time_lag = config.time_lag
    t_overlap = config.t_overlap
    # ---
    # --- Making list of time-windows
    t_bb = np.arange(
        start_t - start_t + config.start_t,
        end_t - start_t + config.start_t,
        time_lag - t_overlap,
    )
    t_end = t_bb + time_lag
    time_length = abs(end_t - start_t)
    t_bb = t_end[t_end <= time_length] - time_lag
    t_end = t_bb + time_lag
    # -----------------------------------------------------------

    # config.dataarchive_type == "SDS":
    print("SDS Data Archive type")
    client = Client(basepath)
    tmpst = client.get_waveforms(
        config.data_network, "*", "*", "*", start_t, end_t
    )

    # Get the intersection between the list of available stations
    # and the list of requested stations:
    tmpst_select = Stream()
    for ch in config.channel:
        tmpst_select += tmpst.select(channel=ch)
    tmpst_stations = [tr.stats.station for tr in tmpst_select]
    stations = sorted(set(tmpst_stations) & set(config.stations))

    # Retain only requested channel and stations:
    st = Stream(tr for tr in tmpst_select if tr.stats.station in stations)
    if not st:
        print("Could not read any trace!")
        sys.exit(1)
    st.sort()

    # --- Check for gaps and time-window adjustment:
    gaps_sta = {}
    sta_nodata = []
    stagaps = []
    for ssta in stations:
        gaps_sta[ssta] = []
        tmpst = st.select(station=ssta)
        #
        # --- Checking start-end of the trace
        tr_start = abs(tmpst[0].stats.starttime - start_t)
        tr_end = abs(tmpst[-1].stats.endtime - start_t)
        lendat_sec = tr_end - tr_start
        if lendat_sec < (end_t - start_t) / 3:
            # print(ssta, 'short data')
            if ssta not in sta_nodata:
                sta_nodata.append(ssta)
                continue
        #
        gaps_tmp = tmpst.get_gaps()
        # print(tmpst, len(tmpst.get_gaps()))
        #
        # -- list of gap starts&ends in seconds from start_t
        sta_gapbeg = [gg[4] - start_t for gg in gaps_tmp]
        sta_gapend = [gg[5] - start_t for gg in gaps_tmp]
        for idg in range(len(gaps_tmp)):
            gstart = sta_gapbeg[idg]
            gend = sta_gapend[idg]
            idx1 = (np.abs(t_bb - gstart)).argmin()
            idx2 = (np.abs(t_bb - gend)).argmin()
            dte = min(t_bb - gend)
            # print(gstart, idx1, gend, idx2)
            gaps_sta[ssta].append([idx1, idx2])
        # idx1 = (np.abs(t_bb - tr_start)).argmin()
        # idx2 = (np.abs(t_bb - tr_end)).argmin()
        idx1 = np.argwhere((t_bb - tr_start) >= 0)[0][0]
        idx2 = np.argwhere((tr_end - t_end) >= 0)[-1][0]
        # print(station, idx1, idx2, len(t_bb[idx1:idx2+1]), len(t_bb))
        if len(t_bb[idx1 : idx2 + 1]) < len(t_bb):
            if idx1 > 0:
                gst1 = [0, idx1]
                gaps_sta[ssta].append(gst1)
            if idx2 < len(t_bb) - 1:
                gst2 = [idx2 + 1, len(t_bb) - 1]
                gaps_sta[ssta].append(gst2)

        if len(gaps_sta[ssta]) > 0 and ssta not in stagaps and ssta not in sta_nodata:
            stagaps.append(ssta)

    # Remove stations with too short data
    for sta in sta_nodata:
        for tr in st.select(station=sta):
            st.remove(tr)

    persta = np.round(100.0 / len(stations) * len(stagaps), 0)
    if persta < 10.0:
        for sta in stagaps:
            for tr in st.select(station=sta):
                st.remove(tr)
        tbb_adj = t_bb
        tend_adj = np.array(tbb_adj) + time_lag
    else:
        st.merge(method=1, fill_value="interpolate")
        idwin_not = []
        for kk in gaps_sta.keys():
            #
            for gg in gaps_sta[kk]:
                ids = [i for i in range(gg[0], gg[1] + 1) if i not in idwin_not]
                for ii in ids:
                    idwin_not.append(ii)
        if len(idwin_not) > 0:
            #
            tbb_adj = [t_bb[i] for i in range(len(t_bb)) if i not in idwin_not]
            tend_adj = np.array(tbb_adj) + time_lag
        else:
            # print('No gaps in data')
            tbb_adj = t_bb
            tend_adj = np.array(tbb_adj) + time_lag
    # -------------------------------------------------------------------------
    # Check sampling rate -----------------------------------------------------
    config.delta = None
    for tr in st:
        tr.detrend(type="constant")
        tr.taper(type="hann", max_percentage=0.005, side="left")
        sampling_rate = tr.stats.sampling_rate
        # Resample data, if requested
        if config.sampl_rate_data:
            if sampling_rate >= config.sampl_rate_data:
                dec_ct = int(sampling_rate / config.sampl_rate_data)
                tr.decimate(dec_ct, strict_length=False, no_filter=True)
            else:
                raise ValueError(
                    "Sampling frequency for trace %s is lower than %s"
                    % (tr.id, config.sampl_rate_data)
                )
        delta = tr.stats.delta
        if config.delta is None:
            config.delta = delta
        else:
            if delta != config.delta:
                raise ValueError(
                    "Trace %s has different delta: %s (expected: %s)"
                    % (tr.id, delta, config.delta)
                )
    # Recompute sampling rate after resampling
    config.sampl_rate_data = st[0].stats.sampling_rate

    # ---Will not actually need it with Gap check  --- Check if true!!!
    # Check for common starttime and endtime of the traces
    # st_starttime = max([tr.stats.starttime for tr in st])
    # st_endtime = min([tr.stats.endtime for tr in st])
    # if config.start_time:
    #     st.trim(max(st_starttime, UTCDateTime(config.start_time)),
    #             min(st_endtime, UTCDateTime(config.end_time)))
    # else:
    #     st.trim(st_starttime, st_endtime)

    # --- cut the data to the selected length dt------------------------------
    if config.cut_data:
        st.trim(
            st[0].stats.starttime + config.cut_start,
            st[0].stats.starttime + config.cut_start + config.cut_delta,
        )
    else:
        config.cut_start = 0.0

    # config.starttime = st[0].stats.starttime
    config.starttime = start_t

    # attach station list and trace ids to config file
    config.stations = [tr.stats.station for tr in st]
    config.trids = [tr.id for tr in st]

    print("Number of traces in stream = ", len(st))
    # st.plot()
    return st, tbb_adj
