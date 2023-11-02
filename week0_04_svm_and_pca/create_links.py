import os
import glob
import subprocess

def get_git_current_branch():
    result = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return result.decode('utf-8').strip()

def get_git_remote_url():
    result = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
    url = result.decode('utf-8').strip()

    if "https://" in url:
        # HTTPS format: https://github.com/username/repo.git
        github_username, repo_name = url.split("github.com/")[1].split("/")
    else:
        # SSH format: git@github.com:username/repo.git
        github_username, repo_name = url.split(':')[-1].split('/')

    repo_name = repo_name.split('.')[0]  # Remove ".git"
    return github_username, repo_name


# Get the current branch name
branch_name = get_git_current_branch()

# Get the remote github username and repo name
github_username, repo_name = get_git_remote_url()

# Base directory and base GitHub link
base_dir = os.path.abspath(os.path.curdir)

# Construct the base GitHub link
base_link = f'https://colab.research.google.com/github/{github_username}/{repo_name}/blob/{branch_name}/'

# Get all .ipynb files in the directory
notebooks = glob.glob(os.path.join(base_dir, '*.ipynb'))

# Generate and print links
lines = []
for notebook in notebooks:
  relative_path = os.path.relpath(notebook)
  link = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({base_link}{relative_path})"
  line = f"* {os.path.splitext(os.path.basename(notebook))[0]}: {link}" 
  lines.append(line)
print('\n'.join(lines))

# with open(os.path.join(base_dir, 'README.md'), 'a') as iofile:
#     iofile.write('\n'.join(lines))