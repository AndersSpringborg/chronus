from unittest.mock import call

import pytest
from pyghmi.ipmi.sdr import SensorReading

from chronus.domain.system_sample import SystemSample
from chronus.SystemIntegration.system_service_interfaces.ipmi_system_service import IpmiSystemService


@pytest.fixture
def mock_ipmi(mocker):
    mocker.patch("pyghmi.ipmi.private.localsession.Session")
    mocker.patch("pyghmi.ipmi.command.Command.get_sensor_reading", return_value=get_sensor_data)

    def mock_reading(sensor_reading: SensorReading):
        return mocker.patch(
            "pyghmi.ipmi.command.Command.get_sensor_reading", return_value=sensor_reading
        )

    return mock_reading


def test_returns_system_sample(mock_ipmi):
    # Arrange
    random_sample = get_sensor_data[0]
    mock_ipmi(random_sample)
    ipmi = IpmiSystemService()

    # Act
    sample = ipmi.sample()

    # Assert
    assert sample is not None
    assert isinstance(sample, SystemSample)


def test_gets_power_draw(mock_ipmi):
    # Arrange
    mock = mock_ipmi(
        SensorReading(
            {
                "name": "System Level",
                "type": "Power",
                "id": 1,
                "value": 20.0,
                "imprecision": 1.5,
                "states": [],
                "state_ids": [],
                "health": 0,
            },
            "W",
        )
    )
    ipmi = IpmiSystemService()

    # Act
    sample = ipmi.sample()

    # Assert
    print(mock.call_args_list)
    assert call("Total_Power") in mock.call_args_list
    assert sample.current_power_draw == 20.0


def test_gets_cpu_temp(mock_ipmi):
    # Arrange
    mock = mock_ipmi(
        SensorReading(
            {
                "name": "CPU_Temp",
                "type": "Temperature",
                "id": 3,
                "value": 54.0,
                "imprecision": 1.5,
                "states": [],
                "state_ids": [],
                "health": 0,
            },
            "°C",
        )
    )
    ipmi = IpmiSystemService()

    # Act
    sample = ipmi.sample()

    # Assert
    assert call("CPU_Temp") in mock.call_args_list
    assert sample.cpu_temp == 54.0

def test_gets_cpu_power(mock_ipmi):
    # Arrange
    mock = mock_ipmi(
        SensorReading(
            {
                "name": "CPU1 Power",
                "type": "Power",
                "id": 3,
                "value": 54.0,
                "imprecision": 1.5,
                "states": [],
                "state_ids": [],
                "health": 0,
            },
            "W",
        )
    )
    ipmi = IpmiSystemService()

    # Act
    sample = ipmi.sample()

    # Assert
    assert call("CPU1 Power") in mock.call_args_list
    assert sample.cpu_power == 54.0

