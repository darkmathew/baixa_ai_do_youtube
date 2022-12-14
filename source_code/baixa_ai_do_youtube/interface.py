from PyQt5.QtWidgets import QApplication, QFileDialog, QLineEdit, QMessageBox
from PyQt5 import uic, QtCore
from qt_thread_updater import get_updater
from datetime import datetime
from os import getcwd
from .color import get_color_hex
from .youtube import YoutubeDownloader
from .database import Database
from threading import Thread

class Interface:

    def __init__(self, logger) -> None:
        self.app = QApplication([])
        self.logger = logger
        self.get_color_hexadecimal = get_color_hex

    def start(self) -> None:
        self.load_window()
        self.conect_buttons()

        self.main_window.show()


    def load_window(self) -> None:
        """
        Carrega a interface
        """
        self.main_window = uic.loadUi("./baixa_ai_do_youtube/gui/main_ui.ui")


    def update_progress_bar(self, value) -> None:
        """
        Atualiza a progress bar na interface
        """
        get_updater().call_in_main(
            self.main_window.progressBar.setValue, value
        )

    def update_label_status(self, text, color="white", text_color="white", default_text_color="white") -> None:
        """
        Atualiza o label de status na interface
        """
        styleSheet = 'QLabel{color: '+ text_color + '; border-radius: 4px; background-color: ' + color + ';  border: 1px solid black;}'        
        get_updater().call_in_main(self.main_window.label_status.setAlignment, QtCore.Qt.AlignCenter)
        get_updater().call_in_main(self.main_window.label_status.setStyleSheet, styleSheet)
        get_updater().call_in_main(self.main_window.label_status.setText, text)
        text_color = self.get_color_hexadecimal(default_text_color)


    def update_text_edit_log(self, text, color="white", bold=False, with_time=True, default_color="white") -> None:
        """
        Atualiza o text edit de log na interface
        """
        current_datetime = ""
        if with_time:
            current_datetime = f'[{datetime.now().strftime("%H:%M:%S")}]'

        final_text = f"<font color={color}>{current_datetime} {text}</font>"
        if bold:
            final_text = f"<b>{final_text}</b>"

        get_updater().call_in_main(self.main_window.textEdit_activities.append, final_text)
        color = self.get_color_hexadecimal(default_color)

    def conect_buttons(self) -> None:
        self.main_window.pushButton_Download.clicked.connect(self.start_download_process)
        self.main_window.pushButton_openFileDialog.clicked.connect(self.select_path)

    
    def combobox_changed(self) -> None:
        self.main_window.comboBox.currentIndexChanged.connect(self.get_combo_box_value)


    def get_combo_box_value(self) -> str:
        """
        Retorna o modo de download selecionado pelo usu??rio.
        """
        match self.main_window.comboBox.currentText():
            case "Baixar apenas em formato mp3":
                return "mp3_only"
            case "Baixar v??deo [Qualidade Alta] (arquivo maior)":
                return "video_high_quality"
            case "Baixar v??deo [Qualidade Baixa] (arquivo menor)":
                return "video_low_quality"
            case "Baixar v??deo [Qualidade Alta] + mp3":
                return "video_high_quality_and_mp3"
            case "Baixar v??deo [Qualidade Baixa] + mp3":
                return "video_low_quality_and_mp3"
            case _:
                self.logger.log("A op????o selecionada pelo usu??rio n??o foi poss??vel de ser identificada, o programa ir?? baixar apenas o arquivo em formato mp3.")
                return "mp3_only"
    

    def handle_buttons(self, is_active: bool = False) -> None:
        """
        Habilita ou desabilita os bot??es da interface.
        """
        buttons = [
            self.main_window.pushButton_openFileDialog,
            self.main_window.pushButton_Download,
        ]
        for button in buttons:
            button.setEnabled(is_active)


    def handle_line_edits(self, is_active: bool = False) -> None:
        """
        Habilita ou desabilita os campos de texto da interface.
        """
        line_edits = [
            self.main_window.lineEdit_filePath,
            self.main_window.lineEdit_youtubeLink,
        ]
        for line_edit in line_edits:
            line_edit.setEnabled(is_active)


    def reset_line_edits(self) -> None:
        """
        Limpa os campos de texto da interface.
        """
        line_edits = [
            self.main_window.lineEdit_filePath,
            self.main_window.lineEdit_youtubeLink,
        ]
        for line_edit in line_edits:
            line_edit.setText("")


    def select_path(self) -> None:
        """
        Abre uma janela para o usu??rio selecionar o diret??rio onde os arquivos ser??o salvos.
        """
        qfile_dialog = QFileDialog()
        path = getcwd()
        title_window = "Pasta para salvar os arquivos"
        self.main_window.lineEdit_filePath.setText(QFileDialog.getExistingDirectory(qfile_dialog, title_window, path))


    def validate_line_edit(self, linedit: QLineEdit, message: str) -> bool:
        """
        Valida se o campo de texto est?? preenchido corretamente.

        linedit: Campo de texto a ser validado.
        message: Mensagem a ser exibida caso o campo de texto n??o esteja preenchido corretamente.

        Retorna True se o campo de texto estiver preenchido corretamente.        
        """
        if linedit.text() == "" or linedit.text() == " " or len(linedit.text()) < 5:
            self.update_label_status(message, self.get_color_hexadecimal("red"))
            return False
        
        return True

    def execute_all_validations(self) -> bool:
        """
        Realiza todas as valida????es necess??rias para iniciar o processo de download.
        Retorna True se todas as valida????es forem executadas com sucesso.
        """
        if not self.validate_line_edit(self.main_window.lineEdit_filePath, "Selecione um diret??rio para salvar os arquivos"):
            return False

        if not self.validate_line_edit(self.main_window.lineEdit_youtubeLink, "Insira um link v??lido do youtube"):
            return False

        return True

    def start_download_process(self) -> None:
        """
        Inicia o processo de download.
        """
        if not self.execute_all_validations():
            return
            
        self.update_label_status("Programa iniciado", self.get_color_hexadecimal("light_gray"), text_color=self.get_color_hexadecimal("black"))
        self.update_text_edit_log("Verificando links", self.get_color_hexadecimal("white"))
        self.handle_buttons(False)
        self.handle_line_edits(False)
        self.update_progress_bar(0)

        self.file_path = self.main_window.lineEdit_filePath.text()
        self.youtube_link = self.main_window.lineEdit_youtubeLink.text().replace(" ", "")

        yt_downloader = YoutubeDownloader(self, self.youtube_link, self.file_path, self.get_combo_box_value(), Database())
            
        # Thread para executar o processo de download em paralelo.
        thread_yt_downloader = Thread(target=yt_downloader.start, daemon=True, name="thread_yt_downloader")
        thread_yt_downloader.start()


    def download_completed(self) -> None:
        """
        Executa a????es quando o download ?? finalizado.
        """
        self.update_label_status(
            "Download finalizado.", 
            self.get_color_hexadecimal("green"), 
            text_color=self.get_color_hexadecimal("black")
        )
        self.update_text_edit_log(f"Todos os arquivos foram baixados com sucesso em: {self.file_path}", self.get_color_hexadecimal("green"))
        self.handle_buttons(True)
        self.handle_line_edits(True)
        self.reset_line_edits()        
        self.update_progress_bar(100)
        
        
        
    def download_failed(self) -> None:
        """
        Executa a????es quando o download falha.
        """
        self.update_label_status(
            "O download falhou, tente novamente.", 
            self.get_color_hexadecimal("red"), 
            text_color=self.get_color_hexadecimal("black")
        )
        self.update_text_edit_log("Ocorreu um erro durante o download, tente novamente", self.get_color_hexadecimal("red"))
        self.handle_buttons(True)
        self.handle_line_edits(True)
        self.reset_line_edits()
        self.update_progress_bar(0)

    def show_message_box(self, title: str, message: str, icon: QMessageBox.Icon = QMessageBox.Warning) -> QMessageBox:
        """
        Exibe uma caixa de mensagem para o usu??rio.

        title: T??tulo da caixa de mensagem.
        message: Mensagem a ser exibida.
        icon: ??cone a ser exibido na caixa de mensagem.
        """
        messagebox = QMessageBox()
        messagebox.setIcon(icon)
        messagebox.setWindowTitle(title)
        messagebox.setText(message)
        return messagebox

    
    def show_update_notification(self) -> bool:
        """
        Exibe uma caixa de mensagem para o usu??rio informando que h?? uma nova vers??o dispon??vel para download.

        Retorna True se o usu??rio clicar em 'Baixar Atualiza????o'. Retorna False se o usu??rio clicar em 'N??o quero atualizar'.
        """        
        message_box : QMessageBox = self.show_message_box(
            "Atualiza????o dispon??vel", 
            "Foi detectado que h?? uma nova vers??o dispon??vel para este aplicativo. O download ser?? iniciado automaticamente ao clicar em 'Baixar Atualiza????o'. O tempo de download pode variar de acordo com a velocidade da sua internet."
        )
        message_box.addButton('   Baixar Atualiza????o   ', message_box.ActionRole)
        message_box.addButton('N??o quero atualizar', message_box.ActionRole)
        button_changed = message_box.exec_()
        if button_changed == 0:
            return True
        return False