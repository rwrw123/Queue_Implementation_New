import unittest
from queue_implementation import Queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_enqueue_different_types(self):
        for value in [1, "string", 3.14, {"key": "value"}]:
            self.queue.enqueue(value)
            self.assertFalse(self.queue.is_empty())
            self.assertEqual(self.queue.dequeue(), value)

    def test_persistent_state(self):
        items = [1, 2, 3, 4, 5]
        for item in items:
            self.queue.enqueue(item)
        for item in items:
            self.assertEqual(self.queue.dequeue(), item)
        self.assertTrue(self.queue.is_empty())

    def test_dequeue_from_empty(self):
        self.assertIsNone(self.queue.dequeue())

    def test_stress_queue(self):
        for _ in range(10000):
            self.queue.enqueue("test")
        for _ in range(5000):
            self.queue.dequeue()
        self.assertEqual(self.queue.size(), 5000)
        for _ in range(5000):
            self.queue.dequeue()
        self.assertTrue(self.queue.is_empty())

if __name__ == '__main__':
    unittest.main()

