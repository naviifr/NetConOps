from plugins.tcp_connect import TCP_Connect
from plugins.banner import Banner

registry = {
    "tcp" : TCP_Connect,
    "banner" : Banner
}
