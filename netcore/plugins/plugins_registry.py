from plugins.tcp_connect import TCP_Connect
from core.models import Plugin

Registry = {
    Plugin.TCP: TCP_Connect
}
