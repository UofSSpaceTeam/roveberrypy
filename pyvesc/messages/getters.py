from pyvesc.messages.base import VESCMessage

class ReqSubscription(metaclass=VESCMessage):
    """ Request what messages a device is subscribed to.

    """
    id = 36
    fields = [
            ('subscription', 's')
    ]

