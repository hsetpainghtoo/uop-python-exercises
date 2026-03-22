# Lanfeng Sale Data Analysis
# Lanfeng Fuel Management System
# modified by : digital Engineer Tech
# version : 2.0.0
# date : 2025-12-10
# license : MIT
# contact : iih , @nck

import sys
import sys
import os
import datetime
import warnings
import logging
import traceback

# Setup Logging
def setup_logging():
    # Detect if we are running as a script or frozen exe
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
        
    log_file = os.path.join(application_path, 'app_debug.log')
    
    logging.basicConfig(
        filename=log_file,
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        force=True
    )
    logging.info(f"Logging initialized. File: {log_file}")
    sys.excepthook = handle_exception

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

# Suppress cryptography warnings if needed
warnings.filterwarnings("ignore")

import mysql.connector
from mysql.connector import Error
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QTableWidget, QTableWidgetItem, QDateEdit, 
                             QHeaderView, QFrame, QMessageBox, QComboBox, QDialog, QFormLayout, QGroupBox)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QColor, QFont, QIcon, QPixmap

# SSH Import
from sshtunnel import SSHTunnelForwarder

# --- CONFIGURATION ---
CONNECTION_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'asdffdsa',
    'database': 'fuel_management',
    'use_ssh': True,
    'ssh_host': '192.168.0.100',
    'ssh_port': 22,
    'ssh_user': 'pos',
    'ssh_pass': '    ' # 4 spaces
}

