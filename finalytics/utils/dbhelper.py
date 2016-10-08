__author__ = 'indiquant'

import os
import sqlite3
from enum import Enum
from qrymaker import qry_createtable


_DB = r'C:\temp\strat\webdata.sqlite3'
_db = r'C:\temp\webdata.sqlite3'


class EnumDBOptionTable(Enum):
    undl = 1
    opt_type = 2
    exc_type = 3
    expiry = 4
    strike = 5
    recdate = 6
    rectime = 7
    undl_type = 8
    spot = 9
    bidpx = 10
    bidqty = 11
    askpx = 12
    askqty = 13
    lastpx = 14
    volume = 15


def read_rectimes(undl, recdate):
    qry = "SELECT rectime FROM options_intraday WHERE undl = '{undl}'".format(undl=undl) + \
          " AND recdate = {recdate}".format(recdate=str(recdate)) + \
          " GROUP BY rectime ORDER BY rectime"
    _res = execute_r(_db, qry)
    if _res:
        return [r[0] for r in _res]

    else:
        return None


def read_options(undl, recdate, rectime):
    """
    :type recdate: int
    :type rectime: int
    """
    qry = "SELECT * FROM options_intraday WHERE undl = '{undl}'".format(undl=undl) + \
          " AND recdate = {recdate} AND rectime = {rectime}".format(recdate=str(recdate), rectime=str(rectime))
    return execute_r(_db, qry)


def dbname():
    return _DB


def createfileifmissing(fname):
    if not os.path.exists(fname):
        open(fname, 'w')


def createtable(dbname, tname, colnames, coltypes, pkeys):
    conn = sqlite3.connect(dbname)

    _qry = qry_createtable(tname, colnames, coltypes, pkeys)

    conn.execute(_qry)

    conn.commit()


def create_table(tname, colnames, coltypes, primarykeys):
    conn = sqlite3.connect(_DB)

    _qry = qry_createtable(tname, colnames, coltypes, primarykeys)

    conn.execute(_qry)

    conn.commit()


def bulkinsert(dbname, tname, colnames, rows):
    conn = sqlite3.connect(dbname)

    _qry = "INSERT OR REPLACE INTO " + tname + " ("

    for cname in colnames:
        _qry += ' ' + cname + ','

    _qry = _qry.rstrip(',')
    _qry += ') VALUES ('

    for cname in colnames:
        _qry += ' ?,'

    _qry = _qry.rstrip(',')
    _qry += ')'

    for _row in rows:
        conn.execute(_qry, _row)

    conn.commit()


def bulkinsert_codes(tname, colnames, rows):
    conn = sqlite3.connect(_DB)

    _qry = "INSERT OR REPLACE INTO " + tname + " ("

    for cname in colnames:
        _qry += ' ' + cname + ','

    _qry = _qry.rstrip(',')
    _qry += ') VALUES ('

    for cname in colnames:
        _qry += ' ?,'

    _qry = _qry.rstrip(',')
    _qry += ')'

    for _row in rows:
        conn.execute(_qry, _row)

    conn.commit()


def execute_r(dbname, qry):
    conn = sqlite3.connect(dbname)
    try:
        cur = conn.cursor()
        cur.execute(qry)
        x = cur.fetchall()
        conn.close()
        return x

    except sqlite3.OperationalError:
        conn.close()
        return None


def execute_w(dbname, qry):
    conn = sqlite3.connect(dbname)
    try:
        cur = conn.cursor()
        cur.execute(qry)
        conn.commit()
        conn.close()

    except sqlite3.OperationalError:
        conn.close()
        return None


if __name__ == '__main__':
    qry = "SELECT * FROM codes WHERE undltype='S'"
    x = execute_r(qry)
    print 'pause'
