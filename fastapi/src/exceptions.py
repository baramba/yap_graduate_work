class PromoNotFoundException(Exception):
    def __init__(self, code: str):
        super().__init__(f"There is no promo with code = `{code}`.")


class PromoIsNotStartedException(Exception):
    def __init__(self, code: str):
        super().__init__(f"Promo with code = `{code}` is not started.")


class PromoIsExpiredException(Exception):
    def __init__(self, code: str):
        super().__init__(f"Promo with code = `{code}` is expired.")


class NoAvailableActivationsException(Exception):
    def __init__(self, code: str):
        super().__init__(f"Promo with code = `{code}` has no available activations.")
