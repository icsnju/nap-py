# nap-py: 容器引擎接口
----

该项目希望综合docker，rkt，lxc/lxd及runC等容器相关开源项目中关于容器引擎，计算，存储，网络资源的语义，为nap-core项目提供一个比较稳定和统一的抽象接口。
我们不追求完全实现上述项目中的所有特性。
自顶向下，从上层组件的需求出发，结合现有容器开源项目已实现的功能，来设计这个接口。
由于docker的发展和功能要比其它项目更成熟，所以目前主要以docker为基础，基于`docker-py`来实现。

项目使用python 2开发，依赖的`docker-py`，可通过pip来安装
```
sudo pip install docker-py
```

## 参考文档
+ [Docker RESTful API v1.22](https://docs.docker.com/engine/reference/api/docker_remote_api_v1.22/)
+ [rkt Doc](https://github.com/coreos/rkt/blob/master/Documentation/commands.md)
+ [lxc Doc](https://linuxcontainers.org/lxc/documentation/#python)
+ [runC](https://github.com/opencontainers/runc)

+ [rkt vs. others](https://coreos.com/rkt/docs/latest/rkt-vs-other-projects.html)