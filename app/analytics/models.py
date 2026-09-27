from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import StrEnum
from typing import Optional


class Direction(StrEnum):
    BUY = "BUY"
    SELL = "SELL"
    WAIT = "WAIT"


class SignalState(StrEnum):
    WAIT = "WAIT"
    BIAS = "BIAS"
    SETUP = "SETUP"
    TRIGGER = "TRIGGER"
    CONFIRMED = "CONFIRMED"


@dataclass(frozen=True)
class AnalysisResult:
    symbol: str
    timeframe: str
    direction: Direction
    confidence: int
    state: SignalState
    entry_low: Optional[float] = None
    entry_high: Optional[float] = None
    stop_loss: Optional[float] = None
    tp1: Optional[float] = None
    tp2: Optional[float] = None
    tp3: Optional[float] = None
    rr: Optional[float] = None
    reason: str = ""
    alternative: str = ""
    data_timestamp: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")
        if self.state == SignalState.WAIT and self.direction != Direction.WAIT:
            raise ValueError("WAIT state requires WAIT direction")
        if self.entry_low is not None and self.entry_high is not None:
            if self.entry_low > self.entry_high:
                raise ValueError("entry_low cannot exceed entry_high")
