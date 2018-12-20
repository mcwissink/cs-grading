#!/bin/bash
# Author: Joel Stehouwer, jbs24
# Modified by binki and mcw33 somewhat
# Use this to grade cs112 labs super awesome-like!
# /home/cs/112/current$

# don't mess things up if things get messed up
set -e

# Ensure we are in a proper directory
if ! [[ ${PWD} =~ ^/home/cs/[[:digit:]]+/current$ ]]; then
  echo "you done be in the wrong directory" >&2
  exit 1
fi

if ! [[ $1 =~ ^[[:digit:]]+$ ]]; then
  echo "you must pass the current lab as a parameter like: Usage: ${0} 1" >&2
  exit 1
fi

if [[ $1 =~ ^0 ]]; then
  echo "you should not prefix your lab number with a zero. Try again." >&2
  exit 1
fi

home=$(pwd) # This will be cs/112/current
labNum="${1}" # This is the number of the lab
ignoreRule="${2}" # -i to run only for specified students, -e to exclude specified students
gradedir=${HOME}/Documents/gradelab${labNum}
mkdir -p "${gradedir}"
catfile=${gradedir}/output.txt # The file that this script will write to

ls

doCommand() {
  echo "Running ${@}" >> $catfile
  { "${@}" 2>&1 || true; } >> $catfile
  echo "Finished ${@}" >> $catfile
  echo >> $catfile
}

for dir in ./*; do
  echo $dir
  echo "Removing old executable"
  rm ~/go

  isIgnored=
    for studentDir in "$@"; do
      [[ "${dir##*/}" == "${studentDir}" ]] && isIgnored=1
    done

  if [[ "${isIgnored}" && "${ignoreRule}" == "-e" ]]; then
    echo "skipping ${dir}"
    echo "skipped ${dir}" >> $catfile
  elif [[ ! "${isIgnored}" && "${ignoreRule}" == "-i" ]]; then
    echo "skipping ${dir}"
  else
    for labDir in "${dir}"/[lL]{,ab}{,0}"${labNum}"; do
      if ! [[ -e ${labDir} ]]; then
        echo "Unable to find lab results in $dir: $(ls "${dir}")" >> $catfile
      else
        pushd "${labDir}"
        echo "${labDir}" >> $catfile
        ls >> $catfile
    	  echo >> $catfile
        # Allow g++ to fail because the student may have failed, just like Kristofer Paul Gunadi Brink
        sources=()
        for f in *.cpp *.c++ *.cxx; do
          [[ -e ${f} ]] && sources+=(${f})
        done
        doCommand g++ "${sources[@]}" -Wall -o ~/go
    	  echo >> $catfile
        # Allow to fail becaus ethe student may have failed. Period.
        doCommand timeout 5 ~/go
        cat *.h >> $catfile
        cat *.cpp >> $catfile
        studentdir=${gradedir}/${dir}
        for extraFile in *.ods *.xls*; do
          if [[ -e ${extraFile} ]]; then
            # do not make a student dir if there aren't special files to put there in the first place
            mkdir -p "${studentdir}"
            cp -vi "${extraFile}" "${studentdir}"/ >> $catfile
          fi
        done
        popd
      fi
    done
    echo -e "$dir\n\n\n" >> $catfile
  fi
done
