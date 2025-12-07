import os, shutil
def copy_recursive(src, dst):
    entries = os.listdir(src)
    for entry in entries:
       src_path = os.path.join(src, entry)
       if os.path.isfile(src_path):
           shutil.copy(src_path, dst)
       elif os.path.isdir(src_path):
           dst_path = os.path.join(dst, entry)
           os.mkdir(dst_path)
           copy_recursive(src_path, dst_path)
    