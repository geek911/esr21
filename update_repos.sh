#!/bin/sh
for repo in /Users/ckgathi/source/esr21-dashboard /Users/ckgathi/source/esr21-labs /Users/ckgathi/source/esr21-metadata-rules /Users/ckgathi/source/esr21-prn /Users/ckgathi/source/esr21-reference /Users/ckgathi/source/esr21-subject /Users/ckgathi/source/esr21-subject-validation /Users/ckgathi/source/esr21-visit-schedule; do
    (cd "${repo}" && git checkout develop && git pull)
done
