# Desk Fit

Desk Fit is a web application designed to help you stay active while working. Initially conceived as a simple timer to encourage physical activity during breaks, the app has evolved into a comprehensive tool that allows you to create and organize workouts, schedule weekly routines, and track your performance.

## Distinctiveness and Complexity

**Desk Fit** stands out from other course projects due to its innovative features and the advanced technologies used:

1. **Use of Web Worker for Timer**: The timer component uses a Web Worker to ensure accuracy even when the app is in the background. This approach addresses the common issue of timers slowing down when the browser is not active.

2. **Sortable.js for Dynamic Workout Organization**: Integration with Sortable.js allows for the management of workouts through drag-and-drop functionality. The app lets you assign a workout to each day of the week, with logic that prevents adding more than one workout per day, dynamically modifying sorting options.

3. **Personalized Scheduling and Tracking**: Users can not only create custom workouts but also plan their entire week of training. Additionally, they can monitor the number of repetitions performed for each exercise, making Desk Fit a complete fitness tool.

These features not only increase the complexity of the project but also make it a versatile and useful application that goes well beyond the minimum course requirements.

## Key Features

- **Active Timer with Web Worker**: Stay active during work hours using the timer that reminds you to take a break and move.
- **Workout Creation and Management**: Create custom workouts with exercises, sets, repetitions, and rest times.
- **Weekly Workout Planning**: Organize your workouts throughout the week, assigning each workout to a specific day.
- **Performance Tracking**: Keep track of the number of repetitions performed for each exercise.

## Technologies Used

- **Django**: Backend framework for database management and server-side logic.
- **Django Rest Framework**: For handling REST APIs.
- **Django Crispy Forms**: For advanced form handling.
- **Bootstrap 5**: For responsive UI design.
- **Sortable.js**: For workout sorting and drag-and-drop functionality.
- **Webpack**: For managing and bundling JavaScript files.
- **JavaScript (with Web Worker)**: To manage the timer in the background with precision.

## Django Models

- **ActiveBreaksSettings**: Manages user settings for work and break timers.
- **Workout**: Model for user-created workouts.
- **Exercise**: Represents a single exercise with its attributes (muscle groups, difficulty, etc.).
- **WorkoutExercise**: Manages the relationship between workouts and exercises, including sets, repetitions, and work/rest times.
- **PlannedWorkout**: Organizes workouts by days of the week.

## Design and User Interface

The design of **Desk Fit** is based on Bootstrap 5 to ensure a clean and responsive user interface. A central part of the design is the integration with Sortable.js, allowing users to organize workouts via drag-and-drop. This functionality has been optimized to ensure that only one workout can be assigned to each day, dynamically modifying the sorting properties.

## Mobile Responsiveness

The application is sufficiently mobile-responsive, allowing users to access and use key features on mobile devices. However, some areas could be further improved for optimal usability.

## Challenges Faced

1. **Timer Precision in the Background**: One of the main challenges was managing the timer when the application is in the background. Using a Web Worker solved the issue, ensuring the timer remains synchronized even when the browser deprioritizes resources.

2. **Dynamic Management with Sortable.js**: Sortable.js does not natively support dynamic updating of sorting properties. I implemented a solution that prevents adding new workouts to a day once one has been assigned, dynamically updating the sorting options.

## Project Installation and Setup

1. **Clone the repository**

2. **Create a virtual environment and install requirements**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

3. **Run migrations and start the server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

4. **Access the application**:
   Open your browser and go to `http://127.0.0.1:8000`.

### Project Structure

- **`final-project/`**: Root directory containing all the project files and directories.
  - **`assets/`**: Contains assets used in the project.
    - **`javascript/`**: 
      - **`index.js`**: Contains the code for the `sortable.js` functionality, enabling the drag-and-drop feature for organizing workouts.
  
  - **`final_project/`**: Django project directory containing the core configuration files.
    - **`__init__.py`**: Initializes the Django project as a Python package.
    - **`asgi.py`**: ASGI config for deploying the project using ASGI servers.
    - **`settings.py`**: Contains all the configuration settings for the Django project, including installed apps, middleware, database settings, and more.
    - **`urls.py`**: Manages the URL routing for the entire project, directing requests to the appropriate app.
    - **`wsgi.py`**: WSGI config for deploying the project using WSGI servers.

  - **`main/`**: Django application directory where the core functionality of the app resides.
    - **`migrations/`**: Directory containing migration files that manage changes to the database schema.
    - **`static/`**: Contains all the static files (CSS, JavaScript, images, etc.) used in the app.
      - **`audios/`**: Contains audio files used in the application.
      - **`images/`**: Contains image files used in the application.
      - **`main/`**: 
        - **`script.js`**: Contains the `Timer` class and all logic related to the active break timer.
        - **`styles.css`**: Contains the custom CSS styles used throughout the application.
        - **`timer_worker.js`**: Web Worker script that handles the timer logic in the background, communicating with `script.js`.
      - **`favicon.ico`**: The favicon used by the application.
      - **`index-bundle.js`**: Webpack bundled JavaScript file.
      
    - **`templates/`**: Contains all HTML templates used in the app.
      - **`main/`**: Contains templates related to the main functionality of the application.
        - **`index.html`**: The landing page of the application.
        - **`timer.html`**: Template for the timer page where the user can view and interact with the active break timer.
        - **`workout_list.html`**: Lists all workouts created by the user.
        - **`workout_detail.html`**: Displays details of a specific workout, including exercises and sets.
        - **`plan_week.html`**: Allows users to drag-and-drop workouts into specific days of the week using `sortable.js`.
      - **`registration/`**: Contains templates for user authentication.
        - **`login.html`**: Template for user login.
        - **`signup.html`**: Template for user registration.

    - **`__init__.py`**: Initializes the `main` application as a Python package.
    - **`admin.py`**: Registers models to be managed via Django's admin interface.
    - **`apps.py`**: Configuration file for the `main` application.
    - **`forms.py`**: Contains custom Django forms for user input, such as creating and editing workouts.
    - **`models.py`**: Defines the database models, including `ActiveBreaksSettings`, `Workout`, `Exercise`, `WorkoutExercise`, and `PlannedWorkout`.
    - **`serializers.py`**: Defines serializers used in Django REST framework to convert complex data types, such as querysets and model instances, into JSON format.
    - **`urls.py`**: Manages the URL routing specific to the `main` application.
    - **`views.py`**: Contains the application’s view logic, including the handling of user requests, rendering templates, and managing form submissions.

  - **`node_modules/`**: Directory containing all npm packages required for the project.
  - **`.env`**: Environment file containing sensitive information like API keys and database credentials (typically not included in version control).
  - **`db.sqlite3`**: SQLite database file used by the Django project.
  - **`manage.py`**: Command-line utility for interacting with the Django project (e.g., running the server, applying migrations).
  - **`package-lock.json`**: Automatically generated file that describes the exact version of npm packages installed.
  - **`package.json`**: Lists the npm packages and scripts required for the project.
  - **`README.md`**: Documentation file that provides an overview of the project, including setup instructions and usage.
  - **`requirements.txt`**: Lists all Python packages required to run the application, ensuring consistency across different development environments.
  - **`webpack.config.js`**: Configuration file for Webpack, specifying how JavaScript files and other assets should be processed and bundled.
