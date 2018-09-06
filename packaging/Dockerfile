#docker build with --build-arg BASE_IMAGE=centos:7
ARG BASE_IMAGE=""
FROM ${BASE_IMAGE}
RUN yum clean all && \
	rm -rf /var/cache/yum && \
    yum -y downgrade libyaml && \
    yum -y update && \
    yum -y install \
           openssl \
           curl \
           python-devel \
           make \
           gcc \
           gcc-c++ \
           git \
           libyaml-devel \
           yum-utils \
           openssl-devel && \
    curl -1 "https://bootstrap.pypa.io/2.6/get-pip.py" -o "get-pip.py" && \
	python get-pip.py pip==9.0.1 && \
	pip install --upgrade \
		setuptools==36.8.0 \
        cloudify-agent-packager==4.0.2 \
        wheel==0.29.0 \
        setuptools==36.8.0
## No package libffi-devel available in RHEL 6 therefore installing from url
RUN [[ $(cat /etc/*-release) =~ "(Santiago)" ]] && \
    yum install -y https://rpmfind.net/linux/centos/6.10/os/x86_64/Packages/libffi-devel-3.0.5-3.2.el6.x86_64.rpm || \
    yum install -y libffi-devel
ADD linux/provision.sh linux/packager.yaml ~/
