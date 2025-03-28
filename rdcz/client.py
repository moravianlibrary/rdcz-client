from typing import Dict, Generator, List

from solrify import F, SearchQuery, SolrClient, SolrConfig

from .custom_types import RDczField, RDczState
from .schemas import RDczDocument


class RDczClient(SolrClient[RDczDocument]):
    document_type = RDczDocument

    def __init__(self, config: SolrConfig):
        super().__init__(config)

    def search(self, query: SearchQuery) -> Generator[RDczDocument, None, None]:
        record_state_cache: Dict[str, List[RDczState]] = dict()

        for record in super().search(query):
            if record.record_id not in record_state_cache:
                record_state_cache[record.record_id] = list(
                    set(
                        RDczState.map_from(facet[0])
                        for facet in self.facet(
                            F(RDczField.RecordId, record.record_id),
                            RDczField.State,
                        )
                        if facet[1] > 0
                    )
                )

            record.record_state = record_state_cache[record.record_id]

            yield record

    def get_issue(self, issue_id: str) -> RDczDocument:
        return self.get(self.search(F(RDczField.IssueId, issue_id)))

    def get_all_issues(self, record_id: str) -> List[RDczDocument]:
        return list(self.search(F(RDczField.RecordId, record_id)))
