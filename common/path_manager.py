import os.path
from pathlib import Path
from typing import Optional
import platform

class PathManager:
    def __init__(self, report_id: Optional[str] = None):
        self.report_id = report_id

        self.main_catalog = Path().resolve()

        os_path_separation = '\\' if platform.system() == 'Windows' else '/'
        while str(self.main_catalog).split(os_path_separation)[-1] != 'io-project':
            self.main_catalog = self.main_catalog.parent.resolve()

        self.model_llama  = self.main_catalog / 'llama'
        self.cache        = self.main_catalog / 'cache'
        self.fonts        = self.main_catalog / 'fonts'
        self.outputs      = self.main_catalog / 'outputs'
        self.report_path  = None
        self.create_dirs()

    def create_dirs(self):
        self.outputs.mkdir(exist_ok=True, parents=True)
        self.fonts.mkdir(exist_ok=True, parents=True)
        self.cache.mkdir(exist_ok=True, parents=True)
        self.model_llama.mkdir(exist_ok=True, parents=True)

    def get_report_path(self, report_id: Optional[str] = None, return_type: Optional[type] = Path) -> Path:
        assert report_id or self.report_id, 'Nie podałeś nazwy spotkania'
        report_id = report_id if report_id else self.report_id

        self.report_path = (self.outputs / f"{report_id}")
        self.report_path.mkdir(exist_ok=True, parents=True)
        return return_type(self.report_path)

    def get_cache_file(self):
        if os.path.exists(self.cache / 'mails.txt'):
            return self.cache / 'mails.txt'
        return None

if __name__ == "__main__":
    PathManager()
