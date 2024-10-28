# Remove Comments from Files

A versatile Python script to remove commented lines from files, particularly `.conf` files. The script offers various options for customization, including recursive directory processing, comment type specification, logging, and more.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
  - [Basic Usage](#basic-usage)
  - [Options](#options)
  - [Examples](#examples)
- [Logging](#logging)
- [Comment Types](#comment-types)
- [Error Handling](#error-handling)
- [License](#license)
- [Contributing](#contributing)

---

## Features

- **Process Single Files or Directories**: Specify a single file or an entire directory to process.
- **Recursive Processing**: Optionally process directories recursively.
- **Custom Comment Types**: Define which comment characters to remove (e.g., `#`, `;`, `//`).
- **Remove Empty Lines**: Optionally remove empty lines from files.
- **Backup Functionality**: Creates backups of original files before modification.
- **Dry Run Mode**: Preview changes without modifying any files.
- **Logging**: Detailed logging with automatic log file creation.
- **Symlink Handling**: Optionally follow and process symlinked files.
- **File Inclusion/Exclusion Patterns**: Include or exclude files based on patterns.
- **Exception Handling**: Robust error handling with informative log messages.

## Requirements

- **Python 3.x**
- **`docopt` Library**

  Install via pip:

  ```bash
  pip install docopt
  ```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/P1ro/remove_file_comments.git
   ```

2. **Navigate to the Script Directory**

   ```bash
   cd remove_file_comments
   ```

3. **Ensure the Script is Executable**

   ```bash
   chmod +x rm_file_comments.py
   ```

## Usage

### Basic Usage

```bash
python3 rm_file_comments.py [options] [--directory=<dir>]
```

or

```bash
python3 rm_file_comments.py [options] --file=<file>
```

### Options

- `-h`, `--help`: Show help message.
- `--version`: Show script version.
- `-r`, `--recursive`: Recursively process directories.
- `-e`, `--remove-empty-lines`: Remove empty lines.
- `-b`, `--backup-dir=<dir>`: Directory to store backup files (default: `./backup`).
- `--follow-symlinks`: Follow and process symlinks to files.
- `--exclude=<pattern>`: Exclude files matching the pattern (supports wildcards).
- `--include=<pattern>`: Include only files matching the pattern (supports wildcards).
- `-v`, `--verbose`: Increase verbosity level.
- `-q`, `--quiet`: Decrease verbosity level.
- `--dry-run`: Perform a dry run without modifying files.
- `--log-file=<file>`: Specify the log file name.
- `--comment-types=<chars>`: Specify comment characters to remove (e.g., `--comment-types="#;//"`). Separate multiple characters with semicolons (`;`).
- `--file=<file>`: Specify a single file to process.

### Examples

1. **Process a Directory with Default Settings**

   ```bash
   python3 rm_file_comments.py --directory=/path/to/directory
   ```

   - Processes `.conf` files in the specified directory.
   - Removes lines starting with `#`.

2. **Process Recursively and Remove Empty Lines**

   ```bash
   python3 rm_file_comments.py --directory=/path/to/directory --recursive --remove-empty-lines
   ```

3. **Specify Comment Types**

   ```bash
   python3 rm_file_comments.py --directory=/path/to/directory --comment-types="#;//"
   ```

   - Removes lines starting with `#` or `//`.

4. **Specify Log File and Verbose Output**

   ```bash
   python3 rm_file_comments.py --directory=/path/to/directory --log-file=my_log.log --verbose
   ```

5. **Process a Single File with Custom Comment Types**

   ```bash
   python3 rm_file_comments.py --file=/path/to/file.conf --comment-types="#;//;/*"
   ```

6. **Dry Run with Automatic Log File**

   ```bash
   python3 rm_file_comments.py --directory=/path/to/directory --dry-run
   ```

   - No changes are made to files.
   - Actions are logged in a file named like `remove_comments_YYYYMMDD_HHMMSS.log`.

## Logging

- **Automatic Log File Creation**: If `--log-file` is not specified, the script creates a log file with the current date and time (e.g., `remove_comments_20230101_123000.log`).
- **Verbosity Levels**:
  - `-v`, `--verbose`: Increases logging detail.
  - `-q`, `--quiet`: Decreases logging detail.
- **Log File Specification**: Use `--log-file=<file>` to specify a custom log file name.

## Comment Types

- **Default Comment Character**: `#`
- **Specify Multiple Comment Characters**:
  - Use `--comment-types` followed by characters separated by semicolons.
  - Example: `--comment-types="#;//;/*"`
- **Regex Pattern**: The script builds a regex pattern based on the specified comment types to identify comment lines.

## Error Handling

- **Try-Except Blocks**: The script includes exception handling to manage errors gracefully.
- **Error Logging**: Errors are logged with detailed messages to help with troubleshooting.
- **File and Directory Checks**: Before processing, the script verifies that files and directories exist and are accessible.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

**Disclaimer**: Use this script at your own risk. Always ensure you have backups of your files before running scripts that modify file contents.
