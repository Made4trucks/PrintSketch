from pathlib import Path


class MarkdownLoader:
    """
    Converts Markdown into structured blocks.
    """

    def load(self, file_path: Path):

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        blocks = []

        table_buffer = []

        def flush_table():
            nonlocal table_buffer

            if not table_buffer:
                return

            rows = []

            for row in table_buffer:

                row = row.strip()

                if row.startswith("|-"):
                    continue

                cells = [
                    cell.strip()
                    for cell in row.strip("|").split("|")
                ]

                rows.append(cells)

            blocks.append({
                "type": "table",
                "rows": rows
            })

            table_buffer = []

        for line in lines:

            text = line.strip()

            if not text:
                flush_table()
                continue

            if text.startswith("|"):
                table_buffer.append(text)
                continue

            flush_table()

            if text.startswith("# "):
                blocks.append({
                    "type": "h1",
                    "text": text[2:]
                })
                continue

            if text.startswith("## "):
                blocks.append({
                    "type": "h2",
                    "text": text[3:]
                })
                continue

            if text.startswith("### "):
                blocks.append({
                    "type": "h3",
                    "text": text[4:]
                })
                continue

            if text == "---":
                blocks.append({
                    "type": "separator"
                })
                continue

            if text.startswith("- "):
                blocks.append({
                    "type": "bullet",
                    "text": text[2:]
                })
                continue

            blocks.append({
                "type": "paragraph",
                "text": text
            })

        flush_table()

        return blocks