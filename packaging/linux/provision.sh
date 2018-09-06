#!/bin/bash

# VERSION/PRERELEASE/BUILD must be exported as they is being read as an env var by the cloudify-agent-packager
export CORE_TAG_NAME="4.5"
export CORE_BRANCH="master"
export GITHUB_USERNAME=$1
export GITHUB_PASSWORD=$2
export AWS_ACCESS_KEY_ID=$3
export AWS_ACCESS_KEY=$4
export REPO=$5
export BRANCH=$6

curl -u $GITHUB_USERNAME:$GITHUB_PASSWORD https://raw.githubusercontent.com/cloudify-cosmo/${REPO}/${CORE_BRANCH}/packages-urls/common_build_env.sh -o ./common_build_env.sh &&
source common_build_env.sh &&
curl https://raw.githubusercontent.com/cloudify-cosmo/cloudify-common/${CORE_BRANCH}/packaging/common/provision.sh -o ./common-provision.sh &&
source common-provision.sh

cd ~
sudo rm -rf ~/.cache
if [[ ! -z $BRANCH ]] && [[ "$BRANCH" != "master" ]];then
    pushd /tmp
        curl -sLO https://github.com/cloudify-cosmo/cloudify-agent/archive/${BRANCH}.tar.gz
        gunzip -t $BRANCH.tar.gz
        test_gzip_file="$?"
        gunzip -c $BRANCH.tar.gz | tar t > /dev/null
        test_tar_file_inside="$?"
        if [ "$test_gzip_file" == "0" ] && [ "$test_tar_file_inside" == "0" ]; then
            rm -rf $BRANCH.tar.gz
            sed -i "s|cloudify-agent\/archive\/.*\.zip|cloudify-agent\/archive\/$BRANCH\.zip|" /vagrant/linux/packager.yaml
            sed -i "s|cloudify-agent\/.*\/dev-requirements.txt|cloudify-agent\/$BRANCH\/dev-requirements.txt|" /vagrant/linux/packager.yaml
            export AWS_S3_PATH="$AWS_S3_PATH/$BRANCH"
        fi
    popd
fi
cd /tmp && cfy-ap -c /vagrant/linux/packager.yaml -f -v &&
create_md5 "tar.gz" &&
[ -z ${AWS_ACCESS_KEY} ] || upload_to_s3 "tar.gz" && upload_to_s3 "md5"
