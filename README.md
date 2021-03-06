<div align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Matlab_Logo.png/667px-Matlab_Logo.png" style="vertical-align: middle;" width="100px"/>
    <h2 style="vertical-align: middle; color:white;font-weight:bold;">MATLAB GRADER SCRAPER </h2>
</div>

---

# grader: powerful Python matlab grader scraping toolkit

[![Package Status](https://img.shields.io/pypi/status/pandas.svg)]()
[![Package Versions][pyversion-button]]()

[md-pypi]: https://pypi.org/project/Markdown/
[pyversion-button]: https://img.shields.io/pypi/pyversions/Markdown.svg
[python-markdown]: https://Python-Markdown.github.io/
[markdown]: https://daringfireball.net/projects/markdown/
[features]: https://Python-Markdown.github.io#Features
[available extensions]: https://Python-Markdown.github.io/extensions

## What is it?

**Grader** is a Python package that provides fast, flexible downloading of your matlab grader code
Check out [**matlab grader**][grader] for more information.

<div align="center">
  <img src="https://www.mathworks.com/products/matlab-grader/_jcr_content/mainParsys/band_copy_copy_12162/backgroundImage.adapt.1200x320.high.jpg/1594326389859.jpg"><br>
</div>

Grader produces files that contain the reference code and learner template with .m extension.
Grader can be used in Python scripts,
the Python and IPython shell.

## Main Features

Here are the things that grader does well:

- Easy matlab grader code scraping(`reference code`, `learner code`, `...`)

[grader]: https://www.mathworks.com/products/matlab-grader.html

## Upcoming Features

- Easy github and matlab grader synchronization
- Email notifications about students submissions and statistics

## Where to get it

The source code is currently hosted on GitHub at:
https://github.com/sarmientoF/grader.git

```sh
# PyPI
pip3 install git+https://github.com/sarmientoF/grader.git

```

## How to use it

- You must be logged with matlab grader account using `Firefox` browser

```python
import grader
grader.getGraderJson()
```

- This code will create a file called `myGrader.json`(this contains the structure of your grader courses, such as: Courses, Assignments, Problems ...)

```python
import grader

if __name__ == "__main__":
    grader.saveProblems() ## MUST BE INSIDE MAIN THREAD
```

- This code will create a folder called `codes`(this contains all the problems contained in your grader courses)

```sh
├── codes
│   ├── Electromagnetism
│   │   ├── Capacitance
│   │   │   ├── ProblemFivePartAEdit
│   │   │   │   ├── reference.m
│   │   │   │   └── starter.m
│   │   │   ├── ProblemFivePartBEdit
│   │   │   │   ├── reference.m
│   │   │   │   └── starter.m
│   │   │   ├── ProblemFourPartAEdit
│   │   │   │   ├── reference.m
│   │   │   │   └── starter.m
│   │   │   ├── ProblemFourPartBEdit
│   │   │   │   ├── reference.m
│   │   │   │   └── starter.m
.   .   .   .   .
.   .   .   .   .
.   .   .   .   .
```

## Dependencies

- [browser_cookie3](https://github.com/borisbabic/browser_cookie3)
- [lxml](https://github.com/lxml/lxml)

## Background

- 3rd year [Systems and Control Engineering](https://educ.titech.ac.jp/sc/eng/) undergrad student at Tokyo Institute of Technology .
- Intern at Pestalozzi Technology at IT [department](https://pestalozzi-tech.com/ja/company/members)
- Scholarship holder of Japan Ministry of Education, Culture, Sports, Science and Technology([MEXT](https://www.mext.go.jp/en/))
- [Android](https://play.google.com/store/apps/details?id=pestalozzi.tech.coachx), iOS, front end and backend developer

<div align="center">
  <img src="https://vprd.ust.hk/sites/vprd-prod.sites2.ust.hk/files/2019-02/Tokyo-Institute-of-Technology-Logo.png" height = "60">
    <img src="https://storage.googleapis.com/cdn_pestalozzitech_onlinecoaching/website/pestalozzi_technology.svg" height = "30" >
    <img src="https://www.tt.emb-japan.go.jp/files/100050878.jpg" height = "60" >
    
</div>

## Getting Help

For usage questions, contact by email [sarmiento](sarmiento:sarmiento.f.aa@m.titech.ac.jp).

## Contributing to grader

All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

Or maybe through using grader you have an idea of your own or are looking for something in the documentation and thinking ‘this can be improved’...you can do something about it!
