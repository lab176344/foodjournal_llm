# Food Journal LLM

Welcome to the **Food Journal LLM**! This application allows users to track their food intake, analyze ingredients, and maintain a personal food journal with ease. The app provides a seamless login and signup system, along with intuitive interfaces for logging meals and reviewing food entries. Basic architechture

![architecture drawio](https://github.com/lab176344/foodjournal_llm/assets/23631821/00e2a55e-8bd3-4d60-a220-bf1606a2768c)

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/)

### Clone the Repository

```bash
git clone https://github.com/your-username/food-journal-llm.git
cd food-journal-llm
```

### Install Dependencies

```bash
poetry install
```

## Configuration

### YAML Configuration

Before running the application, ensure you have a configuration file located at `config/config.yaml`. This file should contain the necessary credentials and settings for user authentication.

Example `config.yaml`:

```yaml
credentials:
  usernames:
    user1:
      name: "User One"
      password: "hashed_password"

cookie:
  name: "food_journal_cookie"
  key: "random_key"
  expiry_days: 30

pre-authorized:
  emails: []
```

### Environment Variables

The application requires an OpenAI API key for some of its functionalities. Create a `.env` file in the root directory and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_openai_api_key_here` with your actual OpenAI API key.

## Usage

### Running the Application

To start the application, run the following command:

```bash
poetry run streamlit run app.py
```

This will launch the Food Journal LLM in your default web browser.

### Application Workflow

1. **Navigation**: Use the sidebar to switch between the Login and Signup pages.
2. **Login**: Enter your username and password to log in. If successful, you will be greeted with a welcome message and access to the food journal features.
3. **Signup**: Register a new user by providing an email, username, and name. Once registered, you can log in with the new credentials.

## Features

- **User Authentication**: Secure login and signup system with cookie-based session management.
- **Food Journal Entry**: Log meals with details such as food items, meal category, date, time, and mood after eating.
- **Ingredient Analysis**: Analyze ingredients for nutritional content and other relevant data.
- **SQL Integration**: Store and retrieve journal entries from an SQL database.

## Contributing

We welcome contributions to enhance the functionality of this application. To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Open a pull request.

Please ensure your contributions adhere to the coding standards and are well-documented.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

Thank you for using **Food Journal LLM**! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

