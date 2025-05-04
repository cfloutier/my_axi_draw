from pathlib import Path
import xml.etree.ElementTree as ET


class SvgEditor:
    def __init__(self):
        self.tree = None
        self.root = None

    def load_svg(self, file_path):
        """Load SVG content from a file as an XML DOM."""
        ET.register_namespace(
            "", "http://www.w3.org/2000/svg"
        )  # Register the default SVG namespace
        self.tree = ET.parse(file_path)
        self.root = self.tree.getroot()

    def edit_svg(self, modifications):
        """Edit the SVG content based on the provided modifications."""
        for element_id, attributes in modifications.items():
            element = self.root.find(f".//*[@id='{element_id}']")
            if element is not None:
                for attr, value in attributes.items():
                    element.set(attr, value)

    def add_path(self, path_data, style=None, element_id=None):
        """Add a new path element to the SVG."""
        if self.root is not None:
            path_element = ET.Element("path")
            path_element.set("d", path_data)  # Set the path data (SVG protocol)
            if style:
                path_element.set("style", style)  # Set the style if provided
            if element_id:
                path_element.set("id", element_id)  # Set the ID if provided
            self.root.append(path_element)  # Append the new path to the root

    def save_svg(self, file_path):
        """Save the modified SVG content to a file."""
        if self.tree is not None:
            self.tree.write(file_path, encoding="utf-8", xml_declaration=True)


def create_page(file_name, size, corner_len):
    """Create a new SVG page with the specified size and corner length."""

    svg = SvgEditor()
    svg_template_path = Path(__file__).parent.parent / "svg_templates"
    file_path = svg_template_path / "empty.svg"
    svg.load_svg(file_path)

    x, y = size

    style = "fill:none;stroke:#FFFFFF;stroke-width:0.5;stroke-opacity:1"

    # M 17.675803,-0.11628818 0.11628818,0 0.23257635,15.698904

    path_data_1 = f"M {corner_len},0 0,0, 0,{corner_len}"
    path_data_2 = f"M {x-corner_len},0 {x},0, {x},{corner_len}"
    path_data_3 = f"M {x},{y-corner_len} {x},{y}, {x-corner_len},{y}"
    path_data_4 = f"M {corner_len},{y} 0,{y}, 0,{y-corner_len}"

    svg.add_path(path_data_1, style=style, element_id="corner_1")
    svg.add_path(path_data_2, style=style, element_id="corner_2")
    svg.add_path(path_data_3, style=style, element_id="corner_3")
    svg.add_path(path_data_4, style=style, element_id="corner_4")

    file_path = svg_template_path / file_name
    svg.save_svg(file_path)


# Main function to test the SvgEditor
if __name__ == "__main__":
    editor = SvgEditor()

    create_page("A4.svg", (210, 297), 10)
    # create_page("A2.svg", (210, 297), 10)

    # # Load an existing SVG file
    # input_file = "empty.svg"

    # input_file = Path(__file__).parent.parent / "svg_templates" / "empty.svg"
    # if not input_file.exists():
    #     raise FileNotFoundError(f"SVG file {input_file} not found.")

    # editor.load_svg(input_file)

    # # Add a multi-line path
    # path_data = "M 10,10 L 20,20 L 30,10 Z"  # Move to (10,10), draw lines, and close the path
    # style = "fill:none;stroke:#FFFFFF;stroke-width:0.5;stroke-opacity:1"
    # editor.add_path(path_data, style=style, element_id="newPath")

    # # # Save the modified SVG to a new file
    # output_file =  Path(__file__).parent / "modified_example.svg"
    # # editor.save_svg(output_file)

    # print(f"SVG modified and saved to {output_file}")
