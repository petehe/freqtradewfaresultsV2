from wfasummaryfile import wfasummaryfile
from wfadb import wfadb

import config as cfg


def main():
    if cfg.DB_OR_FILE == "FILE":
        summaryfile = wfasummaryfile(cfg.wfaresultfolder, cfg.wfasummaryfolder)
        summaryfile.writesummaryfile()
    elif cfg.DB_OR_FILE == "DB":
        db = wfadb(cfg.wfaresultfolder, cfg.wfadbpath)
        db.processresultfolder()


if __name__ == "__main__":
    main()
