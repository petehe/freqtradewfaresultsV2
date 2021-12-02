import pandas as pd


class wfaresultfile:
    def __init__(self, wfaresultfolder, wfaresultfilename):
        self.wfaresultfile = wfaresultfilename
        self.wfaresultfolder = wfaresultfolder

    def stdwfadf(self):
        df = pd.read_csv(self.wfaresultfolder + "/" + self.wfaresultfile)
        df = df.iloc[:, 0:9]
        # Market,IS,Return,Sharpe Ratio,Win Rate,OOS,Return,Win Rate, Market Change
        # change column names to remove duplication
        df.columns = [
            "market",
            "IS",
            "ho_return",
            "ho_sharpe",
            "ho_win",
            "OOS",
            "bt_return",
            "bt_win",
            "bt_marketchange",
        ]
        # remove unneccessory columns
        # df.drop(["IS", "OOS"], axis=1, inplace=True)

        if not df.empty:

            # change market USDT to USDT50 for old wfa files
            df["market"] = df["market"].replace("USDT", "USDT50")

            # process % sign for retuns
            df["ho_return"] = df["ho_return"].str.strip("%")
            df["ho_return"] = df["ho_return"].astype(float) / 100
            df["bt_return"] = df["bt_return"].str.strip("%")
            df["bt_return"] = df["bt_return"].astype(float) / 100
            df["bt_marketchange"] = df["bt_marketchange"].str.strip("%")
            df["bt_marketchange"] = df["bt_marketchange"].astype(float) / 100

            # caluclate win, draw, lose rate from win/draw/lose number

            df[["hoWin", "hoDraw", "hoLose"]] = df["ho_win"].str.split(
                "/",
                expand=True,
            )
            df["hototaltrades"] = (
                df["hoWin"].astype(int)
                + df["hoDraw"].astype(int)
                + df["hoLose"].astype(int)
            )
            df["hoWinrate"] = df["hoWin"].astype(int) / df["hototaltrades"]
            df["hoDrawrate"] = df["hoDraw"].astype(int) / df["hototaltrades"]
            df["hoLoserate"] = df["hoLose"].astype(int) / df["hototaltrades"]
            # remove unneccessory columns
            df.drop(["hoWin", "hoDraw", "hoLose", "ho_win"], axis=1, inplace=True)

            df[["btWin", "btDraw", "btLose"]] = df["bt_win"].str.split(
                "/",
                expand=True,
            )
            df.fillna(0, inplace=True)

            df["bttotaltrades"] = (
                df["btWin"].astype(int)
                + df["btDraw"].astype(int)
                + df["btLose"].astype(int)
            )
            df["btWinrate"] = df["btWin"].astype(int) / df["bttotaltrades"]
            df["btDrawrate"] = df["btDraw"].astype(int) / df["bttotaltrades"]
            df["btLoserate"] = df["btLose"].astype(int) / df["bttotaltrades"]
            # remove unneccessory columns
            df.drop(["btWin", "btDraw", "btLose", "bt_win"], axis=1, inplace=True)

        return df
