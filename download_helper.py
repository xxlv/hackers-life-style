#!/usr/bin/python3

from urllib.request import urlopen

import hashlib

DOWNLOAD_CACHE_DIR='~/Download/.download_helper'

"""
    简单下载工具
    暂时支持断点续传和缓存
"""

def download(url,path='.'):


    _is_valid_url(url)

    file_hash=hashlib.md5(url.encode('utf-8')).hexdigest()

    print("File hash is {}".format(file_hash))


    _download_file(url,path)
    # download from url
    data=urlopen(url)





def _download_file(url,target):

    file_name = url.split('/')[-1]
    u = urlopen(url)
    meta = u.info()
    file_size = int(meta.get_all('Content-Length')[0])
    file_hash=hashlib.md5(url.encode('utf-8')).hexdigest()
    cache_target="{}/{}/{}".format(DOWNLOAD_CACHE_DIR,file_hash,target)
    cache_target_INFO="{}/{}/{}".format(DOWNLOAD_CACHE_DIR,file_hash,"INFO")

    file_size_dl = _load_cache_INFO(cache_target_INFO)

    if file_size_dl == file_size:
        print("Load from cache")
        _copyfile(cache_target,target)
        exit(0)

    block_sz = 8192

    f = open(cache_target, 'wb')
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        _update_cache_INFO(file_size_dl)
        print(status)

    f.close()
    _copyfile(cache_target,target)

def _copyfile(src,target):
    return sutill.copefile(src,target)



def _update_cache_INFO(cache_target_INFO,offset):

    with open(cache_target,'w+') as f:
        f.write(offset)

def _load_cache_INFO(cache_target_INFO):

    with open(cache_target,'r') as f:
        INFO=f.read()
    return INFO



def _is_local_url(url):
    return

def _is_valid_url(url):

    # TODO
    return True


if __name__=='__main__':

    download('http://www.baidu.com','./http.d')
