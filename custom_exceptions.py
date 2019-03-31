class InvalidArgumentError(Exception):
    """Raised when the passed arguments are invalid."""
    pass


class UnexpectedLayoutError(Exception):
    """Raised when assumptions on the layout of the current page are not met."""
    pass
