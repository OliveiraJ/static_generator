import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("h1", "testando")
        node2 = HTMLNode("h1", "testando")
        self.assertEqual(node, node2)

    def test_notEq(self):
        node = HTMLNode("h1", "testando")
        node2 = HTMLNode("h1", "testando2")
        self.assertNotEqual(node, node2)

    def test_propsToHtml(self):
        node = HTMLNode("h1", "testando", props={"style": 'margin:"5px"'})
        self.assertIsInstance(node.props_to_html(), str)
