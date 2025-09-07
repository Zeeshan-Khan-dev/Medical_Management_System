import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import datetime
import os
import tempfile
from PIL import Image, ImageTk
from tkinter.font import Font
import webbrowser
import json
import pickle

class ModernMedicalStore:
    def __init__(self, root):
        self.root = root
        self.root.title("PharmaCare - Medical Store Management")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure theme colors
        self.bg_color = "#f5f6fa"
        self.primary_color = "#487eb0"
        self.secondary_color = "#40739e"
        self.accent_color = "#e84118"
        self.text_color = "#000000"  # Changed to black
        self.light_text = "#f5f6fa"
        
        # Set window icon (replace with your own icon path)
        try:
            self.root.iconbitmap("medical_icon.ico")
        except:
            pass
        
        # Initialize medicine database
        self.medicines = {}
        self.current_transaction = {}
        self.sales_history = []
        
        # Receipt settings
        self.receipt_settings = {
            "header_text": "PHARMA-CARE MEDICAL STORE",
            "address": "123 Health Street, Medtown",
            "phone": "Tel: (555) 123-4567",
            "footer_text": "Thank you for your purchase!",
            "receipt_width": 50,
            "generator_name": "System Admin",
            "show_customer_name": True,
            "show_discount": True,
            "default_discount": 0
        }
        
        # Load sample data
        self.load_sample_data()
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.create_main_container()
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
        
        # Show dashboard by default
        self.show_dashboard()
        
        # Start auto-save
        self.auto_save_data()
        
        # Try to auto-load data
        self.try_auto_load()
    
    def configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        
        # Configure main window background
        self.root.configure(bg=self.bg_color)
        
        # Frame styles
        style.configure('TFrame', background=self.bg_color)
        style.configure('Sidebar.TFrame', background=self.primary_color)
        style.configure('Card.TFrame', background='white', relief=tk.RAISED, borderwidth=1)
        
        # Label styles - Changed text color to black
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=('Segoe UI', 10))
        style.configure('Header.TLabel', font=('Segoe UI', 14, 'bold'), background=self.bg_color, foreground=self.text_color)
        style.configure('Sidebar.TLabel', font=('Segoe UI', 12, 'bold'), background=self.primary_color, foreground=self.text_color)
        style.configure('CardHeader.TLabel', font=('Segoe UI', 11, 'bold'), background='white', foreground=self.text_color)
        style.configure('White.TLabel', background='white', foreground=self.text_color)
        
        # Button styles - Changed text color to black
        style.configure('TButton', font=('Segoe UI', 10), padding=6, foreground=self.text_color)
        style.configure('Primary.TButton', background=self.primary_color, foreground=self.text_color, borderwidth=0)
        style.map('Primary.TButton',
                 background=[('active', self.secondary_color), ('disabled', '#cccccc')],
                 foreground=[('active', self.text_color), ('disabled', '#888888')])
        style.configure('Accent.TButton', background=self.accent_color, foreground=self.text_color, borderwidth=0)
        style.map('Accent.TButton',
                 background=[('active', '#c23616'), ('disabled', '#cccccc')],
                 foreground=[('active', self.text_color), ('disabled', '#888888')])
        style.configure('Sidebar.TButton', font=('Segoe UI', 10), width=15, anchor='w',
                       background=self.primary_color, foreground=self.text_color, borderwidth=0)
        style.map('Sidebar.TButton',
                 background=[('active', self.secondary_color), ('disabled', '#cccccc')],
                 foreground=[('active', self.text_color), ('disabled', '#888888')])
        
        # Entry styles
        style.configure('TEntry', fieldbackground='white', foreground=self.text_color, padding=5)
        
        # Notebook styles
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.bg_color, foreground=self.text_color, padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', 'white')],
                 foreground=[('selected', self.primary_color)])
        
        # Treeview styles
        style.configure('Treeview', background='white', foreground=self.text_color, rowheight=25, fieldbackground='white')
        style.configure('Treeview.Heading', background=self.primary_color, foreground=self.text_color, font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', self.secondary_color)], foreground=[('selected', 'white')])
        
        # Scrollbar styles
        style.configure('Vertical.TScrollbar', background=self.bg_color, bordercolor=self.bg_color, 
                       arrowcolor=self.text_color, troughcolor=self.bg_color)
    
    def create_main_container(self):
        """Create the main container frame"""
        self.main_container = ttk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)
    
    def create_sidebar(self):
        """Create the sidebar navigation"""
        self.sidebar = ttk.Frame(self.main_container, style='Sidebar.TFrame', width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        logo_frame = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        logo_frame.pack(fill=tk.X, pady=(20, 30))
        
        # You can replace this with an actual image logo
        self.logo_label = ttk.Label(logo_frame, text="PharmaCare", style='Sidebar.TLabel', 
                                   font=('Segoe UI', 16, 'bold'), foreground=self.text_color)
        self.logo_label.pack(pady=5)
        
        ttk.Label(logo_frame, text="Medical Store", style='Sidebar.TLabel', 
                 font=('Segoe UI', 10), foreground=self.text_color).pack()
        
        # Navigation buttons
        nav_options = [
            ("Dashboard", "📊", self.show_dashboard),
            ("Inventory", "💊", self.show_inventory),
            ("Sales", "🛒", self.show_sales),
            ("Reports", "📈", self.show_reports),
            ("Settings", "⚙️", self.show_settings)
        ]
        
        for text, icon, command in nav_options:
            btn = ttk.Button(self.sidebar, text=f" {icon}  {text}", style='Sidebar.TButton', 
                           command=command)
            btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Add some spacing
        ttk.Frame(self.sidebar, height=20, style='Sidebar.TFrame').pack(fill=tk.X)
        
        # Footer with version info
        footer_frame = ttk.Frame(self.sidebar, style='Sidebar.TFrame')
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        ttk.Label(footer_frame, text="Dev: Zeeshan Khan", style='Sidebar.TLabel', 
                 font=('Segoe UI', 8), foreground=self.text_color).pack()
    
    def create_main_content(self):
        """Create the main content area"""
        self.content = ttk.Frame(self.main_container)
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create all content frames but don't show them yet
        self.create_dashboard()
        self.create_inventory_tab()
        self.create_sales_tab()
        self.create_reports_tab()
        self.create_settings_tab()
    
    def create_status_bar(self):
        """Create the status bar at the bottom"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        self.status_bar = ttk.Frame(self.main_container, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        ttk.Label(self.status_bar, textvariable=self.status_var, style='TLabel', 
                 font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(self.status_bar, text="© 2025 PharmaCare", style='TLabel', 
                 font=('Segoe UI', 9)).pack(side=tk.RIGHT, padx=10)
    
    def load_sample_data(self):
        """Load sample medicine data"""
        self.medicines = {
            "Paracetamol 500mg": {"price": 150.00, "quantity": 150, "expiry": "13-03-2028", "company": "GSK", "batch": "P123"},
            "Ibuprofen 200mg": {"price": 220.50, "quantity": 80, "expiry": "12-09-2025", "company": "Pfizer", "batch": "I456"},
            "Amoxicillin 250mg": {"price": 350.75, "quantity": 45, "expiry": "23-09-2026", "company": "Novartis", "batch": "A789"},
            "Cetirizine 10mg": {"price": 180.25, "quantity": 60, "expiry": "09-09-2027", "company": "Johnson & Johnson", "batch": "C101"},
            "Omeprazole 20mg": {"price": 420.00, "quantity": 35, "expiry": "20-03-2025", "company": "Roche", "batch": "O202"},
        }
        
        # Initialize with empty sales history for today
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        self.sales_history = []
        self.today_sales_var = tk.StringVar()
        self.today_sales_var.set("Pkr 0.00")  # Initialize today's sales to zero
    
    def show_dashboard(self):
        """Show the dashboard tab"""
        self.hide_all_tabs()
        self.dashboard_frame.pack(fill=tk.BOTH, expand=True)
        self.update_dashboard()
    
    def show_inventory(self):
        """Show the inventory tab"""
        self.hide_all_tabs()
        self.inventory_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_inventory()
    
    def show_sales(self):
        """Show the sales tab"""
        self.hide_all_tabs()
        self.sales_frame.pack(fill=tk.BOTH, expand=True)
        self.refresh_sales_list()
    
    def show_sales_history_window(self):
        """Show the sales history in a separate window"""
        history_window = tk.Toplevel(self.root)
        history_window.title("Sales History")
        history_window.geometry("1000x600")
        self.center_window(history_window)
        
        # Header
        header = ttk.Frame(history_window)
        header.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(header, text="Sales History", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Button frame
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Refresh", style='TButton', 
                  command=lambda: self.refresh_sales_history_tree(sales_tree)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export", style='TButton', 
                  command=self.export_sales_history).pack(side=tk.LEFT, padx=5)
        
        # Sales history treeview with more columns
        sales_tree = ttk.Treeview(history_window, 
                                 columns=('Date', 'Customer', 'Items', 'Quantity', 'Amount', 'Discount', 'Total'), 
                                 show='headings')
        
        # Configure columns
        sales_tree.heading('Date', text='Date')
        sales_tree.heading('Customer', text='Customer')
        sales_tree.heading('Items', text='Items Sold')
        sales_tree.heading('Quantity', text='Total Qty')
        sales_tree.heading('Amount', text='Amount (Pkr)')
        sales_tree.heading('Discount', text='Discount (Pkr)')
        sales_tree.heading('Total', text='Net Total (Pkr)')
        
        sales_tree.column('Date', width=100, anchor='center')
        sales_tree.column('Customer', width=120, anchor='w')
        sales_tree.column('Items', width=250, anchor='w')
        sales_tree.column('Quantity', width=80, anchor='e')
        sales_tree.column('Amount', width=100, anchor='e')
        sales_tree.column('Discount', width=100, anchor='e')
        sales_tree.column('Total', width=100, anchor='e')
        
        scrollbar = ttk.Scrollbar(history_window, 
                                orient=tk.VERTICAL, 
                                command=sales_tree.yview)
        sales_tree.configure(yscroll=scrollbar.set)
        
        sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to view details
        sales_tree.bind('<Double-1>', lambda e: self.view_sale_details(sales_tree))
        
        # Populate initial data
        self.refresh_sales_history_tree(sales_tree)
    
    def refresh_sales_history_tree(self, tree):
        """Refresh the sales history treeview with all data"""
        tree.delete(*tree.get_children())
        
        total_sales = 0.0
        sale_count = 0
        total_qty = 0
        total_discount = 0.0
        
        for sale in sorted(self.sales_history, key=lambda x: x['date'], reverse=True):
            items = ", ".join(f"{item['name']}" for item in sale['items'])
            total_items_qty = sum(item['qty'] for item in sale['items'])
            gross_total = sum(item['price'] * item['qty'] for item in sale['items'])
            discount = gross_total - sale['total']
            
            tree.insert('', 'end', 
                      values=(
                          sale['date'],
                          sale.get('customer', 'Walk-in'),
                          items[:50] + "..." if len(items) > 50 else items,
                          total_items_qty,
                          f"{gross_total:.2f}",
                          f"{discount:.2f}",
                          f"{sale['total']:.2f}"
                      ))
            
            total_sales += sale['total']
            sale_count += 1
            total_qty += total_items_qty
            total_discount += discount
        
        # Add summary row
        if sale_count > 0:
            tree.insert('', 'end', values=(
                "TOTAL",
                f"{sale_count} sales",
                "",
                total_qty,
                f"{total_sales + total_discount:.2f}",
                f"{total_discount:.2f}",
                f"{total_sales:.2f}"
            ), tags=('total',))
            tree.tag_configure('total', background='#f0f0f0', font=('Segoe UI', 9, 'bold'))
        
        # Update status bar
        self.status_var.set(f"Showing {sale_count} sales - Total: Pkr {total_sales:.2f}")
    
    def show_reports(self):
        """Show the reports tab"""
        self.hide_all_tabs()
        self.reports_frame.pack(fill=tk.BOTH, expand=True)
        self.generate_report()
    
    def show_settings(self):
        """Show the settings tab"""
        self.hide_all_tabs()
        self.settings_frame.pack(fill=tk.BOTH, expand=True)
    
    def hide_all_tabs(self):
        """Hide all content tabs"""
        for frame in [self.dashboard_frame, self.inventory_frame, 
                     self.sales_frame, self.reports_frame, self.settings_frame]:
            frame.pack_forget()
    
    def create_dashboard(self):
        """Create the dashboard content"""
        self.dashboard_frame = ttk.Frame(self.content)
        
        # Header
        header = ttk.Frame(self.dashboard_frame)
        header.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(header, text="Dashboard", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Add Sales History button next to refresh
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Sales History", style='TButton', 
                  command=self.show_sales_history_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", style='TButton', 
                  command=self.update_dashboard).pack(side=tk.LEFT, padx=5)
        
        # Cards row
        cards_frame = ttk.Frame(self.dashboard_frame)
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1: Total Medicines
        card1 = ttk.Frame(cards_frame, style='Card.TFrame')
        card1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(card1, text="Total Medicines", style='CardHeader.TLabel').pack(pady=(10, 5))
        self.total_meds_var = tk.StringVar()
        self.total_meds_var.set("0")
        ttk.Label(card1, textvariable=self.total_meds_var, font=('Segoe UI', 24, 'bold'), 
                 style='White.TLabel').pack(pady=5)
        ttk.Label(card1, text="in inventory", style='White.TLabel').pack(pady=(0, 10))
        
        # Card 2: Low Stock
        card2 = ttk.Frame(cards_frame, style='Card.TFrame')
        card2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(card2, text="Low Stock", style='CardHeader.TLabel').pack(pady=(10, 5))
        self.low_stock_var = tk.StringVar()
        self.low_stock_var.set("0")
        ttk.Label(card2, textvariable=self.low_stock_var, font=('Segoe UI', 24, 'bold'), 
                 style='White.TLabel', foreground=self.accent_color).pack(pady=5)
        ttk.Label(card2, text="items need restocking", style='White.TLabel').pack(pady=(0, 10))
        
        # Card 3: Expiring Soon
        card3 = ttk.Frame(cards_frame, style='Card.TFrame')
        card3.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(card3, text="Expiring Soon", style='CardHeader.TLabel').pack(pady=(10, 5))
        self.expiring_var = tk.StringVar()
        self.expiring_var.set("0")
        ttk.Label(card3, textvariable=self.expiring_var, font=('Segoe UI', 24, 'bold'), 
                 style='White.TLabel', foreground=self.accent_color).pack(pady=5)
        ttk.Label(card3, text="items expiring in 3 months", style='White.TLabel').pack(pady=(0, 10))
        
        # Card 4: Today's Sales
        card4 = ttk.Frame(cards_frame, style='Card.TFrame')
        card4.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(card4, text="Today's Sales", style='CardHeader.TLabel').pack(pady=(10, 5))
        self.today_sales_var = tk.StringVar()
        self.today_sales_var.set("Pkr 0.00")
        ttk.Label(card4, textvariable=self.today_sales_var, font=('Segoe UI', 24, 'bold'), 
                 style='White.TLabel', foreground=self.primary_color).pack(pady=5)
        ttk.Label(card4, text="total revenue", style='White.TLabel').pack(pady=(0, 10))
        
        # Card 5: Empty Stocks
        card5 = ttk.Frame(cards_frame, style='Card.TFrame')
        card5.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(card5, text="Empty Stocks", style='CardHeader.TLabel').pack(pady=(10, 5))
        self.empty_stock_var = tk.StringVar()
        self.empty_stock_var.set("0")
        ttk.Label(card5, textvariable=self.empty_stock_var, font=('Segoe UI', 24, 'bold'), 
                 style='White.TLabel', foreground=self.accent_color).pack(pady=5)
        ttk.Label(card5, text="items out of stock", style='White.TLabel').pack(pady=(0, 10))
        
        # Recent sales table
        sales_header = ttk.Frame(self.dashboard_frame)
        sales_header.pack(fill=tk.X, pady=(20, 5))
        
        ttk.Label(sales_header, text="Recent Sales", style='Header.TLabel').pack(side=tk.LEFT)
        
        self.sales_table = ttk.Treeview(self.dashboard_frame, columns=('Date', 'Items', 'Amount'), show='headings')
        self.sales_table.heading('Date', text='Date')
        self.sales_table.heading('Items', text='Items Sold')
        self.sales_table.heading('Amount', text='Amount (Pkr)')
        self.sales_table.column('Date', width=120, anchor='center')
        self.sales_table.column('Items', width=300, anchor='w')
        self.sales_table.column('Amount', width=100, anchor='e')
        
        scrollbar = ttk.Scrollbar(self.dashboard_frame, orient=tk.VERTICAL, command=self.sales_table.yview)
        self.sales_table.configure(yscroll=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.sales_table.pack(fill=tk.BOTH, expand=True)
    
    def update_dashboard(self):
        """Update dashboard statistics"""
        # Update total medicines
        self.total_meds_var.set(str(len(self.medicines)))
        
        # Update low stock items (quantity < 20)
        low_stock = sum(1 for med in self.medicines.values() if 0 < med['quantity'] < 20)
        self.low_stock_var.set(str(low_stock))
        
        # Update expiring soon items (within 3 months)
        today = datetime.datetime.now().date()
        expiring = 0
        for med in self.medicines.values():
            try:
                expiry_date = datetime.datetime.strptime(med['expiry'], "%d-%m-%Y").date()
                if (expiry_date - today).days <= 90:
                    expiring += 1
            except:
                continue
        self.expiring_var.set(str(expiring))
        
        # Update today's sales - now properly filtering by today's date
        today_str = datetime.datetime.now().strftime("%d-%m-%Y")
        today_sales = sum(sale['total'] for sale in self.sales_history if sale['date'] == today_str)
        self.today_sales_var.set(f"Pkr {today_sales:.2f}")
        
        # Update empty stock items
        empty_stock = sum(1 for med in self.medicines.values() if med['quantity'] == 0)
        self.empty_stock_var.set(str(empty_stock))
        
        # Update recent sales table
        self.sales_table.delete(*self.sales_table.get_children())
        for sale in sorted(self.sales_history, key=lambda x: x['date'], reverse=True)[:10]:
            items = ", ".join(f"{item['name']} ({item['qty']})" for item in sale['items'])
            self.sales_table.insert('', 'end', values=(sale['date'], items, f"{sale['total']:.2f}"))
    
    def create_inventory_tab(self):
        """Create the inventory management tab"""
        self.inventory_frame = ttk.Frame(self.content)
        
        # Header
        header = ttk.Frame(self.inventory_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Medicine Inventory", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Button frame
        btn_frame = ttk.Frame(header)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Add Medicine", style='Primary.TButton', 
                  command=self.add_medicine_window).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generate Receipt", command=self.generate_receipt_for_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", style='TButton', 
                  command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        
        # Filter frame
        filter_frame = ttk.Frame(self.inventory_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Company:").pack(side=tk.LEFT)
        self.company_filter = tk.StringVar()
        self.company_filter.set("All")  # Default to show all companies
        
        # Get unique companies from medicines
        all_companies = sorted(set(med.get('company', 'All') for med in self.medicines.values()))
        if "All" not in all_companies:
            all_companies.insert(0, "All")
        
        company_menu = ttk.OptionMenu(filter_frame, self.company_filter, *all_companies, command=self.filter_by_company)
        company_menu.pack(side=tk.LEFT, padx=5)
        
        # Search frame
        search_frame = ttk.Frame(self.inventory_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_medicine)
        
        ttk.Button(search_frame, text="Clear", style='TButton', 
                  command=self.clear_search).pack(side=tk.LEFT, padx=5)
        
        # Medicine list treeview
        self.tree = ttk.Treeview(self.inventory_frame, columns=('Name', 'Company', 'Price', 'Quantity', 'Expiry', 'Batch'), show='headings')
        self.tree.heading('Name', text='Medicine Name')
        self.tree.heading('Company', text='Company')
        self.tree.heading('Price', text='Price (Pkr)')
        self.tree.heading('Quantity', text='Qty')
        self.tree.heading('Expiry', text='Expiry Date')
        self.tree.heading('Batch', text='Batch No.')
        
        self.tree.column('Name', width=200, anchor='w')
        self.tree.column('Company', width=120, anchor='w')
        self.tree.column('Price', width=80, anchor='e')
        self.tree.column('Quantity', width=60, anchor='e')
        self.tree.column('Expiry', width=100, anchor='center')
        self.tree.column('Batch', width=100, anchor='center')
        
        scrollbar = ttk.Scrollbar(self.inventory_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to edit
        self.tree.bind('<Double-1>', self.edit_medicine)
        
        # Context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Edit Medicine", command=self.edit_selected_medicine)
        self.context_menu.add_command(label="Delete Medicine", command=self.delete_medicine)
        self.context_menu.add_command(label="Generate Receipt", command=self.generate_receipt_for_selected)
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def filter_by_company(self, event=None):
        """Filter medicines by company"""
        self.refresh_inventory()
    
    def refresh_inventory(self):
        """Refresh the inventory treeview"""
        self.tree.delete(*self.tree.get_children())
        company_filter = self.company_filter.get()
        
        for name, details in sorted(self.medicines.items()):
            if company_filter == "All" or details.get('company', 'All') == company_filter:
                self.tree.insert('', 'end', values=(
                    name, 
                    details.get('company', 'All'),
                    f"{details['price']:.2f}", 
                    details['quantity'], 
                    details['expiry'], 
                    details['batch']
                ))
        self.status_var.set("Inventory refreshed")
    
    def search_medicine(self, event=None):
        """Search medicine in inventory"""
        search_term = self.search_entry.get().lower()
        company_filter = self.company_filter.get()
        self.tree.delete(*self.tree.get_children())
        
        for name, details in sorted(self.medicines.items()):
            if (company_filter == "All" or details.get('company', 'All') == company_filter) and search_term in name.lower():
                self.tree.insert('', 'end', values=(
                    name, 
                    details.get('company', 'All'),
                    f"{details['price']:.2f}", 
                    details['quantity'], 
                    details['expiry'], 
                    details['batch']
                ))
    
    def clear_search(self):
        """Clear inventory search"""
        self.search_entry.delete(0, tk.END)
        self.refresh_inventory()
        self.status_var.set("Search cleared")
    
    def show_context_menu(self, event):
        """Show context menu for inventory items"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
    
    def edit_selected_medicine(self):
        """Edit the currently selected medicine"""
        selected = self.tree.focus()
        if selected:
            self.edit_medicine(None)
    
    def add_medicine_window(self):
        """Open add medicine window"""
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Add New Medicine")
        self.add_window.geometry("500x500")
        self.add_window.resizable(False, False)
        
        # Center the window
        self.center_window(self.add_window)
        
        # Form fields
        form_frame = ttk.Frame(self.add_window, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Add New Medicine", style='CardHeader.TLabel').pack(pady=(10, 20))
        
        # Medicine Name
        ttk.Label(form_frame, text="Medicine Name:").pack(anchor='w', padx=20)
        self.name_entry_add = ttk.Entry(form_frame, width=40)
        self.name_entry_add.pack(padx=20, pady=(0, 10))
        
        # Company (entry field)
        ttk.Label(form_frame, text="Company:").pack(anchor='w', padx=20)
        self.company_entry_add = ttk.Entry(form_frame, width=40)
        self.company_entry_add.pack(padx=20, pady=(0, 10))
        
        # Price
        ttk.Label(form_frame, text="Price (Pkr):").pack(anchor='w', padx=20)
        self.price_entry_add = ttk.Entry(form_frame, width=40)
        self.price_entry_add.pack(padx=20, pady=(0, 10))
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").pack(anchor='w', padx=20)
        self.qty_entry_add = ttk.Entry(form_frame, width=40)
        self.qty_entry_add.pack(padx=20, pady=(0, 10))
        
        # Expiry Date
        ttk.Label(form_frame, text="Expiry Date (DD-MM-YYYY):").pack(anchor='w', padx=20)
        self.expiry_entry_add = ttk.Entry(form_frame, width=40)
        self.expiry_entry_add.pack(padx=20, pady=(0, 10))
        
        # Batch Number
        ttk.Label(form_frame, text="Batch Number:").pack(anchor='w', padx=20)
        self.batch_entry_add = ttk.Entry(form_frame, width=40)
        self.batch_entry_add.pack(padx=20, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Medicine", style='Primary.TButton', 
                  command=self.save_new_medicine).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", style='TButton', 
                  command=self.add_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def save_new_medicine(self):
        """Save new medicine to inventory"""
        try:
            name = self.name_entry_add.get().strip()
            if not name:
                messagebox.showerror("Error", "Medicine name cannot be empty", parent=self.add_window)
                return
                
            company = self.company_entry_add.get().strip()
            price = float(self.price_entry_add.get())
            quantity = int(self.qty_entry_add.get())
            expiry = self.expiry_entry_add.get().strip()
            batch = self.batch_entry_add.get().strip()
            
            if not expiry or not batch:
                messagebox.showerror("Error", "Expiry date and batch number cannot be empty", parent=self.add_window)
                return
            
            if name in self.medicines:
                messagebox.showerror("Error", "Medicine already exists", parent=self.add_window)
                return
                
            self.medicines[name] = {
                'company': company,
                'price': price,
                'quantity': quantity,
                'expiry': expiry,
                'batch': batch
            }
            
            messagebox.showinfo("Success", f"Medicine '{name}' added successfully", parent=self.add_window)
            self.add_window.destroy()
            self.refresh_inventory()
            self.refresh_sales_list()
            self.status_var.set(f"Medicine '{name}' added successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and quantity", parent=self.add_window)
    
    def edit_medicine(self, event):
        """Edit selected medicine"""
        selected = self.tree.focus()
        if not selected:
            return
            
        values = self.tree.item(selected, 'values')
        old_name = values[0]
        medicine = self.medicines[old_name]
        
        self.edit_window = tk.Toplevel(self.root)
        self.edit_window.title("Edit Medicine")
        self.edit_window.geometry("500x550")
        self.edit_window.resizable(False, False)
        
        # Center the window
        self.center_window(self.edit_window)
        
        # Form fields
        form_frame = ttk.Frame(self.edit_window, style='Card.TFrame')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(form_frame, text="Edit Medicine", style='CardHeader.TLabel').pack(pady=(10, 20))
        
        # Medicine Name - Make it editable
        ttk.Label(form_frame, text="Medicine Name:").pack(anchor='w', padx=20)
        self.name_entry_edit = ttk.Entry(form_frame, width=40)
        self.name_entry_edit.insert(0, old_name)
        self.name_entry_edit.pack(padx=20, pady=(0, 10))
        
        # Company (entry field)
        ttk.Label(form_frame, text="Company:").pack(anchor='w', padx=20)
        self.company_entry_edit = ttk.Entry(form_frame, width=40)
        self.company_entry_edit.insert(0, medicine.get('company', ''))
        self.company_entry_edit.pack(padx=20, pady=(0, 10))
        
        # Price
        ttk.Label(form_frame, text="Price (Pkr):").pack(anchor='w', padx=20)
        self.price_entry_edit = ttk.Entry(form_frame, width=40)
        self.price_entry_edit.insert(0, medicine['price'])
        self.price_entry_edit.pack(padx=20, pady=(0, 10))
        
        # Quantity
        ttk.Label(form_frame, text="Quantity:").pack(anchor='w', padx=20)
        self.qty_entry_edit = ttk.Entry(form_frame, width=40)
        self.qty_entry_edit.insert(0, medicine['quantity'])
        self.qty_entry_edit.pack(padx=20, pady=(0, 10))
        
        # Expiry Date
        ttk.Label(form_frame, text="Expiry Date (DD-MM-YYYY):").pack(anchor='w', padx=20)
        self.expiry_entry_edit = ttk.Entry(form_frame, width=40)
        self.expiry_entry_edit.insert(0, medicine['expiry'])
        self.expiry_entry_edit.pack(padx=20, pady=(0, 10))
        
        # Batch Number
        ttk.Label(form_frame, text="Batch Number:").pack(anchor='w', padx=20)
        self.batch_entry_edit = ttk.Entry(form_frame, width=40)
        self.batch_entry_edit.insert(0, medicine['batch'])
        self.batch_entry_edit.pack(padx=20, pady=(0, 20))
        
        # Buttons
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(pady=(10, 0))
        
        ttk.Button(button_frame, text="Update", style='Primary.TButton', 
                  command=lambda: self.update_medicine(old_name)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", style='TButton', 
                  command=self.edit_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def update_medicine(self, old_name):
        """Update existing medicine in inventory"""
        try:
            new_name = self.name_entry_edit.get().strip()
            if not new_name:
                messagebox.showerror("Error", "Medicine name cannot be empty", parent=self.edit_window)
                return
                
            company = self.company_entry_edit.get().strip()
            price = float(self.price_entry_edit.get())
            quantity = int(self.qty_entry_edit.get())
            expiry = self.expiry_entry_edit.get().strip()
            batch = self.batch_entry_edit.get().strip()
            
            if not expiry or not batch:
                messagebox.showerror("Error", "Expiry date and batch number cannot be empty", parent=self.edit_window)
                return
            
            # If name changed, remove old entry and add new one
            if old_name != new_name:
                if new_name in self.medicines:
                    messagebox.showerror("Error", "Medicine name already exists", parent=self.edit_window)
                    return
                    
                # Remove old entry and create new one
                medicine_data = self.medicines.pop(old_name)
                medicine_data.update({
                    'company': company,
                    'price': price,
                    'quantity': quantity,
                    'expiry': expiry,
                    'batch': batch
                })
                self.medicines[new_name] = medicine_data
            else:
                # Just update the existing medicine
                self.medicines[old_name].update({
                    'company': company,
                    'price': price,
                    'quantity': quantity,
                    'expiry': expiry,
                    'batch': batch
                })
            
            messagebox.showinfo("Success", "Medicine updated successfully", parent=self.edit_window)
            self.edit_window.destroy()
            self.refresh_inventory()
            self.refresh_sales_list()
            self.status_var.set("Medicine updated successfully")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for price and quantity", parent=self.edit_window)
    
    def delete_medicine(self):
        """Delete selected medicine"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medicine to delete")
            return
            
        name = self.tree.item(selected, 'values')[0]
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete '{name}'?", icon='warning'):
            del self.medicines[name]
            self.refresh_inventory()
            self.refresh_sales_list()
            self.status_var.set(f"Medicine '{name}' deleted successfully")
    
    def create_sales_tab(self):
        """Create the sales transaction tab"""
        self.sales_frame = ttk.Frame(self.content)
        
        # Header
        header = ttk.Frame(self.sales_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Sales Transaction", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Left frame (medicine selection)
        left_frame = ttk.Frame(self.sales_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10), pady=5)
        
        ttk.Label(left_frame, text="Available Medicines", style='Header.TLabel', 
                 font=('Segoe UI', 11)).pack(anchor='w')
        
        # Search frame
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.sales_search_entry = ttk.Entry(search_frame, width=30)
        self.sales_search_entry.pack(side=tk.LEFT, padx=5)
        self.sales_search_entry.bind('<KeyRelease>', self.search_sales_medicine)
        
        ttk.Button(search_frame, text="Clear", style='TButton', 
                  command=self.clear_sales_search).pack(side=tk.LEFT, padx=5)
        
        # Medicine list for sales
        self.sales_tree = ttk.Treeview(left_frame, columns=('Name', 'Company', 'Price', 'Stock'), show='headings')
        self.sales_tree.heading('Name', text='Medicine Name')
        self.sales_tree.heading('Company', text='Company')
        self.sales_tree.heading('Price', text='Price (Pkr)')
        self.sales_tree.heading('Stock', text='In Stock')
        
        self.sales_tree.column('Name', width=200, anchor='w')
        self.sales_tree.column('Company', width=120, anchor='w')
        self.sales_tree.column('Price', width=80, anchor='e')
        self.sales_tree.column('Stock', width=80, anchor='e')
        
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.sales_tree.yview)
        self.sales_tree.configure(yscroll=scrollbar.set)
        
        self.sales_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to add to cart
        self.sales_tree.bind('<Double-1>', self.add_to_cart_from_tree)
        
        # Right frame (cart)
        right_frame = ttk.Frame(self.sales_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0), pady=5)
        
        ttk.Label(right_frame, text="Current Sale", style='Header.TLabel', 
                 font=('Segoe UI', 11)).pack(anchor='w')
        
        # Cart treeview
        self.cart_tree = ttk.Treeview(right_frame, columns=('Name', 'Price', 'Qty', 'Total'), show='headings')
        self.cart_tree.heading('Name', text='Medicine Name')
        self.cart_tree.heading('Price', text='Price (Pkr)')
        self.cart_tree.heading('Qty', text='Qty')
        self.cart_tree.heading('Total', text='Total (Pkr)')
        
        self.cart_tree.column('Name', width=180, anchor='w')
        self.cart_tree.column('Price', width=80, anchor='e')
        self.cart_tree.column('Qty', width=60, anchor='e')
        self.cart_tree.column('Total', width=80, anchor='e')
        
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.cart_tree.yview)
        self.cart_tree.configure(yscroll=scrollbar.set)
        
        self.cart_tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to remove from cart
        self.cart_tree.bind('<Double-1>', self.remove_from_cart)
        
        # Quantity frame
        qty_frame = ttk.Frame(right_frame)
        qty_frame.pack(fill=tk.X, pady=(10, 5))
        
        ttk.Label(qty_frame, text="Quantity:").pack(side=tk.LEFT)
        self.qty_entry = ttk.Entry(qty_frame, width=10)
        self.qty_entry.pack(side=tk.LEFT, padx=5)
        self.qty_entry.insert(0, "1")
        
        ttk.Button(qty_frame, text="Add to Cart", style='Primary.TButton', 
                  command=self.add_to_cart).pack(side=tk.RIGHT)
        
        # Discount frame
        discount_frame = ttk.Frame(right_frame)
        discount_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(discount_frame, text="Discount %:").pack(side=tk.LEFT)
        self.discount_entry = ttk.Entry(discount_frame, width=5)
        self.discount_entry.pack(side=tk.LEFT, padx=5)
        self.discount_entry.insert(0, str(self.receipt_settings["default_discount"]))
        
        # Customer name frame
        customer_frame = ttk.Frame(right_frame)
        customer_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(customer_frame, text="Customer:").pack(side=tk.LEFT)
        self.customer_entry = ttk.Entry(customer_frame)
        self.customer_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.customer_entry.insert(0, "Walk-in Customer")
        
        # Total frame
        total_frame = ttk.Frame(right_frame)
        total_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(total_frame, text="Gross Total:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.gross_total_var = tk.StringVar()
        self.gross_total_var.set("Pkr 0.00")
        ttk.Label(total_frame, textvariable=self.gross_total_var, font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(total_frame, text="Net Total:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(20, 0))
        self.net_total_var = tk.StringVar()
        self.net_total_var.set("Pkr 0.00")
        ttk.Label(total_frame, textvariable=self.net_total_var, font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Button frame
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Remove Selected", style='TButton', 
                  command=self.remove_from_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Cart", style='TButton', 
                  command=self.clear_cart).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Complete Sale", style='Accent.TButton', 
                  command=self.complete_sale).pack(side=tk.RIGHT)
    
    def refresh_sales_list(self):
        """Refresh the sales treeview"""
        self.sales_tree.delete(*self.sales_tree.get_children())
        for name, details in sorted(self.medicines.items()):
            self.sales_tree.insert('', 'end', values=(
                name, 
                details.get('company', 'All'),
                f"{details['price']:.2f}", 
                details['quantity']
            ))
    
    def search_sales_medicine(self, event=None):
        """Search medicine in sales list"""
        search_term = self.sales_search_entry.get().lower()
        self.sales_tree.delete(*self.sales_tree.get_children())
        for name, details in sorted(self.medicines.items()):
            if search_term in name.lower():
                self.sales_tree.insert('', 'end', values=(
                    name, 
                    details.get('company', 'All'),
                    f"{details['price']:.2f}", 
                    details['quantity']
                ))
    
    def clear_sales_search(self):
        """Clear sales search"""
        self.sales_search_entry.delete(0, tk.END)
        self.refresh_sales_list()
    
    def add_to_cart(self):
        """Add selected medicine to cart with specified quantity"""
        selected = self.sales_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medicine to add to cart")
            return
            
        name = self.sales_tree.item(selected, 'values')[0]
        medicine = self.medicines[name]
        
        try:
            qty = int(self.qty_entry.get())
            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be positive")
                return
                
            if qty > medicine['quantity']:
                messagebox.showerror("Error", "Not enough stock available")
                return
                
            if name in self.current_transaction:
                self.current_transaction[name]['quantity'] += qty
            else:
                self.current_transaction[name] = {
                    'price': medicine['price'],
                    'quantity': qty
                }
            
            # Update stock (temporarily until sale is completed)
            self.medicines[name]['quantity'] -= qty
            self.refresh_sales_list()
            self.refresh_cart()
            self.status_var.set(f"{qty} units of {name} added to cart")
            
            # Reset quantity entry
            self.qty_entry.delete(0, tk.END)
            self.qty_entry.insert(0, "1")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity")
    
    def add_to_cart_from_tree(self, event):
        """Add medicine to cart when double-clicked in treeview"""
        self.add_to_cart()
    
    def refresh_cart(self):
        """Refresh the cart and calculate total"""
        self.cart_tree.delete(*self.cart_tree.get_children())
        gross_total = 0.0
        
        for name, details in self.current_transaction.items():
            item_total = details['price'] * details['quantity']
            gross_total += item_total
            self.cart_tree.insert('', 'end', values=(
                name,
                f"{details['price']:.2f}",
                details['quantity'],
                f"{item_total:.2f}"
            ))
        
        # Calculate discount and net total
        try:
            discount_percent = float(self.discount_entry.get())
        except ValueError:
            discount_percent = 0
        
        discount_amount = gross_total * (discount_percent / 100)
        net_total = gross_total - discount_amount
        
        self.gross_total_var.set(f"Pkr {gross_total:.2f}")
        self.net_total_var.set(f"Pkr {net_total:.2f}")
    
    def remove_from_cart(self, event=None):
        """Remove selected item from cart"""
        selected = self.cart_tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove from cart")
            return
            
        name = self.cart_tree.item(selected, 'values')[0]
        qty = self.current_transaction[name]['quantity']
        
        # Return stock
        self.medicines[name]['quantity'] += qty
        del self.current_transaction[name]
        
        self.refresh_sales_list()
        self.refresh_cart()
        self.status_var.set(f"{name} removed from cart")
    
    def clear_cart(self):
        """Clear all items from cart"""
        if not self.current_transaction:
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear the cart?", icon='warning'):
            # Return all items to stock
            for name, details in self.current_transaction.items():
                self.medicines[name]['quantity'] += details['quantity']
            
            self.current_transaction.clear()
            self.refresh_sales_list()
            self.refresh_cart()
            self.status_var.set("Cart cleared")
    
    def complete_sale(self):
        """Complete the sale and generate receipt"""
        if not self.current_transaction:
            messagebox.showwarning("Warning", "Cart is empty")
            return
            
        try:
            discount_percent = float(self.discount_entry.get())
        except ValueError:
            discount_percent = 0
        
        # Calculate totals
        gross_total = sum(details['price'] * details['quantity'] for details in self.current_transaction.values())
        discount_amount = gross_total * (discount_percent / 100)
        net_total = gross_total - discount_amount
        
        # Create sale record
        today = datetime.datetime.now().strftime("%d-%m-%Y")
        sale_record = {
            'date': today,
            'customer': self.customer_entry.get(),
            'items': [{
                'name': name,
                'qty': details['quantity'],
                'price': details['price']
            } for name, details in self.current_transaction.items()],
            'gross_total': gross_total,
            'discount': discount_amount,
            'total': net_total
        }
        
        # Add to history
        self.sales_history.append(sale_record)
        
        # Generate receipt
        receipt = self.generate_receipt()
        
        # Show receipt window
        self.show_receipt_window(receipt)
        
        # Clear cart after sale
        self.current_transaction.clear()
        self.refresh_sales_list()
        self.refresh_cart()
        
        # Update dashboard to show new sales total
        self.update_dashboard()
        
        self.status_var.set("Sale completed successfully")
    
    def generate_receipt_for_selected(self):
        """Generate receipt for selected medicine in inventory"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a medicine first")
            return
            
        name = self.tree.item(selected, 'values')[0]
        
        # Create temporary transaction with quantity 1
        temp_transaction = {
            name: {
                'price': self.medicines[name]['price'],
                'quantity': 1
            }
        }
        
        # Generate receipt
        receipt = self.generate_receipt(temp_transaction)
        
        # Show receipt window
        self.show_receipt_window(receipt)
    
    def generate_receipt(self, transaction=None):
        """Generate receipt text"""
        if transaction is None:
            transaction = self.current_transaction
        
        receipt = []
        width = self.receipt_settings["receipt_width"]
        
        # Header
        receipt.append("="*width)
        receipt.append(self.receipt_settings["header_text"].center(width))
        receipt.append(self.receipt_settings["address"].center(width))
        receipt.append(self.receipt_settings["phone"].center(width))
        receipt.append("="*width)
        
        # Date and customer info
        receipt.append(f"Date: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        
        if self.receipt_settings["show_customer_name"]:
            customer_name = self.customer_entry.get()
            receipt.append(f"Customer: {customer_name}")
        
        receipt.append("-"*width)
        
        # Items header
        receipt.append("{:<25} {:<6} {:<8} {:<10}".format("ITEM", "QTY", "PRICE", "TOTAL"))
        receipt.append("-"*width)
        
        # Items
        gross_total = 0.0
        for name, details in transaction.items():
            amount = details['price'] * details['quantity']
            gross_total += amount
            receipt.append("{:<25} {:<6} {:<8.2f} {:<10.2f}".format(
                name[:25], details['quantity'], details['price'], amount))
        
        receipt.append("-"*width)
        
        # Totals
        receipt.append("GROSS TOTAL:".ljust(40) + f"PKR {gross_total:.2f}".rjust(10))
        
        if self.receipt_settings["show_discount"]:
            try:
                discount_percent = float(self.discount_entry.get())
            except ValueError:
                discount_percent = 0
            
            if discount_percent > 0:
                discount_amount = gross_total * (discount_percent / 100)
                net_total = gross_total - discount_amount
                
                receipt.append(f"DISCOUNT ({discount_percent}%):".ljust(40) + f"-PKR {discount_amount:.2f}".rjust(10))
                receipt.append("NET TOTAL:".ljust(40) + f"PKR {net_total:.2f}".rjust(10))
            else:
                net_total = gross_total
        else:
            net_total = gross_total
        
        receipt.append("-"*width)
        
        # Generator name in a box
        generator_line = f" Generated by: {self.receipt_settings['generator_name']} "
        box_width = width - 4
        if len(generator_line) > box_width:
            generator_line = generator_line[:box_width]
        
        receipt.append("+" + "-"*(width-2) + "+")
        receipt.append("|" + generator_line.center(width-2) + "|")
        receipt.append("+" + "-"*(width-2) + "+")
        
        # Footer
        receipt.append(self.receipt_settings["footer_text"].center(width))
        receipt.append("="*width)
        
        return "\n".join(receipt)
    
    def show_receipt_window(self, receipt_text):
        """Display receipt in a new window with print button"""
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Sale Receipt")
        receipt_window.geometry("500x700")
        self.center_window(receipt_window)
        
        text = scrolledtext.ScrolledText(receipt_window, wrap=tk.WORD, width=60, height=30,
                                        font=('Consolas', 10), padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        text.insert(tk.END, receipt_text)
        text.config(state='disabled')
        
        button_frame = ttk.Frame(receipt_window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Print Receipt", style='Primary.TButton', 
                  command=lambda: self.print_receipt(receipt_text)).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Done", style='TButton', 
                  command=receipt_window.destroy).pack(side=tk.LEFT, padx=10)
    
    def print_receipt(self, receipt_text):
        """Print the receipt to default printer"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt') as tmp_file:
                tmp_file.write(receipt_text)
                tmp_file_path = tmp_file.name
            
            # Print using system command
            if os.name == 'nt':  # Windows
                os.startfile(tmp_file_path, 'print')
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'lpr {tmp_file_path}')
            
            # Schedule the file to be deleted after printing
            self.root.after(5000, lambda: os.unlink(tmp_file_path))
            
            self.status_var.set("Receipt sent to printer")
        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print receipt: {str(e)}")
            self.status_var.set("Printing failed")
    
    def view_sale_details(self, tree):
        """View details of a selected sale"""
        selected = tree.focus()
        if not selected:
            return
            
        sale_date = tree.item(selected, 'values')[0]
        
        # Skip if this is the summary row
        if sale_date == "TOTAL":
            return
        
        # Find the sale in history
        sale = next((s for s in self.sales_history if s['date'] == sale_date), None)
        if not sale:
            return
            
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Sale Details - {sale_date}")
        details_window.geometry("500x400")
        self.center_window(details_window)
        
        # Create text widget
        text = scrolledtext.ScrolledText(details_window, wrap=tk.WORD, 
                                       font=('Consolas', 10), padx=10, pady=10)
        text.pack(fill=tk.BOTH, expand=True)
        
        # Format sale details
        details = []
        details.append(f"Sale Date: {sale_date}")
        if 'customer' in sale:
            details.append(f"Customer: {sale['customer']}")
        details.append("-"*50)
        details.append("{:<30} {:<10} {:<10} {:<10}".format("Item", "Qty", "Price", "Total"))
        details.append("-"*50)
        
        for item in sale['items']:
            item_total = item['price'] * item['qty']
            details.append("{:<30} {:<10} {:<10.2f} {:<10.2f}".format(
                item['name'][:30], item['qty'], item['price'], item_total))
        
        details.append("-"*50)
        details.append(f"Gross Total: Pkr {sale['gross_total']:.2f}")
        if 'discount' in sale and sale['discount'] > 0:
            details.append(f"Discount: Pkr {sale['discount']:.2f}")
        details.append(f"Net Total: Pkr {sale['total']:.2f}")
        
        text.insert(tk.END, "\n".join(details))
        text.config(state='disabled')
    
    def export_sales_history(self):
        """Export sales history to a file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Sales History As"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    # Write header
                    f.write("Date,Customer,Item,Quantity,Price,Gross Total,Discount,Net Total\n")
                    
                    # Write data
                    for sale in self.sales_history:
                        for item in sale['items']:
                            f.write(f"{sale['date']},{sale.get('customer', 'Walk-in')},{item['name']},{item['qty']},{item['price']},{sale['gross_total']},{sale.get('discount', 0)},{sale['total']}\n")
                
                messagebox.showinfo("Success", f"Sales history exported to {file_path}")
                self.status_var.set(f"Sales history exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save the file: {str(e)}")
                self.status_var.set("Error exporting sales history")
    
    def create_reports_tab(self):
        """Create the reports tab"""
        self.reports_frame = ttk.Frame(self.content)
        
        # Header
        header = ttk.Frame(self.reports_frame)
        header.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(header, text="Reports", style='Header.TLabel').pack(side=tk.LEFT)
        
        # Report type selection
        report_frame = ttk.Frame(self.reports_frame)
        report_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(report_frame, text="Report Type:").pack(side=tk.LEFT)
        self.report_type = tk.StringVar()
        report_options = ['Inventory List', 'Low Stock', 'Expiring Soon', 'Empty Stocks', 'Sales Summary']
        self.report_type.set(report_options[0])
        
        report_menu = ttk.OptionMenu(report_frame, self.report_type, *report_options)
        report_menu.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(report_frame, text="Generate", style='Primary.TButton', 
                  command=self.generate_report).pack(side=tk.LEFT, padx=5)
        
        # Button frame
        btn_frame = ttk.Frame(report_frame)
        btn_frame.pack(side=tk.RIGHT)
        
        ttk.Button(btn_frame, text="Print", style='TButton', 
                  command=self.print_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Export", style='TButton', 
                  command=self.export_report).pack(side=tk.LEFT, padx=5)
        
        # Report display area
        self.report_text = scrolledtext.ScrolledText(self.reports_frame, wrap=tk.WORD, 
                                                   font=('Consolas', 10), padx=10, pady=10)
        self.report_text.pack(fill=tk.BOTH, expand=True)
    
    def generate_report(self):
        """Generate the selected report"""
        report_type = self.report_type.get()
        self.report_text.delete(1.0, tk.END)
        
        if report_type == "Inventory List":
            self.generate_inventory_report()
        elif report_type == "Low Stock":
            self.generate_low_stock_report()
        elif report_type == "Expiring Soon":
            self.generate_expiring_report()
        elif report_type == "Empty Stocks":
            self.generate_empty_stock_report()
        elif report_type == "Sales Summary":
            self.generate_sales_summary_report()
    
    def generate_inventory_report(self):
        """Generate inventory list report"""
        report = []
        report.append("MEDICAL STORE INVENTORY REPORT".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append("="*80)
        report.append("{:<25} {:<15} {:<10} {:<10} {:<12} {:<10}".format(
            "Medicine Name", "Company", "Price", "Quantity", "Expiry Date", "Batch No."))
        report.append("-"*80)
        
        total_value = 0.0
        for name, details in sorted(self.medicines.items()):
            item_value = details['price'] * details['quantity']
            total_value += item_value
            report.append("{:<25} {:<15} {:<10.2f} {:<10} {:<12} {:<10}".format(
                name[:25], details.get('company', 'All')[:15], details['price'], 
                details['quantity'], details['expiry'], details['batch']))
        
        report.append("="*80)
        report.append("TOTAL INVENTORY VALUE:".ljust(60) + f"PKR {total_value:.2f}".rjust(20))
        report.append("="*80)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.status_var.set("Inventory report generated")
    
    def generate_low_stock_report(self):
        """Generate low stock report (quantity < 20)"""
        report = []
        report.append("LOW STOCK REPORT (Quantity < 20)".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append("="*80)
        report.append("{:<25} {:<15} {:<10} {:<10} {:<12} {:<10}".format(
            "Medicine Name", "Company", "Price", "Quantity", "Expiry Date", "Batch No."))
        report.append("-"*80)
        
        low_stock_items = 0
        for name, details in sorted(self.medicines.items()):
            if 0 < details['quantity'] < 20:
                low_stock_items += 1
                report.append("{:<25} {:<15} {:<10.2f} {:<10} {:<12} {:<10}".format(
                    name[:25], details.get('company', 'All')[:15], details['price'], 
                    details['quantity'], details['expiry'], details['batch']))
        
        if low_stock_items == 0:
            report.append("No low stock items found (all items have quantity >= 20)".center(80))
        
        report.append("="*80)
        report.append(f"Total low stock items: {low_stock_items}".center(80))
        report.append("="*80)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.status_var.set(f"Low stock report generated ({low_stock_items} items)")
    
    def generate_expiring_report(self):
        """Generate report for medicines expiring soon (within 3 months)"""
        report = []
        report.append("EXPIRING SOON REPORT (within 3 months)".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append("="*80)
        report.append("{:<25} {:<15} {:<10} {:<10} {:<12} {:<10}".format(
            "Medicine Name", "Company", "Price", "Quantity", "Expiry Date", "Batch No."))
        report.append("-"*80)
        
        today = datetime.datetime.now().date()
        expiring = 0
        
        for name, details in sorted(self.medicines.items()):
            try:
                expiry_date = datetime.datetime.strptime(details['expiry'], "%d-%m-%Y").date()
                if (expiry_date - today).days <= 90:  # Within 3 months
                    expiring += 1
                    report.append("{:<25} {:<15} {:<10.2f} {:<10} {:<12} {:<10}".format(
                        name[:25], details.get('company', 'All')[:15], details['price'], 
                        details['quantity'], details['expiry'], details['batch']))
            except ValueError:
                continue
        
        if expiring == 0:
            report.append("No expiring items found (all items expire after 3 months)".center(80))
        
        report.append("="*80)
        report.append(f"Total expiring items: {expiring}".center(80))
        report.append("="*80)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.status_var.set(f"Expiring soon report generated ({expiring} items)")
    
    def generate_empty_stock_report(self):
        """Generate report for medicines with empty stock (quantity = 0)"""
        report = []
        report.append("EMPTY STOCK REPORT (Quantity = 0)".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append("="*80)
        report.append("{:<25} {:<15} {:<10} {:<12} {:<10}".format(
            "Medicine Name", "Company", "Price", "Expiry Date", "Batch No."))
        report.append("-"*80)
        
        empty_stock_items = 0
        for name, details in sorted(self.medicines.items()):
            if details['quantity'] == 0:
                empty_stock_items += 1
                report.append("{:<25} {:<15} {:<10.2f} {:<12} {:<10}".format(
                    name[:25], details.get('company', 'All')[:15], details['price'], 
                    details['expiry'], details['batch']))
        
        if empty_stock_items == 0:
            report.append("No empty stock items found (all items have quantity > 0)".center(80))
        
        report.append("="*80)
        report.append(f"Total empty stock items: {empty_stock_items}".center(80))
        report.append("="*80)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.status_var.set(f"Empty stock report generated ({empty_stock_items} items)")
    
    def generate_sales_summary_report(self):
        """Generate sales summary report"""
        report = []
        report.append("SALES SUMMARY REPORT".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        report.append("="*80)
        report.append("{:<12} {:<15} {:<10} {:<15} {:<15}".format(
            "Date", "Transactions", "Items Sold", "Gross Total", "Net Total"))
        report.append("-"*80)
        
        # Group sales by date
        sales_by_date = {}
        for sale in self.sales_history:
            date = sale['date']
            if date not in sales_by_date:
                sales_by_date[date] = {
                    'transactions': 0,
                    'items_sold': 0,
                    'gross_total': 0.0,
                    'net_total': 0.0
                }
            
            sales_by_date[date]['transactions'] += 1
            sales_by_date[date]['items_sold'] += sum(item['qty'] for item in sale['items'])
            sales_by_date[date]['gross_total'] += sale['gross_total']
            sales_by_date[date]['net_total'] += sale['total']
        
        # Sort by date (newest first)
        sorted_dates = sorted(sales_by_date.keys(), reverse=True)
        
        for date in sorted_dates:
            data = sales_by_date[date]
            report.append("{:<12} {:<15} {:<10} {:<15.2f} {:<15.2f}".format(
                date, 
                data['transactions'], 
                data['items_sold'], 
                data['gross_total'], 
                data['net_total']
            ))
        
        # Add totals
        total_transactions = sum(data['transactions'] for data in sales_by_date.values())
        total_items = sum(data['items_sold'] for data in sales_by_date.values())
        total_gross = sum(data['gross_total'] for data in sales_by_date.values())
        total_net = sum(data['net_total'] for data in sales_by_date.values())
        
        report.append("="*80)
        report.append("{:<12} {:<15} {:<10} {:<15.2f} {<-15.2f}".format(
                "TOTAL", 
                total_transactions, 
                total_items, 
                total_gross, 
                total_net
            ))
        report.append("="*80)
        
        self.report_text.insert(tk.END, "\n".join(report))
        self.status_var.set(f"Sales summary report generated ({total_transactions} transactions)")
    
    def print_report(self):
        """Print the current report"""
        report = self.report_text.get(1.0, tk.END)
        try:
            # For Windows
            if os.name == 'nt':
                os.system(f'echo "{report}" > PRN')
            # For Linux (requires lp command)
            else:
                os.system(f'lp -o raw <<< "{report}"')
            messagebox.showinfo("Success", "Report sent to printer")
        except:
            messagebox.showerror("Error", "Could not print report automatically")
    
    def export_report(self):
        """Export the current report to a file"""
        report = self.report_text.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Report As"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(report)
                messagebox.showinfo("Success", f"Report saved to {file_path}")
                self.status_var.set(f"Report exported to {file_path}")
            except:
                messagebox.showerror("Error", "Could not save the file")
                self.status_var.set("Error exporting report")
    
    def create_settings_tab(self):
        """Create the settings tab"""
        self.settings_frame = ttk.Frame(self.content)
        
        # Notebook for different setting categories
        notebook = ttk.Notebook(self.settings_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Store Information Tab
        store_tab = ttk.Frame(notebook)
        notebook.add(store_tab, text="Store Information")
        
        # Store information
        ttk.Label(store_tab, text="Store Information", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5))
        
        info_frame = ttk.Frame(store_tab)
        info_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(info_frame, text="Store Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.store_name_entry = ttk.Entry(info_frame, width=30)
        self.store_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.store_name_entry.insert(0, self.receipt_settings["header_text"])
        
        ttk.Label(info_frame, text="Address:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.address_entry = ttk.Entry(info_frame, width=30)
        self.address_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.address_entry.insert(0, self.receipt_settings["address"])
        
        ttk.Label(info_frame, text="Phone:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.phone_entry = ttk.Entry(info_frame, width=30)
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        self.phone_entry.insert(0, self.receipt_settings["phone"])
        
        # Receipt Settings Tab
        receipt_tab = ttk.Frame(notebook)
        notebook.add(receipt_tab, text="Receipt Settings")
        
        ttk.Label(receipt_tab, text="Receipt Settings", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5))
        
        fields = [
            ("Header Text:", "header_text", self.receipt_settings["header_text"]),
            ("Address:", "address", self.receipt_settings["address"]),
            ("Phone:", "phone", self.receipt_settings["phone"]),
            ("Footer Text:", "footer_text", self.receipt_settings["footer_text"]),
            ("Receipt Width:", "receipt_width", self.receipt_settings["receipt_width"]),
            ("Generator Name:", "generator_name", self.receipt_settings["generator_name"]),
            ("Default Discount %:", "default_discount", self.receipt_settings["default_discount"]),
            ("Show Customer Name:", "show_customer_name", self.receipt_settings["show_customer_name"]),
            ("Show Discount:", "show_discount", self.receipt_settings["show_discount"])
        ]
        
        self.settings_entries = {}
        for i, (label, name, value) in enumerate(fields):
            frame = ttk.Frame(receipt_tab)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            ttk.Label(frame, text=label).pack(side=tk.LEFT)
            
            if isinstance(value, bool):
                var = tk.BooleanVar(value=value)
                entry = ttk.Checkbutton(frame, variable=var)
                entry.pack(side=tk.RIGHT)
                self.settings_entries[name] = var
            else:
                entry = ttk.Entry(frame)
                entry.insert(0, str(value))
                entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
                self.settings_entries[name] = entry
        
        # Data Management Tab
        data_tab = ttk.Frame(notebook)
        notebook.add(data_tab, text="Data Management")
        
        ttk.Label(data_tab, text="Data Management", style='CardHeader.TLabel').pack(anchor='w', pady=(10, 5))
        
        # Data management buttons
        btn_frame = ttk.Frame(data_tab)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Save Data", style='Primary.TButton', 
                  command=self.save_data).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="Load Data", style='TButton', 
                  command=self.load_data).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Save button for settings
        btn_frame = ttk.Frame(self.settings_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Save Settings", style='Primary.TButton', 
                  command=self.save_settings).pack(side=tk.RIGHT, padx=5)
    
    def save_data(self):
        """Save all application data to a file"""
        data = {
            'medicines': self.medicines,
            'sales_history': self.sales_history,
            'receipt_settings': self.receipt_settings,
            'today_sales': self.today_sales_var.get()
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Medical Store Data", "*.pkl"), ("All Files", "*.*")],
            title="Save Medical Store Data"
        )
        
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)
                messagebox.showinfo("Success", f"Data saved successfully to {file_path}")
                self.status_var.set(f"Data saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save data: {str(e)}")
                self.status_var.set("Error saving data")
    
    def load_data(self):
        """Load application data from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Medical Store Data", "*.pkl"), ("All Files", "*.*")],
            title="Open Medical Store Data"
        )
        
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.medicines = data.get('medicines', {})
                self.sales_history = data.get('sales_history', [])
                self.receipt_settings = data.get('receipt_settings', self.receipt_settings)
                self.today_sales_var.set(data.get('today_sales', "Pkr 0.00"))
                
                # Update UI
                self.refresh_inventory()
                self.refresh_sales_list()
                self.update_dashboard()
                
                # Update settings UI
                self.store_name_entry.delete(0, tk.END)
                self.store_name_entry.insert(0, self.receipt_settings["header_text"])
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, self.receipt_settings["address"])
                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, self.receipt_settings["phone"])
                
                messagebox.showinfo("Success", f"Data loaded successfully from {file_path}")
                self.status_var.set(f"Data loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not load data: {str(e)}")
                self.status_var.set("Error loading data")
    
    def auto_save_data(self):
        """Auto-save data to a default location"""
        try:
            data = {
                'medicines': self.medicines,
                'sales_history': self.sales_history,
                'receipt_settings': self.receipt_settings,
                'today_sales': self.today_sales_var.get()
            }
            
            # Save to a default location in temp directory
            save_path = os.path.join(tempfile.gettempdir(), "pharmacare_autosave.pkl")
            
            with open(save_path, 'wb') as f:
                pickle.dump(data, f)
            
            # Schedule the next auto-save
            self.root.after(300000, self.auto_save_data)  # Auto-save every 5 minutes
        except Exception as e:
            print(f"Auto-save failed: {str(e)}")
    
    def try_auto_load(self):
        """Try to auto-load data from default location"""
        try:
            save_path = os.path.join(tempfile.gettempdir(), "pharmacare_autosave.pkl")
            if os.path.exists(save_path):
                with open(save_path, 'rb') as f:
                    data = pickle.load(f)
                
                self.medicines = data.get('medicines', {})
                self.sales_history = data.get('sales_history', [])
                self.receipt_settings = data.get('receipt_settings', self.receipt_settings)
                self.today_sales_var.set(data.get('today_sales', "Pkr 0.00"))
                
                # Update UI
                self.refresh_inventory()
                self.refresh_sales_list()
                self.update_dashboard()
                
                # Update settings UI
                self.store_name_entry.delete(0, tk.END)
                self.store_name_entry.insert(0, self.receipt_settings["header_text"])
                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, self.receipt_settings["address"])
                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, self.receipt_settings["phone"])
                
                self.status_var.set("Auto-loaded previous session data")
        except Exception as e:
            print(f"Auto-load failed: {str(e)}")
    
    def save_settings(self):
        """Save system settings"""
        try:
            self.receipt_settings["header_text"] = self.store_name_entry.get()
            self.receipt_settings["address"] = self.address_entry.get()
            self.receipt_settings["phone"] = self.phone_entry.get()
            
            self.receipt_settings["footer_text"] = self.settings_entries["footer_text"].get()
            self.receipt_settings["receipt_width"] = int(self.settings_entries["receipt_width"].get())
            self.receipt_settings["generator_name"] = self.settings_entries["generator_name"].get()
            self.receipt_settings["default_discount"] = float(self.settings_entries["default_discount"].get())
            
            # Handle boolean values
            if isinstance(self.settings_entries["show_customer_name"], tk.BooleanVar):
                self.receipt_settings["show_customer_name"] = self.settings_entries["show_customer_name"].get()
                self.receipt_settings["show_discount"] = self.settings_entries["show_discount"].get()
            
            # Update discount entry in sales tab
            self.discount_entry.delete(0, tk.END)
            self.discount_entry.insert(0, str(self.receipt_settings["default_discount"]))
            
            messagebox.showinfo("Success", "Settings saved successfully")
            self.status_var.set("Settings updated")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def center_window(self, window):
        """Center a window on screen"""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernMedicalStore(root)
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit? All unsaved changes will be auto-saved."):
            # Perform one final auto-save
            try:
                data = {
                    'medicines': app.medicines,
                    'sales_history': app.sales_history,
                    'receipt_settings': app.receipt_settings,
                    'today_sales': app.today_sales_var.get()
                }
                
                save_path = os.path.join(tempfile.gettempdir(), "pharmacare_autosave.pkl")
                with open(save_path, 'wb') as f:
                    pickle.dump(data, f)
            except Exception as e:
                print(f"Final auto-save failed: {str(e)}")
            
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()