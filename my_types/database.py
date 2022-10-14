from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class radioActivity:
    radio: str
    guild_id: int
    channel_id: int

sql_command: TypeAlias = str
lastrowid: TypeAlias = int