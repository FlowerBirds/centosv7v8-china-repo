#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import shutil
from datetime import datetime

# 兼容Python2的编码处理
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except NameError:
    # Python3无需设置默认编码
    pass


def get_centos_full_version():
    """
    从/etc/redhat-release文件中获取CentOS的完整版本号（主版本+小版本）
    :return: 元组(主版本, 小版本)，如("7", "7.0.1406")；无法识别则返回(None, None)
    """
    release_file = "/etc/redhat-release"
    if not os.path.exists(release_file):
        print("错误：未找到{}文件，无法识别系统版本".format(release_file))
        return (None, None)

    try:
        # 兼容Python2的文件打开方式
        with open(release_file, "r") as f:
            content = f.read().strip()
    except (IOError, OSError):
        print("错误：无权限读取{}，请使用root权限运行脚本".format(release_file))
        return (None, None)

    # 适配CentOS的两种版本格式
    pattern = r"CentOS(?: Linux)? release (\d+)\.([\d\.]+)"
    match = re.search(pattern, content)
    if not match:
        print("错误：无法从系统文件中识别CentOS 7/8的具体版本")
        return (None, None)

    main_version = match.group(1)
    full_version = "{}.{}".format(main_version, match.group(2))

    # 过滤非7/8版本
    if main_version not in ["7", "8"]:
        print("错误：当前系统为CentOS {}，仅支持CentOS7/8版本".format(main_version))
        return (None, None)
    return (main_version, full_version)


def backup_all_repo_files():
    """
    备份/etc/yum.repos.d/下所有.repo文件到时间戳命名的备份目录
    :return: 备份目录路径，失败则返回None
    """
    repo_dir = "/etc/yum.repos.d"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_dir = os.path.join(repo_dir, "repo_bak_{}".format(timestamp))

    try:
        # 兼容Python2，手动判断目录是否存在，避免exist_ok参数报错
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        else:
            print("错误：备份目录{}已存在，避免覆盖，终止备份".format(backup_dir))
            return None

        # 兼容Python2的目录遍历
        repo_files = [f for f in os.listdir(repo_dir) if f.endswith(".repo")]

        if not repo_files:
            print("提示：{}下无.repo文件，无需备份".format(repo_dir))
            return backup_dir

        for repo_file in repo_files:
            src_path = os.path.join(repo_dir, repo_file)
            dst_path = os.path.join(backup_dir, repo_file)
            shutil.copy2(src_path, dst_path)
            print("已备份：{} -> {}".format(src_path, dst_path))

        print("所有.repo文件已备份至：{}".format(backup_dir))
        return backup_dir
    except (IOError, OSError):
        print("错误：无权限操作{}，请使用root权限运行".format(repo_dir))
        return None
    except Exception as e:
        print("备份异常：{}".format(str(e)))
        return None


def generate_yum_repo(main_version, full_version):
    """
    根据CentOS完整版本生成对应的清华vault源YUM配置文件
    :param main_version: 主版本号7/8
    :param full_version: 完整版本号，如7.0.1406、8.5.2111
    :return: 成功返回True，失败返回False
    """
    repo_path = "/etc/yum.repos.d/CentOS-Base.repo"

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

    # 校验小版本是否支持
    if full_version not in supported_versions[main_version]:
        support_list = sorted(supported_versions[main_version].keys())
        print("错误：不支持CentOS {}版本".format(full_version))
        print("支持的CentOS{}系列版本：{}".format(main_version, support_list))
        return False

    vault_version = supported_versions[main_version][full_version]
    repo_template = ""

    # CentOS7 repo模板
    if main_version == "7":
        repo_template = """[base]
name=CentOS-{0} - Base - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/os/$basearch/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-7

[updates]
name=CentOS-{0} - Updates - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/updates/$basearch/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-7

[extras]
name=CentOS-{0} - Extras - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/extras/$basearch/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-7

[centosplus]
name=CentOS-{0} - Plus - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/centosplus/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-7
""".format(full_version, vault_version)

    # CentOS8 repo模板
    elif main_version == "8":
        repo_template = """[baseos]
name=CentOS-{0} - BaseOS - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/BaseOS/$basearch/os/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-Official

[appstream]
name=CentOS-{0} - AppStream - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/AppStream/$basearch/os/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-Official

[extras]
name=CentOS-{0} - Extras - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/extras/$basearch/os/
gpgcheck=1
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-Official

[powertools]
name=CentOS-{0} - PowerTools - Tsinghua Vault
baseurl=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/{1}/PowerTools/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=https://mirrors.tuna.tsinghua.edu.cn/centos-vault/RPM-GPG-KEY-CentOS-Official
""".format(full_version, vault_version)

    try:
        with open(repo_path, "w") as f:
            f.write(repo_template)
        print("✅ 成功生成CentOS {}的清华源配置：{}".format(full_version, repo_path))
        return True
    except (IOError, OSError):
        print("❌ 无权限写入{}，请使用root权限运行".format(repo_path))
        return False
    except Exception as e:
        print("❌ 配置生成失败：{}".format(str(e)))
        return False


def main():
    # 1. 校验Python版本（仅提示，不强制退出）
    if sys.version_info < (3, 0):
        print("⚠️  警告：当前为Python2环境，建议使用Python3运行（Python2已停止维护）")

    # 2. 校验root权限
    if hasattr(os, "geteuid") and os.geteuid() != 0:
        print("⚠️  警告：无root权限将无法完成备份和配置修改")
        # 兼容Python2的输入方式
        if sys.version_info < (3, 0):
            confirm = raw_input("是否继续（y/n，n退出）：").strip().lower()
        else:
            confirm = input("是否继续（y/n，n退出）：").strip().lower()
        if confirm != "y":
            sys.exit(0)

    # 3. 全量备份repo文件
    print("\n===== 开始备份YUM源配置 =====")
    backup_dir = backup_all_repo_files()
    if not backup_dir:
        print("备份失败，终止操作")
        sys.exit(1)

    # 4. 识别系统版本
    print("\n===== 开始识别系统版本 =====")
    main_version, full_version = get_centos_full_version()
    if not main_version or not full_version:
        print("版本识别失败，终止操作")
        sys.exit(1)
    print("已识别系统版本：CentOS {}".format(full_version))

    # 5. 生成YUM源配置
    print("\n===== 开始生成清华Vault源 =====")
    if not generate_yum_repo(main_version, full_version):
        print("配置生成失败，可从备份目录恢复：{}".format(backup_dir))
        sys.exit(1)

    # 6. 后续操作提示
    print("\n===== 操作完成 =====")
    print("📁 原有配置备份目录：{}".format(backup_dir))
    print("🔧 建议执行以下命令刷新缓存：")
    print("   yum clean all && yum makecache")
    print("   yum repolist enabled")


if __name__ == "__main__":
    main()
