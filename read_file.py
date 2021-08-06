import os


def read_file(file_path):
    os.chdir(file_path)
    all_file = os.listdir()
    files = []
    for f in all_file:
        if os.path.isdir(f):
            files.extend(read_file(file_path + '\\' + f))
            os.chdir(file_path)
        else:
            files.append(str(f))
    return files


if __name__ == '__main__':
    list_name = read_file("C:\\Users\\wz\\Documents\\apk\\cardpool_new")
    strs = ""
    for name in list_name:
        strs = strs  +"'" +name + "',"
    print(strs)