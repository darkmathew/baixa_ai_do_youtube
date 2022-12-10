import os
from .utils import get_date_and_time, get_date

class ProgramLogger:

    def __init__(self, log_file=f"log_{get_date()}.txt"):
        self.log_file = log_file
        self.log_folder = "./baixa_ai_do_youtube/logs/"

        self.create_logs_folder()
        if not self.log_file_exists():
            self.create_log_file()

    def create_logs_folder(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def log_file_exists(self):
        return True if os.path.exists(self.log_folder + self.log_file) else False

    def create_log_file(self):
        with open(self.log_folder + self.log_file, "w", encoding="utf-8") as log:
            log.write(f"Log gerado em {get_date_and_time()}")

    def log(self, message: str):
        with open(self.log_folder + self.log_file, "a", encoding="utf-8") as log:
            log.write(f"{get_date_and_time()} - {message}")


if __name__ == "__main__":
    logger = ProgramLogger()
    logger.log("Teste de log")