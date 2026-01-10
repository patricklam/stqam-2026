import unittest
from unittest.mock import Mock

from .model import Model
from .controller import Controller

class CoverageTests(unittest.TestCase):
    def test_model_story_one(self):
        m = Model()
        c = Controller(m)
        rc = c.model_story_one()
        self.assertEqual(rc, [17, 1729, "2025", []])

    def test_model_story_two(self):
        m = Model()
        c = Controller(m)
        rc = c.model_story_two()
        self.assertEqual(rc, [17, 1729, "2025"])

    # Run tests 1-2 with invocation: python3 -m unittest a1q1c.test_suite -k calls
    # 1. Write a test that ensures that Controller calls m.wait() exactly once.
    # Fails when settings.WHICH_STORY = "one".
    def test_controller_calls_wait_once(self):
        pass

    # 2. Write a test that ensures that Controller calls m.append_to_resource() four times.
    # Fails when settings.WHICH_STORY = "two".
    def test_controller_calls_append_to_resource_four_times(self):
        pass


    # Run this test and tests 3-4 with invocation: python3 -m unittest -k three
    def test_model_story_three_real(self):
        m = Model()
        c = Controller(m)
        rc = c.model_story_three()
        self.assertEqual(rc, [6, 5])

    # 3. Write a test that tests the Controller's calls to the Model, but hardcodes the Model's response to get_resource.
    # Run just this test with invocation: python3 -m unittest a1q1c.test_suite -k stubbing
    # Succeeds when settings.WHICH_STORY = "four"
    # Fails when settings.WHICH_STORY = "three"
    def test_controller_story_three_via_model_stubbing_get_resource_return_value(self):
        pass

    # 4. Write a test that creates a mock but maintains a real list for model.resource.
    # Run just this test with invocation: python3 -m unittest a1q1c.test_suite -k faking
    # Succeeds when settings.WHICH_STORY = "three"
    # Fails when settings.WHICH_STORY = "four"
    def test_controller_story_three_via_model_faking_get_resource_return_value(self):
        pass
