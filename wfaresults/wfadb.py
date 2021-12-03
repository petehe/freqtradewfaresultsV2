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
        timeframe = restofname[4]
        epoch = restofname[5]
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
                maxtrades = row["maxtrades"]
                IS_Start = row["IS"].split("_")[0]
                IS_End = row["IS"].split("_")[1]
                HO_return = row["ho_return"]
                HO_Sharpe = row["ho_sharpe"]
                HO_WinRate = row["ho_win"]
                OOS_start = row["OOS"].split("_")[0]
                OOS_end = row["OOS"].split("_")[1]
                bt_total_trades = row["bt_total_trades"]
                bt_total_profit = row["bt_total_profit"]
                bt_avg_profit = row["bt_avg_profit"]
                bt_drawdown = row["bt_drawdown"]
                bt_wins = row["bt_wins"]
                bt_draws = row["bt_draws"]
                bt_loses = row["bt_loses"]
                bt_win_rate = row["bt_win_rate"]
                bt_win_days = row["bt_win_days"]
                bt_avg_duration = row["bt_avg_duration"]
                bt_avg_duration_win = row["bt_avg_duration_win"]
                bt_avg_duration_lose = row["bt_avg_duration_lose"]
                bt_marketchange = row["bt_marketchange"]
                bt_left_total_trades = row["bt_left_total_trades"]
                bt_left_avg_profit = row["bt_left_avg_profit"]
                bt_left_total_profit = row["bt_left_total_profit"]
                bt_left_avg_duration = row["bt_left_avg_duration"]
                bt_left_wins = row["bt_left_wins"]
                bt_left_draws = row["bt_left_draws"]
                bt_left_loses = row["bt_left_loses"]
                bt_left_win_rate = row["bt_left_win_rate"]

                insert_sql = (
                    'INSERT INTO "main"."wfaresultsV2" ("Strategy", "Market", "MaxTrades", "timeframe", "epoch","IS_Start","IS_End", "HOReturn", "HOSharpeRatio", "HOWinRate",'
                    + '"OOS_Start","OOS_End", "TotalTrades", "TotalProfit", "AvgProfit", "Drawdown", "Wins", "Draws", "Loses", "WinRate", "WinDay",'
                    + '"AvgDuration", "AvgDur_Win", "AvgDur_Lose", "MarketChange",'
                    + '"Lefttotaltrades", "Leftavgprofit", "Lefttotalprofit", "Leftavgduration", "Leftwin", "Leftdraws", "Leftlose", "LeftWinRate")'
                    + "VALUES"
                    + f"('{strategy}', '{market}', '{maxtrades}', '{timeframe}', '{epoch}', '{IS_Start}',{IS_End}, '{HO_return}', '{HO_Sharpe}', '{HO_WinRate}', "
                    + f"'{OOS_start}','{OOS_end}', '{bt_total_trades}', '{bt_total_profit}', '{bt_avg_profit}', '{bt_drawdown}', '{bt_wins}', '{bt_draws}', '{bt_loses}', '{bt_win_rate}', '{bt_win_days}', "
                    + f"'{bt_avg_duration}', '{bt_avg_duration_win}', '{bt_avg_duration_lose}', '{bt_marketchange}',"
                    + f"'{bt_left_total_trades}', '{bt_left_total_profit}', '{bt_left_avg_profit}', '{bt_left_avg_duration}', '{bt_left_wins}', '{bt_left_draws}', '{bt_left_loses}', '{bt_left_win_rate}');"
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
