from setuptools import setup
from corpwechatbot.__about__ import __name__, __version__, __url__, __author__, __author_email__, __description__
import setuptools


with open("README.md", 'r', encoding='utf8') as f:
    long_description = f.read()

setup(
    name = __name__,  # 包名称
    version = __version__,
    author = __author__,
    author_email = __author_email__,
    description = __description__,
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        'requests >= 2.23.0',
        'cptools >= 1.4.1'
    ],
    url = __url__,
    packages = setuptools.find_packages(),  # 让setuptools自动发现包
    platforms = 'any',  # 包使用的平台
    classifiers = [
        'Programming Language :: Python :: 3',  # 采用编程语言
        'License :: OSI Approved :: GNU General Public License (GPL)',  # 采用的许可证协议
        'Operating System :: OS Independent',  # 操作系统
    ]
)