from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# noinspection PyUnresolvedReferences,PyPackageRequirements
import chat.routing

application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			chat.routing.websocket_urlpatterns
		)
	),
})
