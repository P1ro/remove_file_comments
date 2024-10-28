#!/usr/bin/env python3
"""
Usage:
  remove_comments.py [options] [--directory=<dir>]
  remove_comments.py -h | --help
  remove_comments.py --version

Options:
  -h --help                   Show this screen.
  --version                   Show version.
  -r --recursive              Recursively process directories.
  -e --remove-empty-lines     Remove empty lines.
  -b --backup-dir=<dir>       Directory to store backup files [default: ./backup].
  --follow-symlinks           Follow and process symlinks to files.
  --exclude=<pattern>         Exclude files matching the pattern (supports wildcards).
  --include=<pattern>         Include only files matching the pattern (supports wildcards).
  -v --verbose                Increase verbosity level.
  -q --quiet                  Decrease verbosity level.
  --dry-run                   Perform a dry run without modifying files.
  --log-file=<file>           Specify log file name.
  --comment-types=<chars>     Specify comment characters to remove (e.g., "#;//").
  --file=<file>               Specify a single file to process.
"""

import os
import sys
import re
import shutil
from docopt import docopt
import fnmatch
import logging
from datetime import datetime

__version__ = '1.2.0'

def setup_logging(verbose, quiet, log_file):
    # Set logging level
    if verbose and not quiet:
        level = logging.INFO
    elif quiet and not verbose:
        level = logging.ERROR
    else:
        level = logging.WARNING

    # Create a log file with the current date and time if not specified
    if not log_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"remove_comments_{timestamp}.log"

    # Configure logging
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_file,
    )

def remove_comments(file_path, backup_dir, remove_empty_lines, dry_run, comment_types):
    try:
        # Check if the file exists
        if not os.path.exists(file_path):
            logging.warning(f"Skipping {file_path}: File does not exist.")
            return

        # Check if it's a regular file
        if not os.path.isfile(file_path):
            logging.warning(f"Skipping {file_path}: Not a regular file.")
            return

        # Calculate relative path for backup
        relative_path = os.path.relpath(file_path)
        backup_path = os.path.join(backup_dir, relative_path + '.bak')

        # Ensure the backup directory exists
        if not dry_run:
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)

        # Create a backup of the original file in the backup directory
        if not dry_run:
            shutil.copy2(file_path, backup_path)

        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Prepare the regex pattern for comment lines
        comment_chars = [re.escape(char) for char in comment_types.split(';')]
        comment_pattern = '|'.join(comment_chars)
        if remove_empty_lines:
            pattern = rf'^\s*({comment_pattern}|$)'
        else:
            pattern = rf'^\s*({comment_pattern})'

        regex = re.compile(pattern)

        # Filter out lines that are comments or empty
        new_lines = [line for line in lines if not regex.match(line)]

        if dry_run:
            logging.info(f"[Dry Run] Would process {file_path}")
        else:
            # Write the filtered lines back to the file
            with open(file_path, 'w') as file:
                file.writelines(new_lines)
            logging.info(f"Processed {file_path}")
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")

def process_file(file_path, backup_dir, remove_empty_lines, dry_run, comment_types):
    remove_comments(file_path, backup_dir, remove_empty_lines, dry_run, comment_types)

def process_directory(directory, backup_dir, recursive, remove_empty_lines, follow_symlinks, include_pattern, exclude_pattern, dry_run, comment_types):
    try:
        for root, dirs, files in os.walk(directory, followlinks=follow_symlinks):
            for filename in files:
                file_path = os.path.join(root, filename)

                # Exclude files based on patterns
                if exclude_pattern and fnmatch.fnmatch(filename, exclude_pattern):
                    continue
                if include_pattern and not fnmatch.fnmatch(filename, include_pattern):
                    continue

                # Skip symlinks if not following them
                if not follow_symlinks and os.path.islink(file_path):
                    continue

                # Process .conf files or files matching include_pattern
                if filename.endswith('.conf') or (include_pattern and fnmatch.fnmatch(filename, include_pattern)):
                    remove_comments(file_path, backup_dir, remove_empty_lines, dry_run, comment_types)

            if not recursive:
                break
    except Exception as e:
        logging.error(f"Error processing directory {directory}: {e}")

def main():
    arguments = docopt(__doc__, version=__version__)

    # Retrieve command-line arguments
    file_path = arguments['--file']
    directory = arguments['--directory']
    backup_dir = arguments['--backup-dir']
    recursive = arguments['--recursive']
    remove_empty_lines = arguments['--remove-empty-lines']
    follow_symlinks = arguments['--follow-symlinks']
    exclude_pattern = arguments['--exclude']
    include_pattern = arguments['--include']
    verbose = arguments['--verbose']
    quiet = arguments['--quiet']
    dry_run = arguments['--dry-run']
    log_file = arguments['--log-file']
    comment_types = arguments['--comment-types'] or '#'

    # Setup logging
    setup_logging(verbose, quiet, log_file)

    # Ensure the backup directory exists (if not in dry run mode)
    if not dry_run:
        try:
            os.makedirs(backup_dir, exist_ok=True)
        except Exception as e:
            logging.error(f"Error creating backup directory {backup_dir}: {e}")
            sys.exit(1)

    if file_path:
        process_file(file_path, backup_dir, remove_empty_lines, dry_run, comment_types)
    elif directory:
        if not os.path.isdir(directory):
            logging.error(f"Error: {directory} is not a valid directory.")
            sys.exit(1)
        process_directory(directory, backup_dir, recursive, remove_empty_lines, follow_symlinks, include_pattern, exclude_pattern, dry_run, comment_types)
    else:
        logging.error("Error: Either --file or --directory must be specified.")
        sys.exit(1)

if __name__ == '__main__':
    main()
