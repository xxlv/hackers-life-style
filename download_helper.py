#!/usr/bin/python3

from urllib.request import urlopen
import hashlib
import os
from os.path import expanduser

HOME = expanduser("~")
DOWNLOAD_CACHE_DIR='{}/Downloads/downloadHelper'.format(HOME)
BLOCK_SIZE=1024

"""
    简单下载工具
    暂时支持断点续传和缓存
"""

def download(url,path='.'):
    _download_file(url,path)


def _download_file(url,target):

    if not _is_valid_url(url):
        exit(-1)

    file_name = url.split('/')[-1]
    u = urlopen(url)
    meta = u.info()

    if(meta.get_all('Content-Length')):
        file_size = int(meta.get_all('Content-Length')[0])
    else:
        file_size=0

    if file_size <=0:
        print("file size <= 0")
        exit(-1)

    print("file size is {}".format(file_size))

    file_hash=hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_target="{}/{}".format(DOWNLOAD_CACHE_DIR,file_hash)
    cache_target_INFO="{}/{}/{}".format(DOWNLOAD_CACHE_DIR,file_hash,"INFO")
    cache_target_FILE="{}/{}".format(cache_target,"{}.data".format(file_hash))
    _init_cache_INFO_ENV(cache_target,cache_target_INFO)

    file_size_dl = int(_load_cache_INFO(cache_target_INFO))

    if(file_size_dl >0 and file_size_dl < file_size):
        print("从 {} 开始继续下载".format(file_size_dl))

    if(file_size_dl > file_size):
        _update_cache_INFO(cache_target_INFO,0)
        file_size_dl=0
    if(file_size_dl == file_size):
        print("Load from cache ")

    if  file_size_dl < file_size:
        block_sz = BLOCK_SIZE
        f = open(cache_target_FILE, 'wb')

        while True:
            buffer =u.read(block_sz)
            if not buffer:
                break
            file_size_dl += len(buffer)
            f.write(buffer)
            _update_cache_INFO(cache_target_INFO,file_size_dl)
            _print_process(file_size_dl,file_size)
        f.close()
    else:
        pass

    _fast_copyfile(cache_target_FILE,target)

def _fast_copyfile(src,target):
    print("CP file from {} to {}".format(src,target))
    # TODO fast cp here
    if os.path.isfile(target):
        print("File {} exists ".format(target))
        exit(-1)

    cp_shell="""
        cp {} {}
    """.format(src,target)
    os.system(cp_shell)





def _print_process(file_size_dl,file_size):

    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status + chr(8)*(len(status)+1)
    print(status)


def _init_cache_INFO_ENV(cache_target,cache_target_INFO):

    if not os.path.exists(cache_target):
        os.makedirs(cache_target)
        print("Create dir {}".format(cache_target))

    if not os.path.isfile(cache_target_INFO):
        open(cache_target_INFO,'w+').close()
        print("Create file {}".format(cache_target_INFO))


    return True

def _update_cache_INFO(cache_target_INFO,offset):
    with open(cache_target_INFO,'w+') as f:
        f.write(str(offset))

def _load_cache_INFO(cache_target_INFO):
    with open(cache_target_INFO,'r') as f:
        offset=f.read()
    if not offset:
        offset=0
    else:
        offset=int(offset)

    return offset

def _is_local_url(url):
    # TODO
    return True

def _is_valid_url(url):
    # TODO
    return True


# MAIN
if __name__=='__main__':

    download('https://github.com/xxlv/hackers-life-style/archive/master.zip','master.zip')
