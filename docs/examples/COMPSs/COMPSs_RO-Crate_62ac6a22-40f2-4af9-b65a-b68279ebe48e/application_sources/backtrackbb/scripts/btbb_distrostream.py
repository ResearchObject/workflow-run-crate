# -*- coding: utf8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

import os
import sys
import time
import math
import shutil
import numpy as np
from glob import glob

from pycompss.api.task import task
from pycompss.api.parameter import (
    IN,
    OUT,
    INOUT,
    FILE_OUT,
    COLLECTION_IN,
    COLLECTION_OUT,
    COLLECTION_FILE_IN,
    COLLECTION_FILE_OUT,
    DICTIONARY_IN,
    STREAM_IN,
    STREAM_OUT,
    Type,
    Depth,
)
from pycompss.api.api import compss_wait_on
from pycompss.api.api import compss_barrier
from pycompss.api.api import compss_delete_object
from pycompss.streams.distro_stream import FileDistroStream


from backtrackbb.mod_setup import configure
from backtrackbb.read_traces import read_traces
from backtrackbb.init_filter import init_filter
from backtrackbb.read_grids import (
    read_grid,
)  # notice read_grid instead read_grids
from backtrackbb.summary_cf import summary_cf, empty_cf
from backtrackbb.mod_utils import read_locationTremor, read_locationEQ
from backtrackbb.plot import plt_SummaryOut
from backtrackbb.rec_memory import init_recursive_memory
from backtrackbb.mod_btbb import run_btbb
from backtrackbb.mod_btbb import run_btbb_no_fig


DEBUG = False


def create_folder(folder):
    os.makedirs(folder)
    print("Created: " + str(folder))


def clean_folder(folder):
    shutil.rmtree(folder, ignore_errors=True)


@task(
    fds=STREAM_OUT, id=IN, data_path=IN, days=IN, hours=IN, sleep=IN,
)
def write_files(fds, id, data_path, days, hours, sleep):
    """Simulates a station that generates data."""
    src_filename = f"IM.{id}.00.UD"  # id = STXXX
    dst_path = fds.base_dir
    for d in days:
        for h in hours:
            # Build src and dst names
            d = str(d).zfill(2)
            h = str(h).zfill(2)
            dst_filename = f"{d}_{h}_{id}"
            src = os.path.join(data_path, d, h, src_filename)
            dst = os.path.join(dst_path, dst_filename)

            # Write file
            print(f"Generating file: {dst}")
            shutil.copy(src, dst)

            # Sleep between generated files
            time.sleep(sleep)

    # Mark the stream for closure
    fds.close()


# @task(returns=COLLECTION_FILE_OUT, fds=STREAM_IN, n_stations=IN, sleep=IN)
def read_files(fds, n_stations, sleep):
    """Read the data from the stations as it is generated."""
    traces = dict()

    while not fds.is_closed():
        print(".", end="")
        new_files = fds.poll()
        if len(new_files) > 0:
            print("\nReceived files:")
            for nf in sorted(new_files):
                print(os.path.basename(nf))

        for nf in sorted(new_files):
            d, h, _ = os.path.basename(nf).split("_")
            key = d + h
            if key not in traces.keys():
                traces[key] = []
            traces[key].append(nf)
            if len(traces[key]) == n_stations:
                print(f"\nReceived all: {key}")
                print("Summary: %s" % [(k, len(v)) for k, v in traces.items()])
                yield key, traces[key]

        # Sleep between requests
        time.sleep(sleep)

    new_files = fds.poll()
    for nf in sorted(new_files):
        d, h, _ = os.path.basename(nf).split("_")
        key = d + h
        if key not in traces.keys():
            traces[key] = []
        traces[key].append(nf)
        if len(traces[key]) == n_stations:
            print(f"\nAll received: {key}")
            print("Summary: %s" % [(k, len(v)) for k, v in traces.items()])
            yield key, traces[key]

    print("Finished polling files.")


@task(returns=3, config=INOUT, traces=COLLECTION_FILE_IN)
def reading_data(config, basepath, traces):
    # ---Reading data---------------------------------------------------------
    # st = read_traces(config)  # old method - can cause issues with paths
    st = read_traces(config, basepath, traces)
    # ------------------------------------------------------------------------
    t_bb = np.arange(
        config.start_t, config.end_t, config.time_lag - config.t_overlap
    )
    # selecting the time windows that do not exceed the length of the data---
    t_ee = t_bb + config.time_lag
    data_length = st[0].stats.endtime - st[0].stats.starttime
    t_bb = t_ee[t_ee <= data_length] - config.time_lag
    print("Number of time windows = ", len(t_bb))
    # ------------------------------------------------------------------------
    return st, t_bb, t_ee