# --- 2. LOGIN DIALOG ---
class AppLoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FMS Enterprise Login")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(350, 220)
        self.setStyleSheet("""
            QDialog { background-color: #ECEFF1; }
            QLabel { font-size: 14px; color: #37474F; }
            QLineEdit { 
                padding: 8px; 
                border: 1px solid #CFD8DC; 
                border-radius: 4px;
                background-color: white;
            }
            QPushButton {
                background-color: #1a237e;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #283593; }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("FMS Enterprise")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a237e; margin-bottom: 10px;")
        layout.addWidget(title)

        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        # Button
        self.btn_login = QPushButton("LOGIN")
        self.btn_login.clicked.connect(self.check_credentials)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if username == "admin" and password == "admin":
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid Username or Password")


# --- 3. SALES MANAGER APPLICATION ---
class SalesManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fuel Management - Sales Analysis")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(1300, 700)
        
        self.conn = None
        self.tunnel = None

        self.columns = [
            "voucher_no", "created_at",
            "nozzle_id", "sale_price", "sale_liter", 
            "total_price", "device_totalizer_liter", 
            "device_totalizer_amount", "state"
        ]

        self.init_ui()
        self.apply_styles()
        
        # Auto-Connect after UI loads
        QTimer.singleShot(100, lambda: self.connect_process(CONNECTION_CONFIG))

    def init_ui(self):
        # Main Container (HBox)
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # --- LEFT SIDEBAR ---
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(250)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(10)
        
        # App Title in Sidebar
        # App Title / Logo in Sidebar
        logo_label = QLabel()
        logo_label.setObjectName("AppLogo")
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Try to load logo, fallback to text if missing
        pixmap = QPixmap("logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(200, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setStyleSheet("padding: 20px; background-color: #1a237e;")
        else:
            logo_label.setText("FMS\nENTERPRISE")
            logo_label.setObjectName("AppTitle") # Revert to text style
            
        sidebar_layout.addWidget(logo_label)
        
        # Navigation Buttons
        # self.nav_dashboard = QPushButton("  Dashboard") 
        self.nav_transactions = QPushButton("  Transactions")
        # self.nav_settings = QPushButton("  Settings")
        
        # Just add the single button
        self.nav_transactions.setCheckable(True)
        self.nav_transactions.setObjectName("NavButton")
        sidebar_layout.addWidget(self.nav_transactions)
            
        self.nav_transactions.setChecked(True) # Default active
        
        sidebar_layout.addStretch()
        
        # User Profile Stub
        user_lbl = QLabel("User: Admin\nRole: Manager")
        user_lbl.setObjectName("UserProfile")
        user_lbl.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(user_lbl)
        
        main_layout.addWidget(sidebar)

        # --- RIGHT CONTENT AREA ---
        content_area = QWidget()
        content_area.setObjectName("ContentArea")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)

        # 1. Top Header (Breadcrumbs)
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        page_title = QLabel("Sales Transactions")
        page_title.setObjectName("PageTitle")
        header_layout.addWidget(page_title)
        header_layout.addStretch()
        header_layout.addWidget(QLabel("v2.0.0-Enterprise-beta"))
        
        content_layout.addWidget(header_frame)

        # 2. Action Ribbon (Filters)
        ribbon = QFrame()
        ribbon.setObjectName("Ribbon")
        ribbon_layout = QHBoxLayout(ribbon)
        ribbon_layout.setContentsMargins(15, 10, 15, 10)
        ribbon_layout.setSpacing(15)

        # Date Group
        ribbon_layout.addWidget(QLabel("Date Period:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())
        ribbon_layout.addWidget(self.date_input)

        # Separator
        line1 = QFrame()
        line1.setFrameShape(QFrame.VLine)
        line1.setObjectName("RibbonSep")
        ribbon_layout.addWidget(line1)

        # Nozzle Group
        ribbon_layout.addWidget(QLabel("Nozzle:"))
        self.nozzle_input = QLineEdit()
        self.nozzle_input.setPlaceholderText("ID")
        self.nozzle_input.setFixedWidth(60)
        ribbon_layout.addWidget(self.nozzle_input)
        
        # Buttons
        self.search_btn = QPushButton("REFRESH DATA")
        self.search_btn.setObjectName("ActionBtn")
        self.search_btn.clicked.connect(self.load_sales_data)
        ribbon_layout.addWidget(self.search_btn)
        
        ribbon_layout.addStretch()
        content_layout.addWidget(ribbon)

        # 3. Data Grid
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([c.replace("_", " ").upper() for c in self.columns])
        self.table.setAlternatingRowColors(True)
        self.table.setShowGrid(True)
        self.table.setGridStyle(Qt.DotLine)
        self.table.itemChanged.connect(self.handle_cell_change)
        
        # Header formatting
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        header.setDefaultSectionSize(120)
        
        content_layout.addWidget(self.table)
        
        main_layout.addWidget(content_area)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # --- STATUS BAR ---
        self.db_status_label = QLabel("Disconnected")
        self.db_status_label.setStyleSheet("color: black; padding: 4px 8px; border-radius: 4px;")
        self.statusBar().addPermanentWidget(self.db_status_label)

    def connect_process(self, creds):
        if self.conn: self.conn.close()
        if self.tunnel: self.tunnel.stop()

        try:
            db_host = creds['host']
            db_port = creds['port']

            if creds['use_ssh']:
                self.statusBar().showMessage("Establishing SSH Tunnel...")
                logging.info(f"Connecting to SSH: {creds['ssh_host']}:{creds['ssh_port']} as {creds['ssh_user']}")
                
                # --- FIXED SSH CONNECTION (Cleaned up arguments) ---
                self.tunnel = SSHTunnelForwarder(
                    (creds['ssh_host'], creds['ssh_port']),
                    ssh_username=creds['ssh_user'],
                    ssh_password=creds['ssh_pass'],
                    # Where the DB is relative to the SSH server 
                    remote_bind_address=(creds['host'], creds['port'])
                )
                self.tunnel.start()
                
                # Point MySQL to the local end of the tunnel
                db_host = '127.0.0.1'
                db_port = self.tunnel.local_bind_port
                logging.info(f"SSH Tunnel Active. Local Bind Port: {db_port}")

            # Connect to MySQL
            logging.info(f"Connecting to MySQL: {db_host}:{db_port}...")
            self.conn = mysql.connector.connect(
                host=db_host,
                port=db_port,
                user=creds['user'],
                password=creds['password'],
                database=creds['database'],
                use_pure=True,  # Force pure python to avoid C-extension crashes
                connection_timeout=10
            )
            
            self.statusBar().showMessage(f"Connected to {creds['database']} via {'SSH' if creds['use_ssh'] else 'Direct'}")
            self.db_status_label.setText("CONNECTED")
            self.db_status_label.setStyleSheet("color: black;padding: 4px 8px; border-radius: 4px;")
            
            # --- AUTO-DETECT LAST ACTIVE DATE ---
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT MAX(DATE(created_at)) FROM sales")
                result = cursor.fetchone()
                if result and result[0]:
                    last_date = result[0] # Returns a datetime.date object
                    # Convert python date to QDate
                    q_date = QDate(last_date.year, last_date.month, last_date.day)
                    self.date_input.setDate(q_date)
                    print(f"Auto-selected last active date: {last_date}")
            except Exception as e:
                print(f"Date auto-detection failed: {e}")

            # Auto-load data (now using the correct date)
            self.load_sales_data()

        except Exception as e:
            logging.error("Connection Failed", exc_info=True)
            if self.tunnel: self.tunnel.stop()
            # print(f"ERROR: {e}") 
            QMessageBox.critical(self, "Connection Error", f"Failed to connect:\n{str(e)}")
            self.db_status_label.setText("ERROR")
            self.db_status_label.setStyleSheet("color: white; font-weight: bold; background-color: #D32F2F; padding: 4px 8px; border-radius: 4px;")
            # self.show_login()

    def load_sales_data(self):
        if not self.conn: return

        selected_date = self.date_input.date().toString("yyyy-MM-dd")
        nozzle_id = self.nozzle_input.text().strip()

        cols_sql = ", ".join([f"`{c}`" for c in self.columns])
        # IMPORTANT: Fetch ID explicitly as the first column for internal use
        base_query = f"SELECT id, {cols_sql} FROM sales WHERE DATE(created_at) = %s"
        params = [selected_date]
        
        # Optional Nozzle Filter
        if nozzle_id:
            base_query += " AND nozzle_id = %s"
            params.append(nozzle_id)

        try:
            cursor = self.conn.cursor()
            cursor.execute(base_query, tuple(params))
            rows = cursor.fetchall()

            self.table.blockSignals(True)
            self.table.setRowCount(0)

            for row_idx, row_data in enumerate(rows):
                self.table.insertRow(row_idx)
                
                # Extract hidden ID (index 0) and visible data (index 1+)
                row_id = row_data[0]
                visible_data = row_data[1:]

                for col_idx, value in enumerate(visible_data):
                    item = QTableWidgetItem(str(value) if value is not None else "")
                    
                    # Store ID in the first column's hidden UserRole data
                    if col_idx == 0: 
                        item.setData(Qt.UserRole, row_id)
                        # Optionally make the first visible column read-only (e.g. Voucher No)
                        item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                        item.setBackground(QColor("#F5F5F5"))
                    
                    self.table.setItem(row_idx, col_idx, item)

            self.table.blockSignals(False)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
            self.statusBar().showMessage(f"Loaded {len(rows)} rows for {selected_date}")

        except Error as e:
            QMessageBox.critical(self, "SQL Error", str(e))

    def handle_cell_change(self, item):
        row = item.row()
        col = item.column()
        column_name = self.columns[col]
        new_value = item.text()
        
        # Retrieve hidden ID from the first column of this row
        first_item = self.table.item(row, 0)
        if not first_item: return
        
        row_id = first_item.data(Qt.UserRole)
        if not row_id:
            QMessageBox.warning(self, "Error", "Cannot update: Row ID missing.")
            return

        try:
            cursor = self.conn.cursor()
            sql = f"UPDATE sales SET `{column_name}` = %s WHERE id = %s"
            cursor.execute(sql, (new_value, row_id))
            self.conn.commit()
            self.statusBar().showMessage(f"Updated ID {row_id}: Set {column_name} = {new_value}")
            item.setBackground(QColor("#E8F5E9")) # Light Green success
        except Error as e:
            self.conn.rollback()
            QMessageBox.critical(self, "Update Failed", str(e))

    def closeEvent(self, event):
        if self.tunnel: self.tunnel.stop()
        if self.conn: self.conn.close()
        event.accept()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ECEFF1;
            }
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
                color: #263238;
            }
            
            /* SIDEBAR */
            QFrame#Sidebar {
                background-color: #263238; /* Blue Grey 900 */
                border-right: 1px solid #263238;
            }
            QLabel#AppTitle {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
                padding: 20px;
                background-color: #1a237e; /* Deep Blue Brand */
                margin-bottom: 20px;
            }
            QLabel#UserProfile {
                color: #B0BEC5;
                font-size: 12px;
                padding: 20px;
                border-top: 1px solid #37474F;
            }
            QPushButton#NavButton {
                background-color: transparent;
                color: #CFD8DC;
                border: none;
                text-align: left;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
                border-left: 4px solid transparent;
            }
            QPushButton#NavButton:hover {
                background-color: #37474F;
                color: white;
            }
            QPushButton#NavButton:checked {
                background-color: #37474F;
                color: white;
                border-left: 4px solid #448AFF; /* Accent Blue */
            }
            
            /* RIGHT CONTENT */
            QWidget#ContentArea {
                background-color: #ECEFF1; /* Light Grey Bg */
            }
            
            /* HEADER */
            QLabel#PageTitle {
                font-size: 24px;
                font-weight: 300;
                color: #37474F;
                margin-bottom: 5px;
            }
            
            /* RIBBON / TOOLBAR */
            QFrame#Ribbon {
                background-color: #ffffff;
                border: 1px solid #CFD8DC;
                border-radius: 4px;
            }
            QFrame#RibbonSep {
                color: #ECEFF1;
            }
            
            /* INPUTS */
            QLineEdit, QDateEdit {
                border: 1px solid #CFD8DC;
                border-radius: 2px;
                padding: 6px;
                background: white;
                selection-background-color: #448AFF;
            }
            QLineEdit:focus, QDateEdit:focus {
                border: 1px solid #448AFF;
            }
            
            /* ACTION BUTTONS */
            QPushButton#ActionBtn {
                background-color: #448AFF;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 15px;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 11px;
                letter-spacing: 0.5px;
            }
            QPushButton#ActionBtn:hover {
                background-color: #2979FF;
            }
            
            /* DATA TABLE (LEDGER STYLE) */
            QTableWidget {
                background-color: white;
                border: 1px solid #B0BEC5;
                gridline-color: #ECEFF1;
                font-family: 'Consolas', 'Segoe UI Mono', monospace; /* Accounting Number Font */
            }
            QHeaderView::section {
                background-color: #fafafa;
                color: #546E7A;
                padding: 8px;
                border: none;
                border-bottom: 2px solid #CFD8DC;
                border-right: 1px solid #ECEFF1;
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
            }
            QTableWidget::item {
                padding-left: 5px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #0D47A1;
            }
        """)



if __name__ == "__main__":
    setup_logging()
    app = QApplication(sys.argv)
    
    # Login Dialog Loop
    login = AppLoginDialog()
    if login.exec_() == QDialog.Accepted:
        # Proceed to Main Application if valid
        window = SalesManager()
        window.show()
        sys.exit(app.exec_())
    else:
        # Exit if cancelled
        sys.exit()