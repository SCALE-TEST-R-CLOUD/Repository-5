import os
import random
import string
import subprocess
import time
from pathlib import Path
from datetime import datetime

# =========================
# CONFIG
# =========================

OUTPUT_DIR = "random_repo_content-latest"

COMMITS_COUNT = 200
FILES_PER_COMMIT = 2
FILE_SIZE_KB = 1 * 1024

MIN_DEPTH = 1
MAX_DEPTH = 5

EXTENSIONS = [
    ".txt", ".json", ".xml", ".csv", ".log",
    ".md", ".yaml", ".yml", ".js", ".py",
    ".java", ".html", ".css", ".sql", ".conf"
]

FILE_SIZE_BYTES = FILE_SIZE_KB * 1024

# =========================
# SETUP
# =========================

# Create output directory
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# Change working directory to output dir
os.chdir(OUTPUT_DIR)


def random_name(min_len=5, max_len=15):
    chars = string.ascii_lowercase + string.digits
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(chars, k=length))


def random_content(length=200):
    chars = string.ascii_letters + string.digits + " \n"
    return ''.join(random.choices(chars, k=length))


def create_random_file(path, size_bytes):
    with open(path, "w", encoding="utf-8") as f:
        written = 0

        while written < size_bytes:
            line = random_content() + "\n"
            f.write(line)
            written += len(line.encode("utf-8"))


def run_git(cmd):
    subprocess.run(cmd, check=True)

# =========================
# CREATE COMMITS
# =========================

for commit_no in range(1, COMMITS_COUNT + 1):

    print(f"\n========== Commit {commit_no}/{COMMITS_COUNT} ==========")

    for _ in range(FILES_PER_COMMIT):

        # Random nested path
        depth = random.randint(MIN_DEPTH, MAX_DEPTH)
        folders = [random_name() for _ in range(depth)]

        dir_path = os.path.join(*folders)
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        # Random filename
        file_name = random_name() + random.choice(EXTENSIONS)
        file_path = os.path.join(dir_path, file_name)

        # Create file
        create_random_file(file_path, FILE_SIZE_BYTES)

        print(f"Created: {file_path}")

    # Git add
    run_git(["git", "add", "."])

    # Commit message
    commit_message = (
        f"auto commit #{commit_no} - "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    # Commit
    try:
        run_git(["git", "commit", "-m", commit_message])
        print(f"Committed: {commit_message}")

    except subprocess.CalledProcessError:
        print("Nothing to commit.")

    # Optional delay for realistic timestamps
    time.sleep(1)

    print("\nPushing commit...")
    run_git(["git", "push"])

    time.sleep(10)


print("\nDone.")
print(f"Successfully created and pushed {COMMITS_COUNT} commits.")