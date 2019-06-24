
from pathlib import Path
import os

class DirPair:
# TODO allow S3 or somesuch

    def __init__(self, fromdir, todir):
        self.fromdir = Path(fromdir)
        self.todir = Path(todir)
        self.validate()

    def validate(self):
        assert self.fromdir.is_dir()
        assert self.todir.is_dir()
        # TODO verify both dirs are writable

    def xfernow(self, thresh=1048576, maxage > 60):
        self.validate()
        # TODO make this recursive
        for child in fromdir.iterdir():
            if not child.is_file() or child.is_symlink():
                continue
            stats = child.stat()
            currtime = time.time()
            threshtime = currtime - maxage
            # TODO verify all paths writable
            if stats.st_size < thresh or stats.st_atime > threshtime or stats.st_mtime > threshtime or stats.st_ctime > threshtime:
                continue
            # TODO accept already synced stuff
            


        



class SyncingPair:

    def __init__(self, dirpair, path):
        self.dirpair = dirpair
        


def filestatus(fname):


def syncfile(frm, to):

