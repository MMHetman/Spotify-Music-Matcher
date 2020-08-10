from google.cloud import storage


def upload_file_to_bucket(file, bucket_filename, bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(bucket_filename)
    blob.upload_from_filename(file)
