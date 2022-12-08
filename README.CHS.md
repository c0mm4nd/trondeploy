# TronDeploy

TronDeploy是一个用于部署tron protocal全节点与服务的容器。

## 用法

```bash
docker build . -t trondeploy
docker run -d -p8090:8090 -p50545:50545 -p18888:1888 -p18888:1888/udp --name tron_fullnode trondeploy
```

## 详细信息

端口。
| 端口 | 服务 | 必须打开？ |
| --- | --- | --- |
| 8090 | HTTP Restful API | 如果需要ETL，是的 | 
| 8091 | HTTP Restful API (solidity) | 否 | 
| 18888 | P2P | 是的，以便更好地同步 |
| 50051 | gRPC | 否 |
| 50545 | HTTP JSON RPC | 如果需要ETL，是的 |
| 50555 | HTTP JSON RPC (solidity) | 否 |

文件和文件夹。
| 文件夹 | 内容 |
| --- | --- |
| /tron | 工作区的根目录 |
| /tron/output-directory/| 区块链数据文件夹（>1.4T） |
| /tron/logs/ | logs文件夹 |
| /tron/FullNode.jar | fullnode可执行文件 |
| /tron/main_net_config.conf | 配置 |
| /tron/start.sh | 容器的入口 | 
