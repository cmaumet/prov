'''Test cases for the prov.persistence Django app

@author: Trung Dong Huynh <trungdong@donggiang.com>
@copyright: University of Southampton 2012
'''

import os
import json
import unittest
import logging
from prov.model import ProvBundle
from prov.model.test import examples
from prov.persistence.models import save_bundle, PDBundle

logger = logging.getLogger(__name__)


class SaveLoadTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        self.documents = []

        unittest.TestCase.__init__(self, methodName=methodName)

    def setUp(self):
        pass

    def tearDown(self):
        logger.debug('Deleting all test bundles (%d in total)' % len(self.documents))
        PDBundle.objects.filter(pk__in=self.documents).delete()

    def save_load_graph(self, name, prov_doc):
        logger.debug('Saving PROV document: %s...' % name)
        pdbundle = save_bundle(prov_doc, name)
        db_doc_pk = pdbundle.pk
        self.documents.append()

        logger.debug('Loading bundle from DB: %s...' % name)
        db_doc = PDBundle.objects.get(pk=db_doc_pk)
        loaded_prov_doc = db_doc.get_prov_bundle()
        self.assertEqual(loaded_prov_doc, prov_doc, 'Round-trip DB saving/loading failed:  %s.' % name)

    def testExamples(self):
        for name, doc_method in examples.tests:
            self.save_load_graph(name, doc_method())

    def testProvToolboxJSON(self):
        json_path = os.path.dirname(os.path.abspath(examples.__file__)) + '/json/'
        filenames = os.listdir(json_path)
        for filename in filenames:
            if filename.endswith('.json'):
                with open(json_path + filename) as json_file:
                    prov_doc = json.load(json_file, cls=ProvBundle.JSONDecoder)
                    self.save_load_graph(filename, prov_doc)

if __name__ == "__main__":
    from django.test.utils import setup_test_environment
    setup_test_environment()
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
