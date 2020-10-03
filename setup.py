from setuptools import setup

setup(
    name='grader',
    version='1.0.0',
    description='Matlab Grader management package',
    url='git@github.com/sarmientoF/grader.git',
    author='Fernando Sarmiento',
    author_email='fsarmientod@uni.pe',
    license='unlicense',
    packages=['grader'],
    package_dir={'.': 'grader'},
    zip_safe=False,
    install_requires=[
        "browser_cookie3",
        "lxml",
    ]
)
