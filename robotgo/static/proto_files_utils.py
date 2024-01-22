import logging
import os
import subprocess


def generate_proto_files():
    directory = f"{os.path.dirname(os.path.abspath(__file__))}/proto_files"
    proto_file_path = os.path.join(directory, "test.proto")

    if not os.path.exists(proto_file_path) or not os.path.isfile(proto_file_path):
        logging.error(f"Error: File {proto_file_path} not found.")
        return

    files_in_directory = os.listdir(directory)
    if len(files_in_directory) > 0 and "test_pb2.py" not in files_in_directory:
        command = (
            f"poetry run python -m grpc_tools.protoc -I. "
            f"--python_out=. --pyi_out=. --grpc_python_out=. {proto_file_path}"
        )

        subprocess.run(command, shell=True)
        logging.info("proto files generation completed.")
    else:
        logging.error("Error: There are other files in the directory")
