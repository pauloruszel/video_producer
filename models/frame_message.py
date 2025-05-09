from dataclasses import dataclass
import json
import uuid

@dataclass
class FrameMessage:
    camera_id: str
    timestamp: str
    frame_base64: str
    source_type: str
    encoding: str
    frame_id: str = str(uuid.uuid4())  # gera UUID automaticamente ao instanciar

    def to_json(self):
        return json.dumps({
            "frameId": self.frame_id,
            "cameraId": self.camera_id,
            "timestamp": self.timestamp,
            "frame": self.frame_base64,
            "sourceType": self.source_type,
            "encoding": self.encoding
        })