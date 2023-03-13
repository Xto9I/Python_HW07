import os
from os import mkdir
import sys
from pathlib import Path
import shutil
import re


images = []
documents = []
audio = []
video = []
archives = []
others = []

container_list = {
    "images": images,
    "video": video,
    "documents": documents,
    "audio": audio,
    "archives": archives
}

REGISTER_EXTENSIONS = {
    'JPEG': "images",
    'PNG': "images",
    'JPG': "images",
    'SVG': "images",
    'AVI': "video",
    'MP4': "video",
    'MOV': "video",
    'MKV': "video",
    'DOC': "documents",
    'DOCX': "documents",
    'TXT': "documents",
    'PDF': "documents",
    'XLSX': "documents",
    'PPTX':"documents",
    'MP3': "audio",
    'OGG': "audio",
    'WAV': "audio",
    'AMR': "audio",
    'ZIP': "archives",
    'GZ': "archives",
    'TAR': "archives"
}

FOLDERS = ['archives', 'video', 'audio', 'documents', 'images', 'others']
EXTENSIONS = set()
UNKNOWN = set()
other_folders =[]

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()

folder_for_scan = sys.argv[1]


def get_extension(filename: str) -> str:
   
    return Path(filename).suffix[1:].upper()


def normalize(name: str) -> str:

    t_name = name.translate(TRANS)
    t_name = re.sub(r'\W', '_', t_name)
    return t_name


def remove_empty_folders(other_folders):

    for item in other_folders:
        if not os.listdir(item):
            os.rmdir(item)


def scan(folder: Path):

    for item in folder.iterdir():

        if item.name == ".DS_Store":
            pass

        # Робота з текою   
        if item.is_dir():
            if item.name not in FOLDERS:
                fullname_folder = folder / item.name
                t_name = normalize(item.name)
                norm_fullname_folder = folder / t_name
                os.rename(fullname_folder, norm_fullname_folder)
                other_folders.append(norm_fullname_folder)
                scan(item)
            else:
                scan(item)
        
        # Робота з файлом
        else:
            ext = get_extension(item.name)  # взяти розширення
            fullname = folder / item.name
            t_name = normalize(item.stem)   # транслітерація
            new_name = t_name + "." + ext
            norm_fullname = folder / new_name
            os.rename(fullname, norm_fullname)

            # переміщення файлів по текам
            if ext in REGISTER_EXTENSIONS:
                foldername = REGISTER_EXTENSIONS.get(ext)
                try:
                    if not os.path.exists("{}{}{}".format(folder_for_scan, os.sep, foldername)):
                        mkdir("{}{}{}".format(folder_for_scan, os.sep, foldername))
                    shutil.move(norm_fullname, "{}{}{}{}{}".format(folder_for_scan, os.sep, foldername, os.sep, new_name))
                except:
                    continue
            else:
                foldername = "others"
                try:
                    if not os.path.exists("{}{}{}".format(folder_for_scan, os.sep, foldername)):
                         mkdir("{}{}{}".format(folder_for_scan, os.sep, foldername))
                    shutil.move(norm_fullname, "{}{}{}{}{}".format(folder_for_scan, os.sep, foldername, os.sep, new_name))
                except:
                    continue

            # формулювання списків документів та розширень для виведення користувачу
            if not ext:  
                others.append(norm_fullname)   
            else:
                try:
                    container_name = REGISTER_EXTENSIONS[ext]
                    container = container_list[container_name]
                except KeyError:
                    UNKNOWN.add(ext)
                    others.append(norm_fullname)
                    continue
                EXTENSIONS.add(ext)
                container.append(norm_fullname)
            
            # розпаковка архівів
            if REGISTER_EXTENSIONS.get(ext) == "archives":
                
                path_archives = "{}{}{}".format(folder_for_scan, os.sep, foldername)               
                for item in Path(path_archives).iterdir():
                    if ext:
                        filename = item
                        print(filename)
                        if not os.path.exists("{}{}{}{}{}".format(folder_for_scan, os.sep, "archives", os.sep, t_name)):
                            mkdir("{}{}{}{}{}".format(folder_for_scan, os.sep, "archives", os.sep, t_name))
                        extract_dir = Path(("{}{}{}{}{}".format(folder_for_scan, os.sep, "archives", os.sep, t_name)))
                        archive_format = str(ext.lower())
                        shutil.unpack_archive(filename, extract_dir, archive_format)


def start_sort():

    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))

    remove_empty_folders(other_folders)
    
    print(f'archives: {archives}')
    print(f'audio: {audio}')
    print(f'documents: {documents}')
    print(f'images: {images}')
    print(f'others: {others}')
    print(f'video: {video}')
    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')


if __name__ == '__main__':
    start_sort()