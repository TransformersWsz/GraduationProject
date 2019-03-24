class PoolEmptyError(Exception):

    def __init__(self, errorInfo):
        super().__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return self.errorInfo
