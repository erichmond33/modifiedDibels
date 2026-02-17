import os
from indexer import CodeIndexer

repo_path = os.getcwd() # Current directory
indexer = CodeIndexer(repo_path)
indexer.index() # Re-index the repo to ensure graph is up-to-date

# Use the commit hashes obtained from 'git log --oneline -2'
base_commit = '1a2bbb6' # Older commit
head_commit = 'cdcf377' # Newer commit

print(f"Generating changelog for changes between {base_commit} and {head_commit}")
changelog_output = indexer.generate_changelog(repo_path, base_commit, head_commit)
print("\n--- Generated Changelog Prompt ---")
print(changelog_output)