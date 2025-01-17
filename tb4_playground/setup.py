from setuptools import find_packages, setup

package_name = 'tb4_playground'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='khaled',
    maintainer_email='khaledgabr77@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'odom_listener = tb4_playground.odom_listener:main',
            'velocity_pub = tb4_playground.velocity_pub:main',
        ],
    },
)
