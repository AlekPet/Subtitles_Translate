#!python3
# Author: AlekPet


import os
from tempfile import mkstemp
import shutil
import re
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


# copy_(True)
def translate_subtitles(path=os.path.dirname(__file__), from_src='', to='ru'):
    """Function Translate subtitles"""
    path_process = os.path.join(path, 'process')
    path_complete = os.path.join(path, 'complete')
    srt_files = list(filter(lambda f: os.path.isfile(os.path.join(path_process,f)) and f.endswith('.srt'), os.listdir(path_process)))
    srt_len = len(srt_files)

    print(f"Файлов с субтитрами найдено: {srt_len}")
    for k_file, file in enumerate(srt_files):
        ext_start = file.rfind('.')
        new_name_ = f"{file[:ext_start]}_{to}{file[ext_start:]}"
        new_name_ = os.path.join(path_complete, new_name_)
        fh, abs_path = mkstemp()

        with os.fdopen(fh, 'w', encoding='utf-8') as new_file:

            with open(os.path.join(path_process, file), 'r+', encoding='utf-8') as f_old:
                lines = f_old.readlines()
                prog = 0
                step = 100 / len(lines)

                for k, line in enumerate(lines):
                    line_ = line.rstrip('\n')

                    print('\rОбработка файла "' + file + '" : ({0:1.1f}%) [Файл: {1} из {2}]'.format(prog, k_file+1, srt_len), end='', flush=True)

                    if not regx.search(line_) and len(line_) != 0:
                        if from_src:
                            trans = translator.translate(line_, src=from_src, dest=to)
                        else:
                            trans = translator.translate(line_, dest=to)
                        new_file.write(line.replace(line, trans.text + '\n'))
                    else:
                        new_file.write(line)

                    prog += step

        shutil.move(abs_path, new_name_)
    print('\nПеревод завершен!')


def check_lang(to='ru'):
    """Check support languages to translate"""
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
        print('''
Перевод субтитров:
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
            if check_lang(trans_to):
                if not check_lang(trans_src):
                    trans_src = ''

                translate_subtitles(os.path.join(os.path.dirname(__file__)), trans_src, trans_to)
            else:
                print('Язык указан неверно используйте команду "la", для определения языка!')

        if cin == 'la':
            print('\n'.join([f"{s.capitalize()} -> {n}" for n, s in LANGUAGES.items()]))


if __name__ == '__main__':
    main()
