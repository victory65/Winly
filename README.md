# 🏆 Winly V2 - MT5 Trade History Analyzer
![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)

**Winly V2** is a powerful, beautiful desktop app that connects directly to your MetaTrader 5 terminal and gives you deep insights into your real trading performance.

---

## 📋 Version History

### Winly V1 (Original)
- Basic trade analysis only
- Showed: Current Balance, Total Real Trades, Win Rate
- Identified best performing pair and most traded pair
- Simple text recommendation
- Smart filter (skipped deposits, swaps, commissions, bonuses, etc.)
- No data export or charts

### Winly V2 (Current – This Version)
**Major upgrades added:**
- Full trade reconstruction (accurate entry & exit prices)
- Handles partial closes correctly
- CSV export with exact columns: `date`, `pair`, `type`, `size`, `entry`, `exist`, `profit`, `cumulative_equity`
- Equity Curve Graph (time vs cumulative equity) – saved as high-quality PNG (matplotlib, fully offline)
- Cumulative equity tracking after every closed trade
- Cleaner recommendation display
- Ready for standalone .exe with all new features included

---

## ✨ Features (Winly V2)

- Modern Tkinter GUI with scrollable window
- One-click full trade history analysis
- Smart symbol filter (ignores fake/deposit operations)
- Accurate trade reconstruction (entry price, exit price, partial closes)
- **New:** Export complete trade log to CSV (exact columns requested)
- **New:** Equity Curve Graph – basic line plot (Time vs Cumulative Equity) + save as PNG
- Shows: Current Balance • Total Real Trades • Win Rate • Smart Recommendation
- Cumulative equity calculated for every trade
- Works with **any MT5 broker** (FBS, IC Markets, Exness, etc.)
- 100% offline – nothing is sent over the internet

---

## ⚠️ Important – Please Read Before Using
> Make sure to read the readme file that comes with this app for best results and to avoid common issues, such as:
>
> - Incorrect server name (check exact name on MT5 login screen)
> - Wrong MT5 path (must point to `terminal64.exe` or `terminal.exe`)
> - Using a demo or new account with no history

---

## 📥 Installation & Usage

### Option 1: Run from Source
1. Clone the repo:
   ```bash
   git clone https://github.com/victory65/Winly.git
   cd Winly
