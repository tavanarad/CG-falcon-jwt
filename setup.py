from setuptools import setup, find_packages

with open('requirements.txt', 'r') as reqs:
    install_req = []
    install_req.extend(reqs.read().split('\n'))

setup(
    name='CheetaJWT',
    version='1.3',
    packages=find_packages(),
    url='https://github.com/tavanarad/CG-falcon-jwt',
    license='MIS',
    author='Morteza Tavanarad',
    author_email='tavanarad@gmail.com',
    description='A falcon middleware to handle the JWT header',
    install_requires=install_req
)
