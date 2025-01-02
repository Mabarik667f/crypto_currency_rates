class BaseError(Exception):

    def __init__(self, field, msg: str) -> None:
        super().__init__(msg)
        self.field = field
        self.msg = msg

    def to_dict(self):
        return {self.field: self.msg}
