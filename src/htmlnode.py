class HTMLNode:
    def __init__(
        self,
        tag=None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props if props is not None else {}

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, node) -> bool:
        if not isinstance(node, HTMLNode):
            return NotImplemented
        return (
            self.tag == node.tag
            and self.value == node.value
            and self.children == node.children
            and self.props == node.props
        )

    def to_html(self):
        raise NotImplementedError("Não implementado ainda")

    def props_to_html(self) -> str:
        if len(self.props) == 0:
            return ""

        props_str = ""
        for k, v in self.props.items():
            props_str += f" {k}='{v}'"
        return props_str
