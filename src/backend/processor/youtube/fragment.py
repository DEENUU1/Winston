from dataclasses import dataclass


@dataclass
class Fragment:
    start_time: float
    end_time: float
    transcriptions: str
