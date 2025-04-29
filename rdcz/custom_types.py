from solrify import MappingEnum


class RDczField(MappingEnum):
    IssueId = ("issue_id", "id")
    RecordId = ("record_id", "titul_id")

    Barcode = ("barcode", "carkod")
    ControlNumber = ("control_number", "pole001")
    Nbn = ("nbn", "cnb")
    Isxn = ("isxn", "isxn")
    Signature = ("signature", "signatura")

    State = ("state", "stav")

    Title = ("title", "title")
    VolumeYear = ("volume_year", "rozsah")
    VolumeNumber = ("volume_number", "cast")
    Bundle = ("bundle", "cisloper")


class RDczState(MappingEnum):
    Finished = ("Finished", "dokončeno")
    InProgress = ("InProgress", "zpracování")
    Planned = ("Planned", "plánováno")
    Revision = ("Revision", "revize")


class RDczException(Exception):
    pass
