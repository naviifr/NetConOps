from plugins.tcp_connect import TCP_Connect
from plugins.banner import Banner

registry = {
    TCP_Connect.name : TCP_Connect,
    Banner.name : Banner
}
