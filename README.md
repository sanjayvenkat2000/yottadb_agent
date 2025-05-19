# yottadb_agent

An LLM agent to assist in writing M test scripts. The agent integrates with GitLab to create various M artifacts.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)

## Features

- Generates M test scripts using LLM
- Integrates with GitLab for artifact management
- Automated test script suggestions
- Eventually will learn enough to be a good M programmer...

## Requirements

- Python 3.8+
- [Poetry](https://python-poetry.org/) (for dependency management and virtual environments)
- Git

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/sanjayvenkat2000/yottadb_agent.git
    cd yottadb_agent
    ```

2. **Install Poetry (if not already installed):**
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    Or follow the [official Poetry installation instructions](https://python-poetry.org/docs/#installation).

3. **Install dependencies and set up virtual environment:**
    ```bash
    poetry install
    ```

## Usage

1. **Activate the Poetry virtual environment:**
    ```bash
    poetry shell
    ```
    
2. **Set the required environment variables:**
    ```bash
    # Set your API keys (replace the values with your actual keys)
    export GOOGLE_API_KEY=your_google_api_key
    export GITLAB_ACCESS_TOKEN=your_gitlab_access_token
    ```

3. **Run the test suggestion agent: (review the code and update as required)**
    ```bash
    python yottaagent/test_suggestion_agent.py
    ```
