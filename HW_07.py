import collections
import shutil
import sys
from datetime import datetime
from pathlib import Path


# ВИБАЧТЕ ЩО ТАК ПІЗНО, БУЛИ ВЕЛИКІ ПРОБЛЕМИ ЗІ СВІТЛОМ ТА ПРОВАЙДЕРОМ (ІНТЕРНЕТ)


extension_dict = {
    "documents": [".doc", ".docx", ".xls", ".xlsx", ".txt", ".pdf"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "archives": [".zip", ".gz", ".tar"],
}

CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ?<>,!@#[]#$%^&*()-=; "
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_","_", "_")
TRANS = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = t
    TRANS[ord(c.upper())] = t.upper()


def normalize(name):
    global TRANS
    return name.translate(TRANS)


def is_file_exists(file, to_dir):
    if file in to_dir.iterdir():
        add_name = datetime.now().strftime("%d_%m_%Y_%H_%M_%S_%f")
        new_name = file.resolve().stem + f"_{add_name}_" + file.suffix
        new_name_path = Path(to_dir, new_name)
        return new_name_path
    return file


def is_fold_exists(file, to_dir):
    if to_dir.exists():
        folder_sort(file, to_dir) 
    else:
        Path(to_dir).mkdir()
        folder_sort(file, to_dir)
    

def folder_sort(file, to_dir):
    latin_name = normalize(file.name)    
    new_file = Path(to_dir, latin_name) 
    file_path = is_file_exists(new_file, to_dir) 
    file.replace(file_path) 


def show_result(p):
    total_dict = collections.defaultdict(list) 
    files_dict = collections.defaultdict(list)  

    for item in p.iterdir():
        if item.is_dir():
            for file in item.iterdir():
                if file.is_file():
                    total_dict[item.name].append(file.suffix)
                    files_dict[item.name].append(file.name) 
    for k, v in files_dict.items():
        print(f" Folder '{k}' contains files: ")
        print(f" ---- {v}")

    
    print("   File sorting completed successfully!!!   ")
    print("| {:^25} |{:^18}| {:^51} ".format("Folder", "files,pcs", "file's extensions"))
   
    for key, value in total_dict.items():
        k, a, b = key, len(value), ", ".join(set(value))
        print("| {:<25} |{:^18}| {:<51} ".format(k, a, b))


def sort_file(folder, p):
    for i in p.iterdir():
        if i.name in ("documents", "audio", "video", "images", "archives", "other"): 
            continue
        if i.is_file():
            flag = False  
            for f, suf in extension_dict.items():
                if i.suffix.lower() in suf:
                    to_dir = Path(folder, f)
                    is_fold_exists(i, to_dir)
                    flag = True  
                else:
                    continue
            if not flag: 
                to_dir = Path(folder, "other")
                is_fold_exists(i, to_dir)
        elif i.is_dir():
            if len(list(i.iterdir())) != 0:
                sort_file(folder, i) 
            else:
                shutil.rmtree(i)  

    for j in p.iterdir():
        if j.name == "archives" and len(list(j.iterdir())) != 0:
            for arch in j.iterdir():
                if arch.is_file() and arch.suffix in (".zip", ".gz", ".tar"):
                    try:
                        arch_dir_name = arch.resolve().stem  
                        path_to_unpack = Path(p, "archives", arch_dir_name) 
                        shutil.unpack_archive(arch, path_to_unpack)
                    except:
                        print(f" Error unpacking the archive!!! '{arch.name}'!\n")
                    finally:
                        continue
                else:
                    continue
        elif j.is_dir() and not len(list(j.iterdir())):
            shutil.rmtree(j)
    


def main():
    path = sys.argv[1]  
    folder = Path(path)
    p = Path(path)
    try:
        sort_file(folder, p)
    except FileNotFoundError:
        print("\n The folder was not found!!! \n")
        return
    return show_result(p)


if __name__ == "__main__":
    main()