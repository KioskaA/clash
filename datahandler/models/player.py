from typing import Literal


class BasePlayer():

    __slots__ = ("tag", "name", "_raw_data")

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"<{self.__class__.__name__} tag={self.tag} name={self.name}>"

    def __eq__(self, other):
        return isinstance(other, BasePlayer) and self.tag == other.tag
    
    def __init__(self, data):
        self._raw_data = data
        self.tag = data.get("tag")
        self.name = data.get("name")

class ClanMember(BasePlayer):
    ...

class LeaveReason():

    __slots__ = ("reason_text", "kicker", "reason", "is_kicked")

    def __str__(self):
        return self.reason

    def __repr__(self):
        return f"<{self.__class__.__name__} reason={self.reason}>"
    
    def __init__(self, reason: Literal["left", "kicked"], reason_text: str | None = None, kicker: ClanMember | None = None):
        if reason not in ["left", "kicked"]:
            raise ValueError(f"reason must be either 'left' or 'kicked', got '{reason}'")
        
        if kicker is not None and not isinstance(kicker, ClanMember):
            raise TypeError(f"kicker must be ClanMember or None, got {type(kicker).__name__}")

        if reason == "kicked" and kicker == None:
            raise ValueError("kicker must be provided when reason is 'kicked'")

        self.reason = reason
        self.reason_text = str(reason_text)
        self.kicker = kicker
        self.is_kicked = True if reason == "kicked" else self.is_kicked = False
