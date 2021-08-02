import os

from setuptools import setup


if os.environ.get('CI_COMMIT_TAG'):
    version = os.environ['CI_COMMIT_TAG']
elif os.environ.get('VERSION'):
    version = os.environ['VERSION']
else:
    version = None

if version:
    setup(
        name='easylog',
        version=version,
        description='logger for telemetry',
        long_description='logger for telemetry',
        long_description_content_type='text/plain',
        author='Jayden',
        author_email='hongkang@hongkang.name',
        license='MIT',
        packages=['easylog'],
        url='http://**.**.**.**:18080/keystone/telemetry/easylog',
        zip_safe=False,
        install_requires=[
        ],
        dependency_links=[
            "http://**.**.**.**:31187/simple"
        ],
        python_requires='>=3.7, <=3.8',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Telemetry',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
        ],
        project_urls={
            'Source': 'http://**.**.**.**:****/keystone/telemetry/easylog',
        },
    )
