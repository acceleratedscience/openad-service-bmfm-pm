# Environment variables to point wrapper code to
# public-readable s3 bucket: s3://ad-prod-biomed
#
# Uses: Source (.-run) before running model-hosting api, implementation.py
#   $ # conda activate dti-sol  # Activate your python 3.10 env
#   $ . env.sh && python implementation.py
export GT4SD_S3_HOST=s3.us-east-1.amazonaws.com
export GT4SD_S3_ACCESS_KEY=None
export GT4SD_S3_SECRET_KEY=None
export GT4SD_S3_HOST_HUB=s3.us-east-1.amazonaws.com
export GT4SD_S3_ACCESS_KEY_HUB=None
export GT4SD_S3_SECRET_KEY_HUB=None
export gt4sd_s3_bucket_algorithms="ad-prod-biomed"
export gt4sd_s3_bucket_properties="ad-prod-biomed"
export gt4sd_s3_bucket_hub_algorithms="ad-prod-biomed"
export gt4sd_s3_bucket_hub_properties="ad-prod-biomed"
