from enum import Enum


class DigitizationState(Enum):
    Finished = "Finished"
    InProgress = "InProgress"
    Planned = "Planned"
    NotDigitized = "NotDigitized"
    Unknown = "Unknown"


class UnknownDigitizationStateException(Exception):
    def __init__(state: str):
        super().__init__(f"Unknown digitization state: {state}")
