from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3'
]

setup(
    name='unofficialkeepsolidvpn',
    version='0.0.7',
    description='unofficial keepsolid wireguard fetcher module',
    long_description=open('README.md').read(),
    url='https://github.com/Retch/keepsolid-vpn-wg-fetch',
    author='Retch',
    author_email='retch@mailpoof.com',
    license='GPL-3',
    classifiers=classifiers,
    keywords='keepsolid',
    packages=find_packages(),
    install_requires=['selenium>=3.141.0', 'urllib3>=1.25.9', 'requests==2.26.0']
)