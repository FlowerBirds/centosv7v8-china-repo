# centosv7v8-china-repo
## 1. 前提说明
CentOS7/8版本官方已经归档，默认的安装源无法使用，而且网上大多数提供的国内yum地址也大部分失效。故为了快速有效的使用在线yum，结合国内清华源，来生成有效的repo文件，帮助实施人员解决手动配置慢等问题。
## 2. 使用方法
核心命令：
```
[root@tempoai soft]# wget  https://raw.githubusercontent.com/FlowerBirds/centosv7v8-china-repo/refs/heads/main/install-repo.py
[root@tempoai soft]# python install-repo.py
```
默认使用Linux自带的Python2环境执行脚本，会自动检测当前系统版本，并生成repo文件。例如：
```
[root@tempoai soft]# python install-repo.py
⚠️  警告：当前为Python2环境，建议使用Python3运行（Python2已停止维护）

===== 开始备份YUM源配置 =====
已备份：/etc/yum.repos.d/CentOS-Base.repo -> /etc/yum.repos.d/repo_bak_20251210_160331/CentOS-Base.repo
已备份：/etc/yum.repos.d/test.repo -> /etc/yum.repos.d/repo_bak_20251210_160331/test.repo
所有.repo文件已备份至：/etc/yum.repos.d/repo_bak_20251210_160331

===== 开始识别系统版本 =====
已识别系统版本：CentOS 7.9.2009

===== 开始生成清华Vault源 =====
✅ 成功生成CentOS 7.9.2009的清华源配置：/etc/yum.repos.d/CentOS-Base.repo

===== 操作完成 =====
📁 原有配置备份目录：/etc/yum.repos.d/repo_bak_20251210_160331
🔧 建议执行以下命令刷新缓存：
   yum clean all && yum makecache
   yum repolist enabled
[root@tempoai soft]#
[root@tempoai soft]# yum clean all && yum makecache
已加载插件：fastestmirror, langpacks
正在清理软件源： base extras updates
Cleaning up list of fastest mirrors
Other repos take up 169 M of disk space (use --verbose for details)
已加载插件：fastestmirror, langpacks
Determining fastest mirrors
base                                                                                                                                                                       | 3.6 kB  00:00:00
extras                                                                                                                                                                     | 2.9 kB  00:00:00
updates                                                                                                                                                                    | 2.9 kB  00:00:00
(1/10): base/x86_64/group_gz                                                                                                                                               | 153 kB  00:00:00
(2/10): base/x86_64/primary_db                                                                                                                                             | 6.1 MB  00:00:02
(3/10): extras/x86_64/primary_db                                                                                                                                           | 253 kB  00:00:00
(4/10): base/x86_64/other_db                                                                                                                                               | 2.6 MB  00:00:01
(5/10): extras/x86_64/filelists_db                                                                                                                                         | 305 kB  00:00:01
(6/10): extras/x86_64/other_db                                                                                                                                             | 154 kB  00:00:00
(7/10): base/x86_64/filelists_db                                                                                                                                           | 7.2 MB  00:00:04
(8/10): updates/x86_64/primary_db                                                                                                                                          |  27 MB  00:00:09
(9/10): updates/x86_64/filelists_db                                                                                                                                        |  15 MB  00:00:10
(10/10): updates/x86_64/other_db                                                                                                                                           | 1.6 MB  00:00:00
元数据缓存已建立
[root@tempoai soft]#  yum repolist enabled
已加载插件：fastestmirror, langpacks
Loading mirror speeds from cached hostfile
源标识                                                                          源名称                                                                                                      状态
base/x86_64                                                                     CentOS-7.9.2009 - Base - Tsinghua Vault                                                                     10,072
extras/x86_64                                                                   CentOS-7.9.2009 - Extras - Tsinghua Vault                                                                      526
updates/x86_64                                                                  CentOS-7.9.2009 - Updates - Tsinghua Vault                                                                   6,173
repolist: 16,771
```
执行成功后，提示执行命令即可。脚本会将之前的repo文件进行备份，不影响后续还原。

## 3. 支持版本
```

    # CentOS 7/8全版本vault路径映射（来自清华源官方目录）
    supported_versions = {
        "7": {
            "7.0.1406": "7.0.1406",
            "7.1.1503": "7.1.1503",
            "7.2.1511": "7.2.1511",
            "7.3.1611": "7.3.1611",
            "7.4.1708": "7.4.1708",
            "7.5.1804": "7.5.1804",
            "7.6.1810": "7.6.1810",
            "7.7.1908": "7.7.1908",
            "7.8.2003": "7.8.2003",
            "7.9.2009": "7.9.2009"
        },
        "8": {
            "8.0.1905": "8.0.1905",
            "8.1.1911": "8.1.1911",
            "8.2.2004": "8.2.2004",
            "8.3.2011": "8.3.2011",
            "8.4.2105": "8.4.2105",
            "8.5.2111": "8.5.2111",
            "8.6.2205": "8.6.2205",
            "8.7.2207": "8.7.2207",
            "8.8.2305": "8.8.2305",
            "8.9.2311": "8.9.2311"
        }
    }

```
