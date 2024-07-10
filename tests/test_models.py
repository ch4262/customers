"""
Test cases for Customer Model
"""

import os
import logging
from unittest import TestCase
from unittest.mock import patch
from datetime import date
from wsgi import app
from service.models import Customer, DataValidationError, db
from .factories import CustomerFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  B A S E   T E S T   C A S E S
######################################################################
class TestCaseBase(TestCase):
    """Base Test Case for common setup"""

    # pylint: disable=duplicate-code
    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()


######################################################################
#  C U S T O M E R   M O D E L   T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomer(TestCase):
    """Test Cases for Customer Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_customer(self):
        """It should create a Customer"""

        customer = CustomerFactory()
        customer.create()
        self.assertIsNotNone(customer.id)
        found = Customer.all()
        self.assertEqual(len(found), 1)
        data = Customer.find(customer.id)
        self.assertEqual(data.name, customer.name)
        self.assertEqual(data.address, customer.address)
        self.assertEqual(data.email, customer.email)
        self.assertEqual(data.phone_number, customer.phone_number)
        self.assertEqual(data.member_since, customer.member_since)

    def test_update_a_customer(self):
        """It should Update a Customer"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        customer.create()
        logging.debug(customer)
        self.assertIsNotNone(customer.id)
        # Change it an save it
        customer.category = "k9"
        original_id = customer.id
        customer.update()
        self.assertEqual(customer.id, original_id)
        self.assertEqual(customer.category, "k9")
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].id, original_id)
        self.assertEqual(customers[0].category, "k9")

    def test_update_no_id(self):
        """It should not Update a Customer with no id"""
        customer = CustomerFactory()
        logging.debug(customer)
        customer.id = None
        self.assertRaises(DataValidationError, customer.update)

    def test_list_all_customers(self):
        """It should List all Customers in the database"""
        customers = Customer.all()
        self.assertEqual(customers, [])
        # Create 5 Customers
        for _ in range(5):
            customer = CustomerFactory()
            customer.create()
        # See if we get back 5 customers
        customers = Customer.all()
        self.assertEqual(len(customers), 5)

    def test_delete_a_customer(self):
        """It should Delete a Customer"""
        customer = CustomerFactory()
        customer.create()
        self.assertEqual(len(Customer.all()), 1)
        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)

    def test_serialize_a_customer(self):
        """It should serialize a Customer"""
        customer = CustomerFactory()
        data = customer.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], customer.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], customer.name)
        self.assertIn("address", data)
        self.assertEqual(data["address"], customer.address)
        self.assertIn("email", data)
        self.assertEqual(data["email"], customer.email)
        self.assertIn("phone_number", data)
        self.assertEqual(data["phone_number"], customer.phone_number)
        self.assertIn("member_since", data)
        self.assertEqual(
            date.fromisoformat(data["member_since"]), customer.member_since
        )

    def test_deserialize_a_customer(self):
        """It should de-serialize a Customer"""
        data = CustomerFactory().serialize()
        customer = Customer()
        customer.deserialize(data)
        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.name, data["name"])
        self.assertEqual(customer.address, data["address"])
        self.assertEqual(customer.email, data["email"])
        self.assertEqual(customer.phone_number, data["phone_number"])
        self.assertEqual(
            customer.member_since, date.fromisoformat(data["member_since"])
        )

    def test_deserialize_missing_data(self):
        """It should not deserialize a Customer with missing data"""
        data = {"id": 1, "name": "Jane", "email": "janedoe@example.com"}
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)

    def test_read_customer(self):
        """It should read a Customer"""

        customer = CustomerFactory()
        customer.create()
        data = Customer.find(customer.id)
        self.assertEqual(data.id, customer.id)
        self.assertEqual(data.name, customer.name)
        self.assertEqual(data.address, customer.address)
        self.assertEqual(data.email, customer.email)
        self.assertEqual(data.phone_number, customer.phone_number)
        self.assertEqual(data.member_since, customer.member_since)


######################################################################
#  T E S T   E X C E P T I O N   H A N D L E R S
######################################################################
class TestExceptionHandlers(TestCaseBase):
    """Customer Model Exception Handlers"""

    @patch("service.models.db.session.commit")
    def test_create_exception(self, exception_mock):
        """It should catch a create exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.create)

    @patch("service.models.db.session.commit")
    def test_update_exception(self, exception_mock):
        """It should catch a update exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.update)

    @patch("service.models.db.session.commit")
    def test_delete_exception(self, exception_mock):
        """It should catch a delete exception"""
        exception_mock.side_effect = Exception()
        customer = CustomerFactory()
        self.assertRaises(DataValidationError, customer.delete)


######################################################################
#  Q U E R Y   T E S T   C A S E S
######################################################################
class TestModelQueries(TestCaseBase):
    """Customer Model Query Tests"""

    def test_find_customer(self):
        """It should Find a Customer by ID"""
        customers = CustomerFactory.create_batch(5)
        for customer in customers:
            customer.create()
        logging.debug(customers)

        self.assertEqual(len(Customer.all()), 5)
        # find the 2nd customer in the list
        customer = Customer.find(customers[1].id)
        self.assertIsNot(customer, None)
        self.assertEqual(customer.id, customers[1].id)
        self.assertEqual(customer.name, customers[1].name)
        self.assertEqual(customer.address, customers[1].address)
        self.assertEqual(customer.email, customers[1].email)
        self.assertEqual(customer.phone_number, customers[1].phone_number)
        self.assertEqual(customer.member_since, customers[1].member_since)

    def test_find_all_customers(self):
        """It should Find All Customers"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        count = len(customers)
        found = Customer.all()
        self.assertEqual(len(found), count)

    def test_find_by_name(self):
        """It should Find a Customer by Name"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        name = customers[0].name
        count = len([customer for customer in customers if customer.name == name])
        found = Customer.find_by_name(name)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.name, name)

    def test_find_by_address(self):
        """It should Find a Customer by Address"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        address = customers[0].address
        count = len([customer for customer in customers if customer.address == address])
        found = Customer.find_by_address(address)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.address, address)

    def test_find_by_email(self):
        """It should Find a Customer by Email"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        email = customers[0].email
        count = len([customer for customer in customers if customer.email == email])
        found = Customer.find_by_email(email)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.email, email)

    def test_find_by_phone(self):
        """It should Find a Customer by Phone Number"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        phone_number = customers[0].phone_number
        count = len([customer for customer in customers if customer.phone_number == phone_number])
        found = Customer.find_by_phone(phone_number)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.phone_number, phone_number)

    def test_find_by_member_since(self):
        """It should Find a Customer by their Membership date"""
        customers = CustomerFactory.create_batch(10)
        for customer in customers:
            customer.create()
        member_since = customers[0].member_since
        count = len([customer for customer in customers if customer.member_since == member_since])
        found = Customer.find_by_member_since(member_since)
        self.assertEqual(found.count(), count)
        for customer in found:
            self.assertEqual(customer.member_since, member_since)
