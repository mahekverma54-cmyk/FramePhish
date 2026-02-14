# FramePhish – Clickjacking Scanner & PoC Generator

**Interactive terminal tool to detect basic clickjacking vulnerabilities and instantly generate deceptive overlay Proof-of-Concept HTML files.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/FramePhish?style=social)

## What it does

FramePhish is a lightweight, bug-bounty-focused Python script that helps security researchers and hunters quickly identify clickjacking (UI redressing) vulnerabilities:

- Prompts for a target URL (interactive mode – paste one after another)
- Checks critical anti-framing headers:
  - `X-Frame-Options` (DENY or SAMEORIGIN)
  - `Content-Security-Policy` frame-ancestors directive
- Automatically prepends `https://` if missing
- Displays a colorful verdict: **VULNERABLE** (red) or **Protected** (green)
- If vulnerable → instantly creates a clean, styled **HTML PoC** file containing:
  - The target page loaded in a full-screen iframe
  - Fake overlay buttons ("LOGIN NOW", "CONFIRM TRANSFER", etc.)
  - Timestamp and bug-bounty watermark
- (Optional) Attempts to auto-open the PoC in your default browser

Perfect for fast triage of login pages, admin panels, payment forms, profile settings, etc.

## Features

- Fully interactive CLI – no arguments needed
- Beautiful colored terminal output (using colorama)
- Smart URL normalization
- Graceful error handling & Ctrl+C exit
- Minimal dependencies: only `requests` + `colorama`
- Generates report-ready PoC files with professional styling
- Designed for speed and ease during bug bounty hunting

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/FramePhish.git
cd FramePhish
pip install requests colorama
```
## Usage
```
python framephish.py
```


███████╗██████╗  █████╗ ███╗   ███╗███████╗██████╗ ██╗  ██╗██╗███████╗██╗  ██╗
██╔════╝██╔══██╗██╔══██╗████╗ ████║██╔════╝██╔══██╗██║  ██║██║██╔════╝██║ ██╔╝
█████╗  ██████╔╝███████║██╔████╔██║█████╗  ██████╔╝███████║██║███████╗█████╔╝
██╔══╝  ██╔══██╗██╔══██║██║╚██╔╝██║██╔══╝  ██╔══██╗██╔══██║██║╚════██║██╔═██╗
██║     ██║  ██║██║  ██║██║ ╚═╝ ██║███████╗██║  ██║██║  ██║██║███████║██║  ██╗
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝

Enter URL to scan (Press Enter to exit)
URL → example.com/login

Scanning → https://example.com/login

┌──────────────────────────────────────────────┐
│ VULNERABLE                                  │
└──────────────────────────────────────────────┘

Reason : Missing X-Frame-Options and CSP frame-ancestors
PoC    : framephish_poc_example_com_login.html
Action : Open the file in browser to view demo
Tip    : Capture screenshot/video for your report

## 👨‍💻 Author
Developed for security research & bug bounty workflow optimization.
