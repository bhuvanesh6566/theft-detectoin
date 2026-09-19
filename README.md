<div align="center">

# theft detectoin

**A documented software project by [Bhuvaneshwaran S](https://github.com/bhuvanesh6566).**

[![GitHub](https://img.shields.io/badge/GitHub-bhuvanesh6566-181717?logo=github)](https://github.com/bhuvanesh6566)
[![Issues](https://img.shields.io/github/issues/bhuvanesh6566/theft-detectoin)](https://github.com/bhuvanesh6566/theft-detectoin/issues)

[Source Code](https://github.com/bhuvanesh6566/theft-detectoin) · [Report a Bug](https://github.com/bhuvanesh6566/theft-detectoin/issues)

</div>

---

## Table of Contents

- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## About

This README follows a consistent portfolio documentation format while preserving the repository's existing project-specific documentation.

## Features

- ✅ Project-specific functionality
- ✅ Documented setup and usage
- ✅ Extensible architecture

## Tech Stack

See the project-specific documentation below.

## Getting Started

Clone the repository and follow the project-specific instructions below.

```bash
git clone https://github.com/bhuvanesh6566/theft-detectoin.git
cd theft-detectoin
```

## Usage

Follow the commands and examples in the project documentation below.

## Project Structure

Refer to the repository tree and project documentation below.

## Roadmap

- [ ] Add screenshots or demo GIF
- [ ] Add automated testing documentation
- [ ] Expand troubleshooting documentation

## Contributing

Open an issue for bugs or feature requests, then submit a focused pull request.

## License

See [LICENSE](LICENSE) if present.

---

# Project Documentation

# Laptop Theft Detection System 🔐

A computer-vision project that detects motion/face activity and can send alerts through Telegram.

## Setup
```bash
pip install -r requirements.txt
```
Create `known_faces/` and add authorized reference photos. Configure Telegram credentials through environment/configuration rather than committing secrets.

## Run
```bash
python theft_detection.py
```

## Workflow
1. Monitor for movement
2. Perform face recognition when needed
3. Trigger an alarm for suspicious activity
4. Send an alert/photo through Telegram

> Use only on devices and environments you own or are authorized to monitor.