import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_and_props(self):
        grandchild_node = LeafNode(
            "a",
            "link_grandchild",
            {
                "href": "https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f",
                "class": "btn btn-primary",
            },
        )
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><a href='https://www.boot.dev/lessons/4e8c8d2a-8966-4e7d-acdf-067b1d06225f' class='btn btn-primary'>link_grandchild</a></span></div>",
        )
