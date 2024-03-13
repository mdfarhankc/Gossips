# Gossips: Django Chat Project

**Gossips** is a real-time chat application built with Django and Django Channels. It enables users to create chat rooms, exchange messages, and engage in conversations in real-time.

## Features

- **User Authentication:** Users can sign up, log in, and authenticate to participate in chat rooms.

- **Create and Join Rooms:** Users can create their chat rooms and join existing ones.

- **Real-time Communication:** Utilizing Django Channels, Gossips provides real-time WebSocket communication for instant messaging.

- **User-friendly Interface:** The user interface is designed to be intuitive and responsive, ensuring a smooth chat experience.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/mdfarhankc/Gossips.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

   Access the application at [http://localhost:8000](http://localhost:8000).

## Usage

1. Create a user account or log in if you already have one.

2. Explore existing chat rooms or create your own.

3. Join a chat room and start chatting in real-time.

4. Customize your profile settings and preferences.

## Technologies Used

- Django
- Django Channels
- HTML, CSS, JavaScript, TailwindCSS
- Redis (for channel layer)

## Contributing

If you would like to contribute to Gossips, feel free to submit a pull request. Bug reports, feature requests, and feedback are also welcome!


---