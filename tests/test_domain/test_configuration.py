from chronus.domain.configuration import Configurations


def test_configuration_1_core_1_frequency():
    # arrange
    cores = 1
    frequencies = [1.0]

    # act
    configurations = Configurations(cores, frequencies)

    # assert
    assert len(configurations) == 1
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 1.0


def test_configuration_2_cores_1_frequency():
    # arrange
    cores = 2
    frequencies = [1.0]

    # act
    configurations = Configurations(cores, frequencies)

    # assert
    assert len(configurations) == 2
    assert configurations[0].cores == 1
    assert configurations[0].frequency == 1.0
    assert configurations[1].cores == 2
    assert configurations[1].frequency == 1.0


def test_configuration_2_cores_2_frequency():
    # arrange
    cores = 2
    frequencies = [3.0, 4.0]

    # act
    configurations = Configurations(cores, frequencies)

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
