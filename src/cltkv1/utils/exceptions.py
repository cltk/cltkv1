"""Custom exceptions for ``cltk`` library."""


class CLTKException(Exception):
    """Exception class for the ``cltkv1`` library.

    >>> from cltkv1.utils.exceptions import CLTKException
    >>> raise CLTKException
    Traceback (most recent call last):
      ...
      File "<doctest cltkv1.utils.exceptions.CLTKException[1]>", line 1, in <module>
        raise CLTKException
    cltkv1.utils.exceptions.CLTKException
    """


class UnknownLanguageError(CLTKException):
    """Exception for when a user requests an NLP method that is not
    supported.

    TODO: Mk separate exceptions for unknown lang vs unimplemented operation for a known lang

    >>> from cltkv1.utils.exceptions import UnknownLanguageError
    >>> raise UnknownLanguageError
    Traceback (most recent call last):
      ...
      File "<doctest cltkv1.utils.exceptions.UnknownLanguageError[1]>", line 1, in <module>
        raise UnknownLanguageError
    cltkv1.utils.exceptions.UnknownLanguageError
    """
