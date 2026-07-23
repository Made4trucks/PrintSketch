from __future__ import annotations

import base64
import html
import mimetypes
import sys
from pathlib import Path


SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def image_to_data_uri(image_path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(image_path.name)

    if mime_type is None:
        mime_type = "image/png"

    encoded = base64.b64encode(
        image_path.read_bytes()
    ).decode("ascii")

    return f"data:{mime_type};base64,{encoded}"


def find_preview(case_folder: Path) -> Path | None:
    expected_path = (
        case_folder
        / "preview"
        / "preview_v1.png"
    )

    if expected_path.exists():
        return expected_path

    candidates = sorted(
        path
        for path in case_folder.rglob("*")
        if (
            path.is_file()
            and path.suffix.lower()
            in SUPPORTED_IMAGE_EXTENSIONS
            and "preview" in path.name.lower()
        )
    )

    if candidates:
        return candidates[0]

    return None


def get_originals(
    originals_folder: Path,
) -> dict[str, Path]:
    originals: dict[str, Path] = {}

    for image_path in sorted(
        originals_folder.iterdir()
    ):
        if (
            image_path.is_file()
            and image_path.suffix.lower()
            in SUPPORTED_IMAGE_EXTENSIONS
        ):
            originals[image_path.stem.lower()] = (
                image_path
            )

    return originals


def get_run_folders(
    runs_folder: Path,
) -> list[Path]:
    return sorted(
        (
            path
            for path in runs_folder.iterdir()
            if path.is_dir()
        ),
        key=lambda path: path.name,
    )


def build_image_panel(
    title: str,
    image_path: Path | None,
) -> str:
    safe_title = html.escape(title)

    if image_path is None:
        return f"""
        <section class="image-panel">
            <h3>{safe_title}</h3>
            <div class="missing-image">
                Image not found
            </div>
        </section>
        """

    image_uri = image_to_data_uri(image_path)

    return f"""
    <section class="image-panel">
        <h3>{safe_title}</h3>
        <a
            href="{image_uri}"
            target="_blank"
            title="Open full size"
        >
            <img
                src="{image_uri}"
                alt="{safe_title}"
                loading="lazy"
            >
        </a>
    </section>
    """


def build_case_section(
    case_id: str,
    original_path: Path | None,
    first_preview: Path | None,
    second_preview: Path | None,
    first_run_name: str,
    second_run_name: str,
) -> str:
    safe_case_id = html.escape(case_id.upper())

    original_panel = build_image_panel(
        "Reference",
        original_path,
    )

    first_panel = build_image_panel(
        first_run_name,
        first_preview,
    )

    second_panel = build_image_panel(
        second_run_name,
        second_preview,
    )

    return f"""
    <article class="case-card" id="{html.escape(case_id)}">
        <h2>{safe_case_id}</h2>

        <div class="reference-grid">
            {original_panel}
        </div>

        <div class="comparison-grid">
            {first_panel}
            {second_panel}
        </div>
    </article>
    """


def build_html(
    sections: list[str],
    first_run_name: str,
    second_run_name: str,
    case_ids: list[str],
) -> str:
    navigation = "\n".join(
        f'<a href="#{html.escape(case_id)}">'
        f'{html.escape(case_id.upper())}</a>'
        for case_id in case_ids
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>
        PrintSketch Comparison
    </title>

    <style>
        * {{
            box-sizing: border-box;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            margin: 0;
            background: #111318;
            color: #f4f4f4;
            font-family:
                Arial,
                Helvetica,
                sans-serif;
        }}

        header {{
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 18px 24px;
            background: rgba(17, 19, 24, 0.96);
            border-bottom: 1px solid #343741;
            backdrop-filter: blur(10px);
        }}

        header h1 {{
            margin: 0 0 8px;
            font-size: 22px;
        }}

        header p {{
            margin: 0 0 14px;
            color: #b9bec9;
        }}

        nav {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        nav a {{
            flex: 0 0 auto;
            padding: 7px 11px;
            border: 1px solid #3b3f49;
            border-radius: 7px;
            color: #ffffff;
            text-decoration: none;
            font-size: 13px;
        }}

        nav a:hover {{
            background: #292d36;
        }}

        main {{
            width: min(1500px, 100%);
            margin: 0 auto;
            padding: 24px;
        }}

        .case-card {{
            margin-bottom: 32px;
            padding: 22px;
            background: #1a1d23;
            border: 1px solid #30343d;
            border-radius: 14px;
            scroll-margin-top: 140px;
        }}

        .case-card h2 {{
            margin: 0 0 20px;
            font-size: 26px;
            letter-spacing: 1px;
        }}

        .reference-grid {{
            display: grid;
            grid-template-columns:
                minmax(280px, 700px);
            justify-content: center;
            margin-bottom: 22px;
        }}

        .comparison-grid {{
            display: grid;
            grid-template-columns:
                repeat(2, minmax(0, 1fr));
            gap: 20px;
        }}

        .image-panel {{
            min-width: 0;
        }}

        .image-panel h3 {{
            margin: 0 0 10px;
            text-align: center;
            font-size: 16px;
            color: #d6d9df;
        }}

        .image-panel a {{
            display: block;
        }}

        .image-panel img {{
            display: block;
            width: 100%;
            max-height: 760px;
            object-fit: contain;
            background: #ffffff;
            border-radius: 9px;
            cursor: zoom-in;
        }}

        .missing-image {{
            display: grid;
            min-height: 280px;
            place-items: center;
            border: 1px dashed #626875;
            border-radius: 9px;
            color: #9fa5b1;
        }}

        @media (max-width: 850px) {{
            main {{
                padding: 12px;
            }}

            .case-card {{
                padding: 14px;
            }}

            .comparison-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>

<body>
    <header>
        <h1>PrintSketch Comparison</h1>

        <p>
            {html.escape(first_run_name)}
            versus
            {html.escape(second_run_name)}
        </p>

        <nav>
            {navigation}
        </nav>
    </header>

    <main>
        {''.join(sections)}
    </main>
</body>
</html>
"""


def main() -> None:
    project_root = (
        Path(__file__).resolve().parent.parent
    )

    batch_folder = (
        project_root
        / "Benchmark"
        / "Batch_01"
    )

    originals_folder = (
        batch_folder
        / "Originals"
    )

    runs_folder = (
        batch_folder
        / "Runs"
    )

    comparison_folder = (
        batch_folder
        / "Comparison"
    )

    if not originals_folder.exists():
        raise FileNotFoundError(
            f"Originals folder not found: "
            f"{originals_folder}"
        )

    if not runs_folder.exists():
        raise FileNotFoundError(
            f"Runs folder not found: "
            f"{runs_folder}"
        )

    available_runs = get_run_folders(
        runs_folder
    )

    if len(sys.argv) == 3:
        first_run = runs_folder / sys.argv[1]
        second_run = runs_folder / sys.argv[2]

        if not first_run.is_dir():
            raise FileNotFoundError(
                f"Run not found: {first_run}"
            )

        if not second_run.is_dir():
            raise FileNotFoundError(
                f"Run not found: {second_run}"
            )

    else:
        if len(available_runs) < 2:
            raise RuntimeError(
                "At least two benchmark runs "
                "are required."
            )

        first_run = available_runs[-2]
        second_run = available_runs[-1]

    originals = get_originals(
        originals_folder
    )

    first_cases = {
        path.name.lower(): path
        for path in first_run.iterdir()
        if path.is_dir()
    }

    second_cases = {
        path.name.lower(): path
        for path in second_run.iterdir()
        if path.is_dir()
    }

    case_ids = sorted(
        set(originals)
        | set(first_cases)
        | set(second_cases)
    )

    sections: list[str] = []

    for case_id in case_ids:
        original_path = originals.get(case_id)

        first_case_folder = first_cases.get(
            case_id
        )

        second_case_folder = second_cases.get(
            case_id
        )

        first_preview = (
            find_preview(first_case_folder)
            if first_case_folder
            else None
        )

        second_preview = (
            find_preview(second_case_folder)
            if second_case_folder
            else None
        )

        sections.append(
            build_case_section(
                case_id=case_id,
                original_path=original_path,
                first_preview=first_preview,
                second_preview=second_preview,
                first_run_name=first_run.name,
                second_run_name=second_run.name,
            )
        )

    comparison_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        comparison_folder
        / (
            f"{first_run.name}"
            f"_vs_"
            f"{second_run.name}"
            f".html"
        )
    )

    report_html = build_html(
        sections=sections,
        first_run_name=first_run.name,
        second_run_name=second_run.name,
        case_ids=case_ids,
    )

    output_path.write_text(
        report_html,
        encoding="utf-8",
    )

    print(
        "Comparison HTML generated successfully."
    )
    print(
        f"First run: {first_run.name}"
    )
    print(
        f"Second run: {second_run.name}"
    )
    print(
        f"Cases: {len(case_ids)}"
    )
    print(
        f"Output: {output_path}"
    )


if __name__ == "__main__":
    main()