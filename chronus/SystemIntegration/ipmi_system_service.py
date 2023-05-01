import datetime
from dataclasses import dataclass

import pyghmi.ipmi.command as ipmi
from dataclasses_json import dataclass_json
from pyghmi.ipmi.sdr import SensorReading

from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.system_sample import SystemSample


@dataclass
class SensorData:
    value: float
    states: [str]
    state_ids: [str]
    units: str
    imprecision: float
    name: str
    sensor_type: str
    unavailable: int
    health: int


class IpmiSystemService(SystemServiceInterface):
    def sample(self) -> SystemSample:
        current_power_draw = self._get_system_power_draw()

        return SystemSample(datetime.datetime.now(), current_power_draw=current_power_draw)

    def _get_system_power_draw(self) -> float:
        # Create an IPMI connection
        conn = ipmi.Command()

        # Get the sensor data
        total_power_raw: SensorReading = conn.get_sensor_reading("Total_Power")
        print()
        return total_power_raw.value
