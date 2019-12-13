"""
Functions to create and extract zip file archives. Note that the output file
archive is zipped using ZIP_DEFLATED with the maximum compression level of 9.
"""

import os
from zipfile import ZipFile, ZIP_DEFLATED


def extract_files(source, destination):
    """Extracts a zip archive to the desired output directory.

    Args:
        source (str): The zip archive to be extracted.
        destination (str): The destination for the extracted files.
    """
    with ZipFile(source, "r", ZIP_DEFLATED, compresslevel=9) as zip_file:
        zip_file.extractall(destination)


def zip_dir(name, source, destination):
    """Zips the contents of a directory recursively.

    Args:
        name (str): The name of the archive to be created.
        source (str): The location of the directory to be zipped.
        destination (str): Where the resulting zip archive will be stored.

    Returns:
        str: The path to the output archive.
    """
    archive_path = os.path.join(destination, name)

    with ZipFile(archive_path, "x", ZIP_DEFLATED, compresslevel=9) as zip_file:
        for path, _, files in os.walk(source):
            for file in files:
                # Set the real file path and the relative path for the archive
                real_path = os.path.join(path, file)
                rel_path = real_path.replace(os.path.dirname(source), "")

                # Write the file to the zip archive
                zip_file.write(real_path, rel_path)

    return archive_path


def zip_files(name, sources, destination):
    """Zips a list of files.
    
    Args:
        name (str): The name of the archive to be created.
        sources (list[str]): The location of the files to be zipped.
        destination (str): Where the resulting zip archive will be stored.
        
    Returns:
        str: The path to the output archive.
    """
    archive_path = os.path.join(destination, name)

    with ZipFile(archive_path, "x", ZIP_DEFLATED, compresslevel=9) as zip_file:
        for source in sources:
            zip_file.write(source, source.replace(os.path.dirname(source), ""))

    return archive_path
