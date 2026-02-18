import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog
import MetaTrader5 as mt5
from datetime import datetime
from collections import defaultdict

# ────────────────────────────────────────────────
# Global variables
# ────────────────────────────────────────────────
appName = "Winly"
warning = 'Make sure to read the readme file that comes with this app for best results and to avoid common issues, such as:\n\n- Incorrect server name (check MT5 login screen for exact name if unsure)\n- Wrong MT5 path (browse to terminal64.exe or terminal.exe)\n- Account with no trade history (use a real account with past trades for meaningful analysis)'

account_var    = None
password_var   = None
server_var     = None
mt5_path_var   = None
status_var     = None
root           = None
results_frame  = None


def browse_mt5_path():
    file_path = filedialog.askopenfilename(
        title="Select MetaTrader 5 Terminal (terminal64.exe or terminal.exe)",
        initialdir=r"C:\Program Files",
        filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
    )
    if file_path:
        mt5_path_var.set(file_path)
        status_var.set(f"MT5 path: {os.path.basename(file_path)}")


def is_real_trading_symbol(symbol: str) -> bool:
    """Filter out non-trading symbols like External, corrections, balance ops etc."""
    if not symbol:
        return False
    
    s = symbol.strip().lower()
    
    skip_words = {
        'external', 'internal', 'correction', 'bonus', 'balance',
        'commission', 'swap', 'fee', 'deposit', 'withdrawal',
        'transfer', 'credit', 'adjustment'
    }
    
    if s in skip_words or any(word in s for word in skip_words):
        return False
    
    if len(s) < 3:
        return False
    
    if not any(c.isalpha() for c in s):
        return False
    
    return True


def connect_and_analyze():
    acc_str = account_var.get().strip()
    pwd     = password_var.get().strip()
    srv     = server_var.get().strip()
    path    = mt5_path_var.get().strip()

    if not all([acc_str, pwd, srv, path]):
        messagebox.showwarning("Missing Fields", "Please fill all fields and select MT5 path.")
        return

    try:
        login_num = int(acc_str)
    except ValueError:
        messagebox.showerror("Invalid Input", "Account ID must be a number.")
        return

    if not os.path.exists(path):
        messagebox.showerror("Invalid Path", f"MT5 terminal not found at:\n{path}")
        return

    status_var.set("Launching MetaTrader 5...")
    root.update_idletasks()

    try:
        if not mt5.initialize(path=path, timeout=30000):
            error_code, error_msg = mt5.last_error()
            raise Exception(f"MT5 initialize failed: {error_code} → {error_msg}")

        status_var.set("Logging in...")
        root.update_idletasks()

        if not mt5.login(login=login_num, password=pwd, server=srv):
            error_code, error_msg = mt5.last_error()
            raise Exception(f"MT5 login failed: {error_code} → {error_msg}")

        status_var.set("Connected. Analyzing trade history...")
        root.update_idletasks()

        acc_info = mt5.account_info()
        if acc_info is None:
            raise Exception("Could not retrieve account info")

        from_date = datetime(2020, 1, 1)
        to_date   = datetime.now()

        deals = mt5.history_deals_get(from_date, to_date)
        if deals is None:
            deals = []

        if not deals:
            show_results(0, "0.0%", acc_info.balance, "No trade history found.")
            return

        symbol_stats = defaultdict(lambda: {"profit": 0.0, "count": 0, "wins": 0})

        real_deals_count = 0

        for deal in deals:
            if deal.entry != mt5.DEAL_ENTRY_OUT:
                continue

            symbol = (deal.symbol or "").strip()
            if not is_real_trading_symbol(symbol):
                continue

            real_deals_count += 1

            stats = symbol_stats[symbol]
            stats["profit"] += deal.profit
            stats["count"]  += 1

            if deal.profit > 0:
                stats["wins"] += 1

        if not symbol_stats:
            show_results(real_deals_count, "0.0%", acc_info.balance,
                        "No real trading symbols found in history.\n(Deposits, withdrawals, swaps, corrections skipped)")
            return

        best_pair = max(symbol_stats.items(), key=lambda x: x[1]["profit"])
        best_symbol, best_data = best_pair

        most_traded_pair = max(symbol_stats.items(), key=lambda x: x[1]["count"])
        most_symbol, most_data = most_traded_pair

        total_real_trades = sum(d["count"] for d in symbol_stats.values())
        total_wins        = sum(d["wins"]  for d in symbol_stats.values())

        win_rate = f"{(total_wins / total_real_trades * 100):.1f}%" if total_real_trades > 0 else "0.0%"

        if best_symbol == most_symbol:
            rec = (
                f"**{best_symbol}** is your best & most traded pair!\n"
                f"• Profit: **${best_data['profit']:,.2f}**\n"
                f"• Trades: **{best_data['count']}**  (win rate: {best_data['wins']/best_data['count']*100:.1f}% if >0 trades)"
            )
        else:
            rec = (
                f"Your **highest returning** pair: **{best_symbol}** (+${best_data['profit']:,.2f})\n"
                f"Your **most traded** pair: **{most_symbol}** ({most_data['count']} trades)"
            )

        show_results(
            total_real_trades,
            win_rate,
            acc_info.balance,
            rec
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))
        status_var.set("Connection failed – check credentials, server name or path")
    finally:
        mt5.shutdown()


