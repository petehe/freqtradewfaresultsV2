import pandas as pd
import numpy as np


class wfaresultfile:
    def __init__(self, wfaresultfolder, wfaresultfilename):
        self.wfaresultfile = wfaresultfilename
        self.wfaresultfolder = wfaresultfolder

    def stdwfadf(self):
        df = pd.read_csv(self.wfaresultfolder + "/" + self.wfaresultfile)
        # Market,Max Trades, IS,HO Return,HO Sharpe Ratio,HO Win Rate,OOS,Total Trades,Total Profit, Avg Profit,
        # Drawdown, Wins, Draws, Loses, Win Rate, Win Day,Avg Duration, Avg Dur_Win, Avg Dur_Lose, Market Change,
        # Left total trades, Left avg profit, Left total profit, Left avg duration, Left win, Left draws, Left lose, Left Win Rate
        df.columns = [
            "market",
            "maxtrades",
            "IS",
            "ho_return",
            "ho_sharpe",
            "ho_win",
            "OOS",
            "bt_total_trades",
            "bt_total_profit",
            "bt_avg_profit",
            "bt_drawdown",
            "bt_wins",
            "bt_draws",
            "bt_loses",
            "bt_win_rate",
            "bt_win_days",
            "bt_avg_duration",
            "bt_avg_duration_win",
            "bt_avg_duration_lose",
            "bt_marketchange",
            "bt_left_total_trades",
            "bt_left_avg_profit",
            "bt_left_total_profit",
            "bt_left_avg_duration",
            "bt_left_wins",
            "bt_left_draws",
            "bt_left_loses",
            "bt_left_win_rate",
        ]

        if not df.empty:
            df.replace(r"^\s*$", 0, regex=True)
            df.replace(" ", 0, inplace=True)

            df.fillna(0, inplace=True)

            # process % sign for retuns
            df["ho_return"] = df["ho_return"].str.strip("%")
            df["ho_return"] = df["ho_return"].astype(float) / 100
            df["bt_total_profit"] = df["bt_total_profit"].str.strip("%")
            df["bt_total_profit"] = df["bt_total_profit"].astype(float) / 100
            df["bt_drawdown"] = df["bt_drawdown"].str.strip("%")
            df["bt_drawdown"] = df["bt_drawdown"].astype(float) / 100
            df["bt_marketchange"] = df["bt_marketchange"].str.strip("%")
            df["bt_marketchange"] = df["bt_marketchange"].astype(float) / 100
            df["bt_avg_profit"] = df["bt_avg_profit"].astype(float) / 100
            df["bt_win_rate"] = df["bt_win_rate"].astype(float) / 100
            df["bt_left_avg_profit"] = df["bt_left_avg_profit"].astype(float) / 100
            df["bt_left_total_profit"] = df["bt_left_total_profit"].astype(float) / 100
            df["bt_left_win_rate"] = df["bt_left_win_rate"].astype(float) / 100

        return df
