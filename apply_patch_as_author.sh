#!/usr/bin/env bash

set -e
set -u

patch_filename="${1}"

from_line=$(cat "${patch_filename}" | grep 'From:')

export GIT_COMMITTER_NAME=$(echo "${from_line}" | sed 's/From:\s\?\(.*\)\s\?<\(.*\)>\s\?/\1/')
export GIT_COMMITTER_EMAIL=$(echo "${from_line}" | sed 's/From:\s\?\(.*\)\s\?<\(.*\)>\s\?/\2/')

git am --committer-date-is-author-date "${patch_filename}"