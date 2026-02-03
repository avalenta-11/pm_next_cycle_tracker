from setuptools import setup, find_packages

setup(
    name="pm_next_cycle_tracker",
    version="1.0.2", # Bump version
    packages=find_packages(), # This automatically finds the 'pm_tracker' folder
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-cors",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            # POINT TO THE NEW LOCATION: folder.file:function
            "start-tracker=pm_tracker.app:main",
        ],
    },
)