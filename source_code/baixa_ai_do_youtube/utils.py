from datetime import datetime

def get_date_and_time() -> str:
    """
    Retorna a data e hora atual no formato dd-mm-aaaa hh:mm:ss
    """
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")

def get_date() -> str:
    """
    Retorna a data atual no formato dd-mm-aaaa
    """
    return datetime.now().strftime("%d-%m-%Y")