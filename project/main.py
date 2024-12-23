import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class Product:
    kode: str
    nama: str
    harga: int 
    stok: int

@dataclass
class Transaction:
    timestamp: str
    username: str
    kode_produk: str
    nama_produk: str
    jumlah: int
    total: int

class InventorySystem:
    def __init__(self, product_file: str = './project/products.json', 
                 transaction_file: str = './project/transactions.json'):
        self.product_file = product_file
        self.transaction_file = transaction_file
        self.products: Dict[str, Product] = {}
        self.transactions: List[Transaction] = []
        self.load_data()

    def load_data(self) -> None:
        """Load product and transaction data from files."""
        try:
            with open(self.product_file, 'r') as file:
                products_data = json.load(file)
                self.products = {
                    k: Product(**v) for k, v in products_data.items()
                }
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading products: {e}")

        try:
            with open(self.transaction_file, 'r') as file:
                transactions_data = json.load(file)
                self.transactions = [Transaction(**t) for t in transactions_data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading transactions: {e}")

    def save_data(self) -> None:
        """Save product and transaction data to files."""
        try:
            with open(self.product_file, 'w') as file:
                products_dict = {k: vars(v) for k, v in self.products.items()}
                json.dump(products_dict, file, indent=4)

            with open(self.transaction_file, 'w') as file:
                transactions_list = [vars(t) for t in self.transactions]
                json.dump(transactions_list, file, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    @staticmethod
    def format_currency(amount: int) -> str:
        """Format amount as Indonesian Rupiah."""
        return f"Rp {amount:,}"

    def display_table(self, products: List[Product]) -> None:
        """Display products in a formatted table."""
        headers = ["No", "Kode", "Nama", "Harga", "Stok", "Total"]
        col_widths = [2, 8, 20, 9, 3, 9]
        
        # Print header
        separator = "=" * (sum(col_widths) + len(col_widths) * 3 + 1)
        print(separator)
        header_format = "| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)) + " |"
        print(header_format)
        print(separator)

        # Print rows
        for idx, product in enumerate(products, 1):
            total = product.harga * product.stok
            row = [
                str(idx),
                product.kode,
                product.nama,
                self.format_currency(product.harga),
                str(product.stok),
                self.format_currency(total)
            ]
            row_format = "| " + " | ".join(f"{val:{'^' if i == 0 else '>' if i in [3, 4, 5] else '<'}{w}}" 
                                         for i, (val, w) in enumerate(zip(row, col_widths))) + " |"
            print(row_format)
        
        print(separator)

    def show_products(self, filter_by: Optional[str] = None) -> None:
        """Display products with optional sorting."""
        if not self.products:
            print("\nNo products available.")
            return

        products = list(self.products.values())
        
        # Apply sorting if specified
        sort_key = None
        reverse = False
        
        if filter_by == "nama-asc":
            sort_key = lambda x: x.nama
        elif filter_by == "nama-desc":
            sort_key = lambda x: x.nama
            reverse = True
        elif filter_by == "harga-asc":
            sort_key = lambda x: x.harga
        elif filter_by == "harga-desc":
            sort_key = lambda x: x.harga
            reverse = True

        if sort_key:
            products.sort(key=sort_key, reverse=reverse)
            
        self.display_table(products)

    def add_product(self) -> None:
        """Add a new product to inventory."""
        print("\n=== TAMBAH PRODUK ===")
        
        kode = input("Kode Produk  : ").strip()
        if kode in self.products:
            print("\nKode produk sudah ada!")
            return
            
        nama = input("Nama Produk  : ").strip()
        
        try:
            harga = int(input("Harga Produk : "))
            stok = int(input("Stok Produk  : "))
            if harga < 0 or stok < 0:
                print("\nHarga dan stok tidak boleh negatif!")
                return
        except ValueError:
            print("\nHarga dan stok harus berupa angka!")
            return

        self.products[kode] = Product(kode=kode, nama=nama, harga=harga, stok=stok)
        self.save_data()
        print("\nProduk berhasil ditambahkan!")

    def update_product(self) -> None:
        """Update an existing product."""
        print("\n=== UPDATE PRODUK ===")
        
        kode = input("Masukkan kode produk: ").strip()
        product = self.products.get(kode)
        if not product:
            print("\nProduk tidak ditemukan!")
            return
            
        print(f"\nData produk saat ini:")
        print(f"Nama : {product.nama}")
        print(f"Harga: {self.format_currency(product.harga)}")
        print(f"Stok : {product.stok}")
        
        # Get updates
        nama = input("\nNama baru (kosongkan jika tidak diubah): ").strip()
        if nama:
            product.nama = nama
            
        try:
            harga = input("Harga baru (kosongkan jika tidak diubah): ").strip()
            if harga:
                harga = int(harga)
                if harga < 0:
                    raise ValueError("Harga tidak boleh negatif!")
                product.harga = harga
                
            stok = input("Stok baru (kosongkan jika tidak diubah): ").strip()
            if stok:
                stok = int(stok)
                if stok < 0:
                    raise ValueError("Stok tidak boleh negatif!")
                product.stok = stok
        except ValueError as e:
            print(f"\n{str(e)}")
            return
            
        self.save_data()
        print("\nProduk berhasil diupdate!")

    def process_purchase(self, username: str) -> None:
        """Process a product purchase."""
        print("\n=== BELI PRODUK ===")
        
        kode = input("Masukkan kode produk: ").strip()
        product = self.products.get(kode)
        if not product:
            print("\nProduk tidak ditemukan!")
            return
            
        print(f"\nDetail Produk:")
        print(f"Nama: {product.nama}")
        print(f"Harga: {self.format_currency(product.harga)}")
        print(f"Stok: {product.stok}")
        
        try:
            jumlah = int(input("\nJumlah yang akan dibeli: "))
            if jumlah <= 0:
                print("\nJumlah pembelian harus lebih dari 0!")
                return
            if jumlah > product.stok:
                print("\nStok tidak mencukupi!")
                return
        except ValueError:
            print("\nJumlah harus berupa angka!")
            return
            
        total = jumlah * product.harga
        print(f"\nTotal: {self.format_currency(total)}")
        if input("Konfirmasi pembelian (y/n)? ").lower() != 'y':
            print("\nPembelian dibatalkan.")
            return
            
        # Process transaction
        product.stok -= jumlah
        transaction = Transaction(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Changed from waktu to timestamp
            username=username,
            kode_produk=kode,
            nama_produk=product.nama,
            jumlah=jumlah,
            total=total
        )
        self.transactions.append(transaction)
        self.save_data()
        print("\nPembelian berhasil!")

    def show_transactions(self, username: str, is_admin: bool = False) -> None:
        """Display transaction history."""
        print("\n=== RIWAYAT TRANSAKSI ===")
        
        transactions = self.transactions if is_admin else [
            t for t in self.transactions if t.username == username
        ]
        
        if not transactions:
            print("\nBelum ada transaksi.")
            return
            
        headers = ["Waktu", "Username", "Produk", "Jumlah", "Total"]
        col_widths = [19, 10, 20, 6, 15]
        
        separator = "=" * (sum(col_widths) + len(col_widths) * 3 + 1)
        print(separator)
        header_format = "| " + " | ".join(f"{h:<{w}}" for h, w in zip(headers, col_widths)) + " |"
        print(header_format)
        print(separator)
        
        for t in transactions:
            row = [
                t.timestamp,  # Changed from waktu to timestamp
                t.username,
                t.nama_produk,
                str(t.jumlah),
                self.format_currency(t.total)
            ]
            row_format = "| " + " | ".join(f"{val:{'^' if i == 3 else '>' if i == 4 else '<'}{w}}" 
                                         for i, (val, w) in enumerate(zip(row, col_widths))) + " |"
            print(row_format)
        
        print(separator)

def login() -> Tuple[Optional[str], Optional[str]]:
    """Handle user login."""
    print("\n=== LOGIN SISTEM ===")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username == "admin" and password == "admin123":
        return "admin", username
    elif username == "user" and password == "user123":
        return "user", username
    else:
        print("\nLogin gagal!")
        return None, None

def show_menu(role: str) -> None:
    """Display menu based on user role."""
    print("\nMenu:")
    if role == "admin":
        options = [
            "1. Tambah Produk",
            "2. Update Produk",
            "3. Hapus Produk",
            "4. Urutkan Nama [A-Z]",
            "5. Urutkan Nama [Z-A]",
            "6. Urutkan Harga [0-9]",
            "7. Urutkan Harga [9-0]",
            "8. Riwayat Transaksi",
            "0. Keluar"
        ]
    else:
        options = [
            "1. Beli Produk",
            "2. Riwayat Transaksi",
            "0. Keluar"
        ]
    print("\n".join(options))
    print("\nPilihan: ", end="")

def main() -> None:
    """Main application loop."""
    role, username = login()
    if not role:
        return
        
    system = InventorySystem()
    
    while True:
        system.show_products()
        show_menu(role)
        
        try:
            choice = int(input().strip())
        except ValueError:
            print("\nPilihan tidak valid!")
            continue

        if role == "admin":
            admin_actions = {
                1: system.add_product,
                2: system.update_product,
                3: lambda: print("\nFitur hapus produk belum diimplementasikan"),
                4: lambda: system.show_products("nama-asc"),
                5: lambda: system.show_products("nama-desc"),
                6: lambda: system.show_products("harga-asc"),
                7: lambda: system.show_products("harga-desc"),
                8: lambda: system.show_transactions(username, True),
                0: lambda: print("\nTerima kasih telah menggunakan aplikasi ini!")
            }
            
            action = admin_actions.get(choice)
            if action:
                if choice == 0:
                    action()
                    break
                action()
            else:
                print("\nPilihan tidak valid!")
        else:
            user_actions = {
                1: lambda: system.process_purchase(username),
                2: lambda: system.show_transactions(username),
                0: lambda: print("\nTerima kasih telah menggunakan aplikasi ini!")
            }
            
            action = user_actions.get(choice)
            if action:
                if choice == 0:
                    action()
                    break
                action()
            else:
                print("\nPilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()