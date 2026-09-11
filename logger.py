import sys
from datetime import datetime
from typing import Literal, Union, Dict, Any, Final

EMOJI_MAP: Final[Dict[str, str]] = {
    "INFO": "ℹ️",
    "PUMP": "🚀",
    "DUMP": "📉",
    "WARN": "⚠️",
    "ERROR": "🚨"
}

class CryptoLogger:
    """
    A specialized console logger for tracking cryptocurrency market movements.
    Injects market sentiment indicators and formats telemetry data.
    """
    def __init__(self, service_name: str) -> None:
        """Initializes the logger with a specific tracker service context."""
        self.service_name: str = service_name

    def _format_message(
        self, 
        level: str, 
        msg: str, 
        trend: Union[Literal["UP", "DOWN", "FLAT"], None]
    ) -> str:
        """Formats the log string with timestamps, service name, and emojis."""
        timestamp: str = datetime.utcnow().isoformat()
        emoji: str = EMOJI_MAP.get(level, "📝")
        trend_indicator: str = f" [{trend}]" if trend else ""
        return f"[{timestamp}] [{self.service_name}] {emoji} {level}{trend_indicator}: {msg}"

    def log(
        self, 
        message: str, 
        level: Literal["INFO", "PUMP", "DUMP", "WARN", "ERROR"] = "INFO",
        trend: Union[Literal["UP", "DOWN", "FLAT"], None] = None,
        payload: Union[Dict[str, Any], None] = None
    ) -> None:
        """
        Emits a structured log line to stdout/stderr.

        :param message: Main descriptive log message.
        :param level: Urgency or semantic category of the event.
        :param trend: Market movement direction helper.
        :param payload: Contextual key-value pairs of tracking data.
        """
        formatted_msg = self._format_message(level, message, trend)
        if payload:
            formatted_msg += f" | Telemetry: {payload}"

        if level in ("WARN", "ERROR"):
            sys.stderr.write(formatted_msg + "\n")
            sys.stderr.flush()
        else:
            sys.stdout.write(formatted_msg + "\n")
            sys.stdout.flush()