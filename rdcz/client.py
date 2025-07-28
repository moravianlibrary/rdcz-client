from typing import Dict, Generator, List

from solrify import F, SearchQuery, SolrClient, SolrConfig

from .definitions import RDczField, RDczState
from .schemas import RDczDocument


class RDczClient(SolrClient[RDczDocument]):
    """
    Solr client for querying RDcz (Registr Digitalizace cz) documents.

    This client extends a generic `SolrClient`
    and is specialized to work with `RDczDocument` records,
    using `RDczField` enums for consistent query building.

    Attributes
    ----------
    document_type : Type[RDczDocument]
        The document model used for serialization/deserialization
        of Solr responses.
    """

    document_type = RDczDocument

    def __init__(self, config: SolrConfig):
        """
        Initialize the RDczClient with Solr configuration.

        Parameters
        ----------
        config : SolrConfig
            Configuration for the Solr connection,
            including host, endpoint, timeouts, etc.
        """
        super().__init__(config)

    def search(
        self, query: SearchQuery
    ) -> Generator[RDczDocument, None, None]:
        """
        Execute a Solr search query and yield RDczDocument results.

        This method also augments each document with a `record_state` field,
        which includes all known states
        for the same `record_id` (title) across issues.

        Parameters
        ----------
        query : SearchQuery
            The search query to execute.

        Yields
        ------
        RDczDocument
            An RDcz document with populated `record_state`.
        """
        record_state_cache: Dict[str, List[RDczState]] = dict()

        for record in super().search(query):
            if record.record_id not in record_state_cache:
                record_state_cache[record.record_id] = list(
                    set(
                        RDczState.from_alias(facet[0])
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
        """
        Retrieve a single RDczDocument issue by its unique issue ID.

        Parameters
        ----------
        issue_id : str
            The unique identifier of the issue (Solr field `id`).

        Returns
        -------
        RDczDocument
            The document matching the given issue ID.
        """
        return self.get(self.search(F(RDczField.IssueId, issue_id)))

    def get_all_issues(self, record_id: str) -> List[RDczDocument]:
        """
        Retrieve all issues associated with a given record (title).

        Parameters
        ----------
        record_id : str
            The unique record ID for which to fetch all related issues.

        Returns
        -------
        list of RDczDocument
            A list of documents for all issues belonging to the record.
        """
        return list(self.search(F(RDczField.RecordId, record_id)))
