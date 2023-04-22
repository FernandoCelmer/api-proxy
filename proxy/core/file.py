"""
Module File
"""

from json import dumps


class File:

    @classmethod
    def write(
            cls,
            content: str,
            path_file: str,
            mode: str = 'w',
            dump: bool = True,
            jump: bool = True,
            encoding: str = 'utf8') -> None:
        content = dumps(content, indent=4) if dump else content
        content = f"{content}\n" if jump else content
        try:
            with open(file=path_file, mode=mode, encoding=encoding) as outfile:
                outfile.write(content)
        except PermissionError:
            cls.write_system(content=content, path_file=path_file, mode=mode)

        except Exception as error:
            raise Exception(error)

    @classmethod
    def read(
            cls,
            path_file: str,
            mode: str = 'r',
            encoding: str = 'utf8') -> str:
        try:
            with open(file=path_file, mode=mode, encoding=encoding) as content:
                return content.read()
        except FileNotFoundError:
            cls.touch(path=path_file)
            return cls.read(path_file=path_file, mode=mode, encoding=encoding)

        except Exception as error:
            raise Exception(error)

    @classmethod
    def touch(cls, path: str):
        try:
            cls.write(path_file=path, content="\n", dump=False, jump=False)
        except Exception as error:
            raise Exception(error)
