import customtkinter
import re
from threading import Thread
from pytube import request
from pytube import YouTube

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self._set_appearance_mode("System")

        self.geometry("720x480")
        self.title('PyTube')
        request.default_range_size = 25600
        
        # Progress bar
        self.progressbar = customtkinter.CTkProgressBar(self, width=500)
        self.progressbar.set(0)

        #Error label
        self.error_label = customtkinter.CTkLabel(self, text='Welcome!')
        self.error_label.pack()

        #User input box
        self.user_input = customtkinter.CTkEntry(self, corner_radius=10, width=500, height = 35)
        self.user_input.pack()
        
        
        #Quality selection tab
        self.tabview = customtkinter.CTkTabview(self, height=10)
        
        # Audio tab
        self.tabview.add("Audio")
        self.audio_quality = customtkinter.CTkSegmentedButton(
            self.tabview.tab("Audio"),
            values=["128kbps"])
        self.audio_quality.pack(padx=20, pady=10)
        #self.audio_quality.set('128Kbps')
        
        # Video tab
        self.tabview.add("Video")
        self.video_quality = customtkinter.CTkSegmentedButton(
            self.tabview.tab("Video"), values=['144p','360p','720p'])
        self.video_quality.pack(padx=20, pady=10)
        self.tabview.pack()
        #self.video_quality.set('720p')
        
        


        # Download button
        self.button = customtkinter.CTkButton(self, text="Download", command=self.Download)
        self.button.pack(padx=10, pady=10)
    
    

    def link_validate(self,link):
        ytube = re.findall(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", link)
        if ytube:
            return True #'https://www.youtube.com/watch?v='+ytube[0]
        else: 
            return False
      
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = bytes_downloaded / total_size * 100
        self.error_label.configure(text=f'------------- Download {int(percentage)}% -------------')
        self.error_label.update()

        self.progressbar.set(int(percentage)/100)
        self.update()
        
    
    
        
    def youtube_video_download(self, link, res):
        yt = YouTube(link, on_progress_callback=self.progress_callback)
        vid = yt.streams.filter(progressive=True, resolution=res).first()
        vid.download()


    def youtube_audio_download(self, link, res='128kbps',):
        yt = YouTube(link, on_progress_callback=self.progress_callback)
        audio = yt.streams.filter(only_audio=True, abr=res).first()
        audio.download()

        
    def Download(self):
        if self.link_validate(self.user_input.get()):
            if self.tabview.get() == 'Video':
                if self.video_quality.get() != '':
                    Thread(target=self.youtube_video_download, args=(self.user_input.get(), self.video_quality.get(), )).start()
                    #self.youtube_video_download(self.user_input.get(), self.video_quality.get())
                else:
                    self.error_label.configure(text='Video quality is not selected!')
            elif self.tabview.get() == 'Audio':
                if self.audio_quality.get() == '128kbps':
                    Thread(target=self.youtube_audio_download, args=(self.user_input.get(), self.audio_quality.get(), )).start()
                    #self.youtube_audio_download(self.user_input.get(), self.audio_quality.get())
                else:
                    self.error_label.configure(text='Audio quality is not selected!')
            else:
                self.error_label.configure(text='Format is not selected!')
        else:
            self.error_label.configure(text='Link is not valid!')



if __name__=="__main__":
    app = App()
    app.mainloop()