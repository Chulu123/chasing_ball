from setuptools import find_packages, setup
import os
import glob
package_name = 'spawn_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name, ['worlds/empty_world.world']),
        ('share/' + package_name, ['launch/empty_world.launch.py']),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='chulu',
    maintainer_email='chulu@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
