
class ServiceProviderException(Exception):
    pass


class ServiceProviderDoesNotExistException(ServiceProviderException):
    pass


class InvalidFood(Exception):
    pass
