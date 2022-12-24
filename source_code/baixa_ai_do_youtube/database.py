from json import dumps, loads
from os.path import exists
from os import makedirs

class Database:

    def __init__(self, default_path_to_database: str = "./baixa_ai_do_youtube/database/db.json", db_folder = "./baixa_ai_do_youtube/database/") -> None:        
        self.db_folder = db_folder
        self.default_path_to_database = default_path_to_database        
        self.database = {}

        if not self.check_if_database_exists():
            self.create_database()

        self.load_database()

    def create_db_folder(self) -> None:
        if not exists(self.db_folder):
            makedirs(self.db_folder)

    def create_database(self) -> None:
        """
        Cria o arquivo de banco de dados.
        """
        self.create_db_folder()
        with open(self.default_path_to_database, "w", encoding="utf-8") as file:
            self.database = {
                "files": {
                    "mp3": [],
                    "mp4": []
                }
            }
            file.write(dumps(self.database))

    def check_if_database_exists(self) -> bool:
        """
        Checa se o arquivo de banco de dados existe.
        """
        return True if exists(self.default_path_to_database) else False


    def load_database(self) -> None:
        """
        Carrega o arquivo de banco de dados.
        """
        with open(self.default_path_to_database, "r") as file:
            self.database = loads(file.read())

    def save_database(self) -> None:
        """
        Salva o arquivo de banco de dados.
        """
        def saver():
            with open(self.default_path_to_database, "w") as file:
                file.write(dumps(self.database, indent=4))
        saver()
        self.remove_duplicates()
        saver()

    def add_to_database(self, key: str, value: str) -> None:
        """
        Adiciona uma chave e um valor ao banco de dados.

        Parâmetros:
        key: Chave que representa a extensão do arquivo, para adicionar no banco de dados.
        value: Valor que será adicionado ao banco de dados.
        """
        self.database["files"][key].append(value)
        self.save_database()            

    def check_if_file_is_in_database(self, key: str, value: str) -> bool:
        """
        Checa se um valor está presente no banco de dados.

        Parâmetros:
        key: Chave que representa a extensão do arquivo, para adicionar no banco de dados.
        value: Valor que será adicionado ao banco de dados.
        """
        return True if value in self.database["files"][key] else False

    def remove_duplicates(self) -> None:
        """
        Remove duplicatas do banco de dados.
        """
        for key in self.database["files"].keys():
            self.database["files"][key] = list(set(self.database["files"][key]))
            
       