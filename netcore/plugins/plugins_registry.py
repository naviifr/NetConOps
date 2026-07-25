from plugins.tcp_connect import TCP_Connect
from core.models import Plugin
from plugins.banner import Banner

Registry = {
    Plugin.TCP: TCP_Connect,
    Plugin.BANNER: Banner
}
