#!/usr/bin/env python3

"""Run a command and move the results elsewhere"""

import argparse
import sys
import warnings
import os
import shutil
import subprocess


def tmprun(what, where, dest):
    """Run a command one place and put results elsewhere"""
    cwd = os.getcwd()
    newdir = os.path.join(where, str(os.getpid()))
    os.mkdir(newdir)
    os.chdir(newdir)
    subprocess.run(what, check=True)
    results = os.listdir('.')
    keepfiles = []
    for des in dest:
        for res in results:
            newfile = os.path.join(des, res)
            if os.path.exists(newfile):
                warnings.warn("File exists {}".format(newfile))
                keepfiles.append(res)
                continue
            try:
                shutil.copy2(res, newfile)
            except OSError:
                if os.stat(res).st_size == os.stat(newfile).st_size:
                    warnings.warn("Got error probably ok {}".format(newfile))
                else:
                    keepfiles.append(res)
                    warnings.warn("Failed to copy {}".format(newfile))
    os.chdir(cwd)
    if not keepfiles:
        shutil.rmtree(newdir)


def subtmprun(what, where, dest, cmd, sub):
    """Run through a command on multiple items to a given subdir"""
    subdirs = [os.path.join(x, sub) for x in dest]
    for sbd in subdirs:
        if not os.path.exists(sbd):
            os.mkdir(sbd)
    tmprun([cmd] + what, where, subdirs)


def runlist(what, where, dest, filehand):
    """Read basic TSV and run command on it"""
    for line in filehand:
        if len(line) < 2:
            continue
        breakup = line.split()
        if len(breakup) < 2:
            warnings.warn("Cannot process {}".format(line))
            continue
        sub = breakup[0]
        operands = breakup[1:]
        print('{}: {}'.format(sub, operands))
        subtmprun(operands, where, dest, what, sub)


def cli():
    """Process command line arguments"""
    parser = argparse.ArgumentParser(description='run command, different dest')
    parser.add_argument('what', help='command to run')
    parser.add_argument('where', help='temporary holding')
    parser.add_argument('dest', nargs='+', help='where to send')
    args = parser.parse_args()
    runlist(args.what, args.where, args.dest, sys.stdin)


if __name__ == "__main__":
    cli()
