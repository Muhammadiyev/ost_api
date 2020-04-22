<<<<<<< HEAD
# from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import chat_room.routing
from chat_room.chatmiddleware import TokenAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter(chat_room.routing.websocket_urlpatterns)
    ),
})
=======
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import groups.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            groups.routing.websocket_urlpatterns
        )
    ),
})
>>>>>>> origin
