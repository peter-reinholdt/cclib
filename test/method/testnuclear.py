# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Test the Nuclear method in cclib"""

import sys
import os
import re
import logging
import unittest

import numpy

from cclib.method import Nuclear
from cclib.parser import ccData
from cclib.parser import QChem
from cclib.parser import utils

sys.path.insert(1, "..")

from ..test_data import getdatafile


class NuclearTest(unittest.TestCase):

    def test_stoichiometry(self):
        """Testing stoichoimetry generation."""
        data = ccData()
        data.atomnos = numpy.array([6, 1, 6, 1, 1, 1])
        self.assertEqual(Nuclear(data).stoichiometry(), "C2H4")
        data.charge = 1
        self.assertEqual(Nuclear(data).stoichiometry(), "C2H4(+1)")
        data.charge = -1
        self.assertEqual(Nuclear(data).stoichiometry(), "C2H4(-1)")
        data.charge = 2
        self.assertEqual(Nuclear(data).stoichiometry(), "C2H4(+2)")
        data.charge = 9
        self.assertEqual(Nuclear(data).stoichiometry(), "C2H4(+9)")

    def test_nre(self):
        """Testing nuclear repulsion energy for one logfile where it is printed."""

        data, logfile = getdatafile(QChem, "basicQChem4.2", ["water_mp4sdq.out"])
        nuclear = Nuclear(data)
        nuclear.logger.setLevel(logging.ERROR)

        with open(logfile.filename) as f:
            output = f.read()
        line = re.search('Nuclear Repulsion Energy = .* hartrees', output).group()
        nre = float(line.split()[4])
        nre = utils.convertor(nre, 'Angstrom', 'bohr')
        self.assertAlmostEqual(nuclear.repulsion_energy(), nre, places=7)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(NuclearTest))
