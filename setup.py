from setuptools import setup

setup(
    name='aitutor',
    version='0.1.0',
    py_modules=['aitutor'],
    install_requires=[],
    entry_points='''
        [console_scripts]
        aitutor=aitutor:print_wrapped
    '''
)
