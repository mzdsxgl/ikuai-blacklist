# N1 · AdGuard Home 儿童设备黑名单配置说明

适用：旁路网关 N1（iStoreOS，192.168.100.5）上运行的 AdGuard Home
目标：对孩子设备（.13/.19/.53/.54）做 HTTPS 也能生效的站点级屏蔽

---

## 一、黑名单来源与清洗
本次黑名单**直接对齐你审计产出的权威清单**（同目录 `2026-08-08-10-14-59/`）：
- `domains_merged_filtered.txt` —— 最终可屏蔽域名列表（**1282 个，一行一个，字母序**）
- `domains_excluded.txt` —— 被排除明细（59 个 CSS 伪域名 + 24 个公共服务白名单，带频次）

本文件 `AGH儿童黑名单规则.txt` 的**第一节即这 1282 条逐字转换**（`||域名^`），与权威清单逐项一致；**第二节为附加的 18 条通用娱乐分类**（抖音 / B站 / 淘宝等，非原清单）。

> 历史版本曾把全部域名归并到根域（eTLD+1）并自行剔除伪域名，得到 1071 条。交叉验证发现：你的 1282 是**子域级**写法（如 `chuangshi.qq.com`、`444.1006sd.com`），粒度更精细、且刻意保留了阅文 / 公共服务等子域。故改为**严格沿用你的权威清单**，不再自行根域归并。

## 一-B、交叉验证结论（2026-08-08）
以你给的 `domains_merged_filtered.txt`(1282) + `domains_excluded.txt`(59+24) 为基准，对旧版黑名单逐项对碰：

| 项目 | 结果 |
|------|------|
| 旧版规则数 | 1071（根域级） |
| 根级覆盖率 | 旧版覆盖了权威 1282 中的 **1242 条**（含根域归并覆盖） |
| 真实漏网 | 40 条（多为你刻意保留的阅文 / QQ 阅读 / 公共服务子域，如 `chuangshi.qq.com`、`music.163.com`） |
| 旧版误含 CSS 伪域名 | **4 个**（`wn01.link`、`book.name`、`wnacg01.link`、`div.bookbox`）—— 已随改用权威清单消除 |
| 旧版误封公共服务 | 0（百度 / 必应 / GitHub / Pixiv 等根域已放行） |

**处置**：黑名单重写为 **1282（权威）+ 18（附加）= 1300 条**，逐条复核：
- 第一节与权威 1282 **完全一致（True）**
- 附加 18 条全部就位
- 误含 CSS 伪域名 **0**

> ⚠ 子域级写法提示：权威清单里 `||444.1006sd.com^` 只封该子域，不封根域 `1006sd.com`。若希望整站封死，可把清单批量转换为根域（`||1006sd.com^`）。需要的话我写个转换脚本。

## 二、导入（二选一）
### 方式 A：直接粘贴
AGH 后台 → 过滤 → 黑名单 → 粘贴 `AGH儿童黑名单规则.txt` 全文 → 保存 → 应用配置。

### 方式 B：自定义规则列表
把 txt 放到 N1，如 `/etc/AdGuardHome/kids-blacklist.txt`，AGH → 过滤 → DNS 拦截列表 → 添加自定义列表 → 指向该文件。

## 三、叠加官方规则集（覆盖成人 / 不当内容，自动更新）
AGH → 过滤 → DNS 拦截列表 → 添加：
- AdGuard Family Protection：`https://adguardteam.github.io/AdGuardSDNSFilter/Filters/family_protection.txt`
- AdGuard Adult Filter：`https://adguardteam.github.io/AdGuardSDNSFilter/Filters/adult_filter.txt`

## 四、防绕过（关键）
| 防护 | 位置 | 操作 |
|------|------|------|
| DNS 重定向 | iKuai | 网络设置 → DNS → 开启重定向，LAN 内 53 端口劫持到 N1:53 |
| 封 DoT | N1 / iKuai | REJECT 出站 853 端口 |
| 封 DoH | N1 OpenClash | REJECT `dns.google` / `dns.cloudflare.com` / `doh.opendns.com` / `doh.pub` |

## 五、验证
孩子设备 `nslookup po18.xyz` → 应返回 NXDOMAIN；浏览器开对应站点 → 无法连接（HTTP / HTTPS 均失效）。

## 六、文件
- `AGH儿童黑名单规则.txt` —— **第一节 1282 条**（对齐 `domains_merged_filtered.txt`，AdGuard 语法 `||子域^`）+ **第二节 18 条**（附加娱乐分类，按需启用）
- `AGH儿童黑名单配置说明.md` —— 本说明（含交叉验证结论）
- 权威基准（同目录 `2026-08-08-10-14-59/`）：`domains_merged_filtered.txt`、`domains_excluded.txt`
