# 🛠️ Project Overview

This repository contains two versions of the project:

- **🔒 Secure Version (`main` branch)** – The latest stable and secure implementation.
- **⚠️ Unsecure Version (`unsecure-version2.0` branch)** – An older, insecure version for reference purposes only.

## 📂 Branch Structure

| Branch | Description |
|--------|------------|
| `main` | Secure and stable version of the project. |
| `unsecure-version2.0` | An older version with known security issues. Use for research/testing only. |

## 🚀 Getting Started

### Cloning the Repository
To clone the repository and switch between versions, use the following commands:

```sh
# Clone the repository
git clone https://github.com/your-username/your-repository.git
cd your-repository

# Switch to the secure version
git checkout main

# OR switch to the unsecure version
git checkout unsecure-version2.0
```

## 📦 Required Dependencies
Ensure you have the following Python packages installed before running the project:

```sh
pip install pyOpenSSL Werkzeug python-dotenv django-extensions Django
```

## 🔐 Security Notice
The `unsecure-version2.0` branch contains known vulnerabilities and is **not recommended for production use**. Always use the **main** branch for a secure and up-to-date version.

