<p align="center">
  <img src="https://i.ibb.co/C5XXyCzd/Whats-App-Image-2026-05-30-at-10-01-42-AM.jpg" width="300" height="300" style="border: 4px solid #00ff00; border-radius: 50%; box-shadow: 0 0 40px #00ff00;" alt="HALAKU WOLF INTELEGENCE LOGO" />
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=900&size=36&duration=2000&pause=700&color=00FF00&center=true&vCenter=true&width=700&height=90&lines=%F0%9F%90%BA+WOLF+INTELEGENCE;%E2%9A%94%EF%B8%8F+HALAKU+WOLF+INTELEGENCE;%F0%9F%95%8C+ISLAMIC+CYBER+UNIT;%F0%9F%92%80+AGAINST+ISRAEL+AND+OPPRESSORS;%F0%9F%94%A5+HACK.+DEFEND.+CONQUER." alt="Typing SVG" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/STATUS-🟢_ACTIVE_–_HUNTING-brightgreen?style=for-the-badge&labelColor=000000"/>
  <img src="https://img.shields.io/badge/TEAM-ISLAMIC_CYBER_UNIT-00ff00?style=for-the-badge&labelColor=000000"/>
  <img src="https://img.shields.io/badge/LEADER-HALAKU_WOLF-ff0000?style=for-the-badge&labelColor=000000"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/WOLFSTRA-v2.0-red?style=for-the-badge&logo=python" alt="Version"/>
  <img src="https://img.shields.io/badge/DIOS-Edition-green?style=for-the-badge" alt="DIOS"/>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/License-EDUCATIONAL-yellow?style=for-the-badge" alt="License"/>
</p>

<div align="center">
</div>

<h1 align="center">🐺 WOLFSTRA v2.0 - DIOS EDITION 🐺</h1>

<p align="center">
  <b>UNION Based SQL Injection Exploitation Framework</b><br>
  <i>Column Finder | Union Injector | Data Dumper | DIOS Generator</i>
</p>

<p align="center">
  <a href="https://github.com/halakuwolfintelegence/">
    <img src="https://img.shields.io/badge/GitHub-halakuwolfintelegence-blue?style=social&logo=github" alt="GitHub"/>
  </a>
  <a href="https://www.instagram.com/wolf.intelligence">
    <img src="https://img.shields.io/badge/Instagram-@wolf.intelligence-red?style=social&logo=instagram" alt="Instagram"/>
  </a>
</p>

<hr>

## 📋 Table of Contents

- [📖 Introduction](#-introduction)
- [✨ Features](#-features)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
  - [Auto Mode](#-auto-mode-recommended)
  - [Manual Mode](#-manual-mode)
- [📊 Step-by-Step Workflow](#-step-by-step-workflow)
  - [1️⃣ Column Finder](#1️⃣-column-finder)
  - [2️⃣ Vulnerable Column Detection](#2️⃣-vulnerable-column-detection)
  - [3️⃣ Database Information Gathering](#3️⃣-database-information-gathering)
  - [4️⃣ DIOS - Dump In One Shot](#4️⃣-dios---dump-in-one-shot)
- [🎯 Example Output](#-example-output)
- [🔧 Advanced Commands](#-advanced-commands)
- [📁 Project Structure](#-project-structure)
- [🛡️ Legal Disclaimer](#️-legal-disclaimer)
- [🙏 Credits](#-credits)

<hr>

## 📖 Introduction

**WOLFSTRA** is a powerful **UNION-based SQL Injection exploitation framework** developed by **Wolf Intelligence**. This tool automates the process of:

1. **Finding column count** in vulnerable SQLi parameters
2. **Detecting injectable columns** for string/date output
3. **Extracting database information** (version, user, database name, hostname)
4. **Generating DIOS (Dump In One Shot)** payloads for rapid data extraction

The tool features a beautiful **box-style terminal UI** with color-coded output for better readability.

<hr>

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **Column Finder** | ORDER BY + UNION SELECT NULL techniques with auto-fallback |
| 🎯 **Vulnerable Column Detection** | Identifies which columns can output string data |
| 🗄️ **Database Info Grabber** | Extracts version, user, database name, hostname, datadir |
| 📋 **Table Dumper** | Lists all tables from target database |
| 📑 **Column Dumper** | Lists all columns from specific table |
| 💾 **Data Dumper** | Dumps actual data from tables with custom column selection |
| 🚀 **DIOS Generator** | Generates ready-to-use Dump In One Shot payloads |
| 🎨 **Box-Style UI** | Professional terminal interface with color-coded sections |
| 🤖 **Auto Mode** | One-command full exploitation pipeline |

<hr>

## ⚙️ Installation

### Prerequisites

- Python 3.x
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/halakuwolfintelegence/WOLFSTRA.git

# Navigate to directory
cd WOLFSTRA

# Install dependencies
pip install -r requirements.txt
