import urllib.request
import os
import logging
import datetime
import tarfile
import sys
import shutil
import hashlib

logging.basicConfig(filename="downloader.log",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logger = logging.getLogger('dl')
logger.addHandler(logging.StreamHandler(sys.stdout))

def get_latest_url():
    today = datetime.datetime.today()
    while True:
        url = "http://47.74.159.117/saveInternalTx/backup" + today.strftime("%Y%m%d")
        try:
            # 404 or 200
            urllib.request.urlopen(url)
            return url
        except urllib.error.HTTPError:
            logger.debug("404 for " + url)
            today = today - datetime.timedelta(days=1)
        except Exception as e:
            raise e

def get_latest_md5(folder_url):
    url = folder_url + "/FullNode_output-directory.tgz.md5sum"
    resp = urllib.request.urlopen(url)
    body = resp.read().decode("utf8")
    return body.split(" ")[0]

prev_reported_download_percent = None

def download_hook(count, block_size, total_size):
    global prev_reported_download_percent
    percent = int(count*block_size*100/total_size)
    if prev_reported_download_percent != percent:
        if percent % 5 == 0:
            sys.stdout.write('%s%%' % percent)
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
        prev_reported_download_percent = percent

def download_tgz(folder_url):
    tgz_url = folder_url + "/FullNode_output-directory.tgz"
    logger.warning("start downloading " + tgz_url)
    urllib.request.urlretrieve(tgz_url, "FullNode_output-directory.tgz", reporthook=download_hook)
    logger.warning("sdownloaded")

def uncompress_tgz(md5=None):
    block_size=1<<20
    if md5 is not None:
        hasher = hashlib.md5()
        with open("FullNode_output-directory.tgz", "rb") as f:
            while True:
                data = f.read(block_size)
                if not data:
                    break
                hasher.update(data)
        hash = hasher.hexdigest()
        if hash != md5:
            logger.error("stop uncompression: md5 not matching! "+ hash + " != " + md5)
            return

    with tarfile.open("FullNode_output-directory.tgz") as f:
        logger.warning("start uncompressing")
        f.extractall(".")
    logger.warning("uncompressed output-directory")

def download_jar():
    logger.warning("start downloading FullNode.jar")
    urllib.request.urlretrieve("https://github.com/tronprotocol/java-tron/releases/latest/download/FullNode.jar", "FullNode.jar", reporthook=download_hook)
    logger.warning("sdownloaded")

if __name__=='__main__':
    logger.info("downloader starting")
    if not os.path.exists("FullNode.jar"):
        logger.warning("FullNode not exists")
        download_jar()

    if not os.path.exists("output-directory"):
        logger.warning("output-directory not exists")

        md5 = None
        if os.path.exists("FullNode_output-directory.tgz"):
            logger.warning("FullNode_output-directory.tgz already exists, start uncompressing")
        else:
            url = get_latest_url()
            download_tgz(url)
            md5 = get_latest_md5(url)
        uncompress_tgz(md5)
    logger.warning("everything done, exit downloader")
