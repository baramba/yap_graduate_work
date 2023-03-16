from uuid import UUID


class PromoNotFoundException(Exception):
    def __init__(self, code: str):
        self.message = f"Не существует промокода `{code}`."
        super().__init__(self.message)


class PromoIsNotStartedException(Exception):
    def __init__(self, code: str):
        self.message = f"Действие промокода `{code}` еще не началось."
        super().__init__(self.message)


class PromoIsExpiredException(Exception):
    def __init__(self, code: str):
        self.message = f"Действие промокода `{code}` уже завершилось."
        super().__init__(self.message)


class NoAvailableActivationsException(Exception):
    def __init__(self, code: str):
        self.message = f"У промокода `{code}` нет ни одной доступной активации."
        super().__init__(self.message)


class PromoIsNotActiveException(Exception):
    def __init__(self, code: str):
        self.message = f"Промокод `{code}` не активен."
        super().__init__(self.message)


class PromoIsNotConnectedWithService(Exception):
    def __init__(self, code: str, service_id: UUID):
        self.message = f"Промокод `{code}` не связан с продуктом `{service_id}.`"
        super().__init__(self.message)


class PromoIsNotConnectedWithUser(Exception):
    def __init__(self, code: str, user_id: UUID):
        self.message = f"Промокод `{code}` не связан с пользователем `{user_id}.`"
        super().__init__(self.message)
