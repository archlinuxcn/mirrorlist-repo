### Arch Linux CN Community repo mirrors list

Here is a list of public mirrors of our [community repository](https://github.com/archlinuxcn/repo).

If you interested in making a mirror of our repository, please contact us at repo@archlinuxcn.org.

```ini
# Global CDN (no nodes in mainland China)
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://cdn.repo.archlinuxcn.org/$arch
```

```ini
# University of Science and Technology of China
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
# or with HTTP
# Server = http://mirrors.ustc.edu.cn/archlinuxcn/$arch
```

```ini
# TUNA mirror of Tsinghua University
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch # both IPv4 & IPv6
# Server = https://mirrors.6.tuna.tsinghua.edu.cn/archlinuxcn/$arch # only IPv6
# Server = https://mirrors.4.tuna.tsinghua.edu.cn/archlinuxcn/$arch # only IPv4
# HTTP is also supported
```

```ini
# Chongqing University Open Source Mirror Site
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = http://mirrors.cqu.edu.cn/archlinux-cn/$arch
```

```ini
# Netease (网易)
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = http://mirrors.163.com/archlinux-cn/$arch
```

```ini
# 上海科技大学 Geek Pie 社团
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.geekpie.org/archlinuxcn/$arch
```

```ini
# 电子科技大学 凝聚网络安全工作室
[archlinuxcn]
SigLevel = Optional TrustedOnly
Server = https://mirrors.cnssuestc.org/archlinuxcn/$arch
```
