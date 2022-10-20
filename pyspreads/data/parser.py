from pathlib import Path

import numpy as np


def read(
        fname,
        row_delimiter='\n',
        col_delimiter='\t',
        strike_col=8,
        call_bid_col=1,
        call_ask_col=2,
        put_bid_col=11,
        put_ask_col=12,
        comments='#',
        skiprows=0
):
    """
    Wraps numpy.loadtxt to read market data (strike, call bid, call ask, put bid, put ask) from a multi-line string or file.
    """
    try:
        isfile = isinstance(fname, Path) or Path(fname).is_file()
    except OSError:  # When string is too long for Path init
        isfile = False

    if isfile:
        s = Path(fname).read_text()
    elif isinstance(fname, str):
        s = fname
    else:
        raise ValueError(f"Did not recognize data {fname}; please give a string or path to file.")

    return np.loadtxt(
        s.split(row_delimiter),
        delimiter=col_delimiter,
        usecols=(strike_col, call_bid_col, call_ask_col, put_bid_col, put_ask_col),
        dtype=float,
        skiprows=skiprows,
        comments=comments,
        unpack=True, # Transposes it, so the 0th entry is our strike price column, not the 0th row of data
    )
