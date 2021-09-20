#!/bin/sh
for repo in /Users/astraz/source/esr21-dashboard /Users/astraz/source/esr21-labs /Users/astraz/source/esr21-metadata-rules /Users/astraz/source/esr21-prn /Users/astraz/source/esr21-reference /Users/astraz/source/esr21-subject /Users/astraz/source/esr21-subject-validation /Users/astraz/source/esr21-visit-schedule; do
    (cd "${repo}" && git checkout develop && git pull)
done
