from json import loads, dumps
from os.path import exists
from os import makedirs
from requests import get
from io import BytesIO
from zipfile import ZipFile

class Updater:
    def __init__(self):
        self.json_url = "https://github.com/darkmathew/baixa_ai_do_youtube/tree/main/source_code/appversion.json"
        self.repo_base_url = "https://github.com/darkmathew/baixa_ai_do_youtube/raw/main/windows_executable/"
        self.pyinstaller_one_file_url = self.repo_base_url + "baixa_ai_do_youtube_option1.rar"
        self.pyinstaller_one_folder_url = self.repo_base_url + "baixa_ai_do_youtube_option2.rar"

    def check_for_updates(self):
        """
        Procura por atualizações.
        """
        if self.get_latest_version() > self.read_json()["version"]:
            self.download_latest_version()
        
    def read_json(self):
        """
        Lê o arquivo JSON.
        """
        if exists("appversion.json"):
            if not self.validate_json_keys():
                self.create_json_file()
                
            with open("appversion.json", "r") as file:
                return loads(file.read())
        else:
            self.create_json_file()

    def validate_json_keys(self):
        """
        Valida as chaves do arquivo JSON.
        """
        json = self.read_json()
        if json:
            if "version" in json and "program_option" in json:
                return True
        return False

    def create_json_file(self):
        """
        Cria o arquivo JSON.
        """
        if not exists("appversion.json"):
            with open("appversion.json", "w", encoding="utf-8") as file:
                file.write(dumps(
                    {"version": 0.0, "program_option": 0}
                ))

    def get_latest_version(self):
        """
        Checa a versão mais recente do programa.
        """
        return get(self.json_url).json()["version"]

    def download_latest_version(self) -> bool:
        """
        Baixa a versão mais recente do programa.
        """
        get_program_option = self.get_program_option_installed()
        match get_program_option:
            case 1:
                # Pyinstaller one-file
                request_file = get(self.pyinstaller_one_file_url)
            case 2:
                # Pyinstaller one-folder
                request_file = get(self.pyinstaller_one_folder_url)
            case _:
                # Impedir que o programa seja executado
                return False

        return self.install_latest_version(request_file)

    def install_latest_version(self, request_file) -> bool:
        """
        Instala a versão mais recente do programa.
        """
        if request_file.status_code == 200:
            bytesio_file = BytesIO()
            bytesio_file.write(request_file.content)

            with ZipFile(bytesio_file) as zip_file:
                zip_file.extractall("./")
            return True
        return False

    def get_program_option_installed(self):
        """
        Obtém qual opção de programa o usuário escolheu instalar.

        1. Pyinstaller one-file
        2. Pyinstaller one-folder

        """
        json = self.read_json()
        if json:
            return int(json["program_option"])