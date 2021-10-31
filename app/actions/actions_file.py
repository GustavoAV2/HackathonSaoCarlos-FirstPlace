import os
import time
import random
from settings import FILE_UPLOAD
from werkzeug.utils import secure_filename


def save_file(file, filename: str) -> str:
    if file:
        upload_folder = os.path.join(os.getcwd(), f'{FILE_UPLOAD}{filename}')
        try:
            os.mkdir(upload_folder)
            time.sleep(0.2)
        except (FileExistsError, FileNotFoundError):
            pass
        save_path: str = os.path.join(upload_folder, secure_filename(file.filename))
        try:
            if os.path.isfile(save_path):
                random_number: int = random.randint(0, 1000)
                save_path_rename: str = save_path[:-4] + str(random_number) + save_path[-4:]
                file.save(save_path_rename)
            file.save(save_path)

        except (FileExistsError, FileNotFoundError):
            pass

        file_path = upload_folder[-43:] + "\\" + file.filename
        return file_path
    return ''
