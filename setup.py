from setuptools import setup, find_packages
import pony_admin


def read_file(path):
    with open(path, 'r') as fd:
        return fd.read()

setup(
    name='django-admin-storage',
    version=pony_admin.__version__,
    url=pony_admin.__url__,
    description=pony_admin.__doc__,
    long_description=read_file('README.rst'),
    author=pony_admin.__author__,
    author_email=pony_admin.__email__,
    license=pony_admin.__license__,
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        'Framework :: Django',
    ],
    packages=find_packages(exclude=['tests.runtests.main']),
    include_package_data=True,
    test_suite='tests.runtests.main',
    install_requires=read_file('requirements.txt').splitlines(),
)
