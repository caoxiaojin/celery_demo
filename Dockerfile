FROM centos:7
ENV LANG en_US.UTF-8
# 同步时间
ENV TZ=Asia/Shanghai


RUN yum update -y && yum install epel-release mysql-devel gcc gcc-devel python3-devel -y && yum update -y && yum install python3 -y
RUN pip3 install --upgrade pip

RUN mkdir -p /var/www/

ADD . /var/www/celery_demo/
RUN rm -rf /var/www/celery_demo/venv/


# 5. 安装pip依赖
RUN pip3 install -r /var/www/celery_demo/requirements.txt -i "https://pypi.doubanio.com/simple/"

WORKDIR /var/www/celery_demo/
ENTRYPOINT ["celery","-A","celery_demo","worker","--beat","--scheduler","django"]