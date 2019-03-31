class InvalidArgumentError(Error):
    """Raised when the passed arguments are invalid."""
    pass


class UnexpectedLayoutError(Error):
    """Raised when assumptions on the layout of the current page are not met."""
    pass
