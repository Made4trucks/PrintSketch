from pathlib import Path
import shutil

from project_context import ProjectContext


PROJECT_ROOT = Path(__file__).resolve().parent.parent


PROJECTS_FOLDER = PROJECT_ROOT / "Projects"


class PrintSketchProject:

    def __init__(self, project_name: str):

        self.name = project_name

        self.project_folder = PROJECTS_FOLDER / project_name

    def create(self):

        folders = [

            "",

            "vision",

            "identity",

            "prompt",

            "preview",

            "svg",

            "fusion",

        ]

        for folder in folders:

            (self.project_folder / folder).mkdir(

                parents=True,

                exist_ok=True,

            )

    def import_photo(self, source_image: Path):

        destination = (

            self.project_folder

            / "photo.jpg"

        )

        shutil.copy2(

            source_image,

            destination,

        )

        return destination

    @property

    def photo(self):

        return self.project_folder / "photo.jpg"

    @property

    def vision_folder(self):

        return self.project_folder / "vision"

    @property

    def identity_folder(self):

        return self.project_folder / "identity"

    @property

    def prompt_folder(self):

        return self.project_folder / "prompt"

    @property

    def preview_folder(self):

        return self.project_folder / "preview"

    @property

    def svg_folder(self):

        return self.project_folder / "svg"

    @property

    def fusion_folder(self):

        return self.project_folder / "fusion"
    
    @property
    def context(self) -> ProjectContext:

        return ProjectContext(

        project_name=self.name,

        project_folder=self.project_folder,

        photo=self.photo,

        vision_folder=self.vision_folder,

        identity_folder=self.identity_folder,

        prompt_folder=self.prompt_folder,

        preview_folder=self.preview_folder,

        svg_folder=self.svg_folder,

        fusion_folder=self.fusion_folder,

        exports_folder=self.project_folder / "exports",

    )