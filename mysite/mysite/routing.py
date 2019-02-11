from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# noinspection PyUnresolvedReferences,PyPackageRequirements
import blog.routing

application = ProtocolTypeRouter({
	# (http->django views is added by default)
	'websocket': AuthMiddlewareStack(
		URLRouter(
			blog.routing.websocket_urlpatterns
		)
	),
})
