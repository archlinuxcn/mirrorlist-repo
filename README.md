# Arch Linux CN Community Repository Mirrors

Here is a list of public mirrors of [our community repository](https://github.com/archlinuxcn/repo).

## Usage

Simply install the `archlinuxcn-mirrorlist` package.

To help you choose the best mirror, you can view the [list of mirrors](https://archlinuxcn.org/mirrors/list.html), the [map of mirrors](https://archlinuxcn.org/mirrors/map.html) and the [synchronization status of mirrors](https://build.archlinuxcn.org/grafana/d/iK2vLpGGk/mirrors).

### Debuginfod Configuration

```bash
cp -v archlinuxcn.urls /etc/debuginfod/
```

## Apply Mirror

If you are interested in applying mirror of our repository, please refer to the [application.md](application.md) for instructions.

## Mirrors

### Our main server

```ini
## Our main server (Amsterdam, North Holland, Netherlands) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://repo.archlinuxcn.org/$arch
```

### 校园网联合镜像站

```ini
## 校园网联合镜像站 (中国) (ipv4, ipv6)
## Redirect to suitable educational mirror based on location
[archlinuxcn]
Server = https://mirrors.cernet.edu.cn/archlinuxcn/$arch
```

### 北京外国语大学

```ini
## 北京外国语大学 (北京) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.bfsu.edu.cn/archlinuxcn/$arch
```

### 北京大学

```ini
## 北京大学 (北京) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.pku.edu.cn/archlinuxcn/$arch
```

### 腾讯云

```ini
## 腾讯云 (Global CDN) (http, https, ipv4)
[archlinuxcn]
Server = https://mirrors.cloud.tencent.com/archlinuxcn/$arch
```

### 网易

```ini
## 网易 (浙江杭州) (http, https, ipv4)
[archlinuxcn]
Server = https://mirrors.163.com/archlinux-cn/$arch
```

### 阿里云

```ini
## 阿里云 (Global CDN) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.aliyun.com/archlinuxcn/$arch
```

### 清华大学

```ini
## 清华大学 (北京) (http, https, ipv4, ipv6)
## It is under high load and not recommended for use
[archlinuxcn]
Server = https://mirrors.tuna.tsinghua.edu.cn/archlinuxcn/$arch
```

### 中国科学技术大学

```ini
## 中国科学技术大学 (安徽合肥) (http, https, ipv4, ipv6)
## It is under high load and not recommended for use
[archlinuxcn]
Server = https://mirrors.ustc.edu.cn/archlinuxcn/$arch
```

### 哈尔滨工业大学

```ini
## 哈尔滨工业大学 (黑龙江哈尔滨) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.hit.edu.cn/archlinuxcn/$arch
```

### 吉林大学

```ini
## 吉林大学 (吉林长春) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.jlu.edu.cn/archlinuxcn/$arch
```

### 浙江大学

```ini
## 浙江大学 (浙江杭州) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.zju.edu.cn/archlinuxcn/$arch
```

### 重庆大学

```ini
## 重庆大学 (重庆) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.cqu.edu.cn/archlinuxcn/$arch
```

### 重庆邮电大学

```ini
## 重庆邮电大学 (重庆) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.cqupt.edu.cn/archlinuxcn/$arch
```

### 上海交通大学

```ini
## 上海交通大学 (上海) (https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirror.sjtu.edu.cn/archlinux-cn/$arch
```

### 南京大学

```ini
## 南京大学 (江苏南京) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.nju.edu.cn/archlinuxcn/$arch
```

### 南方科技大学

```ini
## 南方科技大学 (广东深圳) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.sustech.edu.cn/archlinuxcn/$arch
```

### 武昌首义学院

```ini
## 武昌首义学院 (湖北武汉) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.wsyu.edu.cn/archlinuxcn/$arch
```

### 北京交通大学

```ini
## 北京交通大学 (北京) (https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirror.bjtu.edu.cn/archlinuxcn/$arch
```

### 兰州大学

```ini
## 兰州大学 (甘肃兰州) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.lzu.edu.cn/archlinuxcn/$arch
```

### 西安交通大学

```ini
## 西安交通大学 (陕西西安) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xjtu.edu.cn/archlinuxcn/$arch
```

### 南阳理工学院

```ini
## 南阳理工学院 (河南南阳) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirror.nyist.edu.cn/archlinuxcn/$arch
```

### 南京工业大学

```ini
## 南京工业大学 (江苏南京) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.njtech.edu.cn/archlinuxcn/$arch
```

### 上海科技大学

```ini
## 上海科技大学 (上海) (https, ipv4)
[archlinuxcn]
Server = https://mirrors.shanghaitech.edu.cn/archlinuxcn/$arch
```

### 中国科学院软件研究所

```ini
## 中国科学院软件研究所 (北京) (https, ipv4)
[archlinuxcn]
Server = https://mirror.iscas.ac.cn/archlinuxcn/$arch
```

### 北京邮电大学

```ini
## 北京邮电大学 (北京) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.bupt.edu.cn/archlinuxcn/$arch
```

### 國立成功大學

```ini
## 國立成功大學 (臺灣臺南) (http, https, ipv4)
[archlinuxcn]
Server = https://archlinux.ccns.ncku.edu.tw/archlinuxcn/$arch
```

### xTom (香港伺服器)

```ini
## xTom (香港伺服器) (香港) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.hk/archlinuxcn/$arch
```

### xTom (United States server)

```ini
## xTom (United States server) (San Jose, California, United States) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.us/archlinuxcn/$arch
```

### xTom (Netherlands server)

```ini
## xTom (Netherlands server) (Amsterdam, North Holland, Netherlands) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.nl/archlinuxcn/$arch
```

### xTom (Germany server)

```ini
## xTom (Germany server) (Düsseldorf, North Rhine-Westphalia, Germany) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.de/archlinuxcn/$arch
```

### xTom (Estonia server)

```ini
## xTom (Estonia server) (Tallinn, Harju, Estonia) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.ee/archlinuxcn/$arch
```

### xTom (Japan server)

```ini
## xTom (Japan server) (Osaka, Japan) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.jp/archlinuxcn/$arch
```

### xTom (Australia server)

```ini
## xTom (Australia server) (Sydney, New South Wales, Australia) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.xtom.au/archlinuxcn/$arch
```

### University of California, Berkeley

```ini
## University of California, Berkeley (Berkeley, California, United States) (http, https, ipv4, ipv6)
[archlinuxcn]
Server = https://mirrors.ocf.berkeley.edu/archlinuxcn/$arch
```
