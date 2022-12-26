from baixa_ai_do_youtube.interface import Interface
from baixa_ai_do_youtube.prog_logger import ProgramLogger
from baixa_ai_do_youtube.updater import Updater
from sys import exit

if __name__ == "__main__":
    
    logger = ProgramLogger()
    app_interface = Interface(logger)
    updater = Updater(app_interface)

    can_start_app = updater.check_for_updates()
    
    if can_start_app:
        app_interface.start()
        code = app_interface.app.exec_()
        if code == 0:
            exit(code)        