from datetime import datetime
import os
from wfaresultfile import wfaresultfile

from pandas.core.frame import DataFrame
import pandas as pd


class wfasummaryfile:
    def __init__(self, wfaresultfolder, wfasummaryfolder):
        self.wfaresultfolder = wfaresultfolder
        self.wfasummaryfolder = wfasummaryfolder
        self.summary_columns = [
            "strategy",
            "market",
            "ho_return",
            "ho_sharpe",
            "bt_return",
            "bt_marketchange",
            "hototaltrades",
            "hoWinrate",
            "hoDrawrate",
            "hoLoserate",
            "bttotaltrades",
            "btWinrate",
            "btDrawrate",
            "btLoserate",
        ]

    def getstrategyname(self, filename):
        return filename.split("_WFA_")[0]

    def movetostrategylist(self, strategyname, wfalist):
        strategylist = []
        # use copied list to support iteration,
        # when we use wfalist for iteration, it doesn't complete since it is changed inside for loop
        wfalistcopy = wfalist.copy()
        for wfa in wfalistcopy:
            if self.getstrategyname(wfa) == strategyname:
                strategylist.append(wfa)
                wfalist.remove(wfa)
        return strategylist

    def combinestlisttodf(self, strategylist):
        # combine df from multiple files
        combinedf = DataFrame.empty
        stcount = 0
        for strategywfa in strategylist:
            wfafile = wfaresultfile(self.wfaresultfolder, strategywfa)
            stddf = wfafile.stdwfadf()
            if stcount == 0:
                combinedf = stddf
            else:
                combinedf = pd.concat([combinedf, stddf], ignore_index=True)
            stcount = stcount + 1
        return combinedf

    def addheader(self, file):
        for item in self.summary_columns:
            file.write(item + ",")
        file.write("\n")

    def writesummaryfile(self):
        wfalist = os.listdir(self.wfaresultfolder)
        # create summary file name
        summaryfile = (
            self.wfasummaryfolder
            + "/"
            + self.wfaresultfolder
            + "_"
            + str(datetime.now())
            + ".csv"
        )
        with open(summaryfile, "w") as summary:
            self.addheader(summary)
            while len(wfalist):
                strategyname = self.getstrategyname(wfalist[0])

                strategylist = self.movetostrategylist(strategyname, wfalist)

                combinedf = self.combinestlisttodf(strategylist)
                if not combinedf.empty:
                    markets = combinedf["market"].unique()
                    for market in markets:
                        dfbymarket = combinedf[combinedf["market"] == market]
                        summary.write(strategyname + ",")
                        summary.write(market + ",")
                        for column in self.summary_columns[2:]:
                            avg = dfbymarket[column].astype(float).mean()
                            summary.write(str(avg) + ",")
                        summary.write("\n")
                else:
                    print("DateFrame is Empty")
