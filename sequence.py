#!/usr/bin/python3

import sys

import ruamel.yaml  # in python-ruamel-yaml package

SOURCE_YAML = "mirrors.yaml"

KEY_ORDER = (
    "provider",
    "url",
    "comment",
    "region",
    "protocols",
    "location",
    "coordinates",
)

PROVIDER_ORDER = (
    "Our main server",
    # ---------------------------------------------------------------------------------------------------------------
    "校园网联合镜像站",  #                    China                                                                 |
    "中国科学技术大学",  #                    Anhui                                                                 |
    "北京外国语大学",  #                      Beijing         Beijing Foreign Studies University                    |
    "北京交通大学",  #                        Beijing         Beijing Jiaotong University                           |
    "北京邮电大学",  #                        Beijing         Beijing University of Posts and Telecommunications    |
    "中国科学院软件研究所",  #                Beijing         Institute of Software, Chinese Academy of Sciences    |
    "北京大学",  #                            Beijing         Peking University                                     |
    "清华大学",  #                            Beijing         Tsinghua University                                   |
    "重庆大学",  #                            Chongqing       Chongqing University                                  |
    "重庆邮电大学",  #                        Chongqing       Chongqing University of Posts and Telecommunications  |
    "兰州大学",  #                            Gansu                                                                 |
    "南方科技大学",  #                        Guangdong                                                             |
    "哈尔滨工业大学",  #                      Heilongjiang                                                          |
    "南阳理工学院",  #                        Henan                                                                 |
    "荆楚理工学院",  #                        Jingmen, Hubei                                                        |
    "武昌首义学院",  #                        Wuhan, Hubei                                                          |
    "南京工业大学",  #                        Jiangsu         Nanjing Tech University                               |
    "南京大学",  #                            Jiangsu         Nanjing University                                    |
    "吉林大学",  #                            Jilin                                                                 |
    "沈阳航空航天大学",  #                    Liaoning                                                              |
    "西安交通大学",  #                        Shaanxi                                                               |
    "上海交通大学",  #                        Shanghai        Shanghai Jiao Tong University                         |
    "上海科技大学",  #                        Shanghai        ShanghaiTech University                               |
    "浙江大学",  #                            Zhejiang                                                              |
    # ---------------------------------------------------------------------------------------------------------------
    "网易",  #                                Zhejiang                                                              |
    "阿里云",  #                              Global CDN      Alibaba                                               |
    "腾讯云",  #                              Global CDN      Tencent                                               |
    # ---------------------------------------------------------------------------------------------------------------
    "xTom (香港伺服器)",  #                   Hong Kong                                                             |
    "國立成功大學",  #                        Taiwan                                                                |
    # ---------------------------------------------------------------------------------------------------------------
    "xTom (Australia server)",  #             Australia                                                             |
    "xTom (Estonia server)",  #               Estonia                                                               |
    "xTom (Germany server)",  #               Germany                                                               |
    "xTom (Japan server)",  #                 Japan                                                                 |
    "xTom (Netherlands server)",  #           Netherlands                                                           |
    "University of California, Berkeley",  #  Berkeley, California, United States                                   |
    "xTom (United States server)",  #         San Jose, California, United States                                   |
    # ---------------------------------------------------------------------------------------------------------------
)


def main():
    mirrors = []
    yaml = ruamel.yaml.YAML()
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = yaml.load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    for m in mirrors:
        for key in reversed(KEY_ORDER):
            if key in m:
                m.move_to_end(key, last=False)
    mirrors.sort(key=lambda m: PROVIDER_ORDER.index(m["provider"]))
    with open(SOURCE_YAML, "w", encoding="utf-8") as output:
        yaml.explicit_start = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump({"archlinuxcn": mirrors}, output)


if __name__ == "__main__":
    main()
