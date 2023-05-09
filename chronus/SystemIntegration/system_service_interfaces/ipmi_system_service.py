import datetime
from dataclasses import dataclass

import psutil
import pyghmi.ipmi.command as ipmi
from dataclasses_json import dataclass_json
from pyghmi.ipmi.sdr import SensorReading

from chronus.domain.interfaces.system_service_interface import SystemServiceInterface
from chronus.domain.system_sample import CpuFreq, SystemSample


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


def _get_cpu_freq() -> [CpuFreq]:
    return psutil.cpu_freq(percpu=True)


class IpmiSystemService(SystemServiceInterface):
    _conn: ipmi.Command

    def __init__(self):
        self._conn = ipmi.Command()

    def sample(self) -> SystemSample:
        current_power_draw = self._get_system_power_draw()
        cpu_temp = self._get_cpu_temp()
        cpu_power = self._get_cpu_power()
        cpu_freq = _get_cpu_freq()

        return SystemSample(
            datetime.datetime.now(),
            current_power_draw=current_power_draw,
            cpu_temp=cpu_temp,
            cpu_power=cpu_power,
            cpu_freq=cpu_freq,
        )

    def _get_system_power_draw(self) -> float:
        # Create an IPMI connection

        # Get the sensor data
        total_power_raw: SensorReading = self._conn.get_sensor_reading("Total_Power")

        return total_power_raw.value

    def _get_cpu_temp(self):
        # Get the sensor data
        cpu_temp_raw: SensorReading = self._conn.get_sensor_reading("CPU_Temp")

        return cpu_temp_raw.value

    def _get_cpu_power(self):
        # Get the sensor data
        cpu_power_raw: SensorReading = self._conn.get_sensor_reading("CPU_Power")

        return cpu_power_raw.value
