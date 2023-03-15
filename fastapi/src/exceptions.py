from uuid import UUID


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


class PromoIsNotActiveException(Exception):
    def __init__(self, code: str):
        self.message = f"Promo with code = `{code}` is not active."
        super().__init__(self.message)


class PromoIsNotConnectedWithService(Exception):
    def __init__(self, code: str, service_id: UUID):
        self.message = f"Promo with code = `{code}` is not connected with service `{service_id}.`"
        super().__init__(self.message)


class PromoIsNotConnectedWithUser(Exception):
    def __init__(self, code: str, user_id: UUID):
        self.message = f"Promo with code = `{code}` is not connected with user `{user_id}.`"
        super().__init__(self.message)
