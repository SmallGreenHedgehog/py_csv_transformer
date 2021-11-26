from os import getcwd, listdir
from os.path import abspath

from transformers import LeadConvToRingerDogCSVFileTransformer


def get_paths_of_files_in_source_folder() -> tuple:
    """Возвращает перечень csv в src директории"""
    source_dir_path = abspath(getcwd() + '/source_csv_files')
    files_in_src_dir = filter(lambda f: f.endswith('csv'), listdir(source_dir_path))
    return tuple(f'{source_dir_path}/{cur_file}' for cur_file in files_in_src_dir)


if __name__ == '__main__':
    try:
        dst_dir_path = abspath(getcwd() + '/result_csv_files')
        NeededTransformer = LeadConvToRingerDogCSVFileTransformer

        for cur_file_path in get_paths_of_files_in_source_folder():
            NeededTransformer(
                src_file_path=cur_file_path,
                dst_dir_path=dst_dir_path,
                reusable_field_names_tuple=(
                    'first_name', 'last_name', 'channel_name',
                    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'
                ),
            ).extract_data_to_result_file()

    except Exception as e:
        print(f'Ошибка выполнения обработки конвертации: {e}')
