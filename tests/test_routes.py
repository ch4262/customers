"""
TestCustomer API Service Test Suite
"""

import os
import logging
from unittest import TestCase
from wsgi import app
from service.common import status
from service.models import db, Customer
from .factories import CustomerFactory
from datetime import date

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql+psycopg://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/customers"


######################################################################
#  T E S T   C A S E S
######################################################################
# pylint: disable=too-many-public-methods
class TestCustomerResource(TestCase):
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        app.app_context().push()

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        self.client = app.test_client()
        db.session.query(Customer).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    ############################################################
    # Utility function to bulk create customers
    ############################################################
    def _create_customer(self, count: int = 1) -> list:
        """Factory method to create customers in bulk"""
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            response = self.client.post(BASE_URL, json=test_customer.serialize())

            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = response.get_json()
            test_customer.id = new_customer["id"]
            test_customer.name = new_customer["name"]
            test_customer.address = new_customer["address"]
            test_customer.email = new_customer["email"]
            test_customer.phone_number = new_customer["phone_number"]
            test_customer.member_since = date.fromisoformat(new_customer["member_since"])
            customers.append(test_customer)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Customer Service REST API")

    def test_create_customer(self):
        """It should Create a new Customer"""
        test_customer = CustomerFactory()
        logging.debug("Test Customer: %s", test_customer.serialize())
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_customer = response.get_json()
        self.assertEqual(new_customer["name"], test_customer.name)
        self.assertEqual(new_customer["address"], test_customer.address)
        self.assertEqual(new_customer["email"], test_customer.email)
        self.assertEqual(new_customer["phone_number"], test_customer.phone_number)
        self.assertEqual(new_customer["member_since"], test_customer.member_since.isoformat())

        # TODO: Uncomment this code when get_customers is implemented
        # Check that the location header was correct
        # response = self.client.get(location)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # new_customer = response.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name)
        # self.assertEqual(new_customer["address"], test_customer.address)
        # self.assertEqual(new_customer["email"], test_customer.email)
        # self.assertEqual(new_customer["phone_number"], test_customer.phone_number)
        # self.assertEqual(new_customer["member_since"], test_customer.member_since.isoformat())

    def test_read_customer(self):
        """It should read an existing Customer"""
        test_customer = CustomerFactory()
        logging.debug("Test Customer: %s", test_customer.serialize())
        response = self.client.post(BASE_URL, json=test_customer.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_customer = response.get_json()
        self.assertEqual(new_customer["name"], test_customer.name)
        self.assertEqual(new_customer["address"], test_customer.address)
        self.assertEqual(new_customer["email"], test_customer.email)
        self.assertEqual(new_customer["phone_number"], test_customer.phone_number)
        self.assertEqual(new_customer["member_since"], test_customer.member_since.isoformat())

        # Retrieve the newly created customer
        # self.assertEqual(0, new_customer["id"])
        read_response = self.client.get(f"{BASE_URL}/{int(new_customer['id'])}")
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)

        # Validate the data matches
        retrieved_customer = read_response.get_json()
        self.assertEqual(retrieved_customer["name"], test_customer.name)
        self.assertEqual(retrieved_customer["address"], test_customer.address)
        self.assertEqual(retrieved_customer["email"], test_customer.email)
        self.assertEqual(retrieved_customer["phone_number"], test_customer.phone_number)
        self.assertEqual(retrieved_customer["member_since"], test_customer.member_since.isoformat())
        
        response = self.client.get(f"{BASE_URL}/-1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # self.assertIn("Customer with id [-1] not found", response.get_data(as_text=True))

    # ----------------------------------------------------------
    # TEST LIST
    # ----------------------------------------------------------
    def test_get_customer_list(self):
        """It should Get a list of Customers"""
        self._create_customer(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)
