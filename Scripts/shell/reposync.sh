def sync_repositories():
    # Prompt for GitHub repository URL
    github_repo_url = input("Enter GitHub repository URL: ")

    # Prompt for CodeCommit repository URL
    codecommit_repo_url = input("Enter CodeCommit repository URL: ")

    # Clone GitHub repository
    import subprocess
    subprocess.run(["git", "clone", github_repo_url])

    # Change directory to the cloned repository
    import os
    repo_name = os.path.basename(github_repo_url).split('.')[0]
    os.chdir(repo_name)

    # Push to CodeCommit repository
    subprocess.run(["git", "push", codecommit_repo_url, "--all"])

    # Navigate back to the parent directory
    os.chdir('..')

    # Delete the local repository
    import shutil
    shutil.rmtree(repo_name)

    print("GitHub to CodeCommit sync completed.")
