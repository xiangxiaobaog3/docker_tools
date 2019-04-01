# -*- coding:utf-8 -*-
import docker

client = docker.APIClient(base_url='unix://var/run/docker.sock', version='1.21', timeout=5)
# print(client.version())


# TODO 去掉images[key]列表
"""获取全部镜像"""

# 处理value值
def deal_value(value):
    if type(value) == list:
        return value[0]
    if type(value) == dict:
        for key in value:
            return value[key]
    if type(value) == str and len(value) > 60:
        return value[:12]
    else:
        return value


def get_all_image_info():
    for images in client.images():
        images_dict = {}
        for key in images:
            if key == "RepoTags":
                images_dict["ImageName"] = images[key]
            elif key == "Size":
                images_dict["ImageSize"] = images[key]
        print(images_dict)


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

print(client.logs(container="d3eab940e020",tail=15).decode('utf-8'))
# get_all_container_info()

