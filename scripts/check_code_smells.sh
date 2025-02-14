#!/usr/bin/env bash
set -e
# fail on python pdbs
# exclude venv bc circleci adds the symlink inside our repo, the SOBs
if git ls-files | grep py | xargs grep -r 'pdb.set_trace()'; then
  echo "Found pdb"
  exit 1
fi

# from pre-commit.sample
# figure out what to diff against
if git rev-parse --verify HEAD >/dev/null 2>&1
then
    against=HEAD
else
    # Initial commit: diff against an empty tree object
    against=4b825dc642cb6eb9a060e54bf8d69288fbee4904
fi

# If there are whitespace errors, print the offending file names and fail.
! git diff-index --check --cached $against -- && echo -e  "Whitespace errors! ^^\n=======" && exit 1

echo "No blocking code smells"
