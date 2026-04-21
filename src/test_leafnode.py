import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "isso é um link!", {"href": "https://www.google.com.br"})
        self.assertEqual(
            node.to_html(), "<a href='https://www.google.com.br'>isso é um link!</a>"
        )
