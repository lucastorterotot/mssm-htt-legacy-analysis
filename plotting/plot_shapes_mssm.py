#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
#import Dumbledraw.rootfile_parser_inputshapes as rootfile_parser
import Dumbledraw.rootfile_parser as rootfile_parser
import Dumbledraw.styles as styles

import argparse
import copy
import yaml

import logging
logger = logging.getLogger("")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "Plot categories using Dumbledraw from shapes produced by shape-producer module."
    )
    parser.add_argument(
        "-l", "--linear", action="store_true", help="Enable linear x-axis")
    parser.add_argument(
        "-s", "--split", action="store_true", help="Enable linear x-axis")
    parser.add_argument(
        "-ns", "--nosig", action="store_true", help="Enable signal plotting")
    parser.add_argument(
        "-c",
        "--channels",
        nargs="+",
        type=str,
        required=True,
        help="Channels")
    parser.add_argument("-e", "--era", type=str, required=True, help="Era")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="ROOT file with shapes of processes")
    parser.add_argument(
        "--control-variable",
        type=str,
        default=None,
        help="Enable plotting goodness of fit shapes for given variable")
    parser.add_argument(
        "--png", action="store_true", help="Save plots in png format")
    parser.add_argument(
        "--normalize-by-bin-width",
        action="store_true",
        help="Normelize plots by bin width")
    parser.add_argument(
        "--fake-factor",
        action="store_true",
        help="Fake factor estimation method used")
    parser.add_argument(
        "--embedding",
        action="store_true",
        help="Fake factor estimation method used")
    parser.add_argument(
        "--chi2test",
        action="store_true",
        help="Print chi2/ndf result in upper-right of subplot")
    parser.add_argument(
        "-o", "--output-dir",
        help="Output directory for the plots.")
    parser.add_argument("--control-region", action="store_true",
                        help="Skip signal categories")
    parser.add_argument("--model-independent", action="store_true",
                        help="Plot shapes from model independent analysis.")
    parser.add_argument("--blinded",
                        action="store_true",
                        help="Do not draw data.")
    parser.add_argument("--ml_mass",
                        action="store_true",
                        help="Use if mTtot is replaced by the ML predictions.")
    return parser.parse_args()


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def main(args):
    if args.control_variable is None:
        channel_categories = {
            "et": ["1", "13", "15", "16", "20", "21", "32", "33",  "35", "36"],
            "mt": ["1", "13", "15", "16", "20", "21", "32", "33",  "35", "36"],
            "tt": ["1", "16", "20", "21", "32", "35"],
            "em": ["1", "2", "13", "14", "16", "19", "20", "32", "33", "34", "35", "36", "37"]
        }
        if args.model_independent:
            channel_categories = {
                "et": ["32", "33",  "35", "36"],
                "mt": ["32", "33",  "35", "36"],
                "tt": ["32", "35"],
                "em": ["2", "32", "33", "34", "35", "36", "37"]
            }
    else:
        channel_categories = {
            "et": ["100"],
            "mt": ["100"],
            "tt": ["100"],
            "em": ["100"]
        }
    channel_dict = {
        "ee": "ee",
        "em": "e#mu",
        "et": "e#tau_{h}",
        "mm": "#mu#mu",
        "mt": "#mu#tau_{h}",
        "tt": "#tau_{h}#tau_{h}"
    }
    if args.control_variable != None:
        category_dict = {"100": "inclusive"}
    else:
        category_dict = {
            "et": {
                "1": "xxh",
                "13": "t#bar{t}",
                "15": "zll",
                "16": "misc",
                "20": "emb",
                "21": "fakes",
                "32": "No B-tag Tight-m_{T}",
                "33": "No B-tag Loose-m_{T}",
                "35": "B-tag Tight-m_{T}",
                "36": "B-tag Loose-m_{T}",
                },
            "mt": {
                "1": "xxh",
                "13": "t#bar{t}",
                "15": "zll",
                "16": "misc",
                "20": "emb",
                "21": "fakes",
                "32": "No B-tag Tight-m_{T}",
                "33": "No B-tag Loose-m_{T}",
                "35": "B-tag Tight-m_{T}",
                "36": "B-tag Loose-m_{T}",
                },
            "tt": {
                "1": "xxh",
                "16": "misc",
                "20": "emb",
                "21": "fakes",
                "32": "No B-tag",
                "35": "B-tag",
                },
            "em": {
                "1": "xxh",
                "2": "d_{#zeta} < -35 GeV",
                "13": "t#bar{t}",
                "14": "QCD",
                "16": "misc",
                "19": "Diboson",
                "20": "emb",
                "32": "No B-tag, high d_{#zeta}",
                "33": "No B-tag, medium d_{#zeta}",
                "34": "No B-tag, low d_{#zeta}",
                "35": "B-tag, high d_{#zeta}",
                "36": "B-tag, medium d_{#zeta}",
                "37": "B-tag, low d_{#zeta}",
                },

        }

    SM_cats = [v for v in range(30) if v != 2]
    BSM_cats = [v for v in range(30, 40)]
    BSM_cats.append(2)
    
    split_value = 0
    if args.split == True:
        if args.normalize_by_bin_width:
            split_value = 1
        else:
            split_value = 101

    split_dict = {c: split_value for c in ["et", "mt", "tt", "em"]}

    bkg_processes = [
        "VVL", "TTL", "ZL", "jetFakes", "EMB"
    ]
    if not args.fake_factor and args.embedding:
        bkg_processes = [
            "QCD", "VVJ", "VVL", "W", "TTJ", "TTL", "ZJ", "ZL", "EMB"
        ]
    if not args.embedding and args.fake_factor:
        bkg_processes = [
            "VVT", "VVJ", "TTT", "TTJ", "ZJ", "ZL", "jetFakes", "ZTT"
        ]
    if not args.embedding and not args.fake_factor:
        bkg_processes = [
            "QCD", "W", "VVJ", "VVL", "VVT", "TTJ", "TTL", "TTT", "ZJ", "ZL", "ZTT"
#            "QCD", "VVT", "VVJ", "W", "TTT", "TTJ", "ZJ", "ZL", "ZTT"
        ]
    all_bkg_processes = [b for b in bkg_processes]
    legend_bkg_processes = copy.deepcopy(bkg_processes)
    legend_bkg_processes.reverse()

    if "2016" in args.era:
        era = "2016"
    elif "2017" in args.era:
        era = "2017"
    elif "2018" in args.era:
        era = "2018"
    else:
        logger.critical("Era {} is not implemented.".format(args.era))
        raise Exception

    plots = []
    for channel in args.channels:
        if "em" in channel:
            if not args.embedding:
                bkg_processes = [
                    "QCDMC", "VVT", "VVL", "W", "TTT", "TTL", "ZL", "ZTT"
                ]
            if args.embedding:
                bkg_processes = [
                    "QCD", "VVL", "W", "TTL", "ZL", "EMB"
                ]

        for category in channel_categories[channel]:
            if args.control_region and category != "1":
                continue
            jetFakes_str = "jetFakes"
            if int(category) != 2 and int(category) in SM_cats:
                jetFakes_str = "jetFakesSM"
                if "jetFakes" in bkg_processes:
                    bkg_processes[bkg_processes.index("jetFakes")] = jetFakes_str
            else:
                if "jetFakesSM" in bkg_processes:
                    bkg_processes[bkg_processes.index("jetFakesSM")] = jetFakes_str
            rootfile = rootfile_parser.Rootfile_parser(args.input)
            legend_bkg_processes = copy.deepcopy(bkg_processes)
            legend_bkg_processes.reverse()
            # create plot
            if args.split != True:
                plot = dd.Plot(
                    [0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=600)
            else:
                plot = dd.Plot(
                    [0.5, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=600)

            # get background histograms
            for process in bkg_processes:
                if process in [jetFakes_str, "jetFakesEMB"] and channel == "tt":
                    jetfakes_hist = rootfile.get(era, channel, category, process)
                    jetfakes_hist.Add(rootfile.get(era, channel, category, "wFakes"))
                    plot.add_hist(jetfakes_hist, process, "bkg")
                else:
                    plot.add_hist(
                        rootfile.get(era, channel, category, process), process, "bkg")
                plot.setGraphStyle(
                    process, "hist", fillcolor=styles.color_dict[process])

            # get signal histograms
            plot_idx_to_add_signal = [0,2] if not args.split else [1,2]
            for i in plot_idx_to_add_signal:
                if args.model_independent:
                    ggH_hist = rootfile.get(era, channel, category, "ggh_t").Clone()
                    ggH_hist.Add(rootfile.get(era, channel, category, "ggh_i"))
                    ggH_hist.Add(rootfile.get(era, channel, category, "ggh_b"))
                    ggH_hist.Add(rootfile.get(era, channel, category, "TotalBkg"))
                    plot.subplot(i).add_hist(
                        ggH_hist, "ggH")
                    plot.subplot(i).add_hist(
                        ggH_hist, "ggH_top")
                    bbH_hist = rootfile.get(era, channel, category, "bbh").Clone()
                    bbH_hist.Add(rootfile.get(era, channel, category, "TotalBkg"))
                    plot.subplot(i).add_hist(
                        bbH_hist, "bbH")
                    plot.subplot(i).add_hist(
                        bbH_hist, "bbH_top")
                else:
                    mssm_sig_hist = rootfile.get(era, channel, category, "TotalSig").Clone()
                    mssm_sig_hist.Add(rootfile.get(era, channel, category, "TotalBkg"))
                    plot.subplot(i).add_hist(
                        mssm_sig_hist, "mssm_sig")
                    plot.subplot(i).add_hist(
                        mssm_sig_hist, "mssm_sig_top")

            # get observed data and total background histograms
            plot.add_hist(
                rootfile.get(era, channel, category, "data_obs"), "data_obs")
            plot.add_hist(
                rootfile.get(era, channel, category, "TotalBkg"), "total_bkg")

            if args.model_independent:
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "ggH", "hist", linecolor=styles.color_dict["ggH"], linewidth=3)
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "ggH_top", "hist", linecolor=0)
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "bbH", "hist", linecolor=styles.color_dict["bbH"], linewidth=3)
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "bbH_top", "hist", linecolor=0)
            else:
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "mssm_sig", "hist", linecolor=styles.color_dict["bbH"], linewidth=3)
                plot.subplot(0 if not args.split else 1).setGraphStyle(
                    "mssm_sig_top", "hist", linecolor=0)
            plot.setGraphStyle(
                "total_bkg",
                "e2",
                markersize=0,
                fillcolor=styles.color_dict["unc"],
                linecolor=0)

            # assemble ratio
            if args.model_independent:
                bkg_ggH = plot.subplot(2).get_hist("ggH")
                bkg_bbH = plot.subplot(2).get_hist("bbH")
                # bkg_ggH.Add(plot.subplot(2).get_hist("total_bkg"))
                # bkg_bbH.Add(plot.subplot(2).get_hist("total_bkg"))
                plot.subplot(2).add_hist(bkg_ggH, "bkg_ggH")
                plot.subplot(2).add_hist(bkg_ggH, "bkg_ggH_top")
                plot.subplot(2).add_hist(bkg_bbH, "bkg_bbH")
                plot.subplot(2).add_hist(bkg_bbH, "bkg_bbH_top")
                plot.subplot(2).setGraphStyle(
                    "bkg_ggH",
                    "hist",
                    linecolor=styles.color_dict["ggH"],
                    linewidth=3)
                plot.subplot(2).setGraphStyle(
                    "bkg_ggH_top",
                    "hist",
                    linecolor=0)
                plot.subplot(2).setGraphStyle(
                    "bkg_bbH",
                    "hist",
                    linecolor=styles.color_dict["bbH"],
                    linewidth=3)
                plot.subplot(2).setGraphStyle(
                    "bkg_bbH_top",
                    "hist",
                    linecolor=0)
                plot.subplot(2).normalize([
                    "total_bkg", "bkg_ggH", "bkg_ggH_top", "bkg_bbH",
                    "bkg_bbH_top", "data_obs"
                ], "total_bkg")
            else:
                bkg_sig = plot.subplot(2).get_hist("mssm_sig")
                # bkg_sig.Add(plot.subplot(2).get_hist("total_bkg"))
                plot.subplot(2).add_hist(bkg_sig, "bkg_mssm_sig")
                plot.subplot(2).add_hist(bkg_sig, "bkg_mssm_sig_top")
                plot.subplot(2).setGraphStyle(
                    "bkg_mssm_sig",
                    "hist",
                    linecolor=styles.color_dict["bbH"],
                    linewidth=3)
                plot.subplot(2).setGraphStyle(
                    "bkg_mssm_sig_top",
                    "hist",
                    linecolor=0)
                plot.subplot(2).normalize([
                    "total_bkg", "bkg_mssm_sig", "bkg_mssm_sig_top",
                    "data_obs"
                ], "total_bkg")

            # stack background processes
            plot.create_stack(bkg_processes, "stack")

            # normalize stacks by bin-width
            if args.normalize_by_bin_width:
                plot.subplot(0).normalizeByBinWidth()
                plot.subplot(1).normalizeByBinWidth()

            # set axes limits and labels
            # plot.subplot(0).setYlims(
            #     split_dict[channel],
            #     # max(2 * plot.subplot(0).get_hist("total_bkg").GetMaximum(),
            #     #     split_dict[channel] * 2))
            #     max(1.3 * plot.subplot(0).get_hist("total_bkg").GetMaximum(),
            #         split_dict[channel] * 2))

            y_factor_linear = 1.25
            y_max = 0
            flatter_distribution = False
            if channel == "em" and int(category) == 13:
                y_factor_linear = 1.5
            for hist in ["total_bkg", "data_obs"]:
                if plot.subplot(0).get_hist(hist).GetMaximum() > y_max:
                    y_max = plot.subplot(0).get_hist(hist).GetMaximum()
            if args.linear and not args.split:
                plot.subplot(0).setYlims(0, max(y_factor_linear * y_max, split_dict[channel] * 2))
            elif args.linear and args.split:
                plot.subplot(0).setYlims(split_dict[channel], max(y_factor_linear * y_max, split_dict[channel] * 2))
            else:
                if channel == "em" and int(category) in [2, 32, 35, 37]:
                    flatter_distribution = True
                    if int(category) in [35, 37] and args.ml_mass:
                        plot.subplot(0).setYlims(1.e-3, max(2e3 * y_max, split_dict[channel] * 2))
                    else:
                        plot.subplot(0).setYlims(1.e-3, max(5e2 * y_max, split_dict[channel] * 2))
                else:
                    plot.subplot(0).setYlims(1.e-3, max(1e1 * y_max, split_dict[channel] * 2))
                plot.subplot(0).setLogY()
                
            width=.3
            plot.subplot(2).setYlims(1-width, 1+width)#(0.75, 1.8)
            if args.model_independent:
                if channel in ["et", "mt"] and int(category) in [32, 35]:
                    if 1+width < 2:
                        plot.subplot(2).setYlims(1-width, 2)
                elif channel == "tt" and int(category) in [32]:
                    if 1+width < 2:
                        plot.subplot(2).setYlims(1-width, 2)
                elif channel == "tt" and int(category) in [35]:
                    if 1+width < 3:
                        plot.subplot(2).setYlims(1-width, 3)

            if args.linear and args.split:
                # plot.subplot(1).setYlims(1.e-4, split_dict[channel])
                plot.subplot(1).setYlims(1.e-3, split_dict[channel])
                plot.subplot(1).setLogY()
                if int(category) in BSM_cats:
                    plot.subplot(1).setLogX()
                plot.subplot(1).setYlabel(
                    "")  # otherwise number labels are not drawn on axis
            if args.control_variable != None:
                if args.control_variable in styles.x_label_dict[args.channels[0]]:
                    x_label = styles.x_label_dict[args.channels[0]][
                        args.control_variable]
                else:
                    x_label = args.control_variable
                plot.subplot(2).setXlabel(x_label)
            else:
                if int(category) in BSM_cats:
                    plot.subplot(2).setXlabel("m_{T}^{tot} (Puppi) [GeV]")
                    if args.ml_mass:
                        plot.subplot(2).setXlabel("ML predictions [GeV]")
                else:
                    plot.subplot(2).setXlabel("NN score")
            if args.normalize_by_bin_width:
                if int(category) in BSM_cats:
                    plot.subplot(0).setYlabel("dN/dm_{T}^{tot} [1/GeV]")
                    if args.ml_mass:
                        plot.subplot(0).setYlabel("dN/d predictions [1/GeV]")
                else:
                    plot.subplot(0).setYlabel("dN/d score")
            else:
                plot.subplot(0).setYlabel("N_{events}")

            plot.subplot(2).setYlabel("")


            if int(category) in BSM_cats:
                low_edge = max(10, rootfile.get(era, channel, category, "TotalSig").GetBinLowEdge(2))
                #if channel == "em" and int(category) in [32, 33]:
                #    low_edge = 70
                #elif channel == "em" and int(category) in [34]:
                #    low_edge = 80

                plot.setXlims(low_edge, 3000)
                plot.subplot(0).setLogX()
                plot.subplot(2).setLogX()

            #plot.scaleXTitleSize(0.8)
            #plot.scaleXLabelSize(0.8)
            #plot.scaleYTitleSize(0.8)
            plot.scaleYLabelSize(0.8)
            #plot.scaleXLabelOffset(2.0)
            plot.scaleYTitleOffset(1.05)


            #plot.subplot(2).setNYdivisions(3, 5)

            # draw subplots. Argument contains names of objects to be drawn in corresponding order.
            # procs_to_draw = ["stack", "total_bkg", "ggH", "ggH_top", "bbH", "bbH_top", "data_obs"] if not args.split else ["stack", "total_bkg", "data_obs"]
            if category == "1" and args.control_region:
                procs_to_draw = ["stack", "total_bkg", "data_obs"] if not args.split else ["stack", "total_bkg", "data_obs"]
            else:
                if args.model_independent:
                    procs_to_draw = ["stack", "total_bkg", "ggH", "ggH_top", "bbH", "bbH_top"] if not args.split else ["stack", "total_bkg"]
                else:
                    procs_to_draw = ["stack", "total_bkg", "mssm_sig", "mssm_sig_top"] if not args.split else ["stack", "total_bkg"]
            if not "data_obs" in procs_to_draw and not args.blinded:
                procs_to_draw.append("data_obs")
            if args.nosig:
                for p in ["ggH", "ggH_top", "bbH", "bbH_top", "mssm_sig", "mssm_sig_top"]:
                    if p in procs_to_draw:
                        procs_to_draw.remove(p)
            plot.subplot(0).Draw(procs_to_draw)
            if args.split == True:
                if category == "1" and args.control_region:
                    procs_to_draw = ["stack", "total_bkg"]
                    if not args.blinded:
                        procs_to_draw.append("data_obs")
                    plot.subplot(1).Draw(procs_to_draw)
                else:
                    if args.nosig:
                        procs_to_draw = ["stack", "total_bkg", "data_obs"]
                        if args.blinded:
                            procs_to_draw.remove("data_obs")
                    else:
                        if args.model_independent:
                            procs_to_draw = ["stack", "total_bkg", "ggH", "bbH", "ggH_top", "bbH_top", "data_obs"]
                        else:
                            procs_to_draw = ["stack", "total_bkg", "mssm_sig", "mssm_sig_top", "data_obs"]
                        if args.blinded:
                            procs_to_draw.remove("data_obs")
                    plot.subplot(1).Draw(procs_to_draw)
            if category == "1" and args.control_region:
                plot.subplot(2).Draw([
                    "total_bkg",
                    "data_obs"
                ])
            else:
                if args.nosig:
                    procs_to_draw = ["total_bkg", "data_obs"]
                    if args.blinded:
                        procs_to_draw.remove("data_obs")
                else:
                    if args.model_independent:
                        procs_to_draw = ["total_bkg", "bkg_ggH", "bkg_bbH", "bkg_ggH_top", "bkg_bbH_top", "data_obs"]
                    else:
                        procs_to_draw = ["total_bkg", "bkg_mssm_sig", "bkg_mssm_sig_top", "data_obs"]
                    if args.blinded:
                        procs_to_draw.remove("data_obs")
                plot.subplot(2).Draw(procs_to_draw)

            # create legends
            suffix = ["", "_top"]
            for i in range(2):

                pos=3
                if channel == "em" and int(category) in [13]:
                    pos = 1
                height, width, NColumns = 0.2, 0.4, 2
                if int(category) in SM_cats and not args.linear:
                    height, width, NColumns = 0.1, 0.8, 4
                if int(category) in BSM_cats and not args.linear:
                    height, width, NColumns = 0.4, 0.2, 1
                    if flatter_distribution:
                        height, width, NColumns = 0.2, 0.4, 2
                if channel in ["em"]:
                    n_bgs = 6
                elif channel in ["et", "mt"]:
                    n_bgs = 5
                elif channel in ["tt"]:
                    n_bgs = 5
                n_bgs += 2 # data and bkg unc
                if args.blinded:
                    n_bgs-=1 # no data in this case
                if args.model_independent:
                    n_sigs = 2
                else:
                    n_sigs = 1
                n_sigs_bak = n_sigs
                if args.nosig:
                    n_sigs = 0
                tot_in_legend = n_bgs + n_sigs
                if args.linear:
                    height *= tot_in_legend/int(tot_in_legend/2.+0.5)
                    width *= 1./2
                    NColumns = int(NColumns/2)
                if args.nosig and args.linear:
                    height *= tot_in_legend/(tot_in_legend+n_sigs_bak)
                    if args.blinded:
                        height *= (tot_in_legend+.2)/(tot_in_legend)
                if args.nosig and not args.linear:
                    height *= int(tot_in_legend/2.+0.5)/int((tot_in_legend+n_sigs_bak)/2.+0.5)
                if width >= 0.8:
                    width = 0.75
                if height <= 0.15:
                    height = 0.15
                plot.add_legend(width=width, height=height, pos=pos)

                for process in legend_bkg_processes:
                    plot.legend(i).add_entry(
                        0, process, styles.legend_label_dict[process.replace("TTL", "TT").replace("VVL", "VV")], 'f')
                plot.legend(i).add_entry(0, "total_bkg", "Bkg. unc.", 'f')
                if not args.blinded:
                    plot.legend(i).add_entry(0, "data_obs", "Data", 'PE')
                if args.control_region and category == "1":
                    # plot.legend(i).add_entry(0 if not args.split else 1, "mssm_sig%s" % suffix[i], "#splitline{H #rightarrow #tau#tau}{(m_{H}=1200 GeV)}", 'l')
                    pass
                elif not args.nosig:
                    if args.model_independent:
                        plot.legend(i).add_entry(0 if not args.split else 1, "ggH%s" % suffix[i], "ggH 400 GeV", 'l')
                        plot.legend(i).add_entry(0 if not args.split else 1, "bbH%s" % suffix[i], "bbH 400 GeV", 'l')
                    else:
                        #plot.legend(i).add_entry(0 if not args.split else 1, "mssm_sig%s" % suffix[i], "#splitline{h,H,A #rightarrow #tau#tau}{m_{H} = 400 GeV}", 'l')
                        plot.legend(i).add_entry(0 if not args.split else 1, "mssm_sig%s" % suffix[i], "SM Higgs", 'l')
                if NColumns != 1:
                    plot.legend(i).setNColumns(NColumns)
            plot.legend(0).Draw()
            plot.legend(1).setAlpha(0.0)
            plot.legend(1).Draw()

            if args.chi2test:
                import ROOT as r
                f = r.TFile(args.input, "read")
                background = f.Get("htt_{}_{}_Run{}_{}/TotalBkg".format(
                    channel, category, args.era, "prefit"
                    if "prefit" in args.input else "postfit"))
                data = f.Get("htt_{}_{}_Run{}_{}/data_obs".format(
                    channel, category, args.era, "prefit"
                    if "prefit" in args.input else "postfit"))
                chi2 = data.Chi2Test(background, "UW CHI2/NDF")
                plot.DrawText(0.7, 0.3,
                              "\chi^{2}/ndf = " + str(round(chi2, 3)))

            for i in range(2):
                plot.add_legend(
                    reference_subplot=2, pos=1, width=0.5, height=0.06)
                if not args.blinded:
                    plot.legend(i + 2).add_entry(0, "data_obs", "Data", 'PE')
                if args.control_region and category == "1":
                    pass
                elif not args.nosig:
                    if args.model_independent:
                        plot.legend(i + 2).add_entry(0 if not args.split else 1, "ggH%s" % suffix[i],
                                             "ggH+bkg.", 'l')
                        plot.legend(i + 2).add_entry(0 if not args.split else 1, "bbH%s" % suffix[i],
                                             "bbH+bkg.", 'l')
                    else:
                        plot.legend(i + 2).add_entry(0 if not args.split else 1, "mssm_sig%s" % suffix[i],
                                                     "H+bkg.", 'l')
                plot.legend(i + 2).add_entry(0, "total_bkg", "Bkg. unc.", 'f')
                plot.legend(i + 2).setNColumns(3)
            # plot.legend(2).Draw()
            # plot.legend(3).setAlpha(0.0)
            # plot.legend(3).Draw()

            # draw additional labels
            # plot.DrawCMS()
            if "2016" in args.era:
                plot.DrawLumi("35.9 fb^{-1} (2016, 13 TeV)")
            elif "2017" in args.era:
                plot.DrawLumi("41.5 fb^{-1} (2017, 13 TeV)")
            elif "2018" in args.era:
                plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
            else:
                logger.critical("Era {} is not implemented.".format(args.era))
                raise Exception

            posChannelCategoryLabelLeft = None
            plot.DrawChannelCategoryLabel(
                "%s, %s" % (channel_dict[channel], category_dict[channel][category]),
                begin_left=posChannelCategoryLabelLeft)
            # plot.DrawChannelCategoryLabel(
            #     "%s, %s" % (str(channel), str(int(category))),
            #     begin_left=posChannelCategoryLabelLeft)

            plot.subplot(0).setGraphStyle("data_obs", "e0", markersize=.5)
            plot.subplot(2).setGraphStyle("data_obs", "e0", markersize=.5)
            ax=plot.subplot(2)._hists['total_bkg'][0].GetXaxis()
            ax.SetMoreLogLabels()
            ax.SetNoExponent()

            # save plot
            postfix = "prefit" if "prefit" in args.input else "postfit" if "postfit" in args.input else "undefined"
            plot.save("%s/%s_%s_%s_%s%s%s%s%s.%s" % (args.output_dir, args.era, channel, args.control_variable if args.control_variable is not None else category,
                                                     postfix, "_linear" if args.linear else "", "_split" if args.split else "", "_nosignal" if args.nosig else "", "_blinded" if args.blinded else "",
                                                     "png" if args.png else "pdf",
                                                    ))
            plots.append(
                plot
            )  # work around to have clean up seg faults only at the end of the script


if __name__ == "__main__":
    args = parse_arguments()
    setup_logging("{}_plot_shapes.log".format(args.era), logging.INFO)
    main(args)
