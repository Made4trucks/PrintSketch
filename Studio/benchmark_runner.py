from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from project import PrintSketchProject
from production_pipeline import ProductionPipeline


SUPPORTED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


@dataclass
class BenchmarkCase:
    id: str
    image: Path
    output_folder: Path


@dataclass
class BenchmarkResult:
    case_id: str
    success: bool
    error: str | None = None


class BenchmarkRunner:

    def __init__(self, run_name: str = "v2") -> None:

        self.batch_folder = (
            Path(__file__).resolve().parent.parent
            / "Benchmark"
            / "Batch_01"
        )

        self.originals_folder = (
            self.batch_folder
            / "Originals"
        )

        self.run_folder = (
            self.batch_folder
            / "Runs"
            / run_name
        )

    def get_projects(self) -> list[BenchmarkCase]:

        projects = []

        if not self.originals_folder.exists():
            raise FileNotFoundError(
                f"Originals folder does not exist: "
                f"{self.originals_folder}"
            )

        for image_path in sorted(self.originals_folder.iterdir()):

            if (
                image_path.is_file()
                and image_path.suffix.lower()
                in SUPPORTED_IMAGE_EXTENSIONS
            ):

                projects.append(
                    BenchmarkCase(
                        id=image_path.stem,
                        image=image_path,
                        output_folder=(
                            self.run_folder
                            / image_path.stem
                        ),
                    )
                )

        if not projects:
            raise RuntimeError(
                f"No benchmark images found in: "
                f"{self.originals_folder}"
            )

        return projects

    def prepare_run(
        self,
        projects: list[BenchmarkCase],
    ) -> None:

        self.run_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        for project in projects:

            project.output_folder.mkdir(
                parents=True,
                exist_ok=True,
            )

    def run_case(
        self,
        case: BenchmarkCase,
    ) -> BenchmarkResult:

        try:

            project = PrintSketchProject(
                project_name=case.id,
                projects_folder=self.run_folder,
            )

            project.create()
            project.import_photo(case.image)

            pipeline = ProductionPipeline(project)
            pipeline.run()

            return BenchmarkResult(
                case_id=case.id,
                success=True,
            )

        except Exception as error:

            return BenchmarkResult(
                case_id=case.id,
                success=False,
                error=str(error),
            )

    def print_summary(
        self,
        results: list[BenchmarkResult],
    ) -> None:

        successful = [
            result
            for result in results
            if result.success
        ]

        failed = [
            result
            for result in results
            if not result.success
        ]

        print()
        print("=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)
        print(f"Successful: {len(successful)}")
        print(f"Failed: {len(failed)}")
        print()

        for result in results:

            status = (
                "SUCCESS"
                if result.success
                else "FAILED"
            )

            print(
                f"{status:<8} {result.case_id}"
            )

            if result.error:

                print(
                    f"         Error: {result.error}"
                )

    def run(self) -> None:

        started_at = datetime.now()

        projects = self.get_projects()
        self.prepare_run(projects)

        results = []

        print("=" * 60)
        print("PRINTSKETCH BENCHMARK RUNNER")
        print("=" * 60)
        print(f"Run: {self.run_folder.name}")
        print(
            f"Started: "
            f"{started_at:%Y-%m-%d %H:%M:%S}"
        )
        print(f"Cases: {len(projects)}")
        print()

        for index, case in enumerate(
            projects,
            start=1,
        ):

            print()
            print("=" * 60)
            print(
                f"[{index:02d}/{len(projects):02d}] "
                f"{case.id}"
            )
            print("=" * 60)

            result = self.run_case(case)
            results.append(result)

            if result.success:

                print()
                print(
                    f"Case completed successfully: "
                    f"{case.id}"
                )

            else:

                print()
                print(
                    f"Case failed: {case.id}"
                )
                print(
                    f"Error: {result.error}"
                )

        finished_at = datetime.now()
        duration = finished_at - started_at

        self.print_summary(results)

        print()
        print(
            f"Finished: "
            f"{finished_at:%Y-%m-%d %H:%M:%S}"
        )
        print(
            f"Duration: "
            f"{duration}"
        )
        print(
            f"Results folder: "
            f"{self.run_folder}"
        )


if __name__ == "__main__":

    BenchmarkRunner(
        run_name="v2"
    ).run()