from chronus.domain.configuration import Configurations
from chronus.domain.interfaces.cpu_info_service_interface import CpuInfo


def test_configuration_1_core_1_frequency():
    # arrange
    info = CpuInfo(cpu="cpu", cores=1, frequencies=[1.0])

    # act
    configurations = Configurations(info)

    # assert
    assert len(configurations) == 1
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 1.0


def test_configuration_2_cores_1_frequency():
    # arrange
    info = CpuInfo(cpu="cpu", cores=2, frequencies=[1.0])


    # act
    configurations = Configurations(info)

    # assert
    assert len(configurations) == 2
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 1.0
    assert configurations[1].cores == 2
    assert configurations[1].frequency == 1.0


def test_configuration_2_cores_2_frequency():
    # arrange
    info = CpuInfo(cpu="cpu", cores=2, frequencies=[3.0, 4.0])

    # act
    configurations = Configurations(info)

    # assert
    assert len(configurations) == 4
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 3.0

    assert configurations[1].cores == 1
    assert configurations[1].frequency == 4.0

    assert configurations[2].cores == 2
    assert configurations[2].frequency == 3.0

    assert configurations[3].cores == 2
    assert configurations[3].frequency == 4.0

def test_configuration_with_2_threads_per_core_makes_configuration_for_running_1_thread_and_2_threads():
    info = CpuInfo(cpu="cpu", cores=1, frequencies=[1.0], threads_per_core=2)

    configurations = Configurations(info)

    assert len(configurations) == 2
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 1.0
    assert configurations[0].threads_per_core == 1

    assert configurations[1].cores == 1
    assert configurations[1].frequency == 1.0
    assert configurations[1].threads_per_core == 2
