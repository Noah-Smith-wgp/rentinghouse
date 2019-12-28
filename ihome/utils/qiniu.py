from qiniu import Auth, put_data
from django.conf import settings
import logging

log = logging.getLogger('django')


def qiniu_upload(data):
    """七牛云存储上传文件"""
    if not data:
        return None
    try:
        # 创建对象
        q = Auth(access_key=settings.QINIU_ACCESS_KEY, secret_key=settings.QINIU_SECRET_KEY)

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(settings.QINIU_BUCKET_NAME)
        print(token)

        # 上传文件
        ret, info = put_data(token, None, data)
    except Exception as e:
        log.error(e)
    else:
        if info and info.status_code != 200:
            print(info)
            raise Exception("上传文件到七牛失败")

        # 返回七牛中保存的图片名，这个图片名也是访问七牛获取图片的路径
        key = ret['key']
        print(key)
        return key


if __name__ == '__main__':
    file_name = input("输入上传的文件")
    with open(file_name, "rb") as f:
        qiniu_upload(f.read())
