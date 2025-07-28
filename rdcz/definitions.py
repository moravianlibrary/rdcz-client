from solrify import MappingEnum


class RDczField(MappingEnum):
    """
    Enumeration of Solr field mappings for RDcz (Registr Digitalizace cz).

    These fields are used for mapping Solr document fields to their internal
    representation when querying or indexing documents in the RDcz context.
    """

    IssueId = "id"
    RecordId = "titul_id"

    Barcode = "carkod"
    ControlNumber = "pole001"
    Nbn = "cnb"
    Isxn = "isxn"
    Signature = "signatura"

    State = "stav"

    Title = "title"
    VolumeYear = "rozsah"
    VolumeNumber = "cast"
    Bundle = "cisloper"


class RDczState(MappingEnum):
    """
    Enumeration of digitization states for RDcz items.

    These states reflect the processing or completion status
    of digitized documents in the RDcz system.

    Attributes
    ----------
    Finished : str
        Digitization has been completed.
    InProgress : str
        Digitization is currently in progress.
    Planned : str
        Digitization is planned but not yet started.
    Revision : str
        Item is under revision or review.
    """

    Finished = "dokončeno"
    InProgress = "zpracování"
    Planned = "plánováno"
    Revision = "revize"


class RDczException(Exception):
    """
    Custom exception class for RDcz-related errors.

    This exception should be raised in cases of errors specific
    to RDcz operations or validations.

    Examples
    --------
    >>> raise RDczException("Invalid record ID")
    Traceback (most recent call last):
        ...
    RDczException: Invalid record ID
    """

    pass
