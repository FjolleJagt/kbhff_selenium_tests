class KbhffApiError(Exception):
    """Base Class for errors in this API"""
    pass

class InvalidArgumentError(KbhffApiError):
    """Raised when the passed arguments are invalid."""
    pass

class UnexpectedLayoutError(Exception):
    """Raised when assumptions on the layout of the current page are not met."""
    pass

class NoEmailReceivedError(KbhffApiError):
    """Raised when no email as specified could be found."""
    pass

class PageNotImplementedError(KbhffApiError):
    def __init__(self, offending_page, valid_page_dict):
        self.message = "{page_name} is not a known page name. \nKnown page names are: {known}".format(\
                page_name = offending_page,
                known = ", ".join(valid_page_dict.keys()))

    def __str__(self):
        return self.message

class InvalidUserError(KbhffApiError):
    """ Raised when login did not go as expected."""
    pass
