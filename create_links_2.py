import os
import glob
import subprocess
import fire

def get_git_current_branch():
    result = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return result.decode('utf-8').strip()

def get_git_remote_url():
    result = subprocess.check_output(["git", "config", "--get", "remote.origin.url"])
    url = result.decode('utf-8').strip()
    if "https://" in url:
        github_username, repo_name = url.split("github.com/")[1].split("/")
    else:
        github_username, repo_name = url.split(':')[-1].split('/')
    repo_name = repo_name.split('.')[0]
    return github_username, repo_name

def generate_colab_links(directory):
    # Get the current branch name and the remote URL
    branch_name = get_git_current_branch()
    github_username, repo_name = get_git_remote_url()

    # Construct the base GitHub link
    base_link = f'https://colab.research.google.com/github/{github_username}/{repo_name}/blob/{branch_name}/'

    # Get all .ipynb files in the directory
    notebooks = glob.glob(os.path.join(directory, '*.ipynb'))
    lines = []
    # Generate and print links
    for notebook in notebooks:
        relative_path = os.path.relpath(os.path.abspath(notebook))
        link = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]({base_link}{relative_path})"
        lines.append(f"* {os.path.splitext(os.path.basename(notebook))[0]}: {link}")
    return lines

def generate_pdf_links(directory):
    # Get the current branch name and the remote URL
    branch_name = get_git_current_branch()
    github_username, repo_name = get_git_remote_url()

    # Construct the base GitHub link
    base_link = f'https://github.com/{github_username}/{repo_name}/blob/{branch_name}/'

    # Get all .pdf files in the directory
    pdfs = glob.glob(os.path.join(directory, '*.pdf'))
    lines = []
    # Generate and print links
    for pdf in pdfs:
        relative_path = os.path.relpath(os.path.abspath(pdf))
        link = f"[{os.path.basename(pdf)}]({base_link}{relative_path})"
        lines.append(f"* {link}")
    return lines

def generate_links(directory):
    print("\nNotebooks:")
    notebook_lines = generate_colab_links(directory)
    print("\nPDFs:")
    pdf_lines = generate_pdf_links(directory)
    
    with open(os.path.join(directory, 'README.md'), 'w') as iofile:
        iofile.write('Slides:\n\n'+'\n'.join(pdf_lines)+'\n\n')
        iofile.write('Notebooks:\n\n'+'\n'.join(notebook_lines)+'\n\n')

def main():
    fire.Fire(generate_links)

if __name__ == "__main__":
    main()
