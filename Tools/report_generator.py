from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)

from markdown_loader import MarkdownLoader


class ReportGenerator:

    def __init__(self):

        self.docs_dir = Path("Docs")
        self.report_dir = self.docs_dir / "Benchmark Reports"
        self.output_dir = self.docs_dir / "Benchmark PDFs" / "Sprint01"

        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.styles = getSampleStyleSheet()
        self.loader = MarkdownLoader()

    # ---------------------------------------------------------

    def build_pdf(self, markdown_file: Path):

        output_pdf = self.output_dir / (markdown_file.stem + ".pdf")

        doc = SimpleDocTemplate(
            str(output_pdf),
            rightMargin=2 * cm,
            leftMargin=2 * cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm,
        )

        story = []

        blocks = self.loader.load(markdown_file)

        for block in blocks:

            block_type = block["type"]

            if block_type == "h1":
                story.append(
                    Paragraph(block["text"], self.styles["Heading1"])
                )
                story.append(Spacer(1, 0.3 * cm))

            elif block_type == "h2":
                story.append(
                    Paragraph(block["text"], self.styles["Heading2"])
                )
                story.append(Spacer(1, 0.2 * cm))

            elif block_type == "h3":
                story.append(
                    Paragraph(block["text"], self.styles["Heading3"])
                )

            elif block_type == "paragraph":
                story.append(
                    Paragraph(block["text"], self.styles["BodyText"])
                )

            elif block_type == "bullet":
                story.append(
                    Paragraph(
                        f"• {block['text']}",
                        self.styles["BodyText"],
                    )
                )

            elif block_type == "separator":
                story.append(
                    HRFlowable(width="100%")
                )
                story.append(Spacer(1, 0.25 * cm))

            elif block_type == "table":
                #
                # Tabele dodamy w następnym kroku.
                # Na razie je pomijamy.
                #
                pass

        doc.build(story)

        print(f"✓ {output_pdf.name}")

    # ---------------------------------------------------------

    def generate(self):

        reports = sorted(self.report_dir.glob("*.md"))

        print()
        print("Generating PDFs...")
        print()

        for report in reports:
            self.build_pdf(report)

        print()
        print("Done.")


if __name__ == "__main__":
    ReportGenerator().generate()