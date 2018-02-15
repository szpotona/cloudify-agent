#!/bin/bash -e

# If /etc/sudoers.d exists, add a file there to disable TTY requirement
# for the current user.
# Otherwise, if /etc/sudoers exist, add a line there to disable TTY requirement
# for the current user.
# Otherwise, do nothing.

AGENT_USER=$1
MAYBE_SUDO=$2

SUDOERS_D="/etc/sudoers.d"
SUDOERS="/etc/sudoers"
DISABLETTY_LINE="Defaults:${AGENT_USER} !requiretty"

if [ -z "${MAYBE_SUDO}" ]; then
    MAYBE_SUDO="/bin/sh -c"
fi

if [ -d "${SUDOERS_D}" ]; then
    MY_SUDOERS=${SUDOERS_D}/cfy-${AGENT_USER}
    echo "${SUDOERS_D} exists; adding ${MY_SUDOERS} to disable TTY requirement for ${AGENT_USER}"
    echo ${DISABLETTY_LINE} | ${MAYBE_SUDO} 'EDITOR="tee" visudo -f '${MY_SUDOERS}
elif [ -f "${SUDOERS}" ]; then
    echo "${SUDOERS} exists; disabling TTY requirement for ${AGENT_USER}"
    echo ${DISABLETTY_LINE} | ${MAYBE_SUDO} 'EDITOR="tee -a" visudo -f '${SUDOERS}
else
    echo "Neither ${SUDOERS_D} nor ${SUDOERS} found; skipping"
fi
