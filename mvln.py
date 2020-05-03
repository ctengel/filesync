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
    if os.path.lexists(dst):
        # Some annoying programs will amend but overwrite the link
        # The following lets it still work
        # TODO needs to be handled better
        srcst = os.stat(src)
        dstst = os.stat(dst)
        assert srcst.st_size > dstst.st_size - 1024
        assert srcst.st_size < dstst.st_size + 1024
        assert srcst.st_mtime == dstst.st_mtime
    shutil.move(src, dst)
    # note - src and dst can be a little counter intuitive
    os.symlink(dst, src)


def moveold(src, dst, tm_thresh=1800, sz_thresh=2097152):
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
    parser.add_argument('-a', '--age', type=int, default=1800,
                        help='Min age in seconds')
    parser.add_argument('-s', '--size', type=int, default=2097152,
                        help='Min size in bytes')
    args = parser.parse_args()
    moveold(args.source, args.dest, args.age, args.size)


if __name__ == "__main__":
    _cli()
