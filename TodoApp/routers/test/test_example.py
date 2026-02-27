import pytest


def test_equal_or_not():
    assert 3==3
    assert 3!=1

class Student():
    def __init__(self,first_name,last_name,major,years):
        self.first_name=first_name
        self.last_name=last_name
        self.major=major
        self.years=years

@pytest.fixture
def default_employee():
    return Student("John","Doe","CS",3)


def test_person_initialization(default_employee):
    # s=Student("John","Doe","CS",3)
    # s.first_name=="John","First name should be John"
    assert default_employee.first_name=="John","First name should be John"
        