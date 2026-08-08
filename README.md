# iKuai 儿童设备黑名单

供 iKuai 路由器「封锁管理 → 新增封锁清单 → URL 拉取」使用的域名黑名单，hosts 格式，DNS 层拦截（HTTP + HTTPS 通封）。

## 文件说明

| 文件 | 用途 |
|---|---|
| `ikuai_blacklist_hosts.txt` | **iKuai 直接拉取的文件**，hosts 格式 `0.0.0.0 域名`，共 1282 条 |
| `AGH儿童黑名单规则.txt` | AdGuardHome 原始规则（`\|\|子域^` 格式），本仓库的来源 |
| `AGH儿童黑名单配置说明.md` | 黑名单来源、清洗、防绕过说明 |
| `start_blacklist_server.bat` | 本地临时起 HTTP 服务用（非必须，GitHub raw 可替代） |

## iKuai 配置

1. 网络设置 → 封锁管理 → 新增封锁清单
2. 名称：`儿童设备黑名单`
3. URL 填本仓库 raw 地址（见下方「Raw URL」）
4. 保存，iKuai 自动拉取；显示「拉取成功 / 共 1282 条」即生效

> 拉取后黑名单存于 iKuai 本地，与 GitHub 是否在线无关。

## 更新流程

1. 更新 `AGH儿童黑名单规则.txt`
2. 由 AGH 规则转换：`grep -oP '^\|\|[^^]+' AGH儿童黑名单规则.txt | sed 's/^||//' | sort -u | while read d; do echo "0.0.0.0 $d"; done > ikuai_blacklist_hosts.txt`
3. commit & push → raw URL 自动更新

## Raw URL

```
https://raw.githubusercontent.com/<用户名>/ikuai-blacklist/main/ikuai_blacklist_hosts.txt
```