@task(returns=1, st=INOUT)
def remove_mean_and_trend(st):
    # ---remove mean and trend------------------------------------------------
    st.detrend(type="constant")
    st.detrend(type="linear")
    # ------------------------------------------------------------------------


@task(returns=1, p_outputs=COLLECTION_IN)
def filter_outputs(p_outputs):
    # ----filter outputs------------------------------------------------------
    # new:
    p_outputs = np.concatenate(p_outputs).ravel().tolist()  # flatten
    triggers = list(filter(None, p_outputs))
    return triggers
    # ------------------------------------------------------------------------


@task(file_out_triggers=FILE_OUT)
def write_outputs(file_out_triggers, triggers):
    # ----------Outputs-------------------------------------------------------
    # writing output
    eventids = []
    with open(file_out_triggers, "w") as f:
        for trigger in triggers:
            # check if eventid already exists
            while trigger.eventid in eventids:
                # increment the last letter by one
                evid = list(trigger.eventid)
                evid[-1] = chr(ord(evid[-1]) + 1)
                trigger.eventid = "".join(evid)
            eventids.append(trigger.eventid)
            f.write(str(trigger) + "\n")
            # sort picks by station
            picks = sorted(trigger.picks, key=lambda x: x.station)
            for pick in picks:
                f.write(str(pick) + "\n")
    # ------------------------------------------------------------------------


