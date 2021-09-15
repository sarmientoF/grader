from setuptools import setup, find_packages

setup(
    name='grader',
    version='1.0.0',
    description='Matlab Grader management package',
    url='git@github.com/sarmientoF/grader.git',
    author='Fernando Sarmiento',
    author_email='fsarmientod@uni.pe',
    license='unlicense',
    package_dir={"": "lib"},
    packages=find_packages("lib"),
    zip_safe=False,
    install_requires=[
        "GitPython",
        "lxml",
    ]
)
