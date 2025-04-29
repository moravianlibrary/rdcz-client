from solrify import MappingEnum


class RDczField(MappingEnum):
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
    Finished = "dokončeno"
    InProgress = "zpracování"
    Planned = "plánováno"
    Revision = "revize"


class RDczException(Exception):
    pass
