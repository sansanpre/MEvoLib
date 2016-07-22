#-------------------------------------------------------------------------------
#
#   MEvoLib  Copyright (C) 2016  J. Alvarez-Jarreta
#
#   This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
#   This is free software, and you are welcome to redistribute it under certain
#   conditions; type `show c' for details.
#
#-------------------------------------------------------------------------------
# File :  test_Inference_FastTree.py
# Last version :  v1.00 ( 16/Jul/2016 )
# Description :  Test suite for MEvoLib.Inference module: FastTree software
#       tool.
#-------------------------------------------------------------------------------
# Historical report :
#
#   DATE :  16/Jul/2016
#   VERSION :  v1.00
#   AUTHOR(s) :  J. Alvarez-Jarreta
#
#-------------------------------------------------------------------------------

import os
import sys
import unittest

from Bio import SeqIO

from MEvoLib import MissingExtDependencyError
from MEvoLib import Inference
from MEvoLib._py3k import getoutput, viewkeys


#-------------------------------------------------------------------------------

# Try to avoid problems when the OS is in another language
os.environ['LANG'] = 'C'

fasttree_exe = None
if ( sys.platform == 'win32' ) :
    raise MissingExtDependencyError('Testing with FastTree not implemented on' \
                                    ' Windows yet')
else :
    output = getoutput('fasttree')
    if ( ('not found' not in output) and ('FastTree' in output) ) :
        fasttree_exe = 'fasttree'
if ( not fasttree_exe ) :
    raise MissingExtDependencyError('Install FastTree if you want to use it ' \
                                    'from MEvoLib.Inference.get_phylogeny().')


#-------------------------------------------------------------------------------

class InferenceTestCase ( unittest.TestCase ) :

    def setUp ( self ) :
        self.files_to_clean = set()


    def tearDown ( self ) :
        for filename in self.files_to_clean :
            if ( os.path.isfile(filename) ) :
                os.remove(filename)


    def standard_test ( self, informat, outformat, params ) :
        """
        Standard testing procedure used by all tests.

        Arguments :
            informat  ( string )
                Input file format.
            outformat  ( string )
                Output file format.
            params  ( string )
                Arguments passed to the phylogenetic inference tool.
        """
        infile = '{}/f001.mafft_default.aln'.format(informat.capitalize())
        outfile = 'tmp_test.tree'
        self.add_file_to_clean(outfile)
        # Check the input
        self.assertTrue(os.path.isfile(infile))
        self.assertEqual(len(list(SeqIO.parse(infile, informat))), 50)
        # Generate the phylogeny
        t, score = Inference.get_phylogeny(fasttree_exe, infile, informat,
            args=params, outfile=outfile, outfile_format=outformat)
        # Check the output
        self.assertTrue(os.path.isfile(outfile))


    def add_file_to_clean ( self, filename ) :
        """
        Adds a file for deferred removal by the tearDown() routine.

        Arguments :
            filename  ( string )
                File name to remove by the tearDown() routine.
        """
        self.files_to_clean.add(filename)



class FastTreeTestCase ( InferenceTestCase ) :

    def test_simple_phylo_inference ( self ) :
        """
        Test of the phylogenetic inference method for all the available
        configurations with supported input and output formats.
        """
        for keyword in viewkeys(Inference.get_keywords(fasttree_exe)) :
            self.standard_test('fasta', 'newick', keyword)


    def test_conversion_phylo_inference ( self ) :
        """
        Test of the phylogenetic inference method with unsupported input and
        output formats (internal conversion required).
        """
        self.standard_test('phylip', 'nexus', 'default')


#-------------------------------------------------------------------------------

if ( __name__ == '__main__' ) :
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)


#-------------------------------------------------------------------------------
