import setuptools

setuptools.setup(
    name="sprintl",
    packages=setuptools.find_packages(),
    extras_require={
        'jira': ['atlassian-python-api',],
        'dev': ['ipython', 'ipdb',],
    },
    entry_points={
        'console_scripts': [
            'extract_jira = sprintl_jira:main',
        ],
    },
)
