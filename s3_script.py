import os
import json
import boto3
import argparse
from botocore.exceptions import ClientError

class S3Helper:
    def __init__(self, config_file):
        with open(config_file) as f:
            config = json.load(f)
        self.access_key = config["access_key"]
        self.secret_key = config["secret_key"]
        self.bucket_name = config["bucket_name"]
        self.s3 = boto3.client('s3', aws_access_key_id=self.access_key, aws_secret_access_key=self.secret_key)

    def upload_directory(self, local_directory, s3_directory):
        for root, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, local_directory)
                s3_path = os.path.join(s3_directory, relative_path)
                try:
                    self.s3.upload_file(local_path, self.bucket_name, s3_path)
                    print(f"Uploaded {local_path} to {s3_path}")
                except ClientError as e:
                    print(f"Unable to upload {local_path} to {s3_path}: {e}")

    def delete_folder(self, s3_directory):
        objects_to_delete = []
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_directory)
            for obj in response.get('Contents', []):
                objects_to_delete.append({'Key': obj['Key']})
            if objects_to_delete:
                self.s3.delete_objects(Bucket=self.bucket_name, Delete={'Objects': objects_to_delete})
                print(f"Deleted folder {s3_directory}")
            else:
                print(f"No objects found in folder {s3_directory}")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def copy_s3_to_s3(self, source_directory, destination_directory):
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=source_directory)
            for obj in response.get('Contents', []):
                source_key = obj['Key']
                destination_key = source_key.replace(source_directory, destination_directory)
                self.s3.copy_object(CopySource={'Bucket': self.bucket_name, 'Key': source_key},
                                    Bucket=self.bucket_name, Key=destination_key)
                print(f"Successfully copied {source_key} to {destination_key}")
        except ClientError as e:
            print(f"An error occurred: {e}")

    def create_folder(self, s3_path):
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=(s3_path + '/'))
            print(f"Created folder {s3_path}")
        except ClientError as e:
            print(f"An error occurred: {e}")
    
    def download_folder(self, s3_directory, local_directory):
        try:
            os.makedirs(local_directory, exist_ok=True)  # Create local directory if it doesn't exist
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_directory)

            for obj in response.get('Contents', []):
                s3_key = obj['Key']
                local_path = os.path.join(local_directory, os.path.relpath(s3_key, s3_directory))

                # Create local directory if it doesn't exist
                local_dir = os.path.dirname(local_path)
                if not os.path.exists(local_dir):
                    os.makedirs(local_dir)

                if not obj['Key'].endswith('/'):
                    try:
                        self.s3.download_file(self.bucket_name, s3_key, local_path)
                        print(f"Downloaded {s3_key} to {local_path}")
                    except OSError as e:
                        print(f"Error downloading {s3_key}: {e}")
                        continue

            for subdir in response.get('CommonPrefixes', []):
                subdir_path = subdir['Prefix']
                subdir_name = os.path.basename(subdir_path.rstrip('/'))
                self.download_folder(subdir_path, os.path.join(local_directory, subdir_name))

        except ClientError as e:
            print(f"An error occurred: {e}")

    def list_s3_contents(self, output_file="s3_tree.txt"):
        def list_objects(s3_path, depth):
            prefix = "" if depth == 0 else "|  " * (depth - 1) + "|--"
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=s3_path, Delimiter='/')
            for obj in response.get('Contents', []):
                print(prefix + obj['Key'].split('/')[-1])
                with open(output_file, "a") as f:
                    f.write(prefix + obj['Key'].split('/')[-1] + '\n')
            for subdir in response.get('CommonPrefixes', []):
                subdir_name = subdir['Prefix'].split('/')[-2]
                print(prefix + subdir_name)
                with open(output_file, "a") as f:
                    f.write(prefix + subdir_name + '\n')
                list_objects(subdir['Prefix'], depth + 1)

        list_objects("", 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='S3 Helper Tool')
    parser.add_argument('action', choices=['upload', 'delete', 'copy', 'create', 'download', 'list'], help='Action to perform')
    parser.add_argument('--local-dir', help='Local directory path')
    parser.add_argument('--s3-dir', help='S3 directory path')
    parser.add_argument('--source-dir', help='Source directory path in S3')
    parser.add_argument('--destination-dir', help='Destination directory path in S3')
    parser.add_argument('--s3-folder', help='S3 folder path')
    parser.add_argument('--local-download-dir', help='Local directory path for download')
    parser.add_argument('--config-file', default='config.json', help='Path to the config JSON file')

    args = parser.parse_args()

    s3_helper = S3Helper(args.config_file)

    if args.action == 'upload':
        if args.local_dir and args.s3_dir:
            s3_helper.upload_directory(args.local_dir, args.s3_dir)
        else:
            print("Both --local-dir and --s3-dir are required for upload action.")
    elif args.action == 'delete':
        if args.s3_dir:
            s3_helper.delete_folder(args.s3_dir)
        else:
            print("--s3-dir is required for delete action.")
    elif args.action == 'copy':
        if args.source_dir and args.destination_dir:
            s3_helper.copy_s3_to_s3(args.source_dir, args.destination_dir)
        else:
            print("Both --source-dir and --destination-dir are required for copy action.")
    elif args.action == 'create':
        if args.s3_dir:
            s3_helper.create_folder(args.s3_dir)
        else:
            print("--s3-dir is required for create action.")
    elif args.action == 'download':
        if args.s3_folder and args.local_download_dir:
            s3_helper.download_folder(args.s3_folder, args.local_download_dir)
        else:
            print("Both --s3-folder and --local-download-dir are required for download action.")
    elif args.action == 'list':
        s3_helper.list_s3_contents()
