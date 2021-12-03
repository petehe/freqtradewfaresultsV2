from wfadb import wfadb

import config as cfg


def main():
    db = wfadb(cfg.wfaresultfolder, cfg.wfadbpath)
    db.processresultfolder()


if __name__ == "__main__":
    main()
