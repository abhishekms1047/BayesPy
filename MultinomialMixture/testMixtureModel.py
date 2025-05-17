#!/usr/bin/python

import os
import logging
import unittest

import csv
import multinomialMixtureEstimation as MME


def import_file(filename):
    """Python 3 compatible version of ``MME.importFile``."""
    with open(filename, 'r') as infile:
        reader = csv.reader(infile, delimiter='\t')
        mixture = list(map(float, next(reader)))
        multinomials = [list(map(float, row)) for row in reader]
    K = len(multinomials[0]) if multinomials else 2
    return MME.MultinomialMixtureModel(len(mixture), K, multinomials, mixture)


class TestMixtureModel(unittest.TestCase):
    """Tests for the multinomial mixture estimation."""

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        model_path = os.path.join(os.path.dirname(__file__), "sampleModel.txt")
        self.model = import_file(model_path)
        self.dataset = [self.model.sampleRow(8) for _ in range(500)]
        hyper = MME.MultinomialMixtureModelHyperparams(2, 3, [1, 1], [1, 1, 1])
        self.finalModel = MME.computeDirichletMixture(self.dataset, hyper, 10)

    def test_final_model(self):
        mixture = self.finalModel.mixture
        self.assertEqual(len(mixture), 2)
        self.assertAlmostEqual(sum(mixture), 1.0, places=5)

        multinomials = self.finalModel.multinomials
        self.assertEqual(len(multinomials), 2)
        for multinomial in multinomials:
            self.assertEqual(len(multinomial), 3)


if __name__ == "__main__":
    unittest.main()
