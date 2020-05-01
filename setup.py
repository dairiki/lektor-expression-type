import ast
import io
import re

from setuptools import setup

version = '0.1.dev1'

with io.open('README.md', 'rt', encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r'description\s+=\s+(?P<description>.*)')

with open('lektor_expression_type.py', 'rb') as f:
    description = str(ast.literal_eval(_description_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    author='Jeff Dairiki',
    author_email='dairiki@dairiki.org',
    description=description,
    keywords='Lektor plugin',
    license='BSD',
    long_description=readme,
    long_description_content_type='text/markdown',
    name='lektor-expression-type',
    py_modules=['lektor_expression_type'],
    # url='[link to your repository]',
    version=version,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Framework :: Lektor',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Office/Business :: Scheduling',
    ],
    entry_points={
        'lektor.plugins': [
            'expression-type = lektor_expression_type:ExpressionTypePlugin',
        ]
    }
)
