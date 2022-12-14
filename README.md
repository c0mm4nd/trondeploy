# TronDeploy

TronDeploy is a container for deploying tron protocal fullnode with services.

[中文版](./README.CHS.md)

## Usage

```bash
docker build . -t trondeploy
docker run -d -p8090:8090 -p50545:50545 -p18888:18888 -p18888:18888/udp --name tron_fullnode trondeploy
```

## Details

Ports:
| port | service | required? |
| --- | --- | --- |
| 8090 | HTTP Restful API | yes for etl | 
| 8091 | HTTP Restful API (solidity) | no | 
| 18888 | P2P | yes for better sync |
| 50051 | gRPC | no |
| 50545 | HTTP JSON RPC | yes for etl |
| 50555 | HTTP JSON RPC (solidity) | no |

Files & Folders:
| folder | content |
| --- | --- |
| /tron | the root of the workspace |
| /tron/output-directory/| chain data folder (>1.4T) |
| /tron/logs/ | logs folder |
| /tron/FullNode.jar | fullnode executable file |
| /tron/main_net_config.conf | the configuration |
| /tron/start.sh | entry of the container | 

Highly suggest use [docker volume](https://docs.docker.com/storage/volumes/) mounting `/tron` or just `/tron/output-directory` to avoid data loss when restarting container.
