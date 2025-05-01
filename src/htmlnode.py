class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        to_print = ""
        if not self.props:
            return ""
        else:
            for key in self.props:
                to_print += " " + f'{key}="{self.props[key]}"'
            return to_print

    def __repr__(self):
        return f"({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        self_closing_tags = ["img", "br", "hr", "input", "meta", "link"]

        if self.tag is None:
            return self.value or ""
        else:  
            props_html = ""
            if self.props:
                for key, value in self.props.items():
                    # Make sure we're not converting dictionaries to strings
                    if isinstance(value, dict):
                        # This should never happen, but just in case
                        print(f"Warning: Found nested dict in props: {key}={value}")
                    props_html += f' {key}="{value}"'

            # Handle self-closing tags
            if self.tag in self_closing_tags:
                return f"<{self.tag}{props_html} />"
            # For regular tags, require a value
            elif not self.value and self.tag not in self_closing_tags:
                raise ValueError(f"Leafnode: No value specified for {self.tag}")
            else:
                return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        if not self.tag:
            raise ValueError("No tag specified")
        elif not self.children:
            raise ValueError("No children specified")
        else:
            concatenated_strings = ""
            for child in self.children:
                concatenated_strings += child.to_html()
            return f"<{self.tag}>{concatenated_strings}</{self.tag}>"
