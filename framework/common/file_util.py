import os
from common.path_util import DATA_DIR

class FileUtil:

    # BASE_DIR = os.path.abspath(__file__)
    # ROOT_DIR = os.path.dirname(BASE_DIR)
    # FILE_DIR = os.path.join(ROOT_DIR, 'file')

    @staticmethod
    def get_file_stream(file_name, mime_type=None):
        file_path = os.path.join(DATA_DIR, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f'上传文件不存在：{file_path}')

        # requests库上传文件需要文件名、文件二进制数据、文件类型，application/octet-stream为通用二进制流，所有文件都能用
        return (
            file_name,
            open(file_path, 'rb'),
            mime_type or "application/octet-stream"
        )