def main(fds, n_stations, all_config_paths, tw_x_task, consumer_sleep):

    start_time = time.time()

    # Process all configs
    all_configs = []
    for key, traces in read_files(fds, n_stations, consumer_sleep):
        # force a new cfg as sys.argv
        cfg = all_config_paths[key]
        print("Processing config: " + str(cfg))
        sys.argv = ["btbb_continuous.py", cfg]

        config = configure()

        var_twin = config.varWin_stationPair
        print("use of var time window for location:", var_twin)
        # ---Reading data------------------------------------------------------
        st, t_bb, t_ee = reading_data(config, None, traces)  # TASK

        loc_infile = None
        location_jma = None
        # if config.catalog_dir:
        #     if config.data_day:
        #         loc_infile = os.path.join(
        #             config.catalog_dir, config.data_day + config.tremor_file
        #         )
        #     location_jma = os.path.join(config.catalog_dir, config.eq_file)
        # ---------------------------------------------------------------------

        # ---remove mean and trend---------------------------------------------
        remove_mean_and_trend(st)  # TASK
        # ---------------------------------------------------------------------

        # ---init filtering parameters-----------------------------------------
        init_filter(config)  # TASK

        all_configs.append([config, st, t_bb])

    # --Read grids of theoretical travel-times--------------------------------
    # GRD_sta = defaultdict(dict)
    GRD_sta = {}
    coord_sta = {}
    first_station = None
    first_grid_type = None
    for grid_type in config.grid_type:
        for station in config.stations:
            grid_bname = ".".join(("layer", grid_type, station, "time.hdr"))
            grid_bname = os.path.join(config.grid_dir, grid_bname)
            grid_bname = glob(grid_bname)[0]
            GRD_sta[station] = {}
            GRD_sta[station][grid_type], coord_sta[station] = read_grid(
                grid_bname
            )  # TASK
            if first_station is None and first_grid_type is None:
                first_station = station
                first_grid_type = grid_type
    # ------------------------------------------------------------------------

    # sync configs:
    # all_configs = compss_wait_on(all_configs)
    sync_all_configs = []
    for config, st, t_bb in all_configs:
        config = compss_wait_on(config)
        st = compss_wait_on(st)
        t_bb = compss_wait_on(t_bb)
        sync_all_configs.append([config, st, t_bb])
    all_configs = sync_all_configs

    # ---Take the first grid as reference ------------------------------------
    # for x in GRD_sta.keys():
    #     for y in GRD_sta[x].keys():
    #         GRD_sta[x][y] = compss_wait_on(GRD_sta[x][y])
    # grid1 = list(list(GRD_sta.values())[0].values())[0]

    grid1 = GRD_sta[first_station][first_grid_type]
    # grid1 = compss_wait_on(grid1)
    # GRD_sta[first_station][
    #     first_grid_type
    # ] = grid1  # replace since it has been removed at sync.
    # ------------------------------------------------------------------------

    # Next loop
    all_st_CF = []
    all_coord_eq = []
    all_rec_memory = []
    all_file_out_base = []
    for config, st, t_bb in all_configs:

        if config.recursive_memory:
            rec_memory = init_recursive_memory(config)  # TASK
            st_CF = empty_cf(config, st)  # TASK
            if DEBUG:
                st_CF2 = summary_cf(config, st)  # TASK
        else:
            rec_memory = None
            st_CF = summary_cf(config, st)  # TASK
        all_st_CF.append(st_CF)
        all_rec_memory.append(rec_memory)
        # ---------------------------------------------------------------------

        # ----geographical coordinates of the eq's epicenter-------------------
        coord_eq = None
        if loc_infile:
            coord_eq = read_locationTremor(loc_infile, config)  # TASK
        all_coord_eq.append(coord_eq)
        coord_jma = None
        if location_jma:
            coord_jma = read_locationEQ(location_jma, config)  # TASK
        # ---------------------------------------------------------------------
        print("starting BPmodule")

        # -----Create out_dir, if it doesn't exist-----------------------------
        if not os.path.exists(config.out_dir):  # TODO: move to top
            os.mkdir(config.out_dir)

        datestr = st[0].stats.starttime.strftime("%y%m%d%H")
        fq_str = "%s_%s" % (
            np.round(config.frequencies[0]),
            np.round(config.frequencies[-1]),
        )
        ch_str = str(config.channel)[1:-1].replace("'", "")
        file_out_base = "_".join(
            (
                datestr,
                str(len(config.frequencies)) + "fq" + fq_str + "hz",
                str(config.decay_const)
                + str(config.sampl_rate_cf)
                + str(config.smooth_lcc)
                + str(config.t_overlap),
                config.ch_function,
                ch_str,
                "".join(config.wave_type),
                "trig" + str(config.trigger),
            )
        )
        all_file_out_base.append(file_out_base)
        # ---------------------------------------------------------------------

    pos = 0
    for config, st, t_bb in all_configs:
        # ---running program---------------------------------------------------
        print("Running config: " + str(pos))
        st_CF = all_st_CF[pos]
        coord_eq = all_coord_eq[pos]
        rec_memory = all_rec_memory[pos]
        file_out_base = all_file_out_base[pos]
        pos = pos + 1

        # number of blocks of time windows
        num_blocks = int(math.ceil(len(t_bb) / tw_x_task))
        blocks = np.array_split(t_bb, num_blocks)

        p_outputs = []
        for block in blocks:
            p_outputs.append(
                btbb_block(
                    config,
                    block,  # t_bb
                    st,
                    st_CF,
                    coord_eq,
                    coord_sta,
                    rec_memory,
                    grid1,
                    GRD_sta,
                )
            )

        # ----filter outputs---------------------------------------------------
        triggers = filter_outputs(p_outputs)  # TASK
        # ---------------------------------------------------------------------

        # ----------Outputs----------------------------------------------------
        file_out_triggers = file_out_base + "_OUT2.dat"
        file_out_triggers = os.path.join(config.out_dir, file_out_triggers)
        write_outputs(file_out_triggers, triggers)  # TASK
        # ---------------------------------------------------------------------

        # -plot summary output-------------------------------------------------
        file_out_fig = file_out_base + "_FIG2." + config.plot_format
        file_out_fig = os.path.join(config.out_dir, file_out_fig)
        plt_SummaryOut(
            config,
            grid1,
            st_CF,
            st,
            coord_sta,
            triggers,
            t_bb,
            datestr,
            coord_eq,
            coord_jma,
            file_out_fig,
        )  # TASK
        # ---------------------------------------------------------------------

    compss_barrier()
    print("Elapsed time: " + str(time.time() - start_time))


