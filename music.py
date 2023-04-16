'''
# 20230405 00:46 增加绝对路径的配置
'''
import os
import csv
import tkinter as tk
import logging
import time
from datetime import datetime
import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TPE1, TALB, TDRC, TCON


class MusicInfoGUI:
    def __init__(self):
        log_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录的绝对路径
        log_file = os.path.join(log_path, "{}.log".format(time.strftime("%Y-%m-%d",time.localtime())))  # log文件的绝对路径
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s',  encoding='utf-8')
        self.logger = logging.getLogger(__name__)
        self.window = tk.Tk()
        self.window.title("音乐信息管理系统")
        self.window.geometry("800x300")

        self.btn1 = tk.Button(self.window, text="1、点击读取当前路径下所有歌曲文件信息", command=self.read_music_files)
        self.btn1.pack(pady=20)

        self.btn2 = tk.Button(self.window, text="2、更新完music.csv后点击修改歌曲属性信息", command=self.update_music_info)
        self.btn2.pack(pady=20)

        self.label = tk.Label(self.window, text="")
        self.label.pack(pady=20)

        self.window.mainloop()

    def read_music_files(self):
        self.label.config(text="正在获取当前路径下歌曲文件信息……")
        self.window.update_idletasks()
        self.logger.info("正在获取当前路径下歌曲文件信息……")

        if os.path.exists("music.csv"):
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            new_filename = "music" + current_time + ".csv"
            try:
                os.rename("music.csv", new_filename)
                self.label.config(text=f"已将music.csv备份为{new_filename}")
                self.logger.info(f"已将music.csv备份为{new_filename}")
            except Exception as e:
                self.label.config(text=f"备份文件失败：{str(e)}请先关闭该文件")
                self.logger.error(f"备份文件失败：{str(e)}请先关闭该文件")
                raise


        # music_files = [file for file in os.listdir(".") if file.endswith(".mp3")]
        music_files = []
        for file in os.listdir():
            if file.endswith(".mp3"):
                file_path = os.path.abspath(file)
                title, artist, album, year, genre, gettime= "", "", "", "", "", ""
                try:
                    audio = mutagen.File(file_path)
                    if audio:
                        title = audio["TIT2"].text[0]
                        artist = audio["TPE1"].text[0]
                        album = audio["TALB"].text[0]
                        # albumartist = audio["TPE2"].text[0]
                        year = audio["TDRC"].text[0]
                        # year = audio.tag.release_date
                        genre = audio["TCON"].text[0]
                        # genre = audio.tag.genre.name
                        gettime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        self.label.config(text=f"获取{file}信息成功")
                        self.logger.info(f"获取{file}信息成功")
                except Exception as e:
                    self.label.config(text=f"获取{file}信息失败：{str(e)}")
                    self.logger.error(f"获取{file}信息失败：{str(e)}")
                    # print(f"获取{file}信息失败：{str(e)}")
                music_files.append([file, title, artist, album, year, genre, gettime])

            # 获取.flac文件的属性信息
            elif file.endswith(".flac"):
                file_path = os.path.abspath(file)
                title, artist, album, year, genre, gettime= "", "", "", "", "", ""
                try:
                    audio = mutagen.File(file_path)
                    if audio:
                        title = str(audio["title"])
                        title = title.strip("[]").replace("'", "")
                        artist = str(audio["artist"])
                        artist = artist.strip("[]").replace("'", "")
                        album = str(audio["album"])
                        album = album.strip("[]").replace("'", "")
                        # albumartist = str(audio["albumartist"])
                        # albumartist = albumartist.strip("[]").replace("'", "")
                        year = str(audio["year"])
                        year = year.strip("[]").replace("'", "")
                        # year = audio.tag.release_date
                        genre = str(audio["genre"])
                        genre = genre.strip("[]").replace("'", "")
                        # genre = audio.tag.genre.name
                        gettime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                        self.label.config(text=f"获取{file}信息成功")
                        self.logger.info(f"获取{file}信息成功")
                except Exception as e:
                    self.label.config(text=f"获取{file}信息失败：{str(e)}")
                    self.logger.error(f"获取{file}信息失败：{str(e)}")
                    # print(f"获取{file}信息失败：{str(e)}")
                music_files.append([file, title, artist, album, year, genre, gettime])
            else:
                self.label.config(text=f"文件{file}的类型暂不支持，无法获取属性")
                self.logger.error(f"文件{file}的类型暂不支持，无法获取属性")

        output_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录的绝对路径
        output_file = os.path.join(output_path, 'music.csv')  # 输出文件的绝对路径
        with open(output_file, "w", newline="", encoding="gbk") as f:
            writer = csv.writer(f)
            writer.writerow(["文件名", "标题", "歌手", "专辑", "年份", "音乐类型", "获取时间"])
            try:
                writer.writerows(music_files)
            except Exception as e:
                self.label.config(text=f"写入文件music.csv失败: {str(e)}")
                self.logger.error(f"写入文件music.csv失败: {str(e)}")



        self.label.config(text="获取歌曲信息成功，请打开music.csv修改歌曲属性")
        self.logger.info("获取歌曲信息成功，请打开music.csv修改歌曲属性")

    def update_music_info(self):
        self.label.config(text="正在更新歌曲属性信息……")
        self.window.update_idletasks()
        self.logger.info("正在更新歌曲属性信息……")

        updated_count = 0
        failed_count = 0

        read_path = os.path.abspath(os.path.dirname(__file__))  # 获取当前文件所在目录的绝对路径
        read_file = os.path.join(read_path, 'music.csv')  # 输出文件的绝对路径
        with open(read_file, "r", encoding="gbk") as f:
            reader = csv.reader(f)
            next(reader) # skip header row
            for row in reader:
                filename, title, artist, album, year, genre , gettime = row
                filepath = os.path.join(filename)
                if os.path.exists(filepath):
                    try:
                        audio_file = mutagen.File(filepath)
                        # 如果文件类型是MP3
                        if filepath.endswith(".mp3"):
                            # 如果 music.csv 文件中的某个属性有值，则将该属性值更新到 MP3 文件标签中
                            if title:
                                audio_file["TIT2"] = TIT2(encoding=1, text=f"{title}")
                            if artist:
                                audio_file["TPE1"] = TPE1(encoding=1, text=f"{artist}")
                            if album:
                                audio_file["TALB"] = TALB(encoding=1, text=f"{album}")
                            if year:
                                # audio_file.tag.year = year
                                # audio_file.tag.release_date = year
                                audio_file["TDRC"] = TDRC(encoding=0, text=f"{year}")
                            if genre:
                                # audio_file.genre.name = eyed3.id3.Genre(name=genre)
                                audio_file["TCON"] = TCON(encoding=0, text=f"{genre}")
                            # 保存修改后的 MP3 文件
                            audio_file.save()
                            updated_count += 1
                            self.label.config(text=f"成功更新歌曲{filename}的属性信息")
                            self.window.update_idletasks()
                            self.logger.info(f"成功更新歌曲{filename}的属性信息")

                            # print(f"成功更新歌曲{filename}的属性信息")

                        # 如果文件为.flac则执行如下内容
                        elif filepath.endswith(".flac"):
                            # 如果 music.csv 文件中的某个属性有值，则将该属性值更新到 MP3 文件标签中
                            if title:
                                audio_file["title"] = f"{title}"
                            if artist:
                                audio_file["artist"] = f"{artist}"
                            if album:
                                audio_file["album"] = f"{album}"
                            if year:
                                # audio_file.tag.year = year
                                # audio_file.tag.release_date = year
                                audio_file["year"] = f"{year}"
                            if genre:
                                # audio_file.genre.name = eyed3.id3.Genre(name=genre)
                                audio_file["genre"] = f"{genre}"
                            # 保存修改后的 flac 文件
                            audio_file.save()
                            updated_count += 1
                            self.label.config(text=f"成功更新歌曲{filename}的属性信息")
                            self.window.update_idletasks()
                            self.logger.info(f"成功更新歌曲{filename}的属性信息")
                            # print(f"成功更新歌曲{filename}的属性信息")
                        else:
                            failed_count += 1
                            self.label.config(text=f"歌曲{filename}的类型暂不支持，无法更新属性")
                            self.window.update_idletasks()
                            self.logger.error(f"歌曲{filename}的类型暂不支持，无法更新属性")
                            # print(f"歌曲{filename}的类型暂不支持，无法更新属性")
                    except Exception as e:
                        failed_count += 1
                        self.label.config(text=f"歌曲{filename}{str(e)}，无法更新属性，请检查文件是否被占用")
                        self.window.update_idletasks()
                        self.logger.error(f"歌曲{filename}{str(e)}，无法更新属性，请检查文件是否被占用")
                        # print(f"歌曲{filename}{str(e)}，无法更新属性")
                else:
                    failed_count += 1
                    self.label.config(text=f"文件{filename}不存在，无法更新属性")
                    self.window.update_idletasks()
                    self.logger.error(f"文件{filename}不存在，无法更新属性")

        self.label.config(text=f"成功更新{updated_count}首歌曲属性，失败{failed_count}首,失败原因请查看log.log")
        self.logger.error(f"成功更新{updated_count}首歌曲属性，失败{failed_count}首,失败原因请查看log.log")

if __name__ == "__main__":
    app = MusicInfoGUI()
