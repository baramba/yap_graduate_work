class PromoNotFoundException(Exception):
    def __init__(self, code: str):
        self.message = f"There is no promo with code = `{code}`."
        super().__init__(self.message)


class PromoIsNotStartedException(Exception):
    def __init__(self, code: str):
        self.message = f"Promo with code = `{code}` is not started."
        super().__init__(self.message)


class PromoIsExpiredException(Exception):
    def __init__(self, code: str):
        self.message = f"Promo with code = `{code}` is expired."
        super().__init__(self.message)


class NoAvailableActivationsException(Exception):
    def __init__(self, code: str):
        self.message = f"Promo with code = `{code}` has no available activations."
        super().__init__(self.message)
