from pytube import YouTube
from pytube import Playlist
import os
import re
from moviepy.audio.io.AudioFileClip import AudioFileClip


class YoutubeDownloader:

    def __init__(self, app_interface, youtube_link: str, file_path: str, download_option: str) -> None:
        self.app_interface = app_interface
        self.youtube_link = youtube_link
        self.file_path = file_path
        self.download_option = download_option


    def start(self):
                    
        if self.check_if_url_is_a_playlist(self.youtube_link):
            completed = self.download_playlist()
        else:
            completed = self.download_solo_mode()

        if completed:
            self.app_interface.download_completed()            
        else:
            self.app_interface.download_failed()


    def check_if_url_is_a_playlist(self, link: str) -> bool:
        """
        Checa se o link informado pelo usuário se trata de uma Playlist ou não.
        """
        return True if "playlist" in link else False

    
    def download_playlist(self) -> bool:
        try:
            playlist = Playlist(self.youtube_link)
            total_videos = len(playlist.videos)

            self.app_interface.update_text_edit_log(f"Baixando playlist: {playlist.title}")
            self.app_interface.update_text_edit_log(f"Total de vídeos: {total_videos}")
            
            videos_downloaded = 0
            for video in playlist.videos:
                
                self.app_interface.update_text_edit_log(f"Baixando: {video.title}")
                
                if "high_quality" in self.download_option:                    
                    self.download_high_resolution_video(video)
                else:
                    self.download_low_resolution_video(video)


                self.app_interface.update_text_edit_log(f"Vídeo baixado com sucesso.")
                self.app_interface.update_text_edit_log(f"Passando para o próximo vídeo.")            
                
                videos_downloaded += 1            
                
                self.app_interface.update_progress_bar(int((videos_downloaded / total_videos)) * 100)

                self.app_interface.update_label_status(
                    f"{videos_downloaded} de {total_videos} Baixados", 
                    self.app_interface.get_color_hexadecimal("black")
                )

            self.app_interface.update_text_edit_log(f"Playlist baixada com sucesso.")          
            
            self.download_mp3()            
                
        except Exception as error:
            self.app_interface.logger.log(error)
            self.app_interface.update_text_edit_log(f"Verifique o log de erros.")
            return False
        return True


    def download_mp3(self, video_text: str = "videos") -> None:
        """
        Realiza a conversão dos vídeos baixados para mp3. Caso a opção de baixar apenas mp3 tenha sido selecionada.
        video_text: str = "videos" -> Texto que será exibido no label de status.
        """
        if "mp3" in self.download_option:            
            self.app_interface.update_label_status(
                f"Convertendo {video_text} para mp3.", 
                self.app_interface.get_color_hexadecimal("light_blue"), 
                self.app_interface.get_color_hexadecimal("black")
            )

            self.app_interface.update_text_edit_log(f"Convertendo vídeos para mp3.")
            
            remove_video = True if "mp3_only" in self.download_option else False                
            self.convert_videos_to_mp3(remove_video)            
                        


    def download_solo_mode(self):
        pytube_video = YouTube(self.youtube_link)
        self.app_interface.update_text_edit_log(f"Baixando: {pytube_video.title}")

        if "high_quality" in self.download_option:                    
            download_status = self.download_high_resolution_video(pytube_video)
        else:
            download_status = self.download_low_resolution_video(pytube_video)

        if download_status:
            self.app_interface.update_text_edit_log(f"Vídeo baixado com sucesso.")
            self.download_mp3("video")
        else:
            self.app_interface.update_text_edit_log(f"Erro ao baixar vídeo.")
            self.app_interface.update_text_edit_log(f"Verifique o log de erros.")
        return download_status


    def download_high_resolution_video(self, video: YouTube) -> bool:
        try:
            video.streams.get_highest_resolution().download(self.file_path)
        except Exception as error:
            self.app_interface.logger.log(error)
            return False
        return True


    def download_low_resolution_video(self, video: YouTube) -> bool:
        try:
            video.streams.get_lowest_resolution().download(self.file_path)
        except Exception as error:
            self.app_interface.logger.log(error)
            return False
        return True
    

    def convert_videos_to_mp3(self, remove_video: bool = False, video_format: str = "mp4"):
        amount_videos_converted = 0
        for file in os.listdir(self.file_path):
            
            if re.search(video_format, file):
                
                self.app_interface.update_text_edit_log(f"Convertendo {file} para mp3")                                
                
                mp4_path = os.path.join(self.file_path, file)
                mp3_path = os.path.join(self.file_path, os.path.splitext(file)[0]+'.mp3')
                
                new_file = AudioFileClip(mp4_path)
                new_file.write_audiofile(mp3_path)
                
                if remove_video:
                    os.remove(mp4_path)
                
                amount_videos_converted += 1
                
                self.app_interface.update_label_status(
                    f"{amount_videos_converted} convertidos para mp3.", 
                    self.app_interface.get_color_hexadecimal("light_yellow"), 
                    self.app_interface.get_color_hexadecimal("black")
                )

                self.app_interface.update_text_edit_log(f"Convertido com sucesso.")

