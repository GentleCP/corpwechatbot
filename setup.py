import setuptools
from setuptools import setup
from pathlib import Path

requires = [
    'requests >= 2.23.0',
    'cptools >= 1.4.1'
]

about = {}
root_path = Path(__file__).parent
__about__ = root_path.joinpath('corpwechatbot/__about__.py').open('r', encoding='utf-8').read()
exec(__about__, about)

with open("README.md", 'r', encoding='utf8') as f:
    readme = f.read()

setup(
    name = about['__name__'],  # 包名称
    version = about['__version__'],
    author = about['__author__'],
    author_email = about['__author_email__'],
    description = about['__name__'],
    license = about['__license__'],
    url = about['__url__'],
    long_description = readme,
    long_description_content_type="text/markdown",
    install_requires = requires,
    packages = setuptools.find_packages(),  # 让setuptools自动发现包
    platforms = 'any',  # 包使用的平台
    classifiers = [
        'Programming Language :: Python :: 3',  # 采用编程语言
        'License :: OSI Approved :: GNU General Public License (GPL)',  # 采用的许可证协议
        'Operating System :: OS Independent',  # 操作系统
    ],
    entry_points = {
        'console_scripts': ['cwb=corpwechatbot.command:main']
    }

)