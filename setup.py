from setuptools import setup, find_packages
import admin_storage


def read_file(path):
    with open(path, 'r') as fd:
        return fd.read()

setup(
    name='django-admin-storage',
    version=admin_storage.__version__,
    url=admin_storage.__url__,
    description=admin_storage.__doc__,
    long_description=read_file('README.rst'),
    author=admin_storage.__author__,
    author_email=admin_storage.__email__,
    license=admin_storage.__license__,
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
