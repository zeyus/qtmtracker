import asyncio
from typing import Callable, List, Sequence
from .position import Markers
import qtm

class QTMConfig:
    def __init__(self, qtm_server: str, marker_indices: Sequence[int], position_history_length: int, labels: Sequence[str] = []):
        self.qtm_server = qtm_server
        self.marker_indices = marker_indices
        self.position_history_length = position_history_length
        self.labels = labels


class QTMTracker:
    def __init__(self, config: QTMConfig):
        self.frame_count = 0
        self.config = config
        self.frame_callback = None
        self.markers = Markers(self.config.marker_indices, self.config.position_history_length, self.config.labels)


    async def _setup(self) -> None:
        """ Main function """
        connection: qtm.QRTConnection = await qtm.connect(self.config.qtm_server)
        if connection is None:
            return
        
        await connection.stream_frames(components=["3d"], on_packet=self._on_packet)

    def _on_packet(self, packet: qtm.protocol.QRTPacket) -> None:
        """ Callback function that is called everytime a data packet arrives from QTM """
        self.frame_count += 1
        markers: List[qtm.packet.RT3DMarkerPosition]
        _, markers = packet.get_3d_markers()

        for i, marker_idx in enumerate(self.config.marker_indices):
            self.markers[i].add((markers[marker_idx].x, markers[marker_idx].y, markers[marker_idx].z))
        
        if self.frame_callback is not None:
            result = self.frame_callback(self)
            if result is False:
                self.stop()
    
    def set_frame_callback(self, callback: Callable[['QTMTracker'], bool]) -> None:
        self.frame_callback = callback

    def run(self) -> None:
        self.frame_count = 0
        asyncio.ensure_future(self._setup())
        asyncio.get_event_loop().run_forever()

    def run_while(self) -> None:
        self.frame_count = 0
        asyncio.ensure_future(self._setup())
        asyncio.get_event_loop().run_forever()

    def stop(self) -> None:
        asyncio.get_event_loop().stop()