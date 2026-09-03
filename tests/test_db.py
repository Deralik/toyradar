import toyradar.utils as utils

def test_power_to_db():
    assert round(utils.power_to_db(20)) == 13

def test_db_to_power():
    assert round(utils.db_to_power(3)) == 2