import os, shutil
def copy_files_recursive(src, dst):
    os.makedirs(dst, exist_ok=True)
    entries = os.listdir(src)
    for entry in entries:
       src_path = os.path.join(src, entry)
       dst_path = os.path.join(dst, entry)
       if os.path.isfile(src_path, dst_path):
           shutil.copy(src_path, dst)
       elif os.path.isdir(src_path):
           copy_files_recursive(src_path, dst_path)
    