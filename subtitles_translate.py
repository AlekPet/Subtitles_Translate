#!python3
# Author: AlekPet

import os
import sys
import time
from tempfile import mkstemp
import shutil
import re
import argparse
from googletrans import Translator, LANGUAGES

translator = Translator()

regx = re.compile(r"^\d+|\s+$", re.I)


def copy_(rename=True, s='.srt', po='.txt'):
    """Function copy file"""
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            _file = file.replace(s, po)
            if file.endswith(s) and not os.path.exists(os.path.join(os.getcwd(), "txt", _file)):
                shutil.copy2(os.path.join(root, file), os.path.join(os.getcwd(), "txt", file))
                if rename:
                    rename_(file, _file)


def rename_(file, _file):
    """Rename function"""
    os.rename(os.path.join(os.getcwd(), "txt", file), os.path.join(os.getcwd(), "txt", _file))


def translate_subtitles(path, args):
    """Function Translate subtitles"""
    path_process = path
    path_complete = os.path.join(os.path.dirname(__file__), 'complete')
    last_folder = os.path.basename(path)

    if isinstance(args, argparse.Namespace):
        from_src = args.trans_src
        trans_to = args.trans_to
        sleep = args.sleep
        time_sleep = args.time_sleep
        after_lines = args.after_lines
    else:
        from_src = args.get("trans_src", '')
        trans_to = args.get("trans_to", 'ru')
        sleep = args.get("sleep", False)   
        time_sleep = args.get("time_sleep", 3)
        after_lines = args.get("after_lines", 100)        

    if not os.path.exists(os.path.join(path_complete, last_folder)):
        os.mkdir(os.path.join(path_complete, last_folder))
        
    path_complete = os.path.join(path_complete, last_folder) 
    
    srt_files = list(filter(lambda f: os.path.isfile(os.path.join(path_process,f)) and f.endswith('.srt'), os.listdir(path_process)))
    srt_len = len(srt_files)

    
    print(f"Файлов с субтитрами найдено: {srt_len}")
    complete_files = 0
    for k_file, file in enumerate(srt_files):
        ext_start = file.rfind('.')
        new_name_ = f"{file[:ext_start]}_{trans_to}{file[ext_start:]}"
        new_name_ = os.path.join(path_complete, new_name_)
        fh, abs_path = mkstemp()

        with os.fdopen(fh, 'w', encoding='utf-8') as new_file:
            open_file = os.path.join(path_process, file)
            with open(open_file, 'r+', encoding='utf-8') as f_old:
                lines = f_old.readlines()
                len_lines = len(lines)

                if not len_lines:
                    print(f"Файл '{open_file}' пустой и не имеет данных!\n")
                    continue
                prog = 0
                step = 100 / len(lines)

                for k, line in enumerate(lines):
                    line_ = line.rstrip('\n')                  

                    if not regx.search(line_) and len(line_) != 0:
                        if from_src:
                            trans = translator.translate(line_, src=from_src, dest=trans_to)
                        else:
                            trans = translator.translate(line_, dest=trans_to)
                        new_file.write(line.replace(line, trans.text + '\n'))
                    else:
                        new_file.write(line)

                    if sleep and len_lines > after_lines and k!=0 and k % after_lines == 0:
                        time.sleep(time_sleep)
                        
                    prog += step
                    print_out = 'Обработка файла "' + file + '" : ({0:1.1f}%) [Файл: {1} из {2}] [Lines: {3}]'.format(prog, k_file+1, srt_len, len_lines)
                    print(print_out, end='\r', flush=True)  

        shutil.move(abs_path, new_name_)
        complete_files += 1
        
        if(k_file == (srt_len-1)):
            print(f'\nПереведено файлов {complete_files} из {srt_len}!\n')


def check_lang(to='ru', default=''):
    """Check support languages to translate"""
    if to == '':
        to = default
    return to in LANGUAGES.keys()


def check_exists_folders():
    """Check exists folders"""
    for d in ['complete', 'process']:
        dir_name = os.path.join(os.path.dirname(__file__), d)
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)


def main():
    """Main function"""
    cin = ''
    while cin != 'e':
        print(f'''{" Перевод субтитров ".center(30, "*")}
t -> начать перевод субтитров
la -> список языков
-----------
e -> завершить работу
''')
        cin = input('Введите: ')

        if cin == 't':
            check_exists_folders()
            trans_src = input('С какого языка переводить (пустой ответ опред. автомвтически)?: ')
            trans_to = input('На какой язык перевести?: ')
            sleep = False

            path_proccess = os.path.join(os.path.dirname(__file__), 'process')

            if input("Включить задержку?: ") in ('yes','y','1'):
                sleep = True
            
            if input("Укажить путь к srt файлам?: ") in ('yes','y','1'):
                path_proccess = input("Введите путь: ")

            if check_lang(trans_to, 'ru'):
                if not check_lang(trans_src, ''):
                    trans_src = ''

                trans_params = {
                    "trans_src": trans_src,
                    "trans_to": trans_to,
                    "sleep": sleep
                    }

                for root, dirs_, files in os.walk(path_proccess):
                    for d in dirs_:
                        path_ = os.path.join(root, d)
                        print(f"Обрабатываю файлы в папке: {d}")
                        translate_subtitles(path_, trans_params)
                        
                    print(f"Обрабатываю файлы в папке: {os.path.basename(root)}")                
                    translate_subtitles(root, trans_params)                        
            else:
                print('Язык указан неверно используйте команду "la", для определения языка!')

        if cin == 'la':
            print('\n'.join([f"{s.capitalize()} -> {n}" for n, s in LANGUAGES.items()]))

def no_cli(args):  
    path_proccess = os.path.join(os.path.dirname(__file__), 'process')

    if 'la' in args and args.la:
        print('Поддерживаемые языки:')
        print(f'{"Название":<20}{"Значение":>20}')
        print('\n'.join([f"{s.capitalize():<20}{n: >20}" for n, s in LANGUAGES.items()]))
        print()

    if 'path_proccess' in args and args.path_proccess:
        path_proccess = args.path_proccess
        
    if check_lang(args.trans_to, 'ru'):
        if not check_lang(args.trans_src, ''):
            args.trans_src = ''

        for root, dirs_, files in os.walk(path_proccess):
            for d in dirs_:
                path_ = os.path.join(root, d)
                print(f"Обрабатываю файлы в папке: {d}")
                translate_subtitles(path_, args)
                
            print(f"Обрабатываю файлы в папке: {os.path.basename(root)}")                
            translate_subtitles(root, args)
    else:
        print('Язык указан неверно используйте команду "--la", для определения языка!')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate subtitles')
    parser.add_argument("--cli", action=argparse.BooleanOptionalAction, help="Use interface")
    parser.add_argument("--tS", dest="trans_src", default="", type=str, help="Source language (empty detect language auto)")
    parser.add_argument("--tT", dest="trans_to", default="ru", type=str, help="Translate to language")
    parser.add_argument("--la", action=argparse.BooleanOptionalAction, help="List support languages")
    parser.add_argument("--p", dest="path_proccess", help="Path to srt files", type=str)
    parser.add_argument("--sleep", action=argparse.BooleanOptionalAction, help="Enable sleep")
    parser.add_argument("--st", dest="time_sleep", help="Sleep time in seconds", default=3, type=int)
    parser.add_argument("--al", dest="after_lines", help="Sleep program after line", default=100, type=int)
    
    args = parser.parse_args()

    if 'cli' in args and args.cli:
        main()
    else:
        no_cli(args)
