"""
Test Factory to make fake objects for testing
"""

from datetime import date

import factory
from factory.fuzzy import FuzzyDate
from service.models import Customer


class CustomerFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Customer

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("first_name")
    address = factory.Faker("address")
    email = factory.Faker("email")
    phone_number = factory.Faker("phone_number")
    member_since = FuzzyDate(date(2000, 1, 1))

    # Todo: Add your other attributes here...
