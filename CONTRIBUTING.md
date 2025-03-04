# Contributing to ZeenChat

Thank you for considering contributing to ZeenChat! Your help is greatly appreciated, whether it’s fixing a bug, adding a new feature, or improving documentation.

## How to Contribute

### 1. Fork the Repository
First, fork the repository to your GitHub account:
- Go to [ZeenChat Repo](https://github.com/frzn23/zeenchat)
- Click on the **Fork** button in the top right corner
- Clone your forked repository to your local machine:
  ```bash
  git clone https://github.com/your-username/zeenchat.git
  cd zeenchat
  ```

### 2. Create a New Branch
Before making any changes, create a new branch for your contribution:
```bash
git checkout -b feature-name
```
Replace `feature-name` with a meaningful name describing your contribution.

### 3. Set Up Your Development Environment
Ensure you have all dependencies installed:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
pip install -r requirements.txt
```
Also, ensure **Redis** is installed and running before testing the chat functionality.

### 4. Make Your Changes
- Follow the existing coding style
- Write clear and concise commit messages
- Ensure your changes do not break existing functionality

### 5. Run Tests
Before submitting your changes, test the application:
```bash
python manage.py test
```

### 6. Commit and Push Your Changes
Once your changes are tested, commit and push them to your fork:
```bash
git add .
git commit -m "Added feature: short description"
git push origin feature-name
```

### 7. Create a Pull Request (PR)
- Navigate to the **original ZeenChat repository**
- Click on **Pull Requests** → **New Pull Request**
- Select your fork and branch, then submit the PR
- Add a brief description of your changes

## Issues and Feature Requests
- Check the [Issues Page](https://github.com/frzn23/zeenchat/issues) to see if your issue already exists
- If not, create a new issue with a clear title and description
- Label the issue appropriately (e.g., `bug`, `enhancement`, `documentation`)

## Code Guidelines
- Keep code modular and well-commented
- Use meaningful variable and function names
- Avoid unnecessary dependencies

## Community Guidelines
- Be respectful and supportive of all contributors
- Provide constructive feedback
- Focus on making ZeenChat better for everyone

## Contact
For any questions, feel free to:
- Open an issue in the repository
- Email the maintainer at **farzeenghaus23@gmail.com**

Happy coding! 🚀

