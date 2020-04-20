#!/usr/bin/env python3

"""Tools for moving and symlinking files"""

import os
import shutil
import time
import argparse


def mvlns(src, dst, verbose=True):
    """Move a file and replace original with symlink

    Note that it does not do any integrity checking
    """
    if verbose:
        print('move {} to {}'.format(src, dst))
    assert os.path.isfile(src)
    assert not os.path.islink(src)
    assert os.path.isdir(os.path.dirname(dst))
    assert not os.path.lexists(dst)
    shutil.move(src, dst)
    # note - src and dst can be a little counter intuitive
    os.symlink(dst, src)


def moveold(src, dst, tm_thresh=3600, sz_thresh=3600):
    """Move old large filex from src to dest"""
    assert os.path.isdir(src) and os.path.isdir(dst)
    abstm = time.time() - tm_thresh
    with os.scandir(src) as itr:
        for entry in itr:
            if not entry.is_file(follow_symlinks=False):
                continue
            stt = entry.stat()
            if stt.st_size < sz_thresh:
                continue
            if (stt.st_atime > abstm or stt.st_mtime > abstm or
                    stt.st_ctime > abstm):
                continue
            mvlns(entry.path, os.path.join(dst, entry.name))


def _cli():
    parser = argparse.ArgumentParser(description='move and link')
    parser.add_argument('source', help='source directory')
    parser.add_argument('dest', help='target directory')
    args = parser.parse_args()
    moveold(args.source, args.dest)


if __name__ == "__main__":
    _cli()
