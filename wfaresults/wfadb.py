import sqlite3
import os
import datetime
from wfaresultfile import wfaresultfile
import config as cfg


class wfadb:
    def __init__(self, wfaresultfolder, wfadbfile):
        self.wfaresultfolder = wfaresultfolder
        self.wfadbfile = wfadbfile

    def addrecordsfromfile(self, wfafile):
        wfafilename = wfafile.split("_WFA_")
        strategy = wfafilename[0]
        # remove file extension
        restofname = wfafilename[1].split(".")[0]
        # split file name into individual elements
        restofname = restofname.split("_")
        numberofcoins = restofname[0]
        maxtrades = restofname[1]
        timeframe = restofname[5]
        epoch = restofname[6]
        ctime = os.path.getmtime(self.wfaresultfolder + "/" + wfafile)
        createtime = datetime.datetime.utcfromtimestamp(ctime).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        try:

            con = sqlite3.connect(self.wfadbfile)
            cur = con.cursor()
            resultfile = wfaresultfile(self.wfaresultfolder, wfafile)
            resultdf = resultfile.stdwfadf()
            for index, row in resultdf.iterrows():
                market = row["market"]
                IS_Start = row["IS"].split("_")[0]
                IS_End = row["IS"].split("_")[1]
                HO_return = row["ho_return"]
                HO_Sharpe = row["ho_sharpe"]
                HO_win = row["hoWinrate"]
                HO_draw = row["hoDrawrate"]
                HO_lose = row["hoLoserate"]
                HO_totaltrades = row["hototaltrades"]
                OOS_start = row["OOS"].split("_")[0]
                OOS_end = row["OOS"].split("_")[1]
                BT_return = row["bt_return"]
                BT_win = row["btWinrate"]
                BT_draw = row["btDrawrate"]
                BT_lose = row["btLoserate"]
                BT_totaltraders = row["bttotaltrades"]
                market_change = row["bt_marketchange"]

                insert_sql = (
                    'INSERT INTO "main"."wfarecords"'
                    + '("strategy","epoch","market","numberofconins","maxtrades","timeframe","edge","createtime",'
                    + '"ISPeriods","IS_Start","IS_End","HO_return","HO_Sharpe","HO_win","HO_draw","HO_lose","HO_totaltrades",'
                    + '"OOS_start","OOS_end","BT_return","BT_win","BT_draw","BT_lose","BT_totaltrades","market_change","status")'
                    + "VALUES "
                    + f'("{strategy}","{epoch}","{market}","{numberofcoins}","{maxtrades}","{timeframe}",0,"{createtime}",'
                    + f'"{cfg.ISPeriods}","{IS_Start}","{IS_End}","{HO_return}","{HO_Sharpe}","{HO_win}","{HO_draw}","{HO_lose}","{HO_totaltrades}",'
                    + f'"{OOS_start}","{OOS_end}","{BT_return}","{BT_win}","{BT_draw}","{BT_lose}","{BT_totaltraders}","{market_change}",1)'
                )
                cur.execute(insert_sql)

            con.commit()
            con.close()
        except Exception:
            print("connection failed: ")
            raise

    def processresultfolder(self):

        wfalist = os.listdir(self.wfaresultfolder)
        for wfafile in wfalist:
            self.addrecordsfromfile(wfafile)
