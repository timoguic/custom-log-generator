from setuptools import find_packages, setup

setup(
    name="dolos-log-generator",
    version="0.1.1",
    packages=find_packages(),
    include_package_data=True,
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
