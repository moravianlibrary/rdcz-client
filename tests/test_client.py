import unittest
from typing import Any, Dict, List

from solrify import F, SearchQuery, SolrConfig

from rdcz.client import RDczClient
from rdcz.definitions import RDczField, RDczState


class TestClient(unittest.TestCase):
    def setUp(self):
        self.client = RDczClient(
            SolrConfig(
                host="https://registrdigitalizace.cz",
                endpoint="rdcz/search/rdcz/select",
            )
        )

    def _assertQueryResults(
        self, query: SearchQuery, expected_results: List[Dict[str, Any]]
    ):
        for i, record in enumerate(self.client.search(query)):
            self.assertDictEqual(expected_results[i], record.model_dump())

    def test_search_by_barcode(self):
        self._assertQueryResults(
            F(RDczField.Barcode, "2619213824"),
            [
                {
                    "barcode": "2619213824",
                    "bundle": None,
                    "control_number": "000724903",
                    "issue_id": "52802",
                    "isxn": None,
                    "nbn": None,
                    "record_id": 52802,
                    "record_state": [RDczState.Finished],
                    "signature": "1-0022.371",
                    "state": RDczState.Finished,
                    "title": "Lurdy a pouť do Lurd r. 1896 konaná",
                    "volume_number": None,
                    "volume_year": None,
                }
            ],
        )

        self._assertQueryResults(
            F(RDczField.Barcode, "2610280747"),
            [
                {
                    "barcode": "2610280747",
                    "bundle": "1-4",
                    "control_number": "000369077",
                    "issue_id": "80990",
                    "isxn": ["1211-3638"],
                    "nbn": None,
                    "record_id": 80983,
                    "record_state": [RDczState.Finished],
                    "signature": "02649-1051.355",
                    "state": RDczState.Finished,
                    "title": "Bílé Karpaty",
                    "volume_number": "2005",
                    "volume_year": "2005",
                }
            ],
        )

    def test_search_by_cnb(self):
        self._assertQueryResults(
            F(RDczField.Nbn, "cnb002603627"),
            [
                {
                    "barcode": "1001644398",
                    "bundle": None,
                    "control_number": "cpk20142603627",
                    "issue_id": "1004823",
                    "isxn": ["0231-8970"],
                    "nbn": None,
                    "record_id": 542733,
                    "record_state": [RDczState.Finished],
                    "signature": "Nd 001023/1971",
                    "state": RDczState.Finished,
                    "title": "Campanula",
                    "volume_number": "2",
                    "volume_year": None,
                },
                {
                    "barcode": "1002066570",
                    "bundle": None,
                    "control_number": "cpk20142603627",
                    "issue_id": "1009764",
                    "isxn": ["0231-8970"],
                    "nbn": None,
                    "record_id": 542733,
                    "record_state": [RDczState.Finished],
                    "signature": "II 070396/Rok 1970",
                    "state": RDczState.Finished,
                    "title": "Campanula",
                    "volume_number": "1",
                    "volume_year": None,
                },
                {
                    "barcode": "2619002962",
                    "bundle": None,
                    "control_number": "001293351",
                    "issue_id": "1030714",
                    "isxn": ["0231-8970"],
                    "nbn": None,
                    "record_id": 1023570,
                    "record_state": [RDczState.Finished],
                    "signature": "2-0666.043",
                    "state": RDczState.Finished,
                    "title": "Campanula",
                    "volume_number": "3",
                    "volume_year": "1972",
                },
                {
                    "barcode": "2619002964",
                    "bundle": None,
                    "control_number": "001293351",
                    "issue_id": "1030716",
                    "isxn": ["0231-8970"],
                    "nbn": None,
                    "record_id": 1023570,
                    "record_state": [RDczState.Finished],
                    "signature": "2-0666.043",
                    "state": RDczState.Finished,
                    "title": "Campanula",
                    "volume_number": "6",
                    "volume_year": "1984",
                },
                {
                    "barcode": "1002206927",
                    "bundle": None,
                    "control_number": "cpk20142603627",
                    "issue_id": "542733",
                    "isxn": ["0231-8970"],
                    "nbn": None,
                    "record_id": 542733,
                    "record_state": [RDczState.Finished],
                    "signature": "II 086927",
                    "state": RDczState.Finished,
                    "title": "Campanula",
                    "volume_number": "5",
                    "volume_year": None,
                },
            ],
        )

    def test_search_by_invalid_cnb(self):
        self._assertQueryResults(F(RDczField.Nbn, "cnb-invalid"), [])