get_sensor_data = [
    SensorReading(
        {
            "name": "Inlet_Temp",
            "type": "Temperature",
            "id": 1,
            "value": 35.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Outlet_Temp",
            "type": "Temperature",
            "id": 2,
            "value": 40.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "CPU_Temp",
            "type": "Temperature",
            "id": 3,
            "value": 54.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "DIMMG1_Temp",
            "type": "Temperature",
            "id": 4,
            "value": 49.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "DIMMG2_Temp",
            "type": "Temperature",
            "id": 5,
            "value": 49.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "CPU_VR_Temp",
            "type": "Temperature",
            "id": 6,
            "value": 42.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "SOC_VR_Temp",
            "type": "Temperature",
            "id": 7,
            "value": 46.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "VDD_ABCD_Temp",
            "type": "Temperature",
            "id": 8,
            "value": 45.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "VDD_EFGH_Temp",
            "type": "Temperature",
            "id": 9,
            "value": 46.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "PSU1_Temp",
            "type": "Temperature",
            "id": 14,
            "value": 37.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "PSU2_Temp",
            "type": "Temperature",
            "id": 15,
            "value": 36.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Riser1_GPU_Temp",
            "type": "Temperature",
            "id": 16,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Riser2_GPU_Temp",
            "type": "Temperature",
            "id": 17,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Riser3_GPU_Temp",
            "type": "Temperature",
            "id": 18,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Retimer1_Temp",
            "type": "Temperature",
            "id": 19,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Retimer2_Temp",
            "type": "Temperature",
            "id": 20,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "PCIe1_Inlet_Temp",
            "type": "Temperature",
            "id": 21,
            "value": 39.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "PCIe2_Inlet_Temp",
            "type": "Temperature",
            "id": 22,
            "value": 41.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "MID_BP1_Temp",
            "type": "Temperature",
            "id": 27,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "MID_BP2_Temp",
            "type": "Temperature",
            "id": 28,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Rear_BP_Temp1",
            "type": "Temperature",
            "id": 29,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Riser_Int_Temp",
            "type": "Temperature",
            "id": 32,
            "value": 37.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Riser_1_Temp",
            "type": "Temperature",
            "id": 33,
            "value": 38.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {"name": "Riser_2_Temp", "type": "Temperature", "id": 34, "unavailable": 1}, "°C"
    ),
    SensorReading(
        {"name": "Riser_3_Temp", "type": "Temperature", "id": 35, "unavailable": 1}, "°C"
    ),
    SensorReading(
        {
            "name": "Front_NVME_Temp",
            "type": "Temperature",
            "id": 36,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "MID_NVME_Temp",
            "type": "Temperature",
            "id": 37,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "Rear_NVME_Temp",
            "type": "Temperature",
            "id": 38,
            "value": 0.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "°C",
    ),
    SensorReading(
        {
            "name": "CPU_VDDCR",
            "type": "Voltage",
            "id": 42,
            "value": 1.189,
            "imprecision": 0.0028999999999999027,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "SOC_VDDCR",
            "type": "Voltage",
            "id": 43,
            "value": 0.8236,
            "imprecision": 0.0029000000000000137,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_MEM_ABCD",
            "type": "Voltage",
            "id": 44,
            "value": 1.2064,
            "imprecision": 0.0028999999999999027,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_MEM_EFGH",
            "type": "Voltage",
            "id": 45,
            "value": 1.2064,
            "imprecision": 0.0028999999999999027,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_VPP_ABCD",
            "type": "Voltage",
            "id": 46,
            "value": 2.6,
            "imprecision": 0.00649999999999995,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_VPP_EFGH",
            "type": "Voltage",
            "id": 47,
            "value": 2.6,
            "imprecision": 0.00649999999999995,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "P5V_VDD_RearMID",
            "type": "Voltage",
            "id": 48,
            "value": 4.992000000000001,
            "imprecision": 0.012000000000000455,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "P3V_BAT",
            "type": "Voltage",
            "id": 49,
            "value": 3.16,
            "imprecision": 0.010000000000000231,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDDCR_SOC_DUAL",
            "type": "Voltage",
            "id": 50,
            "value": 0.903,
            "imprecision": 0.010499999999999954,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_5_DUAL",
            "type": "Voltage",
            "id": 52,
            "value": 5.096,
            "imprecision": 0.0389999999999997,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_33_RUN",
            "type": "Voltage",
            "id": 53,
            "value": 3.349,
            "imprecision": 0.025500000000000078,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_VTT_EFGH",
            "type": "Voltage",
            "id": 54,
            "value": 0.595,
            "imprecision": 0.010499999999999954,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_18_RUN",
            "type": "Voltage",
            "id": 55,
            "value": 1.815,
            "imprecision": 0.01649999999999996,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_18_DUAL",
            "type": "Voltage",
            "id": 56,
            "value": 1.8370000000000002,
            "imprecision": 0.01650000000000018,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_5_RUN",
            "type": "Voltage",
            "id": 57,
            "value": 5.148,
            "imprecision": 0.0389999999999997,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "P12V_RUN",
            "type": "Voltage",
            "id": 58,
            "value": 11.834,
            "imprecision": 0.09149999999999991,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_VTT_ABCD",
            "type": "Voltage",
            "id": 60,
            "value": 0.595,
            "imprecision": 0.010499999999999954,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "P1V15_BMC",
            "type": "Voltage",
            "id": 61,
            "value": 1.155,
            "imprecision": 0.010499999999999954,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "P1V2_DDR_BMC",
            "type": "Voltage",
            "id": 62,
            "value": 1.2040000000000002,
            "imprecision": 0.010500000000000176,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "VDD_33_DUAL",
            "type": "Voltage",
            "id": 63,
            "value": 3.366,
            "imprecision": 0.025500000000000078,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "FAN1_F_Speed",
            "type": "Fan",
            "id": 70,
            "value": 23290.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN1_R_Speed",
            "type": "Fan",
            "id": 71,
            "value": 19865.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN2_F_Speed",
            "type": "Fan",
            "id": 72,
            "value": 23016.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN2_R_Speed",
            "type": "Fan",
            "id": 73,
            "value": 19591.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN3_F_Speed",
            "type": "Fan",
            "id": 74,
            "value": 20002.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN3_R_Speed",
            "type": "Fan",
            "id": 75,
            "value": 19728.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN4_F_Speed",
            "type": "Fan",
            "id": 76,
            "value": 21509.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN4_R_Speed",
            "type": "Fan",
            "id": 77,
            "value": 18084.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN5_F_Speed",
            "type": "Fan",
            "id": 78,
            "value": 21646.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN5_R_Speed",
            "type": "Fan",
            "id": 79,
            "value": 18084.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN6_F_Speed",
            "type": "Fan",
            "id": 80,
            "value": 21920.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN6_R_Speed",
            "type": "Fan",
            "id": 81,
            "value": 18495.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN7_F_Speed",
            "type": "Fan",
            "id": 82,
            "value": 23427.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "FAN7_R_Speed",
            "type": "Fan",
            "id": 83,
            "value": 19591.0,
            "imprecision": 205.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "RPM",
    ),
    SensorReading(
        {
            "name": "PSU1_PIN",
            "type": "Power",
            "id": 86,
            "value": 96.0,
            "imprecision": 9.0,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "PSU1_POUT",
            "type": "Power",
            "id": 87,
            "value": 92.0,
            "imprecision": 12.0,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "PSU1_VIN",
            "type": "Voltage",
            "id": 88,
            "value": 224.48000000000002,
            "imprecision": 1.8300000000000125,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "PSU1_VOUT",
            "type": "Voltage",
            "id": 89,
            "value": 12.200000000000001,
            "imprecision": 0.15000000000000036,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "PSU1_IIN",
            "type": "Current",
            "id": 90,
            "value": 0.45,
            "imprecision": 0.07500000000000001,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "% A",
    ),
    SensorReading(
        {
            "name": "PSU2_PIN",
            "type": "Power",
            "id": 91,
            "value": 84.0,
            "imprecision": 9.0,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "PSU2_POUT",
            "type": "Power",
            "id": 92,
            "value": 76.0,
            "imprecision": 12.0,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "PSU2_VIN",
            "type": "Voltage",
            "id": 93,
            "value": 224.48000000000002,
            "imprecision": 1.8300000000000125,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "PSU2_VOUT",
            "type": "Voltage",
            "id": 94,
            "value": 12.200000000000001,
            "imprecision": 0.15000000000000036,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "V",
    ),
    SensorReading(
        {
            "name": "PSU2_IIN",
            "type": "Current",
            "id": 95,
            "value": 0.4,
            "imprecision": 0.07500000000000001,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "% A",
    ),
    SensorReading(
        {
            "name": "CPU_Power",
            "type": "Power",
            "id": 102,
            "value": 50.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "MEM_Power",
            "type": "Power",
            "id": 103,
            "value": 12.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "Total_Power",
            "type": "Power",
            "id": 106,
            "value": 168.0,
            "imprecision": 9.0,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "W",
    ),
    SensorReading(
        {
            "name": "Airflow_rate",
            "type": "Other",
            "id": 126,
            "value": 74.0,
            "imprecision": 1.5,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "CFM",
    ),
    SensorReading(
        {
            "name": "Cooling_Status",
            "type": "Other",
            "id": 127,
            "states": ["Redundant"],
            "state_ids": [723712],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PSU1_Fan_Status",
            "type": "Fan",
            "id": 128,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PSU2_Fan_Status",
            "type": "Fan",
            "id": 129,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PSU1_Status",
            "type": "Power Supply",
            "id": 130,
            "states": ["Present"],
            "state_ids": [552704],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PSU2_Status",
            "type": "Power Supply",
            "id": 131,
            "states": ["Present"],
            "state_ids": [552704],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PS_Redundant",
            "type": "Power Supply",
            "id": 132,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PS_Mismatch",
            "type": "Power Supply",
            "id": 133,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE1_AER",
            "type": "Critical interrupt",
            "id": 134,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE2_AER",
            "type": "Critical interrupt",
            "id": 135,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE3_AER",
            "type": "Critical interrupt",
            "id": 136,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE4_AER",
            "type": "Critical interrupt",
            "id": 137,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE5_AER",
            "type": "Critical interrupt",
            "id": 138,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE6_AER",
            "type": "Critical interrupt",
            "id": 139,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE7_AER",
            "type": "Critical interrupt",
            "id": 140,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE8_AER",
            "type": "Critical interrupt",
            "id": 141,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE9_AER",
            "type": "Critical interrupt",
            "id": 142,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "ALL_NVMEs_AER",
            "type": "Critical interrupt",
            "id": 143,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "CPU_ALERT",
            "type": "Processor",
            "id": 144,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "CPU_Prochot",
            "type": "Processor",
            "id": 145,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "CPU_Thermaltrip",
            "type": "Processor",
            "id": 146,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "CPU_MCA_Error",
            "type": "Processor",
            "id": 147,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "TPM_Binding",
            "type": "Physical Security",
            "id": 150,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "TPM_Policy",
            "type": "Physical Security",
            "id": 151,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "TPM_Toggling",
            "type": "Physical Security",
            "id": 152,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "OCP_AER",
            "type": "Critical interrupt",
            "id": 154,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "M2_Card_Fault",
            "type": "Slot/Connector",
            "id": 155,
            "states": ["Slot/connector installed"],
            "state_ids": [2191106],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_1",
            "type": "Memory",
            "id": 160,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {"name": "DIMM_2", "type": "Memory", "id": 161, "states": [], "state_ids": [], "health": 0},
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_3",
            "type": "Memory",
            "id": 162,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {"name": "DIMM_4", "type": "Memory", "id": 163, "states": [], "state_ids": [], "health": 0},
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_5",
            "type": "Memory",
            "id": 164,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {"name": "DIMM_6", "type": "Memory", "id": 165, "states": [], "state_ids": [], "health": 0},
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_7",
            "type": "Memory",
            "id": 166,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {"name": "DIMM_8", "type": "Memory", "id": 167, "states": [], "state_ids": [], "health": 0},
        "",
    ),
    SensorReading(
        {"name": "DIMM_9", "type": "Memory", "id": 168, "states": [], "state_ids": [], "health": 0},
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_10",
            "type": "Memory",
            "id": 169,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_11",
            "type": "Memory",
            "id": 170,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_12",
            "type": "Memory",
            "id": 171,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_13",
            "type": "Memory",
            "id": 172,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_14",
            "type": "Memory",
            "id": 173,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_15",
            "type": "Memory",
            "id": 174,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "DIMM_16",
            "type": "Memory",
            "id": 175,
            "states": ["Present"],
            "state_ids": [814854],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Front_BP1_Cable",
            "type": "Cable/Interconnect",
            "id": 176,
            "states": ["Connected"],
            "state_ids": [1797888],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Front_BP2_Cable",
            "type": "Cable/Interconnect",
            "id": 177,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Front_BP3_Cable",
            "type": "Cable/Interconnect",
            "id": 178,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Middle_BP1_Cable",
            "type": "Cable/Interconnect",
            "id": 179,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Middle_BP2_Cable",
            "type": "Cable/Interconnect",
            "id": 180,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Rear_BP_Cable",
            "type": "Cable/Interconnect",
            "id": 181,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "VGA_Cable",
            "type": "Cable/Interconnect",
            "id": 182,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Front_USB_Cable",
            "type": "Cable/Interconnect",
            "id": 183,
            "states": ["Connected"],
            "state_ids": [1797888],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "M2_Cable",
            "type": "Cable/Interconnect",
            "id": 184,
            "states": ["Connected"],
            "state_ids": [1797888],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Fan_Type_Err",
            "type": "Cable/Interconnect",
            "id": 185,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Chassis_Intr",
            "type": "Physical Security",
            "id": 186,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Intr_Cable",
            "type": "Cable/Interconnect",
            "id": 187,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE1_Status",
            "type": "Add-in Card",
            "id": 192,
            "states": ["Present"],
            "state_ids": [1509377],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE2_Status",
            "type": "Add-in Card",
            "id": 193,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE3_Status",
            "type": "Add-in Card",
            "id": 194,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE4_Status",
            "type": "Add-in Card",
            "id": 195,
            "states": ["Present"],
            "state_ids": [1509377],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE5_Status",
            "type": "Add-in Card",
            "id": 196,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE6_Status",
            "type": "Add-in Card",
            "id": 197,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE7_Status",
            "type": "Add-in Card",
            "id": 198,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE8_Status",
            "type": "Add-in Card",
            "id": 199,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "PCIE9_Status",
            "type": "Add-in Card",
            "id": 200,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "OCP_Status",
            "type": "Add-in Card",
            "id": 201,
            "states": ["Present"],
            "state_ids": [1509377],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "ACPI_State",
            "type": "System ACPI Power State",
            "id": 202,
            "states": ["Online"],
            "state_ids": [2256640],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Watchdog2",
            "type": "Watchdog",
            "id": 203,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Power_Button",
            "type": "Button/switch",
            "id": 204,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Event_Log",
            "type": "Event Log Disabled",
            "id": 205,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive0",
            "type": "Drive Bay",
            "id": 208,
            "states": ["Present"],
            "state_ids": [880384],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive1",
            "type": "Drive Bay",
            "id": 209,
            "states": ["Present"],
            "state_ids": [880384],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive2",
            "type": "Drive Bay",
            "id": 210,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive3",
            "type": "Drive Bay",
            "id": 211,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive4",
            "type": "Drive Bay",
            "id": 212,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive5",
            "type": "Drive Bay",
            "id": 213,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive6",
            "type": "Drive Bay",
            "id": 214,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive7",
            "type": "Drive Bay",
            "id": 215,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive8",
            "type": "Drive Bay",
            "id": 216,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive9",
            "type": "Drive Bay",
            "id": 217,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive10",
            "type": "Drive Bay",
            "id": 218,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive11",
            "type": "Drive Bay",
            "id": 219,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive12",
            "type": "Drive Bay",
            "id": 220,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive13",
            "type": "Drive Bay",
            "id": 221,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive14",
            "type": "Drive Bay",
            "id": 222,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive15",
            "type": "Drive Bay",
            "id": 223,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive16",
            "type": "Drive Bay",
            "id": 224,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive17",
            "type": "Drive Bay",
            "id": 225,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive18",
            "type": "Drive Bay",
            "id": 226,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive19",
            "type": "Drive Bay",
            "id": 227,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive20",
            "type": "Drive Bay",
            "id": 228,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive21",
            "type": "Drive Bay",
            "id": 229,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive22",
            "type": "Drive Bay",
            "id": 230,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive23",
            "type": "Drive Bay",
            "id": 231,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive24",
            "type": "Drive Bay",
            "id": 232,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive25",
            "type": "Drive Bay",
            "id": 233,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive26",
            "type": "Drive Bay",
            "id": 234,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive27",
            "type": "Drive Bay",
            "id": 235,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive28",
            "type": "Drive Bay",
            "id": 236,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive29",
            "type": "Drive Bay",
            "id": 237,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive30",
            "type": "Drive Bay",
            "id": 238,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "Drive31",
            "type": "Drive Bay",
            "id": 239,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "M2_Drive0",
            "type": "Drive Bay",
            "id": 244,
            "states": ["Present"],
            "state_ids": [880384],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "M2_Drive1",
            "type": "Drive Bay",
            "id": 245,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
    SensorReading(
        {
            "name": "BMC_Boot_Up",
            "type": "Microcontroller/Coprocessor",
            "id": 250,
            "states": [],
            "state_ids": [],
            "health": 0,
        },
        "",
    ),
]
