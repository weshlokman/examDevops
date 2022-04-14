import boto3
import psycopg2
import os
from dotenv import load_dotenv

# Connect to AWS S3
s3 = boto3.resource(
    service_name='s3',
    region_name='ca-central-1',
    aws_access_key_id= os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key= os.getenv('AWS_SECRET_KEY')
)


# Print out bucket names
for obj in s3.Bucket('devoptest').objects.all():
    print(obj)

# Download the file from S3
def download_from_s3():
    """
    Upload a file to an AWS S3 bucket.
    """
    try:
        s3.meta.client.download_file('devoptest', 'my.pgsql','tmp/test.pgsql')
    except Exception as e:
        print(e)
        exit(1)

download_from_s3()

# Connect to AWS RDS
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    dbname = "exam",
    password="exam123")

print(conn)
cur = conn.cursor()

# Read in the file
with open('tmp/test.pgsql','rt',encoding="utf8") as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace("\\","") 

# Write the file out again
with open('file.pqsql', 'w',encoding="utf8" ) as file:
  file.write(filedata)

# Read in the file and execute the SQL commands
with open('file.pqsql','rt',encoding="utf8") as file :
  filedata = file.read()
  cur.execute(filedata)
  conn.commit()
  conn.close()
