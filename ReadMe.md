# S3 Helper Script

This script allows you to perform various operations on an S3 bucket using Python and Boto3.

## Prerequisites

- Python 3 installed on your system.
- Boto3 library installed (`pip install boto3`).

## Setup

1. **Store the Script**: Save the `s3_script.py` file in a directory of your choice on your local machine.

2. **Create Config JSON File**: Create an `s3_config.json` file in the same directory as the script. This file will contain your AWS credentials and S3 bucket name. Use the following format:

    ```json
    {
        "access_key": "YOUR_ACCESS_KEY",
        "secret_key": "YOUR_SECRET_KEY",
        "bucket_name": "YOUR_BUCKET_NAME"
    }
    ```

    Replace `YOUR_ACCESS_KEY`, `YOUR_SECRET_KEY`, and `YOUR_BUCKET_NAME` with your actual AWS credentials and bucket name.

## Usage

1. **Run the Script**: Open a terminal or command prompt, navigate to the directory containing the script and the `s3_config.json` file.

2. **Perform Operations**: Run the script with appropriate arguments to perform various operations on your S3 bucket. Here are some example commands:

    - Upload a directory to S3:
        ```
        python3 s3_script.py upload --local-dir /path/to/local/directory --s3-dir path/in/s3/bucket --config s3_config.json
        ```

    - Delete a folder in S3:
        ```
        python3 s3_script.py delete --s3-dir path/to/folder/in/s3/bucket --config s3_config.json
        ```

    - Copy from one location in S3 to another:
        ```
        python3 s3_script.py copy --source-dir source/path/in/s3/bucket --destination-dir destination/path/in/s3/bucket --config s3_config.json
        ```

    - Create a folder in S3:
        ```
        python3 s3_script.py create --s3-dir new/folder/path/in/s3/bucket --config s3_config.json
        ```

    - Download a folder from S3:
        ```
        python3 s3_script.py download --s3-folder path/to/s3/folder --local-download-dir /path/to/local/download/directory --config s3_config.json
        ```

    - List the contents of the S3 bucket:
        ```
        python3 s3_script.py list --config s3_config.json
        ```

3. **Review Output**: The script will provide feedback on the operations it performs. Review the output to ensure that the operations were successful.
4. **Help**: For help on usage and available options, you can use the `--help` option with the script:
    ```
    python3 s3_script.py --help
    ```
    You can also get help for a specific action:
    ```
    python3 s3_script.py upload --help
    python3 s3_script.py delete --help
    python3 s3_script.py copy --help
    python3 s3_script.py create --help
    python3 s3_script.py download --help
    python3 s3_script.py list --help
    ```

That's it! You can now use the S3 Helper script to interact with your S3 bucket easily.
