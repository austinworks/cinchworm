from dataclasses import dataclass, field
from construct import Array, Int16ub, Int16sb, Int24sb, Struct


@dataclass
class Segment:
    min: int
    max: int
    offset: int
    data: list = field(default_factory=list)

    def emit(self):
        format = Struct("min" / Int24sb, "size" / Int16sb,
                        "data" / Array(lambda this: this.size, Int16ub))
        return format.build(
            dict(min=self.min, size=len(self.data), data=[x - self.min for x in self.data]))


class Segmenter:
    ALLOWED_RANGE = 65535

    def __init__(self, data):
        self.data = data

    def segments(self):
        segment_data = []
        segment_idx = 0
        for idx, current in enumerate(self.data):
            if len(segment_data) < segment_idx + 1:
                current_segment = Segment(min=current, max=current, offset=idx)
                segment_data.append(current_segment)
            if current > current_segment.min + self.ALLOWED_RANGE:
                segment_idx += 1
                current_segment = Segment(min=current, max=current, offset=idx)
                segment_data.append(current_segment)
            if current < current_segment.max - self.ALLOWED_RANGE:
                segment_idx += 1
                current_segment = Segment(min=current, max=current, offset=idx)
                segment_data.append(current_segment)
            current_segment.min = min([current, current_segment.min])
            current_segment.max = max([current, current_segment.max])
            current_segment.data.append(current)
        return segment_data
