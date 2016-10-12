from setuptools import setup

setup(name='grammaregex',
      version='0.1.3',
      description='grammaregex - library for matching and finding tree sentence in regex-like way',
      long_description='This library allows you to find single tokens in sentences or match sentence by grammar regex-like expressions.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Science/Research',
      ],
      keywords='nlp text mining text extraction',
      url='https://github.com/krzysiekfonal/grammaregex',
      author='Krzysztof Fonal',
      author_email='krzysiek.fonal@gmail.com',
      license='MIT',
      packages=['grammaregex'],
      install_requires=[
          'spacy',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=True)
