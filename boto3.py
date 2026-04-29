import boto3
import json
import os

# 🔹 CONFIG
BUCKET_NAME = "mayur-static-site-12345667"  # must be unique
REGION = "ap-south-1"
WEBSITE_FOLDER = "./"  # current folder

s3 = boto3.client("s3", region_name=REGION)

# 🔹 1. Create Bucket
def create_bucket():
    print("Creating bucket...")
    s3.create_bucket(
        Bucket=BUCKET_NAME,
        CreateBucketConfiguration={'LocationConstraint': REGION}
    )
    print("✅ Bucket created")

# 🔹 2. Enable Static Website Hosting
def enable_website():
    print("Enabling static hosting...")
    s3.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            'IndexDocument': {'Suffix': 'index.html'}
        }
    )
    print("✅ Website hosting enabled")



# 🔹 4. Upload Files
def upload_files():
    print("Uploading files...")
    for file in os.listdir(WEBSITE_FOLDER):
        if file.endswith((".html", ".css", ".js")):
            s3.upload_file(
                file,
                BUCKET_NAME,
                file,
                ExtraArgs={'ContentType': get_content_type(file)}
            )
            print(f"Uploaded: {file}")
    print("✅ Upload complete")

# 🔹 Helper: Content Type
def get_content_type(filename):
    if filename.endswith(".html"):
        return "text/html"
    elif filename.endswith(".css"):
        return "text/css"
    elif filename.endswith(".js"):
        return "application/javascript"
    return "binary/octet-stream"

# 🔹 MAIN
create_bucket()
enable_website()

upload_files()

print(f"\n🌍 Website URL:")
print(f"http://{BUCKET_NAME}.s3-website-{REGION}.amazonaws.com")
