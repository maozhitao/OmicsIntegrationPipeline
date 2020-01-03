from setuptools import setup
from setuptools import find_packages

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name                            = 'meta-omics',
    version                         = '0.1.0',
    packages                        = find_packages(),
    entry_points                    = {
        'console_scripts': ['meta-omics=omics.bin.run:main'],
    },
    description                     = 'Omics metadata integration package',
    author                          = 'Fangzhou Li',
    author_email                    = 'fzli0805@gmail.com',
    url = 'https://github.com/fangzhouli/meta-omics',
    # download_url = 'https://github.com/fangzhouli/DistributedMissForest/archive/v_01.tar.gz',
    # keywords = ['imputation', 'cluster computing'],
    install_requires                = [
        'biopython'
    ],
    long_description                = long_description,
    long_description_content_type   = 'text/markdown',
    # license='MIT',
    # classifiers=[
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'Topic :: Software Development :: Build Tools',
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 3',
    # ],
)