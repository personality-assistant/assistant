import os
import shutil


def check_dir(path):
    types = (
        ['.svg', '.jpeg', '.png', '.jpg'],
        ['.avi', '.mp4', '.mov', '.mkv'],
        ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
        ['.mp3', '.ogg', '.wav', '.amr'],
        ['.zip', '.gz', '.tar']
    )
    for i in os.listdir(path):
        main_dir = (
            'Pictures', 'Video', 'Documents', 'Music', 'Archives', 'Other',
        )
        if os.path.isdir(path + '/' + i):
            if i not in main_dir:
                print(f'Спускаемся в {path}/{i}')
                check_dir(path + '/' + i)
                try:
                    os.rmdir(f'{path}/{i}')
                    print(f'Папка {path}/{i} удалена')
                except OSError as e:
                    print(f'Error: {i} : {e}')
                print(f'Возвращаемся в {path}')
            else:
                continue
        elif os.path.isfile(path + '/' + i):
            file = os.path.basename(i)
            file_name = normalize(os.path.splitext(file)[0])
            file_type = os.path.splitext(file)[1]
            print(f'{file_name+file_type}')

            try:
                if file_type.lower() in types[0]:
                    os.replace(path + '/' + i, f'test/Pictures/{file_name+file_type}')
                elif file_type.lower() in types[1]:
                    os.replace(path + '/' + i, f'test/Video/{file_name+file_type}')
                elif file_type.lower() in types[2]:
                    os.replace(path + '/' + i, f'test/Documents/{file_name+file_type}')
                elif file_type.lower() in types[3]:
                    os.replace(path+'/'+i, f'test/Music/{file_name+file_type}')
                elif file_type.lower() in types[4]:
                    shutil.unpack_archive(path+'/'+i, f'test/Archives/{file_name}')
                    os.remove(path+'/'+i)
            except Exception:
                print(f'Что-то пошло не так...')
                continue


def normalize(string):
    dict_map = {
        ord('А'): 'A', ord('Б'): 'B', ord('В'): 'V', ord('Г'): 'H', ord('Ґ'): 'G', ord('Д'): 'D', ord('Е'): 'E',
        ord('Є'): 'Ye', ord('Ж'): 'Zh', ord('З'): 'Z', ord('И'): 'Y', ord('І'): 'I', ord('Ї'): 'Yi', ord('Й'): 'Y',
        ord('К'): 'K', ord('Л'): 'L', ord('М'): 'M', ord('Н'): 'N', ord('О'): 'O', ord('П'): 'P', ord('Р'): 'R',
        ord('С'): 'S', ord('Т'): 'T', ord('У'): 'U', ord('Ф'): 'F', ord('Х'): 'Kh', ord('Ц'): 'Ts', ord('Ч'): 'Ch',
        ord('Ш'): 'Sh', ord('Щ'): 'Shch', ord('Ю'): 'Yu', ord('Я'): 'Ya', ord('а'): 'a', ord('б'): 'b', ord('в'): 'v',
        ord('г'): 'h', ord('ґ'): 'g', ord('д'): 'd', ord('е'): 'e', ord('є'): 'ie', ord('ж'): 'zh', ord('з'): 'z',
        ord('и'): 'y', ord('і'): 'i', ord('ї'): 'i', ord('й'): 'i', ord('к'): 'k', ord('л'): 'l', ord('м'): 'm',
        ord('н'): 'n', ord('о'): 'o', ord('п'): 'p', ord('р'): 'r', ord('с'): 's', ord('т'): 't', ord('у'): 'u',
        ord('ф'): 'f', ord('х'): 'kh', ord('ц'): 'ts', ord('ч'): 'ch', ord('ш'): 'sh', ord('щ'): 'shch', ord('ю'): 'iu',
        ord('я'): 'ia', ord('ь'): ''
                }
    symbols = ' ,./\\!@#$%^&*()-=`~:"{}|[];\'>?<№'

    new_string = string.translate(dict_map)
    for char in new_string:
        if char in symbols:
            new_string = new_string.replace(char, '_')

    return new_string



check_dir('test')
