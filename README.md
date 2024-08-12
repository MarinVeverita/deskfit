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

## Project Structure

- **desk_fit/**: Main application directory for Django.
- **templates/**: Contains HTML templates for the frontend.
- **static/**: Contains static files such as CSS, JavaScript, and images.
- **models.py**: Defines the Django models used in the app.
- **views.py**: Contains the logic for the application's views.
- **urls.py**: Manages URL routing.
