import boto3
from botocore.exceptions import NoCredentialsError
import pyqrcode,io,qrcode

ACCESS_KEY = 'AKIA3R6YNNJFEWCZNPNK'
SECRET_KEY = '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'


def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    try:
        s3.upload_file(local_file, bucket, s3_file)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

a = "12345"
x = a + ".png"
qr = pyqrcode.create(a)
qr.png(x, scale=8)
#z=Image.open("12345.png")
uploaded = upload_to_aws('12345.png', 'efarm-bucket', '12345.png')