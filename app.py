# ============================================================================
# PRAGNYA PHARM - Complete Professional Pharmacy System
# ============================================================================
import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import os
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ============================================================================
st.set_page_config(
    page_title="Pragnya Pharm - Smart Pharmacy",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS with Indian pharmacy colors
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Main header with Indian pharmacy green */
    .main-header {
        background: linear-gradient(135deg, #0A5C36 0%, #1E8449 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 8px 25px rgba(10, 92, 54, 0.15);
    }
    
    /* Pharmacy logo style */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    
    .pharmacy-logo {
        font-size: 3rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Metric cards - Professional */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #0A5C36;
        transition: all 0.3s ease;
        margin: 8px 0;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    
    /* Alert system */
    .alert-critical {
        background: linear-gradient(135deg, #E74C3C 0%, #C0392B 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: alertPulse 1.5s infinite;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #F39C12 0%, #D68910 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, #3498DB 0%, #2980B9 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    @keyframes alertPulse {
        0% { opacity: 1; }
        50% { opacity: 0.9; }
        100% { opacity: 1; }
    }
    
    /* Chatbot styling */
    .chat-user {
        background: #E8F6F3;
        padding: 12px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 8px 0;
        max-width: 80%;
        float: left;
        clear: both;
    }
    
    .chat-bot {
        background: #0A5C36;
        color: white;
        padding: 12px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 8px 0;
        max-width: 80%;
        float: right;
        clear: both;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #0A5C36 0%, #1E8449 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(10, 92, 54, 0.3);
    }
    
    /* Sidebar styling */
    .sidebar-header {
        background: linear-gradient(135deg, #0A5C36 0%, #1E8449 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Table styling */
    .dataframe {
        font-size: 14px;
    }
    
    .dataframe th {
        background-color: #0A5C36 !important;
        color: white !important;
    }
    
    .expiring-soon {
        background-color: #FFF3CD !important;
    }
    
    .low-stock {
        background-color: #F8D7DA !important;
    }
    
    /* Status indicators */
    .status-active {
        color: #28B463;
        font-weight: bold;
    }
    
    .status-expired {
        color: #E74C3C;
        font-weight: bold;
    }
    
    .status-warning {
        color: #F39C12;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. DATABASE MANAGER (Indian Pharmacy Style)
# ============================================================================
class IndianPharmacyDB:
    def __init__(self):
        self.db_file = 'pharmacy.db'
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create database tables for Indian pharmacy operations"""
        # Medicines table with Indian naming conventions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT NOT NULL,
                generic_name TEXT,
                company TEXT,
                batch_no TEXT,
                mfg_date TEXT,
                expiry_date TEXT,
                quantity INTEGER DEFAULT 0,
                max_quantity INTEGER,
                min_quantity INTEGER DEFAULT 20,
                mrp REAL,
                purchase_price REAL,
                category TEXT,
                schedule TEXT,
                store_location TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Daily sales records
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT,
                medicine_id INTEGER,
                quantity INTEGER,
                selling_price REAL,
                discount REAL DEFAULT 0,
                gst_percent REAL DEFAULT 18,
                total_amount REAL,
                customer_name TEXT,
                customer_phone TEXT,
                doctor_name TEXT,
                sale_date DATE DEFAULT CURRENT_DATE,
                payment_mode TEXT,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Suppliers (Indian companies)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS suppliers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                gst_no TEXT,
                payment_terms TEXT
            )
        ''')
        
        # Prescriptions
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_name TEXT,
                patient_age INTEGER,
                patient_gender TEXT,
                patient_phone TEXT,
                doctor_name TEXT,
                doctor_license TEXT,
                diagnosis TEXT,
                date TEXT,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        
        # Prescription items
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS prescription_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prescription_id INTEGER,
                medicine_name TEXT,
                dosage TEXT,
                frequency TEXT,
                duration TEXT,
                instructions TEXT,
                FOREIGN KEY (prescription_id) REFERENCES prescriptions (id)
            )
        ''')
        
        # Stock alerts
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id INTEGER,
                alert_type TEXT,
                message TEXT,
                severity TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved BOOLEAN DEFAULT 0,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Auto reorder queue
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS reorder_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                medicine_id INTEGER,
                quantity INTEGER,
                reason TEXT,
                priority TEXT,
                status TEXT DEFAULT 'Pending',
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (medicine_id) REFERENCES medicines (id)
            )
        ''')
        
        # Patient adherence tracking
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_adherence (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_phone TEXT,
                medicine_name TEXT,
                prescribed_date DATE,
                next_refill_date DATE,
                last_refill_date DATE,
                adherence_score INTEGER,
                notes TEXT
            )
        ''')
        
        self.conn.commit()
        self.load_initial_indian_medicines()
    
    def load_initial_indian_medicines(self):
        """Load common Indian medicines"""
        count = self.cursor.execute("SELECT COUNT(*) FROM medicines").fetchone()[0]
        if count == 0:
            # Common Indian medicines with realistic data
            medicines = [
                # Analgesics
                ('Crocin 650mg', 'Paracetamol', 'GSK', 'CRN-2024-01', '2024-01-15', '2025-12-31', 100, 200, 30, 15.0, 8.5, 'Analgesic', 'OTC', 'Rack A1'),
                ('Combiflam', 'Ibuprofen + Paracetamol', 'Sanofi', 'CBF-2024-02', '2024-02-10', '2025-11-30', 75, 150, 25, 25.0, 15.0, 'Analgesic', 'OTC', 'Rack A2'),
                
                # Antibiotics
                ('Augmentin 625mg', 'Amoxicillin + Clavulanic', 'GSK', 'AUG-2024-01', '2024-01-20', '2025-10-31', 50, 100, 20, 180.0, 120.0, 'Antibiotic', 'Schedule H', 'Rack B1'),
                ('Azithral 500mg', 'Azithromycin', 'Alembic', 'AZT-2024-03', '2024-03-05', '2026-03-04', 60, 120, 25, 85.0, 55.0, 'Antibiotic', 'Schedule H', 'Rack B2'),
                
                # Cardiac
                ('Cardace 5mg', 'Ramipril', 'Sun Pharma', 'CRD-2024-01', '2024-01-12', '2025-12-31', 80, 160, 40, 120.0, 85.0, 'Cardiac', 'Schedule H', 'Rack C1'),
                ('Storvas 10mg', 'Atorvastatin', 'Sun Pharma', 'STV-2024-02', '2024-02-18', '2026-02-17', 90, 180, 45, 95.0, 65.0, 'Cardiac', 'Schedule H', 'Rack C2'),
                
                # Diabetic
                ('Glycomet GP 1', 'Metformin + Glimepiride', 'USV', 'GLY-2024-01', '2024-01-25', '2025-12-31', 120, 240, 50, 135.0, 90.0, 'Diabetic', 'Schedule H', 'Rack D1'),
                ('Januvia 100mg', 'Sitagliptin', 'MSD', 'JNV-2024-02', '2024-02-14', '2026-02-13', 40, 80, 20, 480.0, 350.0, 'Diabetic', 'Schedule H', 'Rack D2'),
                
                # Gastrointestinal
                ('Pantop 40mg', 'Pantoprazole', 'Sun Pharma', 'PAN-2024-01', '2024-01-08', '2025-12-31', 150, 300, 60, 45.0, 25.0, 'GI', 'Schedule H', 'Rack E1'),
                ('Cyclopam', 'Dicyclomine + Paracetamol', 'Mankind', 'CYC-2024-03', '2024-03-01', '2026-02-28', 110, 220, 45, 65.0, 35.0, 'GI', 'OTC', 'Rack E2'),
            ]
            
            for med in medicines:
                self.cursor.execute('''
                    INSERT INTO medicines 
                    (brand_name, generic_name, company, batch_no, mfg_date, expiry_date, 
                     quantity, max_quantity, min_quantity, mrp, purchase_price, category, schedule, store_location)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', med)
            
            # Add sample suppliers
            suppliers = [
                ('Medley Pharmaceuticals', '022-12345678', 'orders@medley.com', 'Plot No. 107, Andheri', 'Mumbai', 'Maharashtra', '27AAACM1234M1Z5', 'Net 30'),
                ('Cipla Limited', '022-87654321', 'supply@cipla.com', 'Mumbai Central', 'Mumbai', 'Maharashtra', '27AABCC1234M1Z2', 'Net 45'),
                ('Sun Pharmaceutical', '079-23456789', 'purchase@sunpharma.com', 'Sarkhej-Bavla Highway', 'Ahmedabad', 'Gujarat', '24AABCS1234M1Z3', 'Net 60'),
            ]
            
            for sup in suppliers:
                self.cursor.execute('''
                    INSERT INTO suppliers (name, phone, email, address, city, state, gst_no, payment_terms)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', sup)
            
            self.conn.commit()
    
    def add_medicine(self, medicine_data):
        """Add new medicine to database"""
        try:
            self.cursor.execute('''
                INSERT INTO medicines 
                (brand_name, generic_name, company, batch_no, mfg_date, expiry_date, 
                 quantity, max_quantity, min_quantity, mrp, purchase_price, category, schedule, store_location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', medicine_data)
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            st.error(f"Error adding medicine: {str(e)}")
            return None
    
    def update_stock_from_sales(self, medicine_id, quantity_sold):
        """Update stock after sales - Indian pharmacy style"""
        try:
            # Get current stock
            self.cursor.execute("SELECT quantity FROM medicines WHERE id = ?", (medicine_id,))
            current = self.cursor.fetchone()
            
            if current:
                new_quantity = current[0] - quantity_sold
                if new_quantity < 0:
                    new_quantity = 0
                
                # Update stock
                self.cursor.execute("UPDATE medicines SET quantity = ?, last_updated = CURRENT_TIMESTAMP WHERE id = ?", 
                                  (new_quantity, medicine_id))
                
                # Check if reorder needed
                self.cursor.execute("SELECT min_quantity FROM medicines WHERE id = ?", (medicine_id,))
                min_qty = self.cursor.fetchone()[0]
                
                if new_quantity <= min_qty:
                    self.create_alert(medicine_id, 'LOW_STOCK', 
                                    f'Stock below minimum ({new_quantity}/{min_qty})', 'HIGH')
                    
                    # Auto-add to reorder queue
                    self.cursor.execute('''
                        INSERT INTO reorder_queue (medicine_id, quantity, reason, priority)
                        SELECT id, max_quantity - quantity, 'Auto-reorder: Low stock', 'HIGH'
                        FROM medicines WHERE id = ? AND quantity <= min_quantity
                    ''', (medicine_id,))
                
                self.conn.commit()
                return True
        except Exception as e:
            st.error(f"Error updating stock: {str(e)}")
            return False
    
    def create_alert(self, medicine_id, alert_type, message, severity):
        """Create alert in database"""
        self.cursor.execute('''
            INSERT INTO alerts (medicine_id, alert_type, message, severity)
            VALUES (?, ?, ?, ?)
        ''', (medicine_id, alert_type, message, severity))
        self.conn.commit()
    
    def process_excel_upload(self, df, upload_type):
        """Process Excel uploads for sales or inventory"""
        try:
            if upload_type == 'sales':
                for _, row in df.iterrows():
                    # Find medicine by brand name
                    self.cursor.execute("SELECT id FROM medicines WHERE brand_name LIKE ?", 
                                      (f"%{row['Medicine']}%",))
                    result = self.cursor.fetchone()
                    
                    if result:
                        medicine_id = result[0]
                        quantity = int(row['Quantity'])
                        self.update_stock_from_sales(medicine_id, quantity)
                        
                        # Record sale
                        self.cursor.execute('''
                            INSERT INTO sales (medicine_id, quantity, selling_price, total_amount, sale_date)
                            VALUES (?, ?, ?, ?, DATE('now'))
                        ''', (medicine_id, quantity, row.get('Price', 0), row.get('Total', 0)))
                
                self.conn.commit()
                return True, f"Processed {len(df)} sales records"
                
            elif upload_type == 'inventory':
                for _, row in df.iterrows():
                    self.cursor.execute('''
                        INSERT OR REPLACE INTO medicines 
                        (brand_name, generic_name, company, expiry_date, quantity, mrp, category)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        row.get('Brand Name', ''),
                        row.get('Generic Name', ''),
                        row.get('Company', ''),
                        row.get('Expiry Date', '2025-12-31'),
                        int(row.get('Quantity', 0)),
                        float(row.get('MRP', 0)),
                        row.get('Category', 'Other')
                    ))
                
                self.conn.commit()
                return True, f"Updated {len(df)} inventory items"
                
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        stats = {}
        
        # Total medicines
        self.cursor.execute("SELECT COUNT(*) FROM medicines")
        stats['total_medicines'] = self.cursor.fetchone()[0]
        
        # Low stock count
        self.cursor.execute("SELECT COUNT(*) FROM medicines WHERE quantity <= min_quantity")
        stats['low_stock'] = self.cursor.fetchone()[0]
        
        # Expiring soon (within 30 days)
        self.cursor.execute('''
            SELECT COUNT(*) FROM medicines 
            WHERE date(expiry_date) BETWEEN date('now') AND date('now', '+30 days')
        ''')
        stats['expiring_soon'] = self.cursor.fetchone()[0]
        
        # Today's sales
        self.cursor.execute("SELECT SUM(total_amount) FROM sales WHERE sale_date = DATE('now')")
        today_sales = self.cursor.fetchone()[0]
        stats['today_sales'] = today_sales if today_sales else 0
        
        # Total inventory value
        self.cursor.execute("SELECT SUM(quantity * purchase_price) FROM medicines")
        inv_value = self.cursor.fetchone()[0]
        stats['inventory_value'] = inv_value if inv_value else 0
        
        # Active alerts
        self.cursor.execute("SELECT COUNT(*) FROM alerts WHERE resolved = 0 AND severity = 'HIGH'")
        stats['critical_alerts'] = self.cursor.fetchone()[0]
        
        return stats
    
    def get_expiring_medicines(self, days=30):
        """Get medicines expiring within given days"""
        query = '''
            SELECT brand_name, generic_name, quantity, expiry_date, 
                   julianday(expiry_date) - julianday('now') as days_left
            FROM medicines 
            WHERE days_left BETWEEN 0 AND ?
            ORDER BY days_left
        '''
        return pd.read_sql_query(query, self.conn, params=(days,))
    
    def get_low_stock_medicines(self):
        """Get low stock medicines"""
        query = '''
            SELECT brand_name, generic_name, quantity, min_quantity, 
                   (min_quantity - quantity) as shortage
            FROM medicines 
            WHERE quantity <= min_quantity
            ORDER BY shortage DESC
        '''
        return pd.read_sql_query(query, self.conn)
    
    def search_medicine(self, search_term):
        """Search medicine by name"""
        query = '''
            SELECT * FROM medicines 
            WHERE brand_name LIKE ? OR generic_name LIKE ? OR company LIKE ?
            ORDER BY brand_name
        '''
        return pd.read_sql_query(query, self.conn, 
                               params=(f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

# ============================================================================
# 3. INTELLIGENT CHATBOT
# ============================================================================
class PharmacyChatbot:
    def __init__(self, db):
        self.db = db
        self.context = {}
    
    def process_query(self, user_input):
        """Process user query with Indian pharmacy context"""
        user_input = user_input.lower().strip()
        
        # Update context
        self.update_context(user_input)
        
        # Check for greetings
        if self.is_greeting(user_input):
            return self.get_greeting_response()
        
        # Check for specific medicine queries
        medicine_info = self.extract_medicine_info(user_input)
        if medicine_info:
            return self.get_medicine_response(medicine_info)
        
        # Check for stock queries
        if any(word in user_input for word in ['stock', 'available', 'quantity', 'kitna hai']):
            return self.get_stock_response(user_input)
        
        # Check for expiry queries
        if any(word in user_input for word in ['expire', 'expiry', 'khatam', 'date']):
            return self.get_expiry_response(user_input)
        
        # Check for sales queries
        if any(word in user_input for word in ['sale', 'bikri', 'today sale', 'revenue']):
            return self.get_sales_response()
        
        # Check for prescription queries
        if any(word in user_input for word in ['prescription', 'doctor', 'patient', 'rx']):
            return self.get_prescription_response()
        
        # Check for supplier queries
        if any(word in user_input for word in ['supplier', 'company', 'order', 'supply']):
            return self.get_supplier_response()
        
        # Check for help
        if 'help' in user_input or 'madad' in user_input:
            return self.get_help_response()
        
        # Default response
        return self.get_default_response()
    
    def update_context(self, user_input):
        """Update conversation context"""
        # Extract potential medicine names
        medicines = self.db.cursor.execute("SELECT brand_name FROM medicines").fetchall()
        medicine_names = [m[0].lower() for m in medicines]
        
        for med in medicine_names:
            if med in user_input:
                self.context['last_medicine'] = med
                break
    
    def is_greeting(self, text):
        greetings = ['hello', 'hi', 'hey', 'namaste', 'good morning', 'good afternoon']
        return any(greet in text for greet in greetings)
    
    def get_greeting_response(self):
        responses = [
            "Namaste! I'm your Pragnya Pharm assistant. How can I help you today? 💊",
            "Hello! Welcome to Pragnya Pharm. What pharmacy assistance do you need?",
            "Hi there! Ready to help with your pharmacy queries. What do you need?"
        ]
        return np.random.choice(responses)
    
    def extract_medicine_info(self, text):
        """Extract medicine information from query"""
        medicines = self.db.cursor.execute("SELECT id, brand_name, generic_name FROM medicines").fetchall()
        
        for med_id, brand, generic in medicines:
            if brand.lower() in text or generic.lower() in text:
                return {
                    'id': med_id,
                    'brand': brand,
                    'generic': generic
                }
        return None
    
    def get_medicine_response(self, medicine_info):
        """Get detailed medicine information"""
        query = '''
            SELECT brand_name, generic_name, quantity, expiry_date, mrp, category,
                   julianday(expiry_date) - julianday('now') as days_left
            FROM medicines WHERE id = ?
        '''
        result = self.db.cursor.execute(query, (medicine_info['id'],)).fetchone()
        
        if result:
            brand, generic, qty, expiry, mrp, category, days_left = result
            
            response = f"**{brand}** ({generic})\n\n"
            response += f"📦 **Stock Available:** {qty} units\n"
            response += f"💰 **MRP:** ₹{mrp:.2f}\n"
            response += f"🏷️ **Category:** {category}\n"
            
            if days_left > 0:
                if days_left <= 7:
                    response += f"⚠️ **Expiry Alert:** {int(days_left)} days left ({expiry})\n"
                elif days_left <= 30:
                    response += f"📅 **Expiring:** {int(days_left)} days ({expiry})\n"
                else:
                    response += f"✅ **Expiry Date:** {expiry}\n"
            else:
                response += f"❌ **EXPIRED:** {expiry}\n"
            
            # Add reorder suggestion if low stock
            min_qty = self.db.cursor.execute("SELECT min_quantity FROM medicines WHERE id = ?", 
                                           (medicine_info['id'],)).fetchone()[0]
            if qty <= min_qty:
                shortage = min_qty - qty
                response += f"\n🚨 **Low Stock Alert!** Need {shortage} more units. Want me to create a reorder?"
            
            return response
        return f"Could not find details for {medicine_info['brand']}"
    
    def get_stock_response(self, query):
        """Get stock information"""
        if 'low' in query or 'kam' in query:
            low_stock = self.db.get_low_stock_medicines()
            if len(low_stock) > 0:
                response = "🚨 **Low Stock Medicines:**\n"
                for _, row in low_stock.head(5).iterrows():
                    response += f"• {row['brand_name']}: {row['quantity']} units (Min: {row['min_quantity']})\n"
                if len(low_stock) > 5:
                    response += f"\n... and {len(low_stock) - 5} more items"
                return response
            return "✅ All stock levels are adequate!"
        
        else:
            stats = self.db.get_dashboard_stats()
            return f"**Stock Summary:**\n• Total Medicines: {stats['total_medicines']}\n• Low Stock Items: {stats['low_stock']}\n• Inventory Value: ₹{stats['inventory_value']:,.2f}"
    
    def get_expiry_response(self, query):
        """Get expiry information"""
        if 'soon' in query or '30' in query:
            expiring = self.db.get_expiring_medicines(30)
            if len(expiring) > 0:
                response = "📅 **Medicines Expiring Soon (≤30 days):**\n"
                critical = []
                warning = []
                
                for _, row in expiring.iterrows():
                    days = int(row['days_left'])
                    if days <= 7:
                        critical.append(f"• {row['brand_name']}: {days} days ({row['expiry_date']})")
                    else:
                        warning.append(f"• {row['brand_name']}: {days} days ({row['expiry_date']})")
                
                if critical:
                    response += "\n🚨 **Critical (≤7 days):**\n" + "\n".join(critical[:3])
                if warning:
                    response += "\n⚠️ **Warning (8-30 days):**\n" + "\n".join(warning[:3])
                
                if len(expiring) > 6:
                    response += f"\n\n... and {len(expiring) - 6} more medicines"
                return response
            return "✅ No medicines expiring in the next 30 days!"
        else:
            expiring = self.db.get_expiring_medicines(90)
            return f"There are {len(expiring)} medicines expiring in the next 90 days."
    
    def get_sales_response(self):
        """Get sales information"""
        # Today's sales
        self.db.cursor.execute("SELECT SUM(quantity) as total_qty, SUM(total_amount) as total_amt FROM sales WHERE sale_date = DATE('now')")
        result = self.db.cursor.fetchone()
        
        if result and result[0]:
            return f"**Today's Sales:**\n• Units Sold: {result[0]}\n• Revenue: ₹{result[1]:,.2f}"
        return "No sales recorded today yet."
    
    def get_prescription_response(self):
        """Get prescription information"""
        self.db.cursor.execute("SELECT COUNT(*) FROM prescriptions WHERE status = 'Pending'")
        pending = self.db.cursor.fetchone()[0]
        
        return f"**Prescriptions:**\n• Pending: {pending} prescription(s)\n• Use 'Prescriptions' page to view details."
    
    def get_supplier_response(self):
        """Get supplier information"""
        self.db.cursor.execute("SELECT COUNT(*) FROM suppliers")
        count = self.db.cursor.fetchone()[0]
        
        return f"We work with {count} trusted suppliers. Check 'Suppliers' page for details."
    
    def get_help_response(self):
        """Get help information"""
        return """
        **I can help you with:**
        
        💊 **Medicine Info:** Ask about any medicine (stock, price, expiry)
        📦 **Stock Queries:** "Show low stock", "Check stock levels"
        📅 **Expiry Tracking:** "What's expiring soon?", "Expiry alerts"
        💰 **Sales Info:** "Today's sales", "Revenue"
        📝 **Prescriptions:** Prescription status and details
        🚚 **Suppliers:** Supplier information
        🚨 **Alerts:** Critical alerts and warnings
        
        **Try asking:**
        • "Stock of Crocin"
        • "What's expiring this week?"
        • "Show low stock medicines"
        • "Today's sales report"
        """
    
    def get_default_response(self):
        """Get default response"""
        responses = [
            "I can help with medicine stock, expiry dates, sales reports, and more. What specific information do you need?",
            "I'm here to assist with pharmacy operations. Try asking about medicine stock, expiry, or sales.",
            "Need pharmacy assistance? I can check stock levels, expiry dates, or help with prescriptions."
        ]
        return np.random.choice(responses)

# ============================================================================
# 4. DEMAND FORECASTING ENGINE
# ============================================================================
class DemandForecaster:
    def __init__(self, db):
        self.db = db
    
    def forecast_demand(self, medicine_id, months=3):
        """Forecast demand based on historical sales"""
        try:
            # Get historical sales data
            query = '''
                SELECT date(sale_date) as date, SUM(quantity) as daily_sales
                FROM sales 
                WHERE medicine_id = ? 
                AND sale_date >= date('now', '-90 days')
                GROUP BY date(sale_date)
                ORDER BY date(sale_date)
            '''
            sales_data = pd.read_sql_query(query, self.db.conn, params=(medicine_id,))
            
            if len(sales_data) < 7:
                return self.simple_forecast(medicine_id, months)
            
            # Simple moving average forecast
            sales_data['date'] = pd.to_datetime(sales_data['date'])
            sales_data.set_index('date', inplace=True)
            
            # Calculate moving averages
            weekly_avg = sales_data['daily_sales'].rolling(window=7).mean().iloc[-1]
            monthly_avg = sales_data['daily_sales'].rolling(window=30).mean().iloc[-1]
            
            # Get medicine info
            self.db.cursor.execute("SELECT brand_name, quantity, min_quantity FROM medicines WHERE id = ?", 
                                 (medicine_id,))
            brand, current_qty, min_qty = self.db.cursor.fetchone()
            
            # Calculate forecast
            base_forecast = (weekly_avg + monthly_avg) / 2
            if pd.isna(base_forecast):
                base_forecast = current_qty * 0.3  # Fallback
            
            # Apply seasonal factors
            seasonal_factor = self.get_seasonal_factor()
            adjusted_forecast = base_forecast * seasonal_factor
            
            forecasts = []
            for i in range(1, months + 1):
                month_forecast = adjusted_forecast * 30 * (1 + (i * 0.05))  # 5% monthly growth
                forecasts.append({
                    'month': i,
                    'month_name': (datetime.now() + timedelta(days=30*i)).strftime('%b'),
                    'predicted_demand': int(month_forecast),
                    'confidence': max(0.7, 1 - (i * 0.1)),
                    'reorder_point': int(month_forecast * 0.3)  # 30% of monthly demand
                })
            
            return {
                'medicine': brand,
                'current_stock': current_qty,
                'min_stock': min_qty,
                'weekly_avg': round(weekly_avg, 1) if not pd.isna(weekly_avg) else 0,
                'monthly_avg': round(monthly_avg, 1) if not pd.isna(monthly_avg) else 0,
                'forecasts': forecasts
            }
            
        except Exception as e:
            return self.simple_forecast(medicine_id, months)
    
    def simple_forecast(self, medicine_id, months):
        """Simple forecast when historical data is insufficient"""
        self.db.cursor.execute("SELECT brand_name, quantity, min_quantity FROM medicines WHERE id = ?", 
                             (medicine_id,))
        brand, current_qty, min_qty = self.db.cursor.fetchone()
        
        forecasts = []
        for i in range(1, months + 1):
            # Simple forecast based on current stock and category
            self.db.cursor.execute("SELECT category FROM medicines WHERE id = ?", (medicine_id,))
            category = self.db.cursor.fetchone()[0]
            
            # Category-based base demand
            base_demand = {
                'Analgesic': 30,
                'Antibiotic': 25,
                'Cardiac': 20,
                'Diabetic': 35,
                'GI': 28,
                'Other': 15
            }.get(category, 20)
            
            # Apply growth factor and seasonality
            month_factor = 1 + (i * 0.05)  # 5% monthly growth
            seasonal_factor = self.get_seasonal_factor()
            predicted = int(base_demand * month_factor * seasonal_factor * 30)  # Monthly demand
            
            forecasts.append({
                'month': i,
                'month_name': (datetime.now() + timedelta(days=30*i)).strftime('%b'),
                'predicted_demand': predicted,
                'confidence': max(0.6, 1 - (i * 0.15)),
                'reorder_point': int(predicted * 0.3)
            })
        
        return {
            'medicine': brand,
            'current_stock': current_qty,
            'min_stock': min_qty,
            'weekly_avg': 'N/A',
            'monthly_avg': 'N/A',
            'forecasts': forecasts
        }
    
    def get_seasonal_factor(self):
        """Get seasonal adjustment factor"""
        month = datetime.now().month
        
        # Indian seasonal factors - based on common disease patterns
        seasonal_factors = {
            1: 1.1,   # Jan - Winter illnesses
            2: 1.0,
            3: 1.0,
            4: 1.2,   # Apr - Summer/Allergies
            5: 1.3,   # May - Summer peak
            6: 1.4,   # Jun - Monsoon onset
            7: 1.5,   # Jul - Monsoon peak (high demand)
            8: 1.4,   # Aug - Monsoon continues
            9: 1.3,   # Sep - Post-monsoon
            10: 1.1,  # Oct - Festive season
            11: 1.0,  # Nov
            12: 1.2   # Dec - Winter/Year-end
        }
        
        return seasonal_factors.get(month, 1.0)
    
    def get_reorder_recommendations(self):
        """Generate smart reorder recommendations"""
        query = '''
            SELECT m.id, m.brand_name, m.quantity, m.min_quantity, m.max_quantity,
                   COALESCE(SUM(s.quantity), 0) as monthly_sales
            FROM medicines m
            LEFT JOIN sales s ON m.id = s.medicine_id 
                AND s.sale_date >= date('now', '-30 days')
            WHERE m.quantity <= m.min_quantity * 1.5  # Include buffer
            GROUP BY m.id
            ORDER BY (m.min_quantity - m.quantity) DESC
        '''
        
        low_stock_df = pd.read_sql_query(query, self.db.conn)
        
        recommendations = []
        for _, row in low_stock_df.iterrows():
            forecast = self.forecast_demand(row['id'], 1)
            
            if forecast['forecasts']:
                monthly_prediction = forecast['forecasts'][0]['predicted_demand']
                
                # Calculate optimal reorder quantity
                safety_stock = int(monthly_prediction * 0.3)  # 30% safety stock
                lead_time_demand = int(monthly_prediction * 0.1)  # 10% for lead time
                optimal_reorder = max(
                    row['max_quantity'] - row['quantity'],
                    safety_stock + lead_time_demand
                )
                
                urgency = "HIGH" if row['quantity'] <= row['min_quantity'] * 0.5 else "MEDIUM"
                
                recommendations.append({
                    'medicine': row['brand_name'],
                    'current_stock': row['quantity'],
                    'min_required': row['min_quantity'],
                    'monthly_sales': int(row['monthly_sales']),
                    'predicted_demand': monthly_prediction,
                    'reorder_qty': optimal_reorder,
                    'urgency': urgency,
                    'est_cost': optimal_reorder * 50  # Average cost placeholder
                })
        
        return pd.DataFrame(recommendations) if recommendations else pd.DataFrame()

# ============================================================================
# 5. STREAMLIT UI COMPONENTS
# ============================================================================
def create_header():
    """Create pharmacy header with logo"""
    st.markdown("""
    <div class="main-header">
        <div class="logo-container">
            <span class="pharmacy-logo">💊</span>
            <h1 style="margin:0; font-size: 2.8rem;">PRAGNYA PHARM</h1>
        </div>
        <h3 style="margin:0; font-weight: 400;">Smart Pharmacy Management System</h3>
        <p style="margin:10px 0 0 0; opacity: 0.9;">📍 Indian Pharmacy Compliance | Real-time Tracking | Intelligent Alerts</p>
    </div>
    """, unsafe_allow_html=True)

def create_sidebar(db):
    """Create sidebar navigation"""
    with st.sidebar:
        st.markdown('<div class="sidebar-header"><h3>💊 Navigation</h3></div>', unsafe_allow_html=True)
        
        page = st.radio(
            "Select Module",
            ["🏠 Dashboard", "📦 Stock Manager", "💰 Sales & Billing", 
             "📤 Excel Upload", "🚨 Alerts & Expiry", "📈 Analytics",
             "🤖 AI Assistant", "📝 Prescriptions", "🚚 Suppliers"]
        )
        
        st.markdown("---")
        
        # Quick Stats
        stats = db.get_dashboard_stats()
        
        st.markdown("### 📊 Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Medicines", stats['total_medicines'])
            st.metric("Low Stock", stats['low_stock'])
        with col2:
            st.metric("Expiring Soon", stats['expiring_soon'])
            st.metric("Today Sales", f"₹{stats['today_sales']:,.0f}")
        
        # Critical Alerts
        if stats['critical_alerts'] > 0:
            st.markdown(f'<div class="alert-critical">🚨 {stats["critical_alerts"]} Critical Alerts</div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 📅 System Status")
        st.info(f"Last Updated: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
        
        # Quick Actions
        st.markdown("### ⚡ Quick Actions")
        if st.button("🔄 Refresh All Data"):
            st.rerun()
        
        if st.button("📋 Generate Daily Report"):
            generate_daily_report(db)
        
        if st.button("🆘 Emergency Alert"):
            emergency_alert_mode(db)
        
        return page

def create_dashboard(db):
    """Create main dashboard"""
    stats = db.get_dashboard_stats()
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>Total Medicines</h3><h2>{}</h2></div>'.format(stats['total_medicines']), 
                   unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>Low Stock</h3><h2 style="color:#E74C3C;">{}</h2></div>'.format(stats['low_stock']), 
                   unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>Expiring Soon</h3><h2 style="color:#F39C12;">{}</h2></div>'.format(stats['expiring_soon']), 
                   unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Today Sales</h3><h2 style="color:#28B463;">₹{:,}</h2></div>'.format(int(stats['today_sales'])), 
                   unsafe_allow_html=True)
    
    # Charts Section
    col1, col2 = st.columns(2)
    
    with col1:
        # Stock Status Pie Chart
        st.subheader("📊 Stock Status")
        stock_data = {
            'Status': ['Adequate', 'Low Stock', 'Out of Stock'],
            'Count': [
                stats['total_medicines'] - stats['low_stock'],
                stats['low_stock'],
                len(db.get_low_stock_medicines()[db.get_low_stock_medicines()['quantity'] == 0])
            ]
        }
        fig = px.pie(stock_data, values='Count', names='Status', 
                     color_discrete_sequence=['#28B463', '#F39C12', '#E74C3C'])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Expiry Timeline
        st.subheader("📅 Expiry Timeline (Next 90 Days)")
        expiring_df = db.get_expiring_medicines(90)
        if not expiring_df.empty:
            expiring_df['days_left'] = expiring_df['days_left'].astype(int)
            expiring_df['status'] = expiring_df['days_left'].apply(
                lambda x: 'Critical (<7)' if x <= 7 else 'Warning (8-30)' if x <= 30 else 'Normal'
            )
            
            fig = px.bar(expiring_df.head(10), x='brand_name', y='days_left', 
                        color='status', title='Top 10 Expiring Medicines',
                        color_discrete_map={'Critical (<7)': '#E74C3C', 
                                          'Warning (8-30)': '#F39C12',
                                          'Normal': '#28B463'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("✅ No medicines expiring in next 90 days")
    
    # Recent Alerts
    st.subheader("🚨 Recent Alerts")
    alerts_df = pd.read_sql_query(
        "SELECT a.message, a.severity, m.brand_name, a.created_date "
        "FROM alerts a JOIN medicines m ON a.medicine_id = m.id "
        "WHERE a.resolved = 0 ORDER BY a.created_date DESC LIMIT 5",
        db.conn
    )
    
    if not alerts_df.empty:
        for _, alert in alerts_df.iterrows():
            severity_class = {
                'HIGH': 'alert-critical',
                'MEDIUM': 'alert-warning',
                'LOW': 'alert-info'
            }.get(alert['severity'], 'alert-info')
            
            st.markdown(f'''
            <div class="{severity_class}">
                <strong>{alert['brand_name']}</strong><br>
                {alert['message']}<br>
                <small>{alert['created_date']}</small>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.success("✅ No active alerts")

def stock_manager(db):
    """Stock management page"""
    st.header("📦 Stock Management")
    
    # Search and Filter
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        search_term = st.text_input("🔍 Search Medicine", placeholder="Enter brand or generic name")
    
    with col2:
        category_filter = st.selectbox("Filter by Category", 
                                      ["All", "Analgesic", "Antibiotic", "Cardiac", 
                                       "Diabetic", "GI", "Other"])
    
    with col3:
        stock_filter = st.selectbox("Stock Status", 
                                   ["All", "Low Stock", "Adequate", "Out of Stock"])
    
    # Fetch filtered data
    if search_term:
        medicines_df = db.search_medicine(search_term)
    else:
        medicines_df = pd.read_sql_query("SELECT * FROM medicines", db.conn)
    
    # Apply filters
    if category_filter != "All":
        medicines_df = medicines_df[medicines_df['category'] == category_filter]
    
    if stock_filter == "Low Stock":
        medicines_df = medicines_df[medicines_df['quantity'] <= medicines_df['min_quantity']]
    elif stock_filter == "Out of Stock":
        medicines_df = medicines_df[medicines_df['quantity'] == 0]
    elif stock_filter == "Adequate":
        medicines_df = medicines_df[medicines_df['quantity'] > medicines_df['min_quantity']]
    
    # Display with styling
    if not medicines_df.empty:
        # Calculate days to expiry
        medicines_df['expiry_date'] = pd.to_datetime(medicines_df['expiry_date'])
        medicines_df['days_to_expiry'] = (medicines_df['expiry_date'] - pd.Timestamp.now()).dt.days
        
        # Format columns
        medicines_df['Status'] = medicines_df.apply(
            lambda row: "🟢 Adequate" if row['quantity'] > row['min_quantity'] 
            else "🟡 Low" if row['quantity'] > 0 
            else "🔴 Out", axis=1
        )
        
        medicines_df['Expiry Status'] = medicines_df['days_to_expiry'].apply(
            lambda x: "🟢 >90 days" if x > 90 
            else "🟡 <30 days" if x > 7 
            else "🔴 <7 days" if x > 0 
            else "⚫ Expired"
        )
        
        # Display table
        display_cols = ['brand_name', 'generic_name', 'company', 'quantity', 
                       'min_quantity', 'mrp', 'Status', 'expiry_date', 'Expiry Status']
        
        st.dataframe(
            medicines_df[display_cols].rename(columns={
                'brand_name': 'Brand',
                'generic_name': 'Generic',
                'company': 'Company',
                'quantity': 'Qty',
                'min_quantity': 'Min Qty',
                'mrp': 'MRP',
                'expiry_date': 'Expiry Date'
            }),
            use_container_width=True,
            height=400
        )
        
        # Quick Actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Export to Excel"):
                export_to_excel(medicines_df, "stock_report")
        
        with col2:
            if st.button("🔄 Auto Reorder Low Stock"):
                auto_reorder_low_stock(db, medicines_df)
    
    else:
        st.warning("No medicines found matching your criteria")
    
    # Add/Edit Medicine
    st.subheader("➕ Add/Edit Medicine")
    with st.form("medicine_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            brand_name = st.text_input("Brand Name*")
            generic_name = st.text_input("Generic Name")
            company = st.text_input("Company")
        
        with col2:
            batch_no = st.text_input("Batch Number")
            mfg_date = st.date_input("MFG Date", datetime.now())
            expiry_date = st.date_input("Expiry Date*", datetime.now() + timedelta(days=365))
        
        with col3:
            quantity = st.number_input("Quantity*", min_value=0, step=1)
            min_quantity = st.number_input("Min Quantity*", min_value=1, step=1, value=20)
            mrp = st.number_input("MRP*", min_value=0.0, step=0.5)
            category = st.selectbox("Category", ["Analgesic", "Antibiotic", "Cardiac", 
                                               "Diabetic", "GI", "Other"])
        
        if st.form_submit_button("💾 Save Medicine"):
            if brand_name and quantity >= 0:
                medicine_data = (
                    brand_name, generic_name, company, batch_no, 
                    mfg_date.strftime('%Y-%m-%d'), expiry_date.strftime('%Y-%m-%d'),
                    quantity, quantity * 2, min_quantity, mrp, mrp * 0.6,
                    category, 'OTC', 'Rack A1'
                )
                db.add_medicine(medicine_data)
                st.success("✅ Medicine added successfully!")
                st.rerun()

def sales_billing(db):
    """Sales and billing page"""
    st.header("💰 Sales & Billing")
    
    # Real-time Billing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🛒 New Bill")
        
        # Customer Info
        customer_name = st.text_input("Customer Name")
        customer_phone = st.text_input("Phone Number")
        doctor_name = st.text_input("Referring Doctor")
        
        # Medicine Selection
        medicines_df = pd.read_sql_query("SELECT id, brand_name, generic_name, quantity, mrp FROM medicines", db.conn)
        
        selected_medicines = []
        total_amount = 0
        
        for i in range(3):  # Allow up to 3 medicines per bill
            col_med, col_qty = st.columns([3, 1])
            
            with col_med:
                med_options = {f"{row['brand_name']} (Stock: {row['quantity']})": row['id'] 
                              for _, row in medicines_df.iterrows()}
                medicine_key = st.selectbox(f"Medicine {i+1}", list(med_options.keys()), 
                                          key=f"med_{i}")
            
            with col_qty:
                qty = st.number_input("Qty", min_value=1, max_value=100, value=1, key=f"qty_{i}")
            
            if medicine_key and qty > 0:
                med_id = med_options[medicine_key]
                med_data = medicines_df[medicines_df['id'] == med_id].iloc[0]
                
                if med_data['quantity'] >= qty:
                    subtotal = med_data['mrp'] * qty
                    selected_medicines.append({
                        'id': med_id,
                        'name': medicine_key.split(' (')[0],
                        'qty': qty,
                        'price': med_data['mrp'],
                        'subtotal': subtotal
                    })
                    total_amount += subtotal
                else:
                    st.error(f"❌ Only {med_data['quantity']} units available")
    
    with col2:
        st.subheader("💰 Bill Summary")
        
        if selected_medicines:
            for item in selected_medicines:
                st.write(f"• {item['name']}: {item['qty']} × ₹{item['price']} = ₹{item['subtotal']}")
            
            # Discount and GST
            discount = st.number_input("Discount (%)", min_value=0.0, max_value=100.0, value=0.0)
            gst_percent = st.number_input("GST (%)", min_value=0.0, value=18.0)
            
            discount_amount = total_amount * (discount / 100)
            gst_amount = (total_amount - discount_amount) * (gst_percent / 100)
            final_total = total_amount - discount_amount + gst_amount
            
            st.markdown("---")
            st.metric("Subtotal", f"₹{total_amount:,.2f}")
            st.metric("Discount", f"-₹{discount_amount:,.2f}")
            st.metric("GST", f"+₹{gst_amount:,.2f}")
            st.markdown("---")
            st.markdown(f"### Total: ₹{final_total:,.2f}")
            
            # Payment
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Card", "UPI", "Credit"])
            
            if st.button("💳 Generate Bill", type="primary"):
                bill_no = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # Update stock for each medicine
                for item in selected_medicines:
                    db.update_stock_from_sales(item['id'], item['qty'])
                    
                    # Record sale
                    db.cursor.execute('''
                        INSERT INTO sales 
                        (bill_no, medicine_id, quantity, selling_price, discount, 
                         gst_percent, total_amount, customer_name, customer_phone, 
                         doctor_name, payment_mode)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        bill_no, item['id'], item['qty'], item['price'],
                        discount, gst_percent, item['subtotal'],
                        customer_name, customer_phone, doctor_name, payment_mode
                    ))
                
                db.conn.commit()
                
                # Generate receipt
                st.success(f"✅ Bill Generated: {bill_no}")
                receipt_html = generate_receipt(bill_no, selected_medicines, 
                                              total_amount, discount_amount, 
                                              gst_amount, final_total, customer_name)
                st.components.v1.html(receipt_html, height=600, scrolling=True)
        else:
            st.info("Add medicines to create bill")
    
    # Today's Sales Report
    st.subheader("📊 Today's Sales")
    today_sales = pd.read_sql_query(
        "SELECT s.bill_no, m.brand_name, s.quantity, s.selling_price, "
        "s.total_amount, s.customer_name, s.sale_date "
        "FROM sales s JOIN medicines m ON s.medicine_id = m.id "
        "WHERE date(s.sale_date) = DATE('now') "
        "ORDER BY s.sale_date DESC",
        db.conn
    )
    
    if not today_sales.empty:
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Bills", today_sales['bill_no'].nunique())
        with col2:
            st.metric("Units Sold", int(today_sales['quantity'].sum()))
        with col3:
            st.metric("Revenue", f"₹{today_sales['total_amount'].sum():,.2f}")
        
        st.dataframe(today_sales, use_container_width=True)
    else:
        st.info("No sales today")

def excel_upload(db):
    """Excel upload and processing"""
    st.header("📤 Excel Upload")
    
    # Upload Type Selection
    upload_type = st.radio("Select Upload Type", 
                          ["Sales Data", "Inventory Update", "Supplier List"], 
                          horizontal=True)
    
    # Template Download
    st.subheader("📥 Download Template")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📋 Sales Template"):
            sales_template = pd.DataFrame({
                'Medicine': ['Crocin 650mg', 'Combiflam'],
                'Quantity': [5, 3],
                'Price': [15.0, 25.0],
                'Total': [75.0, 75.0]
            })
            download_excel(sales_template, "sales_template.xlsx")
    
    with col2:
        if st.button("📦 Inventory Template"):
            inventory_template = pd.DataFrame({
                'Brand Name': ['Crocin 650mg'],
                'Generic Name': ['Paracetamol'],
                'Company': ['GSK'],
                'Quantity': [100],
                'MRP': [15.0],
                'Expiry Date': ['2025-12-31'],
                'Category': ['Analgesic']
            })
            download_excel(inventory_template, "inventory_template.xlsx")
    
    with col3:
        if st.button("🚚 Supplier Template"):
            supplier_template = pd.DataFrame({
                'Name': ['Medley Pharmaceuticals'],
                'Phone': ['022-12345678'],
                'Email': ['orders@medley.com'],
                'GST No': ['27AAACM1234M1Z5']
            })
            download_excel(supplier_template, "supplier_template.xlsx")
    
    # File Upload
    st.subheader("📤 Upload File")
    uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'])
    
    if uploaded_file is not None:
        try:
            # Read Excel
            df = pd.read_excel(uploaded_file)
            st.success(f"✅ File loaded: {len(df)} records")
            
            # Preview
            with st.expander("🔍 Preview Data"):
                st.dataframe(df.head(), use_container_width=True)
            
            # Processing Options
            if upload_type == "Sales Data":
                st.info("This will update stock levels based on sales")
                if st.button("🚀 Process Sales Data", type="primary"):
                    success, message = db.process_excel_upload(df, 'sales')
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
            
            elif upload_type == "Inventory Update":
                st.info("This will add/update medicines in inventory")
                if st.button("🚀 Update Inventory", type="primary"):
                    success, message = db.process_excel_upload(df, 'inventory')
                    if success:
                        st.success(f"✅ {message}")
                        st.balloons()
                    else:
                        st.error(f"❌ {message}")
            
            elif upload_type == "Supplier List":
                st.info("This will update supplier database")
                if st.button("🚀 Update Suppliers", type="primary"):
                    # Process suppliers
                    for _, row in df.iterrows():
                        db.cursor.execute('''
                            INSERT OR REPLACE INTO suppliers 
                            (name, phone, email, gst_no)
                            VALUES (?, ?, ?, ?)
                        ''', (row['Name'], row['Phone'], row['Email'], row['GST No']))
                    
                    db.conn.commit()
                    st.success(f"✅ Processed {len(df)} suppliers")
                    st.balloons()
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
    
    # Recent Uploads Log
    st.subheader("📜 Upload History")
    # Add upload logging functionality here

def alerts_expiry(db):
    """Alerts and expiry management"""
    st.header("🚨 Alerts & Expiry Management")
    
    # Tabs for different alert types
    tab1, tab2, tab3 = st.tabs(["📅 Expiry Alerts", "📦 Stock Alerts", "⚠️ Critical Alerts"])
    
    with tab1:
        st.subheader("Medicines Expiring Soon")
        
        # Filter by days
        days_filter = st.slider("Show medicines expiring within (days):", 
                               min_value=1, max_value=90, value=30)
        
        expiring_df = db.get_expiring_medicines(days_filter)
        
        if not expiring_df.empty:
            # Categorize by urgency
            expiring_df['days_left'] = expiring_df['days_left'].astype(int)
            expiring_df['urgency'] = expiring_df['days_left'].apply(
                lambda x: 'Critical (<7)' if x <= 7 
                else 'High (8-30)' if x <= 30 
                else 'Medium (31-60)' if x <= 60 
                else 'Low (61-90)'
            )
            
            # Display by urgency
            urgency_levels = ['Critical (<7)', 'High (8-30)', 'Medium (31-60)', 'Low (61-90)']
            
            for urgency in urgency_levels:
                subset = expiring_df[expiring_df['urgency'] == urgency]
                if not subset.empty:
                    st.markdown(f"### {urgency}")
                    
                    for _, row in subset.head(5).iterrows():
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                        with col1:
                            st.write(f"**{row['brand_name']}**")
                        with col2:
                            st.write(f"Qty: {row['quantity']}")
                        with col3:
                            days_color = "#E74C3C" if row['days_left'] <= 7 else "#F39C12" if row['days_left'] <= 30 else "#28B463"
                            st.markdown(f"<span style='color:{days_color}; font-weight:bold;'>{row['days_left']} days</span>", 
                                      unsafe_allow_html=True)
                        with col4:
                            st.write(row['expiry_date'])
                    
                    if len(subset) > 5:
                        st.caption(f"... and {len(subset) - 5} more")
                    
                    st.markdown("---")
        else:
            st.success("✅ No medicines expiring soon")
    
    with tab2:
        st.subheader("Low Stock Alerts")
        
        low_stock_df = db.get_low_stock_medicines()
        
        if not low_stock_df.empty:
            # Calculate priority
            low_stock_df['priority'] = low_stock_df.apply(
                lambda row: 'HIGH' if row['quantity'] == 0 
                else 'MEDIUM' if row['shortage'] > row['min_quantity'] 
                else 'LOW', axis=1
            )
            
            # Group by priority
            for priority in ['HIGH', 'MEDIUM', 'LOW']:
                subset = low_stock_df[low_stock_df['priority'] == priority]
                if not subset.empty:
                    priority_color = "#E74C3C" if priority == 'HIGH' else "#F39C12" if priority == 'MEDIUM' else "#28B463"
                    st.markdown(f"### <span style='color:{priority_color}'>{priority} Priority</span>", 
                              unsafe_allow_html=True)
                    
                    for _, row in subset.iterrows():
                        with st.container():
                            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                            with col1:
                                st.write(f"**{row['brand_name']}**")
                            with col2:
                                st.write(f"Stock: {row['quantity']}")
                            with col3:
                                st.write(f"Min: {row['min_quantity']}")
                            with col4:
                                shortage = row['min_quantity'] - row['quantity']
                                st.write(f"Short: {shortage}")
                            
                            # Auto-reorder button
                            if st.button(f"📋 Auto-reorder {row['brand_name']}", 
                                       key=f"reorder_{row['brand_name']}"):
                                db.cursor.execute('''
                                    INSERT INTO reorder_queue 
                                    (medicine_id, quantity, reason, priority)
                                    VALUES (?, ?, ?, ?)
                                ''', (db.cursor.execute("SELECT id FROM medicines WHERE brand_name = ?", 
                                                       (row['brand_name'],)).fetchone()[0],
                                     shortage, 'Manual reorder', priority))
                                db.conn.commit()
                                st.success("✅ Added to reorder queue")
                    
                    st.markdown("---")
        else:
            st.success("✅ No low stock alerts")
    
    with tab3:
        st.subheader("Critical Alerts Dashboard")
        
        # Fetch all active alerts
        alerts_df = pd.read_sql_query(
            "SELECT a.*, m.brand_name FROM alerts a "
            "JOIN medicines m ON a.medicine_id = m.id "
            "WHERE a.resolved = 0 "
            "ORDER BY CASE a.severity "
            "WHEN 'HIGH' THEN 1 "
            "WHEN 'MEDIUM' THEN 2 "
            "WHEN 'LOW' THEN 3 END, a.created_date DESC",
            db.conn
        )
        
        if not alerts_df.empty:
            # Alert statistics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Alerts", len(alerts_df))
            with col2:
                high_alerts = len(alerts_df[alerts_df['severity'] == 'HIGH'])
                st.metric("High Severity", high_alerts, delta_color="inverse")
            with col3:
                st.metric("Oldest Alert", alerts_df['created_date'].max().split()[0])
            
            # Display alerts with actions
            for _, alert in alerts_df.iterrows():
                severity_class = {
                    'HIGH': 'alert-critical',
                    'MEDIUM': 'alert-warning',
                    'LOW': 'alert-info'
                }.get(alert['severity'], 'alert-info')
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f'''
                    <div class="{severity_class}">
                        <strong>{alert['brand_name']}</strong> - {alert['alert_type']}<br>
                        {alert['message']}<br>
                        <small>{alert['created_date']}</small>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col2:
                    if st.button("✅ Resolve", key=f"resolve_{alert['id']}"):
                        db.cursor.execute("UPDATE alerts SET resolved = 1 WHERE id = ?", 
                                        (alert['id'],))
                        db.conn.commit()
                        st.rerun()
        else:
            st.success("✅ No active critical alerts")
        
        # Alert Settings
        with st.expander("⚙️ Alert Settings"):
            st.subheader("Configure Alert Thresholds")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                expiry_warning_days = st.slider("Expiry Warning (days)", 
                                               min_value=1, max_value=90, value=30)
            with col2:
                critical_expiry_days = st.slider("Critical Expiry (days)", 
                                                min_value=1, max_value=30, value=7)
            with col3:
                low_stock_percentage = st.slider("Low Stock Threshold (%)", 
                                                min_value=10, max_value=50, value=30)
            
            if st.button("💾 Save Alert Settings"):
                st.success("Alert settings saved!")

def analytics_page(db):
    """Analytics and insights page"""
    st.header("📈 Analytics & Insights")
    
    # Demand Forecasting
    st.subheader("🔮 Demand Forecasting")
    
    # Select medicine for forecasting
    medicines = pd.read_sql_query("SELECT id, brand_name FROM medicines", db.conn)
    selected_med = st.selectbox("Select Medicine", 
                               medicines['brand_name'].tolist())
    
    if selected_med:
        med_id = medicines[medicines['brand_name'] == selected_med]['id'].iloc[0]
        
        # Initialize forecaster
        forecaster = DemandForecaster(db)
        forecast_result = forecaster.forecast_demand(med_id, 3)
        
        if forecast_result:
            # Display forecast summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Stock", forecast_result['current_stock'])
            with col2:
                st.metric("Min Required", forecast_result['min_stock'])
            with col3:
                avg_sales = forecast_result.get('weekly_avg', 0)
                if avg_sales != 'N/A':
                    st.metric("Weekly Avg", f"{avg_sales} units")
            
            # Forecast chart
            forecast_df = pd.DataFrame(forecast_result['forecasts'])
            if not forecast_df.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=forecast_df['month_name'],
                    y=forecast_df['predicted_demand'],
                    name='Predicted Demand',
                    marker_color='#0A5C36'
                ))
                fig.add_trace(go.Scatter(
                    x=forecast_df['month_name'],
                    y=forecast_df['reorder_point'],
                    name='Reorder Point',
                    line=dict(color='#E74C3C', dash='dash')
                ))
                fig.update_layout(
                    title=f"3-Month Demand Forecast for {selected_med}",
                    xaxis_title="Month",
                    yaxis_title="Units",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Smart Recommendations
            st.subheader("💡 Smart Recommendations")
            recommendations = forecaster.get_reorder_recommendations()
            
            if not recommendations.empty:
                relevant_rec = recommendations[recommendations['medicine'] == selected_med]
                if not relevant_rec.empty:
                    rec = relevant_rec.iloc[0]
                    
                    st.markdown(f"""
                    ### Reorder Recommendation for {selected_med}
                    
                    **📊 Current Status:**
                    - Current Stock: {rec['current_stock']} units
                    - Minimum Required: {rec['min_required']} units
                    - Monthly Sales: {rec['monthly_sales']} units
                    
                    **🎯 Forecast & Planning:**
                    - Predicted Monthly Demand: {rec['predicted_demand']} units
                    - Recommended Reorder: **{rec['reorder_qty']} units**
                    - Estimated Cost: ₹{rec['est_cost']:,.0f}
                    - Urgency: **{rec['urgency']}**
                    """)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Add to Reorder Queue", type="primary"):
                            db.cursor.execute('''
                                INSERT INTO reorder_queue 
                                (medicine_id, quantity, reason, priority)
                                VALUES (?, ?, ?, ?)
                            ''', (med_id, rec['reorder_qty'], 
                                 'AI Recommended', rec['urgency']))
                            db.conn.commit()
                            st.success("✅ Added to reorder queue")
                    
                    with col2:
                        if st.button("📧 Notify Supplier"):
                            st.info("Supplier notification feature coming soon")
                else:
                    st.success(f"✅ No immediate reorder needed for {selected_med}")
    
    # Sales Analytics
    st.subheader("💰 Sales Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", 
                                  datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())
    
    # Fetch sales data
    query = '''
        SELECT date(s.sale_date) as sale_date, 
               SUM(s.total_amount) as daily_revenue,
               SUM(s.quantity) as daily_quantity,
               COUNT(DISTINCT s.bill_no) as daily_bills
        FROM sales s
        WHERE date(s.sale_date) BETWEEN ? AND ?
        GROUP BY date(s.sale_date)
        ORDER BY sale_date
    '''
    
    sales_data = pd.read_sql_query(query, db.conn, 
                                  params=(start_date.strftime('%Y-%m-%d'), 
                                         end_date.strftime('%Y-%m-%d')))
    
    if not sales_data.empty:
        # Sales trend chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=sales_data['sale_date'],
            y=sales_data['daily_revenue'],
            name='Daily Revenue',
            line=dict(color='#0A5C36', width=3),
            fill='tozeroy',
            fillcolor='rgba(10, 92, 54, 0.1)'
        ))
        fig.update_layout(
            title="Sales Trend",
            xaxis_title="Date",
            yaxis_title="Revenue (₹)",
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top selling medicines
        st.subheader("🏆 Top Selling Medicines")
        top_meds_query = '''
            SELECT m.brand_name, SUM(s.quantity) as total_sold, 
                   SUM(s.total_amount) as total_revenue
            FROM sales s
            JOIN medicines m ON s.medicine_id = m.id
            WHERE date(s.sale_date) BETWEEN ? AND ?
            GROUP BY m.brand_name
            ORDER BY total_sold DESC
            LIMIT 10
        '''
        
        top_meds = pd.read_sql_query(top_meds_query, db.conn,
                                   params=(start_date.strftime('%Y-%m-%d'), 
                                          end_date.strftime('%Y-%m-%d')))
        
        if not top_meds.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Bar chart
                fig = px.bar(top_meds, x='brand_name', y='total_sold',
                           title='Top 10 Medicines by Quantity Sold',
                           color='total_sold',
                           color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenue chart
                fig = px.bar(top_meds, x='brand_name', y='total_revenue',
                           title='Top 10 Medicines by Revenue',
                           color='total_revenue',
                           color_continuous_scale='Plasma')
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sales data in selected period")

def ai_assistant(db):
    """AI Assistant/Chatbot page"""
    st.header("🤖 Pragnya Pharm AI Assistant")
    
    # Initialize chatbot
    chatbot = PharmacyChatbot(db)
    
    # Chat container
    chat_container = st.container()
    
    # Chat input
    user_input = st.chat_input("Ask me anything about your pharmacy...")
    
    # Display chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Process user input
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'time': datetime.now().strftime('%I:%M %p')
        })
        
        # Get chatbot response
        response = chatbot.process_query(user_input)
        
        # Add bot response to history
        st.session_state.chat_history.append({
            'role': 'bot',
            'content': response,
            'time': datetime.now().strftime('%I:%M %p')
        })
    
    # Display chat history
    with chat_container:
        for message in st.session_state.chat_history[-10:]:  # Show last 10 messages
            if message['role'] == 'user':
                st.markdown(f'''
                <div class="chat-user">
                    <strong>You</strong> <small style="float:right">{message['time']}</small><br>
                    {message['content']}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="chat-bot">
                    <strong>💊 Pharm AI</strong> <small style="float:right">{message['time']}</small><br>
                    {message['content']}
                </div>
                ''', unsafe_allow_html=True)
    
    # Quick query buttons
    st.subheader("⚡ Quick Queries")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📦 Check Low Stock"):
            response = chatbot.get_stock_response("low stock")
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'time': datetime.now().strftime('%I:%M %p')
            })
            st.rerun()
    
    with col2:
        if st.button("📅 Expiring Soon"):
            response = chatbot.get_expiry_response("expiring soon")
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'time': datetime.now().strftime('%I:%M %p')
            })
            st.rerun()
    
    with col3:
        if st.button("💰 Today's Sales"):
            response = chatbot.get_sales_response()
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'time': datetime.now().strftime('%I:%M %p')
            })
            st.rerun()
    
    with col4:
        if st.button("🆘 Help"):
            response = chatbot.get_help_response()
            st.session_state.chat_history.append({
                'role': 'bot',
                'content': response,
                'time': datetime.now().strftime('%I:%M %p')
            })
            st.rerun()
    
    # Recent activity
    st.subheader("📊 Recent Pharmacy Activity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Recent low stock
        low_stock = db.get_low_stock_medicines().head(3)
        if not low_stock.empty:
            st.markdown("**🚨 Recent Low Stock:**")
            for _, row in low_stock.iterrows():
                st.write(f"• {row['brand_name']} ({row['quantity']} units)")
    
    with col2:
        # Recent expiring
        expiring = db.get_expiring_medicines(7).head(3)
        if not expiring.empty:
            st.markdown("**📅 Expiring This Week:**")
            for _, row in expiring.iterrows():
                st.write(f"• {row['brand_name']} ({int(row['days_left'])} days)")

def prescription_module(db):
    """Prescription management module"""
    st.header("📝 Prescription Management")
    st.info("Prescription module coming soon!")

def supplier_module(db):
    """Supplier management module"""
    st.header("🚚 Supplier Management")
    st.info("Supplier module coming soon!")

# ============================================================================
# 6. UTILITY FUNCTIONS
# ============================================================================
def export_to_excel(df, filename):
    """Export DataFrame to Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
    processed_data = output.getvalue()
    
    st.download_button(
        label="📥 Download Excel",
        data=processed_data,
        file_name=f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def download_excel(df, filename):
    """Create download link for Excel"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Template')
    processed_data = output.getvalue()
    
    st.download_button(
        label=f"📥 {filename}",
        data=processed_data,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

def generate_daily_report(db):
    """Generate daily report"""
    stats = db.get_dashboard_stats()
    
    report = f"""
    # Pragnya Pharm - Daily Report
    ## {datetime.now().strftime('%d %B %Y')}
    
    ### 📊 Summary
    - Total Medicines: {stats['total_medicines']}
    - Low Stock Items: {stats['low_stock']}
    - Expiring Soon: {stats['expiring_soon']}
    - Today's Sales: ₹{stats['today_sales']:,.2f}
    
    ### 🚨 Critical Alerts
    """
    
    # Add critical alerts
    critical_alerts = pd.read_sql_query(
        "SELECT a.message, m.brand_name FROM alerts a "
        "JOIN medicines m ON a.medicine_id = m.id "
        "WHERE a.resolved = 0 AND a.severity = 'HIGH'",
        db.conn
    )
    
    if not critical_alerts.empty:
        for _, alert in critical_alerts.iterrows():
            report += f"- {alert['brand_name']}: {alert['message']}\n"
    else:
        report += "- ✅ No critical alerts\n"
    
    # Add low stock items
    report += "\n### 📦 Low Stock Items\n"
    low_stock = db.get_low_stock_medicines()
    if not low_stock.empty:
        for _, item in low_stock.head(5).iterrows():
            report += f"- {item['brand_name']}: {item['quantity']} units (Min: {item['min_quantity']})\n"
    else:
        report += "- ✅ All stock levels adequate\n"
    
    st.download_button(
        label="📥 Download Daily Report",
        data=report,
        file_name=f"daily_report_{datetime.now().strftime('%Y%m%d')}.md",
        mime="text/markdown"
    )

def emergency_alert_mode(db):
    """Emergency alert system"""
    st.warning("🚨 EMERGENCY ALERT MODE ACTIVATED")
    
    # Get all critical issues
    expired = db.get_expiring_medicines(0)  # Expired today
    out_of_stock = db.get_low_stock_medicines()
    out_of_stock = out_of_stock[out_of_stock['quantity'] == 0]
    
    alert_message = "🚨 **EMERGENCY ALERT** 🚨\n\n"
    
    if not expired.empty:
        alert_message += "**❌ EXPIRED MEDICINES:**\n"
        for _, med in expired.iterrows():
            alert_message += f"- {med['brand_name']} (Expired: {med['expiry_date']})\n"
    
    if not out_of_stock.empty:
        alert_message += "\n**📦 OUT OF STOCK:**\n"
        for _, med in out_of_stock.iterrows():
            alert_message += f"- {med['brand_name']}\n"
    
    st.error(alert_message)
    
    # Send email notification (placeholder)
    if st.button("📧 Send Emergency Email"):
        st.info("Emergency email functionality would be implemented here")

def generate_receipt(bill_no, items, subtotal, discount, gst, total, customer_name):
    """Generate HTML receipt"""
    receipt_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; margin-bottom: 20px; }}
            .logo {{ font-size: 24px; font-weight: bold; color: #0A5C36; }}
            .bill-info {{ margin: 10px 0; }}
            .item-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
            .item-table th, .item-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .item-table th {{ background-color: #0A5C36; color: white; }}
            .total {{ font-size: 18px; font-weight: bold; margin-top: 20px; }}
            .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">PRAGNYA PHARM</div>
            <div>Smart Pharmacy Management</div>
        </div>
        
        <div class="bill-info">
            <strong>Bill No:</strong> {bill_no}<br>
            <strong>Date:</strong> {datetime.now().strftime('%d/%m/%Y %I:%M %p')}<br>
            <strong>Customer:</strong> {customer_name if customer_name else 'Walk-in Customer'}<br>
        </div>
        
        <table class="item-table">
            <tr>
                <th>Medicine</th>
                <th>Qty</th>
                <th>Price</th>
                <th>Total</th>
            </tr>
    """
    
    for item in items:
        receipt_html += f"""
            <tr>
                <td>{item['name']}</td>
                <td>{item['qty']}</td>
                <td>₹{item['price']:.2f}</td>
                <td>₹{item['subtotal']:.2f}</td>
            </tr>
        """
    
    receipt_html += f"""
        </table>
        
        <div class="bill-info">
            Subtotal: ₹{subtotal:.2f}<br>
            Discount: -₹{discount:.2f}<br>
            GST: +₹{gst:.2f}<br>
        </div>
        
        <div class="total">
            Grand Total: ₹{total:.2f}
        </div>
        
        <div class="footer">
            Thank you for visiting Pragnya Pharm!<br>
            Contact: +91 98765 43210 | Email: info@pragnyapharm.com<br>
            GST No: 27AAACP1234M1Z5
        </div>
    </body>
    </html>
    """
    
    return receipt_html

def auto_reorder_low_stock(db, low_stock_df):
    """Automatically reorder low stock items"""
    for _, row in low_stock_df.iterrows():
        if row['quantity'] <= row['min_quantity']:
            shortage = row['min_quantity'] - row['quantity'] + 20  # Add buffer
            
            # Add to reorder queue
            db.cursor.execute('''
                INSERT INTO reorder_queue (medicine_id, quantity, reason, priority)
                VALUES (?, ?, ?, ?)
            ''', (row['id'], shortage, 'Auto-reorder: Low stock', 'MEDIUM'))
    
    db.conn.commit()
    st.success(f"✅ {len(low_stock_df)} items added to reorder queue")

# ============================================================================
# 7. MAIN APPLICATION
# ============================================================================
def main():
    """Main application function"""
    # Initialize database
    db = IndianPharmacyDB()
    
    # Create header
    create_header()
    
    # Create sidebar and get selected page
    selected_page = create_sidebar(db)
    
    # Display selected page
    if selected_page == "🏠 Dashboard":
        create_dashboard(db)
    elif selected_page == "📦 Stock Manager":
        stock_manager(db)
    elif selected_page == "💰 Sales & Billing":
        sales_billing(db)
    elif selected_page == "📤 Excel Upload":
        excel_upload(db)
    elif selected_page == "🚨 Alerts & Expiry":
        alerts_expiry(db)
    elif selected_page == "📈 Analytics":
        analytics_page(db)
    elif selected_page == "🤖 AI Assistant":
        ai_assistant(db)
    elif selected_page == "📝 Prescriptions":
        prescription_module(db)
    elif selected_page == "🚚 Suppliers":
        supplier_module(db)

# ============================================================================
# 8. RUN APPLICATION
# ============================================================================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Application Error: {str(e)}")
        st.info("Please refresh the page or contact support.")