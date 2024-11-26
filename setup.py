from setuptools import setup, find_packages

setup(
    name="mzk_digitization_registry",
    version="0.0.1",
    description="Partial Digitization Registry API client",
    author="Robert Randiak",
    author_email="randiak@mzk.com",
    packages=find_packages(),
    install_requires=["lxml", "pydantic", "requests"],
    setup_requires=["wheel"],
    python_requires=">=3.6",
)
