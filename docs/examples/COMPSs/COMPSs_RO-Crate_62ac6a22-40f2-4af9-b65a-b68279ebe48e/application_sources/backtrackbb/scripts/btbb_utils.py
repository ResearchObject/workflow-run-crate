import os
import argparse


def create_parser():
    """Create argument parser.

    :return: Argument parser.
    """
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("studycase", type=str,
                        help="Case to study (e.g. synthetic, vrancea)")
    parser.add_argument("datadir", type=str,
                        help="Input data directory base")
    parser.add_argument("outdir", type=str,
                        help="Output directory base")
    parser.add_argument("config", type=str,
                        help="Base configuration file")
    parser.add_argument("year", type=str,
                        help="Year")
    parser.add_argument("month", type=str,
                        help="Month")
    parser.add_argument("day_start", type=int,
                        help="Starting day")
    parser.add_argument("day_end", type=int,
                        help="Ending day")
    parser.add_argument("hour_start", type=int,
                        help="Starting hour")
    parser.add_argument("hour_end", type=int,
                        help="Ending hour")
    parser.add_argument("tw_x_task", type=int,
                        help="Time windows per task")
    return parser


def parse_input_parameters(show=True):
    """Parse input parameters.

    :param show: Print the input parameters.
    :return: Parsed input parameters.
    """
    parser = create_parser()
    args = parser.parse_args()
    if show:
        print()
        print(">>> WELCOME TO BACKTRACKBB")
        print("> Parameters:")
        print("\t- studycase: %s" % args.studycase)
        print("\t- datadir: %s" % args.datadir)
        print("\t- outdir: %s" % args.outdir)
        print("\t- config: %s" % args.config)
        print("\t- year: %s" % args.year)
        print("\t- month: %s" % args.month)
        print("\t- day start: %s" % args.day_start)
        print("\t- day end: %s" % args.day_end)
        print("\t- hour start: %s" % args.hour_start)
        print("\t- hour end: %s" % args.hour_end)
        print("\t- tw_x_task: %s" % args.tw_x_task)
        print("\n")
    return args
