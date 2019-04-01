# -*- coding:utf-8 -*-
import docker
import datetime

client = docker.APIClient(base_url='unix://var/run/docker.sock', version='1.21', timeout=5)


# TODO 去掉images[key]列表
"""获取全部镜像"""


# 处理value值
def deal_value(value):
    if type(value) == list:
        return value[0].split()[0].replace('/', '')
    if type(value) == dict:
        for key in value:
            return value[key]
    if type(value) == str and len(value) > 60:
        return value[:12]
    else:
        return value


# 日期格式化
def docker_date():
    date = str(datetime.datetime.now())
    date_split = int(date.split()[0].replace('-', ''))
    return date_split


# # 通过容器名获取容器ID
# def get_container_id(containername):
#     for containers in client.containers():
#         for key in containers:
#             print(containers[key])
#             if deal_value(containers[key]) == containername:
#                 print(key)
#         # print(containers_dict)
#
#
# get_container_id("sitech-ecommerce-cart-api")


# 获取所有镜像信息
def get_all_image_info():
    for images in client.images():
        images_dict = {}
        for key in images:
            if key == "RepoTags":
                images_dict["ImageName"] = images[key]
            elif key == "Size":
                images_dict["ImageSize"] = images[key]
        print(images_dict)


# 获取容器信息
def get_all_container_info():
    for containers in client.containers():
        containers_dict = {}
        for key in containers:
            if key == "Names":
                containers_dict["ContainerName"] = deal_value(containers[key])
            elif key == "Image":
                containers_dict["ImageName"] = deal_value(containers[key])
            elif key == "HostConfig":
                containers_dict["Networks"] = deal_value(containers[key])
            elif key == "Id":
                containers_dict["ContainerId"] = deal_value(containers[key])

        print(containers_dict)

get_all_container_info()
# 获取容器日志
def get_container_logs(containerid, tail, since=docker_date()):
    container_logs = client.logs(container=containerid, tail=tail, since=since).decode('utf-8')
    return container_logs

# print(get_container_logs("d3eab940e020", 3000))