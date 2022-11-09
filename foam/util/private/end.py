__all__ = ['END', 'End', 'end']


class end:
    '''End of indented code block

    Example:
        ```python
        class func:
            @staticmethod
            def reciprocal(x: int) -> float:
                return 1.0 / x
            End.Def
        End.Class

        for ith in range(10):
            if ith < 7:
                try:
                    print(func.reciprocal(ith))
                except ZeroDivisionError:
                    print('NaN')
                End.Try
            End.If
        End.For
        ```

    Reference:
        - https://docs.python.org/3/reference/compound_stmts.html

    Statement:
        - [x] if_stmt
        - [x] while_stmt
        - [x] for_stmt
        - [x] try_stmt
        - [x] with_stmt
        - [x] match_stmt
        - [x] funcdef
        - [x] classdef
        - [x] async_with_stmt
        - [x] async_for_stmt
        - [x] async_funcdef
    '''

    IF = If = if_ = None
    WHILE = While = while_ = None
    FOR = For = for_ = None
    TRY = Try = try_ = None
    WITH = With = with_ = None
    MATCH = Match = match_ = None
    CASE = Case = case_ = None  # placeholder only
    DEF = Def = def_ = None
    CLASS = Class = class_ = None
    ASYNC_WITH = AsyncWith = async_with = None
    ASYNC_FOR = AsyncFor = async_for = None
    ASYNC_DEF = AsyncDef = async_def = None


END = End = end
