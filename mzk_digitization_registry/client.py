from requests import Session
from typing import Generator, List, Optional
from cachetools import TTLCache
from .record import DigitizationRegistryRecord


PAGINATE_PAGE_SIZE = 10
REGISTER_SEARCH_ENDPOINT = (
    "https://registrdigitalizace.cz/rdcz/search/rdcz/"
    "select?q={QUERY}&start={START}&rows={ROWS}"
)

cache = TTLCache(maxsize=500, ttl=300)


class DigitizationRegistryClient:
    def __init__(self):
        self._session = Session()

    def _cache_key(self, cnb: Optional[str], isxn: Optional[str]) -> str:
        return f"cnb={cnb}-isxn={isxn}"

    def get_query_records(
        self, query: str
    ) -> Generator[DigitizationRegistryRecord, None, None]:
        start = 0
        while True:
            response = self._session.get(
                REGISTER_SEARCH_ENDPOINT.format(
                    QUERY=query, START=start, ROWS=PAGINATE_PAGE_SIZE
                )
            )

            response.raise_for_status()

            response_data = response.json()["response"]
            num_found = response_data["numFound"]
            documents = response_data["docs"]

            for document in documents:
                yield DigitizationRegistryRecord(document)

            start += PAGINATE_PAGE_SIZE
            if start >= num_found:
                break

    def get_record_by_id(
        self, record_id: str
    ) -> Optional[DigitizationRegistryRecord]:
        documents: List[DigitizationRegistryRecord] = list(
            self.get_query_records(f'id:"{record_id}"')
        )
        if len(documents) != 1:
            return None
        return documents[0]

    def get_record_by_barcode(
        self, barcode: str
    ) -> Optional[DigitizationRegistryRecord]:
        documents: List[DigitizationRegistryRecord] = list(
            self.get_query_records(f'carkod:"{barcode}"')
        )
        if len(documents) != 1:
            return None
        return documents[0]

    def get_issue_records(
        self, cnb: Optional[str] = None, isxn: Optional[str] = None
    ) -> List[DigitizationRegistryRecord]:
        cache_key = self._cache_key(cnb, isxn)

        if cache_key in cache:
            return cache[cache_key]

        if cnb:
            records = list(self.get_query_records((f'ccnb:"{cnb}"')))
            if records:
                cache[cache_key] = records
                return records

        records = list(self.get_query_records((f'isxn:"{isxn}"')))
        cache[cache_key] = records
        return records if isxn else []

    def get_document_record(
        self, cnb: Optional[str] = None, isxn: Optional[str] = None
    ) -> Optional[DigitizationRegistryRecord]:
        records = self.get_issue_records(cnb, isxn)
        return records[0] if len(records) == 1 else None

    def select_volume_record(
        self,
        records: List[DigitizationRegistryRecord],
        barcode: Optional[str] = None,
        year: Optional[str] = None,
        volume: Optional[str] = None,
        bundle: Optional[str] = None,
    ) -> Optional[DigitizationRegistryRecord]:
        for record in records:
            if (barcode is not None and barcode == record.barcode) or (
                (year is None or year == record.year)
                and (volume is None or volume == record.volume)
                and (bundle is None or bundle == record.bundle)
            ):
                return record
        return None
