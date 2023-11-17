# DjCMS
DjCMS is a Django-based web application that allows users to upload their own articles and embed YouTube videos.
This project is perfect for bloggers, content creators, and website owners who want to have full control over their content.

## Features
- User authentication and authorization
- Article creation, editing, and deletion
- YouTube video embedding
- Responsive design
- Search functionality
- Like system
- Commenting and replying system
- Categorising (tagging) system
- Bookmark system

## Installation
1. Clone the repository:
```bash
git clone https://github.com/dev-bittu/djcms.git
```
2. Create a virtual environment and activate it:
```bash
pip install virtualenv
virtualenv env
source env/bin/activate  # for Linux/MacOS
env\Scripts\activate.bat  # for Windows
```
3. Install the dependencies:
```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory of the project and add the following variables:
```bash
SECRET_KEY=your_secret_key_here
DEBUG=True
```
5. Run the migrations & migrate:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser account:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Open your browser and go to http://localhost:8000/admin to access the admin panel. 
Log in with the superuser account you created earlier.

## Usage
0. Login as author (create superuser; superuser is an author).
1. To create a new blog, go to Manage > Blogs and then click on Create New button.
2. Fill in the required fields (title, content, categories) and add a featured image.
3. To embed a YouTube video, copy the video ID from the URL (e.g. https://www.youtube.com/watch?v=abcdefg) and paste it into the "YouTube video ID" field.
4. Click on the "Publish" button to publish the blog.
5. To view the blog on the website, go to http://localhost:8000/latest in your browser, then select blog what you want to read.
6. To search for blogs, use the search bar on the top of the website (navbar).
7. To leave a comment on an blog, scroll down to the bottom of the blog page and fill in the comment form.

# ToDo
- Add forget password
- Share blogs
- Change password
- Profile
- User logo
- Notification system

## Contributing
Contributions are welcome!
If you find a bug or want to suggest a new feature, please open an issue on GitHub.
Pull requests are also appreciated.

## License
This project is licensed under the MIT License.
See the LICENSE file for details.
