#!/usr/bin/env python3

"""Script to move and symlink a single file(s)"""

import argparse
import pathlib
import warnings
import time
import mvln


def movesome(src, dst, files, tm_thresh=1800, sz_thresh=2097152):
    """Move old large filex from src to dest"""
    abstm = time.time() - tm_thresh
    sp = pathlib.Path(src)
    dp = pathlib.Path(dst)
    assert sp.is_dir() and dp.is_dir()
    for file in files:
        path = sp.joinpath(file)
        if path.is_symlink() or not path.is_file():
            warnings.warn('{} is not a normal file'.format(file))
            continue
        stt = path.stat()
        if stt.st_size < sz_thresh:
            warnings.warn('{} is too small'.format(file))
            continue
        if (stt.st_atime > abstm or stt.st_mtime > abstm or
                stt.st_ctime > abstm):
            warnings.warn('{} is too new'.format(file))
            continue
        mvln.mvlns(str(path), str(dp.joinpath(path.name)))


def _cli():
    parser = argparse.ArgumentParser(description='move and link')
    parser.add_argument('source', help='source directory')
    parser.add_argument('dest', help='target directory')
    parser.add_argument('files', nargs='+', help='Which files to move')
    args = parser.parse_args()
    movesome(args.source, args.dest, args.files)


if __name__ == "__main__":
    _cli()
