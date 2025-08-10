import tkinter as tk
from tkinter import messagebox
import win32print
import win32ui

# --- Configuration Constants ---
SIZE_OPTIONS = ["SUCO DE ", "JARRA DE "]
TYPE_OPTIONS = ["NORMAL", "SEM ACUCAR", "SEM GELO", "NATURAL"]
JUICE_FLAVORS = ["LARANJA", "LIMÃO", "MARACUJA", "GOIABA", "ABACAXI"]

BUTTON_STYLE = {
    "width": 20,
    "font": ("Arial", 14, "bold"),
    "bg": "#FFA500",
    "fg": "white",
    "relief": "raised",
    "bd": 4,
    "activebackground": "#FFD700",
    "activeforeground": "#000",
    "cursor": "hand2",
    "padx": 10,
    "pady": 8,
}

FONT_CONFIG = {
    "name": "Arial",
    "height": 40,
    "weight": 700,
}

# --- Printer Logic ---
def print_order(table, size, flavor, option):
    """Sends the formatted order data to the Windows printer."""
    printer_name = win32print.GetDefaultPrinter()
    hPrinter = win32print.OpenPrinter(printer_name)
    pdc = win32ui.CreateDC()
    pdc.CreatePrinterDC(printer_name)
    full_flavor = f"{size}{flavor}"
    pdc.StartDoc(f"Pedido: {table} + {full_flavor} + {option}")
    pdc.StartPage()

    font = win32ui.CreateFont(FONT_CONFIG)
    pdc.SelectObject(font)
    y_gap = FONT_CONFIG["height"] + 20

    pdc.TextOut(100, 100, table)
    pdc.TextOut(100, 100 + y_gap, full_flavor)       # Size + flavor
    pdc.TextOut(100, 100 + 2*y_gap, option)
    pdc.TextOut(100, 100 + 3*y_gap, "-"*30)

    pdc.EndPage()
    pdc.EndDoc()
    pdc.DeleteDC()
    win32print.ClosePrinter(hPrinter)

# --- UI Logic ---
class PedidoSucosApp:
    """Main application class for the juice order system."""

    def __init__(self, root):
        self.root = root
        self.root.title("Pedido Sucos")
        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        # State Variables
        self.table_var = tk.StringVar(value="MESA ")
        self.size_var = tk.StringVar(value=SIZE_OPTIONS[0])
        self.type_var = tk.StringVar(value=TYPE_OPTIONS[0])

        self._build_ui()

    def _build_ui(self):
        self._create_label("Digite a MESA:", 0, 0, colspan=3)
        self._create_entry(self.table_var, 1, 0, colspan=3)

        self._create_label("Tamanho:", 2, 2)
        self._create_radio_group(SIZE_OPTIONS, self.size_var, start_row=3, col=2)

        self._create_label("Opções:", 2, 1)
        self._create_radio_group(TYPE_OPTIONS, self.type_var, start_row=3, col=1)

        self._create_juice_buttons(JUICE_FLAVORS, start_row=3, col=0)

    def _create_label(self, text, row, col, colspan=1):
        tk.Label(self.frame, text=text).grid(row=row, column=col, columnspan=colspan, sticky="w", padx=10)

    def _create_entry(self, var, row, col, colspan=1):
        tk.Entry(self.frame, textvariable=var, width=25).grid(row=row, column=col, columnspan=colspan, pady=10)

    def _create_radio_group(self, options, var, start_row, col):
        for i, option in enumerate(options):
            tk.Radiobutton(self.frame, text=option, variable=var, value=option).grid(row=start_row+i, column=col, sticky="w", padx=10)

    def _create_juice_buttons(self, flavors, start_row, col):
        for i, flavor in enumerate(flavors):
            btn = tk.Button(
                self.frame,
                text=flavor,
                command=self._make_order_callback(flavor),
                **BUTTON_STYLE
            )
            btn.grid(row=start_row+i, column=col, pady=8)

    def _make_order_callback(self, flavor):
        def callback():
            print_order(
                table=self.table_var.get(),
                size=self.size_var.get(),
                flavor=flavor,
                option=self.type_var.get()
            )
            messagebox.showinfo("Impressão enviada", "Os dados foram enviados para a impressora com sucesso!")
        return callback

def main():
    root = tk.Tk()
    app = PedidoSucosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()