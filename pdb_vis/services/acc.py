import bz2
import logging
import os
import re


_log = logging.getLogger(__name__)

RE_ACC = re.compile(r'[0-9 A-Z\(\)]{16}([A-Z])[A-Z ]{7}[ ]+([0-9\.]+)', re.M)


def parse(pdb_ac):
    DSP_ROOT = '/mnt/cmbi4/wi-lists/acc/'
    acc_path = DSP_ROOT + '{}/{}.acc.bz2'.format(pdb_ac, pdb_ac)
    _log.info("Parsing acc for file '{}'".format(pdb_ac))

    if not os.path.exists(acc_path):
        raise ValueError('File not found: {}'.format(acc_path))

    with bz2.BZ2File(acc_path) as f:
        acc_content = f.read()

    m = RE_ACC.findall(acc_content)
    if not m:
        raise Exception("Error parsing '{}'".format(acc_path))

    acc = {}
    for chain, acc_value in m:
        if chain in acc:
            acc[chain].append(float(acc_value))
        else:
            acc[chain] = [float(acc_value)]

    return acc
