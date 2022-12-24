from baixa_ai_do_youtube.interface import Interface
from baixa_ai_do_youtube.prog_logger import ProgramLogger
from baixa_ai_do_youtube.updater import Updater
from sys import exit

if __name__ == "__main__":
    updater = Updater()
    updater.check_for_updates()
    
    logger = ProgramLogger()
    app_interface = Interface(logger)
    app_interface.start()
    code = app_interface.app.exec_()
    if code == 0:
        exit(code)        