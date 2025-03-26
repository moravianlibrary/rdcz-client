from solrify import MappingEnum


class RDczField(MappingEnum):
    IssueId = ("IssueId", "id")
    RecordId = ("RecordId", "titul_id")

    Barcode = ("Barcode", "carkod")
    ControlNumber = ("ControlNumber", "pole001")
    Nbn = ("Nbn", "cnb")
    Isxn = ("Isxn", "isxn")
    Signature = ("Signature", "signatura")

    State = ("State", "stav")

    Title = ("Title", "title")
    VolumeYear = ("VolumeYear", "rozsah")
    VolumeNumber = ("VolumeNumber", "cast")
    Bundle = ("Bundle", "cisloper")


class RDczState(MappingEnum):
    Finished = ("Finished", "dokončeno")
    InProgress = ("InProgress", "zpracování")
    Planned = ("Planned", "plánováno")
    Revision = ("Revision", "revize")


class RDczException(Exception):
    pass
