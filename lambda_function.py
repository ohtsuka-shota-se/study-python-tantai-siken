# lambda_function.py
import boto3

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    bucket = event.get("bucket")
    key = event.get("key")

    if not bucket or not key:
        return {"statusCode": 400, "body": "bucket/key is required"}

    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        body = obj["Body"].read().decode("utf-8")
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}

    return {"statusCode": 200, "body": body}