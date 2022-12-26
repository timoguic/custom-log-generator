from setuptools import find_packages, setup

setup(
    name="dolos-log-generator",
    version="0.2.0",
    packages=find_packages(),
    include_package_data=True,
    description="Versatile log generator with custom patterns and fields",
    long_description=open("README.md", "r").read(),
    install_requires=[
        "click",
        "dateparser",
        "faker",
        "pyyaml",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "dolos_make_logs = cli:make_logs",
        ],
    },
)
