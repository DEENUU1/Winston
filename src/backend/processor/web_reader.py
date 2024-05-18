import os
import uuid

from pyhtml2pdf import converter


class WebReader:
    def __init__(self):
        self.output_dir = os.path.abspath("./media/files/")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def get_full_path(self) -> str:
        filename = uuid.uuid4()
        return os.path.join(self.output_dir, f"{filename}.pdf")

    def convert_html_to_pdf(self) -> str:
        full_path = self.get_full_path()

        converter.convert(
            f"https://react.dev/learn/passing-props-to-a-component",
            full_path,
            print_options={
                "scale": 0.50
            }
        )
        return full_path


if __name__ == "__main__":
    reader = WebReader()
    reader.convert_html_to_pdf()
