#!/bin/bash

# Prompt for GitHub repository URL
read -p "Enter GitHub repository URL: " github_repo_url

# Prompt for CodeCommit repository URL
read -p "Enter CodeCommit repository URL: " codecommit_repo_url

# Clone GitHub repository
git clone $github_repo_url

# Change directory to the cloned repository
repo_name=$(basename $github_repo_url | cut -f 1 -d '.')
cd $repo_name

# Push to CodeCommit repository
git push $codecommit_repo_url --all

# Navigate back to the parent directory
cd ..

# Delete the local repository
rm -rf $repo_name

echo "GitHub to CodeCommit sync completed."
