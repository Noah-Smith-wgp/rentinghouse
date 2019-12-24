from qiniu import Auth, put_data
from django.conf import settings


def qiniu_upload(data):
    # pic = request.FILES.get('pic')
    # data = pic.read()
    q = Auth(access_key=settings.QINIU_ACCESS_KEY, secret_key=settings.QINIU_SECRET_KEY)

    token = q.upload_token(settings.QINIU_BUCKET_NAME)
    print(token)

    ret, info = put_data(token, None, data)
    key = ret['key']
    print(key)
    return key


if __name__ == '__main__':
    file_name = input("输入上传的文件")
    with open(file_name, "rb") as f:
        qiniu_upload(f.read())
