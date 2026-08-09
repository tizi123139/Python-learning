import alibabacloud_oss_v2 as oss
from fastapi import APIRouter
from datetime import timedelta
from alibabacloud_oss_v2 import credentials
router = APIRouter()

cfg = oss.config.load_default()

cred = credentials.StaticCredentialsProvider(
    access_key_id="",
    access_key_secret=""
)
cfg.credentials_provider = cred

cfg.region = "cn-beijing"
client = oss.Client(cfg)

# OSS 域名配置
OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'
OSS_BUCKET = 'java-ai123456hhhh'


@router.get("/oss/presign")
def chat_endpoint(filename: str):
    # 根据文件扩展名判断 Content-Type
    content_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
    }
    ext = filename.split(".")[-1].lower() if "." in filename else "jpg"
    content_type = content_type_map.get(ext, "application/octet-stream")

    pre_result = client.presign(oss.PutObjectRequest(
        bucket=OSS_BUCKET,
        key=filename,
        content_type=content_type,
    ), expires=timedelta(seconds=3600))

    # 返回上传 URL 和可访问的图片路径
    return {
        "uploadUrl": pre_result.url.strip('"'),
        "contentType": content_type,
        "accessUrl": f"https://{OSS_BUCKET}.{OSS_ENDPOINT}/{filename}"
    }