@task(
    returns=1,
    coord_sta={Type: DICTIONARY_IN, Depth: 1},
    GRD_sta={Type: DICTIONARY_IN, Depth: 2},
)
def btbb_block(
    config, t_bb, st, st_CF, coord_eq, coord_sta, rec_memory, grid1, GRD_sta
):
    p_outputs = []
    for t_begin in t_bb:

        fq_str = "%s_%s" % (
            str(np.round(config.frequencies[0])),
            str(np.round(config.frequencies[-1])),
        )
        datestr = st[0].stats.starttime.strftime("%y%m%d%H")

        file_out_fig = (
            datestr
            + "_t"
            + "%06.1f" % (config.cut_start + t_begin)
            + "s_"
            + fq_str
            + "_fig."
            + config.plot_format
        )
        file_out_fig = os.path.join(config.out_dir, file_out_fig)

        if config.plot_results == "True":
            p_outputs.append(
                run_btbb(
                    config,
                    st,
                    st_CF,
                    t_begin,
                    coord_eq,
                    coord_sta,
                    rec_memory,
                    grid1,
                    GRD_sta,
                    file_out_fig,
                )
            )  # run_btbb TASK
        else:
            p_outputs.append(
                run_btbb_no_fig(
                    config,
                    st,
                    st_CF,
                    t_begin,
                    coord_eq,
                    coord_sta,
                    rec_memory,
                    grid1,
                    GRD_sta,
                    file_out_fig,
                )
            )  # run_btbb_no_fig  TASK
    return p_outputs


def main_continuous():
    """
    Python code for running BTBB code over continous data by splitting
    into xxmin chunks of 1 hour
    """
    # --- Input parameters
    root_folder = (
        "/gpfs/scratch/bsc19/bsc19234/BackTrackBB_stream/backtrackbb-master/scripts/"
    )
    root_folder2 = (
        "/gpfs/scratch/bsc19/bsc19234/BackTrackBB_stream/backtrackbb-master/scripts/"
    )
    # -- Path to output folder --
    stream_base = root_folder + "stream/fds"
    outdir_base = root_folder + "out_synthetic_continous_np/2222/01"
    datadir_base = "/gpfs/scratch/pr1ejg00/pr1ejg19/data/2222/01" #root_folder2 + "examples/data/data_Synthetic/2222/01"
    # -- ID base file --
    base_config_file = (
        root_folder + "examples/BT_SyntheticExample_MN_base.conf"
    )
    #
    year = "2222"
    month = "01"
    hours = np.arange(0, 12)
    days = np.arange(1, 2)  # (1, 4)  # (1, 8)

    tw_x_task = 100  # 100 time windows per task

    # Prepare all configurations for the given days and hours
    all_config_paths = dict()
    for day in days:
        for hour in hours:
            day = str(day).zfill(2)
            hour = str(hour).zfill(2)
            outdir = os.path.join(outdir_base, day, hour)
            clean_folder(outdir)
            create_folder(outdir)

            in_datadir = os.path.join(stream_base, f"{day}_{hour}")

            configf_name = "".join(
                ("BT_Synthetic", year, month, day, hour, ".conf")
            )
            config_path = os.path.join(outdir, configf_name)
            cmd = "cp " + base_config_file + " " + config_path
            os.system(cmd)

            with open(config_path, "a") as file:
                file.write("out_dir = '%s'" % str(outdir))
                file.write("\n")
                file.write("data_dir = '%s'" % str(in_datadir))
                file.write("\n")

            all_config_paths[day + hour] = config_path

    # force a new cfg as sys.argv
    print("Processing config: " + str(base_config_file))
    config_path = root_folder + "examples/BT_SyntheticExample_running.conf"
    cmd = "cp " + base_config_file + " " + config_path
    os.system(cmd)

    with open(config_path, "a") as file:
        file.write("out_dir = '%s'\n" % str(outdir_base))
        file.write("data_dir = '%s'\n" % str(datadir_base))

    sys.argv = ["btbb_continuous.py", str(config_path)]
    config = configure()

    # Start stations
    clean_folder(stream_base)
    create_folder(stream_base)
    producer_sleep = 10.0  # s
    consumer_sleep = 0.3 #0.5  # s
    fds = FileDistroStream(base_dir=stream_base)
    n_stations = len(config.stations)
    print(f"Starting stations: {config.stations}")
    for st in config.stations:
        write_files(fds, st, datadir_base, days, hours, producer_sleep)
        time.sleep(consumer_sleep)

    main(fds, n_stations, all_config_paths, tw_x_task, consumer_sleep)


if __name__ == "__main__":
    main_continuous()
