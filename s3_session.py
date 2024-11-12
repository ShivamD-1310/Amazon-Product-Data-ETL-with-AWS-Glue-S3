import boto3
from resource import credentials


def get_client():
    print('Making S3 session')
    return boto3.client('s3',
                        aws_access_key_id=credentials.access_key,
                        aws_secret_access_key=credentials.secret_key)

def load_into_s3(Bucket,Key,Body):
    try:
        s3_client = get_client()
        upload_data = s3_client.put_object(Bucket = Bucket,
                                        Key=Key,
                                        Body=Body)
        print(f"Data Uploaded to the bucket {credentials.bucket}")
    except:
        print(f"Not able to upload data to {credentials.bucket}"  )
