# Winly
Beautiful MT5 Trade History Analyzer with standalone .exe, made with python
# 🏆 Winly - MT5 Trade History Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**Winly** is a simple, beautiful desktop app that connects to your MetaTrader 5 terminal and instantly analyzes your real trading history.

It shows you:
- Your actual **win rate**
- Your **best performing pair**
- Your **most traded pair**
- Clean stats (deposits, swaps, commissions, bonuses, etc. are automatically filtered out)

Perfect for forex, gold, indices, and CFD traders who want honest feedback on their performance.

---

## ✨ Features

- Modern and easy-to-use Tkinter GUI
- One-click full trade history analysis
- Smart symbol filter (ignores fake/deposit operations)
- Shows: Current Balance • Total Real Trades • Win Rate • Smart Recommendation
- Works with **any MT5 broker** (FBS, IC Markets, Exness, etc.)
- Nothing is sent over the internet

---

## ⚠️ Important – Please Read Before Using

> Make sure to read the readme file that comes with this app for best results and to avoid common issues, such as:
> 
> - Incorrect server name (check exact name on MT5 login screen)
> - Wrong MT5 path (must point to `terminal64.exe` or `terminal.exe`)
> - Using a demo or new account with no history

---

## 📥 Installation & Usage

### Option 1: Run from Source (Recommended)

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/Winly.git
   cd Winly
   python winly.py

2. Install the only dependency:
   ```bash
   pip install MetaTrader5
   
3. Run the app:
   ```bash
   python winly.py

**Direct Download (Recommended)**  
→ [Winly.exe (Windows)](https://github.com/yourusername/Winly/releases/latest/download/Winly.exe)

### Option 2: Standalone .exe (No Python needed)

## 🚀 How to Use

Open Winly
Enter your Account ID, Password, and Server (exactly as shown in MT5)
Click Browse → select your MT5 terminal64.exe
(usually C:\Program Files\MetaTrader 5\terminal64.exe)
Click Analyze My Trades
Wait a few seconds → results appear!

Tip: Use a real account with at least 1–2 months of trading for meaningful results.

## 📊 What It Analyzes

Only closed trades (DEAL_ENTRY_OUT)
Only real trading symbols (EURUSD, XAUUSD, GBPJPY, NAS100, etc.)
Automatically skips: deposits, withdrawals, swaps, commissions, bonuses, internal transfers, etc.
Calculates win rate and profit per symbol


## 🔒 Security & Privacy

Your login details are never saved to disk
The app only connects locally to your own MT5 terminal
All analysis happens on your computer

Security Note:
Before pushing to GitHub, remove the default account/password/server values from winly.py (lines with value="...").

## 🛠 Tech Stack

Python 3
Tkinter (GUI)
MetaTrader5 Python package
Built for Windows (tested on Windows 10 & 11)


## 📌 Known Limitations

Windows only (because of MT5 path)
Requires MetaTrader 5 installed
Does not analyze open positions or pending orders (yet)


## 🤝 Contributing
Contributions are welcome!
Ideas for next versions:

Export results to PDF/CSV
Profit charts and graphs
Dark mode
Multi-account support
Auto-detect MT5 path


## 📄 License
MIT License — Free to use for personal and commercial purposes.

Made with ❤️ for traders who want to get better.
If you like the tool, please give the repo a ⭐!
