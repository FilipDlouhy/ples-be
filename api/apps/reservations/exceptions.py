from apps.reservations.dtos import SeatResponseSerializer
from common.exceptions import BadRequestError


class NothingSelectedError(BadRequestError):
    """Neither a standing place nor a seat was chosen; the legacy API answered with the key "message"."""

    def __init__(self):
        super().__init__("Either seats or stand tickets must be filled!")

    def to_data(self):
        return {"message": self.message}


class StandsLimitError(BadRequestError):
    """More standing places were requested than are free."""

    def __init__(self, *, requested, available):
        super().__init__("Count of stands is higher than available count!")
        self.requested = requested
        self.available = available

    def to_data(self):
        return {
            "error": self.message,
            "requested_stands": self.requested,
            "available_count": self.available,
        }


class SeatsTakenError(BadRequestError):
    """Some of the chosen seats already belong to a reservation."""

    def __init__(self, *, seats):
        super().__init__("Some seats already have a reservation!")
        self.seats = seats

    def to_data(self):
        return {
            "error": self.message,
            "full_seats": SeatResponseSerializer(self.seats, many=True).data,
        }
