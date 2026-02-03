from setuptools import setup, find_packages

setup(
    name="pm_next_cycle_tracker",
    version="1.0.0",
    description="A local dashboard for tracking Redmine story readiness.",
    author="Your Name",
    packages=find_packages(),
    py_modules=["app"],  # Includes app.py
    include_package_data=True,
    install_requires=[
        "flask",
        "flask-cors",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "start-tracker=app:main",
        ],
    },
)