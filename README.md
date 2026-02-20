# Web LuXe

[ Web LuXe: High-Dimensional Robust Inference ]

## Overview
Web LuXe is a high-dimensional probabilistic inference engine designed to analyze and monitor web application responses scientifically. It builds a robust statistical baseline using advanced features like entropy, DOM structure, network metrics, and more. It detects anomalies with high confidence across multi-system environments.

## Developer
This project is experimental and under active development. Beginner programmer looking for collaboration and support. For support or contributions, contact the owner: Telegram @LU_XI  

## Features
- Multi-dimensional feature extraction (30+ features)
- Robust probabilistic inference using MinCovDet (Fast-MCD)
- Chi-square thresholding for anomaly detection
- Noise reduction with DOM analysis
- Adaptive calibration with outlier rejection
- Multi-system support: Windows, Linux, Termux, iSH
- Extendable for payload engines, extraction modules, fingerprinting

## Installation

### Windows
1. Install Python 3.11 or above from https://www.python.org/downloads/windows/
2. Open PowerShell and run:
git clone https://github.com/LUXEF7LK/WebLuXe.git
cd WebLuXe
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py

### Linux
1. Install Python 3.11+ and pip
sudo apt update && sudo apt install python3 python3-pip git -y
git clone https://github.com/LUXEF7LK/WebLuXe.git
cd WebLuXe
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 main.py

### Termux
1. Install Python and git
pkg update && pkg install python git -y
git clone https://github.com/LUXEF7LK/WebLuXe.git
cd WebLuXe
pip install --upgrade pip
pip install -r requirements.txt
python main.py

### iSH (iOS Shell)
1. Install Python3 and git
apk update && apk add python3 py3-pip git
git clone https://github.com/LUXEF7LK/WebLuXe.git
cd WebLuXe
pip3 install --upgrade pip
pip3 install -r requirements.txt
python3 main.py

## Notes
- This project is experimental and in active development.
- All features are designed for research and educational purposes.
- Contact the developer for questions or contributions: Telegram @LU_XI
- GitHub username: LUXEF7LK
