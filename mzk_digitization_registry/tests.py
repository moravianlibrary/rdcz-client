import unittest
from .client import DigitizationRegistryClient
from .datatypes import DigitizationState


class TestDigitizationRegistry(unittest.TestCase):
    def setUp(self):
        self.client = DigitizationRegistryClient()

    def test_get_state_by_barcode(self):
        self.assertEqual(
            self.client.get_record_by_barcode("2619213824").digitization_state,
            DigitizationState.Finished,
        )

        self.assertEqual(
            self.client.get_record_by_barcode("2610280747").digitization_state,
            DigitizationState.Finished,
        )

    def test_get_state_for_volume_by_cnb(self):
        self.assertEqual(
            self.client.select_volume_record(
                self.client.get_issue_records(cnb="cnb002603627"), volume="1"
            ).digitization_state,
            DigitizationState.Finished,
        )

    def test_get_state_for_invalid_cnb(self):
        self.assertIsNone(
            self.client.select_volume_record(
                self.client.get_issue_records(cnb="cnb-invalid"), volume="1"
            )
        )

    def test_get_state_for_periodical_issues(self):
        self.assertEqual(
            DigitizationRegistryClient()
            .get_record_by_barcode(barcode="2610172122")
            .digitization_state,
            DigitizationState.Finished,
        )
        self.assertIsNone(
            self.client.select_volume_record(
                self.client.get_issue_records(
                    cnb="cnb001723088", isxn="9788073580742"
                ),
                barcode="2610312769",
                volume="1, učebnice",
            )
        )
        self.assertEqual(
            self.client.select_volume_record(
                self.client.get_issue_records(isxn="0139-505X"),
                year="2021",
                volume="106",
                bundle="1-37",
            ).digitization_state,
            DigitizationState.Finished,
        )
        self.assertIsNone(
            self.client.select_volume_record(
                self.client.get_issue_records(isxn="0139-505X"),
                year="2022",
                volume="107",
                bundle="33",
            ),
        )
        self.assertIsNone(
            self.client.select_volume_record(
                self.client.get_issue_records(isxn="0139-505X"),
                year="2021",
                volume="107",
                bundle="33",
            ),
        )
        self.assertIsNone(
            self.client.select_volume_record(
                self.client.get_issue_records(isxn="0139-505X"),
                year="2022",
                volume="106",
                bundle="33",
            ),
        )
        self.assertIsNone(
            DigitizationRegistryClient().get_document_record(
                cnb="cnb000280880"
            )
        )
