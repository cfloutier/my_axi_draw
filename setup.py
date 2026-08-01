"""
Based on https://github.com/pypa/sampleproject

"""

# Always prefer setuptools over distutils
import pathlib
import setuptools

# install_requires is dynamically created (below) and therefore cannot easily be
# specified in pyproject.toml, so it is specified here.

install_requires = [
    "pyaml>=6",
    "customtkinter>=5",
    "coloredlogs>=15",
    # axidraw internal fork — install locally with: pip install -e C:\dev\__tracer\api\AxiDraw_API\axidrawinternal_whl
    # or on other machines: pip install git+https://github.com/cfloutier/axidrawinternal.git
    "axidrawinternal @ git+https://github.com/cfloutier/axidrawinternal.git",
]


here = pathlib.Path.absolute(pathlib.Path(__file__).parent)

setuptools.setup(
    packages=setuptools.find_packages(exclude=["venv", "docs", "test"]),
    install_requires=install_requires,
)