def show_results(total_trades, win_rate, balance, recommendation):
    for widget in results_frame.winfo_children():
        widget.destroy()

    status_var.set("Analysis complete")

    data = [
        ("Current Balance", f"${balance:,.2f}"),
        ("Real Trades",     str(total_trades)),
        ("Win Rate",        win_rate),
        ("Recommendation",  recommendation),
    ]

    row = 0
    for label_text, value in data:
        lbl_key = ttk.Label(results_frame, text=f"{label_text}:", font=("Helvetica", 11, "bold"))
        lbl_key.grid(row=row, column=0, sticky="w", pady=7, padx=24)

        if label_text == "Recommendation":
            txt = tk.Text(results_frame, height=6, width=45, wrap=tk.WORD,
                          font=("Helvetica", 11), relief="flat", bd=0)
            txt.insert(tk.END, value)
            txt.config(state=tk.DISABLED, bg="white")
            txt.grid(row=row, column=1, sticky="w", pady=7, padx=10)
        else:
            lbl_val = ttk.Label(results_frame, text=value, font=("Helvetica", 11))
            lbl_val.grid(row=row, column=1, sticky="w", pady=7, padx=10)

        row += 1


def clear_results():
    for widget in results_frame.winfo_children():
        widget.destroy()

    ttk.Label(
        results_frame,
        text="Results appear here after successful analysis",
        foreground="gray",
        font=("Helvetica", 11, "italic")
    ).pack(pady=100)

    status_var.set("Ready")


# ────────────────────────────────────────────────
# GUI Setup with Scrollbar
# ────────────────────────────────────────────────
root = tk.Tk()
root.title(appName)
root.geometry("600x600")           # slightly taller + wider to feel more comfortable
root.resizable(False, False)
root.configure(bg="#f0f2f5")

# ─── Scrollable area ───────────────────────────────────────
canvas = tk.Canvas(root, bg="#f0f2f5", highlightthickness=0)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f0f2f5")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ─── All content goes inside scrollable_frame ──────────────

# StringVars
account_var  = tk.StringVar()
password_var = tk.StringVar()
server_var   = tk.StringVar()
mt5_path_var = tk.StringVar()
status_var   = tk.StringVar(value="Enter details and click Analyze")

# Header
tk.Label(scrollable_frame, text=appName, font=("Helvetica", 22, "bold"),
         bg="#87CEEB", fg="navy").pack(fill=tk.X, pady=(10,5))

# Login card
login_card = tk.Frame(scrollable_frame, bg="#87CEEB", relief="raised", bd=2)
login_card.pack(pady=15, padx=40, fill=tk.X)

tk.Label(login_card, text="MetaTrader 5 Account", bg="#87CEEB", fg="navy",
         font=("Helvetica", 15, "bold")).pack(pady=12)

inner = tk.Frame(login_card, bg="white", padx=35, pady=25)
inner.pack(pady=5, fill=tk.X)

# Fields
fields = [
    ("Account ID", account_var,  False),
    ("Password",   password_var, True),
    ("Server",     server_var,   False),
]

for i, (label_text, var, show_char) in enumerate(fields):
    tk.Label(inner, text=label_text + ":", bg="white", font=("Helvetica", 11, "bold")) \
      .grid(row=i, column=0, sticky="w", pady=9, padx=(0,10))
    ttk.Entry(inner, textvariable=var, show="●" if show_char else "", width=38) \
      .grid(row=i, column=1, pady=9, sticky="w")

# MT5 Path
tk.Label(inner, text="MT5 Terminal:", bg="white", font=("Helvetica", 11, "bold")) \
  .grid(row=3, column=0, sticky="w", pady=(18,9), padx=(0,10))

path_frame = tk.Frame(inner, bg="white")
path_frame.grid(row=3, column=1, sticky="ew", pady=(18,9))

ttk.Entry(path_frame, textvariable=mt5_path_var, width=30, state="readonly") \
    .pack(side=tk.LEFT, fill=tk.X, expand=True)
ttk.Button(path_frame, text="Browse", command=browse_mt5_path, width=10) \
    .pack(side=tk.LEFT, padx=(8,0))

# Analyze button
analyze_btn = tk.Button(
    scrollable_frame,
    text="Analyze My Trades",
    bg="#4682B4",
    fg="white",
    font=("Helvetica", 14, "bold"),
    relief="flat",
    padx=50, pady=14,
    command=connect_and_analyze
)
analyze_btn.pack(pady=25)

# Warning / Important notice
info_frame = tk.Frame(scrollable_frame, bg="#fff3cd", relief="solid", bd=1)
info_frame.pack(pady=(5, 20), padx=40, fill=tk.X)

tk.Label(
    info_frame,
    text="⚠️  Important – Before analyzing",
    font=("Helvetica", 11, "bold"),
    bg="#fff3cd",
    fg="#856404"
).pack(anchor="w", padx=15, pady=(12, 4))

ttk.Label(
    info_frame,
    text=warning,
    foreground="#856404",
    background="#fff3cd",
    font=("Helvetica", 10),
    justify="left",
    wraplength=520
).pack(anchor="w", padx=15, pady=(0, 12))

# Status label
ttk.Label(scrollable_frame, textvariable=status_var, foreground="#444", font=("Helvetica", 10)) \
   .pack(pady=(0,15))

# Results area
results_frame = tk.Frame(scrollable_frame, bg="white", relief="sunken", bd=1)
results_frame.pack(pady=10, padx=35, fill=tk.X, expand=False)

clear_results()  # init placeholder

# Mouse wheel scrolling support (Windows/macOS/Linux)
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def _on_linux_scroll(event):
    canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

root.bind_all("<MouseWheel>", _on_mousewheel)
root.bind_all("<Button-4>", _on_linux_scroll)  # Linux scroll up
root.bind_all("<Button-5>", _on_linux_scroll)  # Linux scroll down

root.mainloop()