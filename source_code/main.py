from baixa_ai_do_youtube.interface import Interface
from baixa_ai_do_youtube.prog_logger import ProgramLogger
from sys import exit

if __name__ == "__main__":
    logger = ProgramLogger()
    app_interface = Interface(logger)
    app_interface.start()
    code = app_interface.app.exec_()
    if code == 0:
        exit(code)        