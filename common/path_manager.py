import os.path
from pathlib import Path


class PathManager:
    def __init__(self):
        self.main_catalog = Path().resolve()
        while str(self.main_catalog).split('\\')[-1] != 'io-project':
            self.main_catalog = self.main_catalog.parent.resolve()

        self.model_vosk   = self.main_catalog / 'model_vosk'
        self.outputs      = self.main_catalog / 'outputs'
        self.report_path  = None
        self.create_dirs()

    def create_dirs(self):
        self.outputs.mkdir(exist_ok=True, parents=True)

    def get_report_path(self, report_id: str) -> Path:
        self.report_path = (self.outputs / f"{report_id}")
        self.report_path.mkdir(exist_ok=True, parents=True)
        return self.report_path

if __name__ == "__main__":
    PathManager()
