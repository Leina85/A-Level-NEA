import os
import boto3
from botocore import UNSIGNED
from botocore.config import Config

# File name
sequencing_summary = r"C:\<redacted_path>\NEA\sequencing_summary_PAG07165_2dfda515.txt"

# Only download if the file does not exist
if not os.path.exists(sequencing_summary):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED), region_name='eu-west-1')

    # S3 parameters
    bucket_name = 'ont-open-data'
    s3_key = 'gm24385_2020.11/flowcells/20201026_1645_6B_PAG07165_d42912aa/sequencing_summary_PAG07165_2dfda515.txt'

    # Download file
    s3.download_file(Bucket='ont-open-data', Key='gm24385_2020.11/flowcells/20201026_1645_6B_PAG07165_d42912aa/sequencing_summary_PAG07165_2dfda515.txt', Filename=sequencing_summary)
