import socket
import struct
import logging
from enum import IntEnum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class RCONPacketType(IntEnum):
    LOGIN = 3
    COMMAND = 2
    RESPONSE = 0


@dataclass
class RCONPacket:
    packet_id: int
    packet_type: RCONPacketType
    payload: str


class RCONClient:
    def __init__(self, host: str, port: int, password: str, timeout: float = 5.0):
        self.host = host
        self.port = port
        self.password = password
        self.timeout = timeout
        self._socket: socket.socket | None = None
        self._request_id = 0

    def connect(self) -> None:
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(self.timeout)
        self._socket.connect((self.host, self.port))
        self._authenticate()
        logger.info(f"RCON підключено до {self.host}:{self.port}")

    def disconnect(self) -> None:
        if self._socket:
            self._socket.close()
            self._socket = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.disconnect()

    def send_command(self, command: str) -> str:
        self._request_id += 1
        self._send_packet(RCONPacketType.COMMAND, command, self._request_id)
        response = self._read_packet()
        return response.payload

    def _authenticate(self) -> None:
        self._send_packet(RCONPacketType.LOGIN, self.password, 1)
        response = self._read_packet()
        if response.packet_id == -1:
            raise ConnectionRefusedError("RCON: невірний пароль!")

    def _send_packet(self, packet_type: RCONPacketType, payload: str, packet_id: int) -> None:
        payload_bytes = payload.encode("utf-8")
        data = struct.pack("<ii", packet_id, int(packet_type))
        data += payload_bytes + b"\x00\x00"
        packet = struct.pack("<i", len(data)) + data
        self._socket.sendall(packet)

    def _read_packet(self) -> RCONPacket:
        length_data = self._recv_exact(4)
        length = struct.unpack("<i", length_data)[0]
        body = self._recv_exact(length)
        packet_id, packet_type = struct.unpack("<ii", body[:8])
        payload = body[8:-2].decode("utf-8", errors="replace")
        return RCONPacket(packet_id, RCONPacketType(packet_type), payload)

    def _recv_exact(self, n: int) -> bytes:
        data = b""
        while len(data) < n:
            chunk = self._socket.recv(n - len(data))
            if not chunk:
                raise ConnectionError("RCON: з'єднання розірвано")
            data += chunk
        return data