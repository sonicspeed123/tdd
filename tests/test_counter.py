"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase

# we need to import the unit under test - counter
from src.counter import app

# we need to import the file that contains the status codes
from src import status

class CounterTest(TestCase):
    """Counter tests"""

    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = self.client
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        #make a call to create a counter
        client = self.client
        counterName = 'toIncrement'

        result = client.post(f'/counters/{counterName}')

        #Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        #Check the counter value as a baseline
        self.assertEqual(result.get_data(), (b'{"toIncrement":0}\n'))

        #Make a call to Update the counter that you just created
        result = client.put(f'/counters/{counterName}')

        #Ensure that it returned a successful return code
        self.assertEqual(result.status_code, status.HTTP_200_OK)

        #Check that the counter value is one more than the baseline you measured
        self.assertEqual(result.get_data(), (b'{"toIncrement":1}\n'))

    def test_read_a_counter(self):
        """It should read a counter"""
        client = self.client
        counterName = "readMe"

        result = client.post(f'/counters/{counterName}')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = client.get(f'/counters/{counterName}')
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.get_data(), (b'{"readMe":0}\n'))

    def test_delete_a_counter(self):
        """It should delete a counter"""
        client = self.client
        counterName = "deleteMe"

        result = client.post(f'/counters/{counterName}')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        result = client.delete(f'/counters/{counterName}')
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        result = client.get(f'/counters/{counterName}')
        self.assertEqual(result.status_code, status.HTTP_404_NOT_FOUND)