# Django Blog API

This is a simple Django project implementing a RESTful API for a blog application. It allows users to register, login,logout, create posts, and perform various operations on posts.

## Getting Started

To run this project locally, follow these steps:

### Prerequisites

- Python 3
- virtualenv (optional, but recommended)

### Installation

1. Clone the repository: git clone https://github.com/Elsaeed97/blog.git

2. Navigate to the project directory: cd blog

3. (Optional) Create and activate a virtual environment: virtualenv venv

- Activate Virtualenv: source venv/bin/activate

4. Install dependencies: pip install -r requirements.txt

### Usage

1. Run database migrations:

- python manage.py makemigrations
- python manage.py migrate

2. Run the development server: python manage.py runserver

### Running Tests

- To run tests, use the following command: python manage.py test
