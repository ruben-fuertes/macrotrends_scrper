
class TableParsingError(Exception):
    """Exception created to inform when the table cannot be parsed for
    any reason."""
    pass

class EmptyPageError(Exception):
    """Exception created to inform that the page is empty."""
    pass