from setuptools import setup, find_packages

setup(
    name='lotus',
    version='0.1.0',
    author='kevinSpider',
    author_email="zhangyang.spider@gmail.com",
    description='spider tools', 
    long_description=open('README.md').read(),  # 从 README.md 中读取长描述
    long_description_content_type='text/markdown',  # 长描述的内容类型
    url='https://github.com/kevinspider/lotus',  # 项目主页
    packages=find_packages(),  # 自动发现并包含所有包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # Python 版本要求
    install_requires=[
        "curl_cffi>=0.7.4",
        "loguru>=0.6.0"
    ],
    include_package_data=False,  # 包含包内的非代码文件
    zip_safe=False,  # 如果你的包不支持在压缩文件中运行，设置为 False
)