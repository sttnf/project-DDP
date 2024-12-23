import json
from datetime import datetime

class InventorySystem:
    def __init__(self):
        self.data = self.load_data()
        self.transactions = self.load_transactions()
        
    def load_data(self):
        try:
            with open('products.json', 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError("Format data produk tidak valid.")
                return data
        except (FileNotFoundError, ValueError) as e:
            print(f"Error saat memuat data produk: {e}")
            return {}

            
    def load_transactions(self):
        try:
            with open('transactions.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []
            
    def save_data(self):
        with open('products.json', 'w') as file:
            json.dump(self.data, file, indent=4)
            
    def save_transactions(self):
        with open('transactions.json', 'w') as file:
            json.dump(self.transactions, file, indent=4)

    @staticmethod
    def print_separator():
        print("=" * 77)

    @staticmethod
    def print_header():
        InventorySystem.print_separator()
        print(f"| {'No':2} | {'Kode':8} | {'Nama':20} | {'Harga':9} | {'Stok':3} | {'Total':9} |")
        InventorySystem.print_separator()

    @staticmethod
    def print_row(no, kode, nama, harga, stok, total):
        print(f"| {no:<2} | {kode:<8} | {nama:<20} | {harga:>9} | {stok:>3} | {total:>9} |")

    @staticmethod
    def format_currency(amount):
        return f"Rp {amount:,}"

    def show_products(self, filter_by=None, role="admin"):
        products = list(self.data.values())
        valid_products = [
            p for p in products if all(k in p for k in ["kode", "nama", "harga", "stok"])
        ]

        if not valid_products:
            print("\nTidak ada produk yang valid dalam sistem.")
            return

        if filter_by == "nama-asc":
            valid_products.sort(key=lambda x: x["nama"])
        elif filter_by == "nama-desc":
            valid_products.sort(key=lambda x: x["nama"], reverse=True)
        elif filter_by == "harga-asc":
            valid_products.sort(key=lambda x: x["harga"])
        elif filter_by == "harga-desc":
            valid_products.sort(key=lambda x: x["harga"], reverse=True)

        self.print_header()
        for idx, product in enumerate(valid_products, 1):
            self.print_row(
                idx,
                product['kode'],
                product['nama'],
                self.format_currency(product['harga']),
                product['stok'],
                self.format_currency(product['harga'] * product['stok'])
            )
        self.print_separator()
        self.show_menu(role)

    def show_menu(self, role):
        print("\nMenu:")
        if role == "admin":
            print("1. Lihat Produk")
            print("2. Tambah Produk")
            print("3. Update Produk")
            print("4. Hapus Produk")
            print("5. Urutkan Nama [A-Z]")
            print("6. Urutkan Nama [Z-A]")
            print("7. Urutkan Harga [0-9]")
            print("8. Urutkan Harga [9-0]")
            print("9. Riwayat Transaksi")
            print("0. Keluar")
        else:  # User role
            print("1. Beli Produk")
            print("2. Riwayat Transaksi")
            print("0. Keluar")
        print("\nPilihan: ", end="")

    def add_product(self):
        print("\n=== TAMBAH PRODUK ===")
        
        kode = input("Kode Produk  : ")
        if any(p['kode'] == kode for p in self.data.values()):
            print("\nKode produk sudah ada!")
            return
            
        nama = input("Nama Produk  : ")
        try:
            harga = int(input("Harga Produk : "))
            stok = int(input("Stok Produk  : "))
            if harga < 0 or stok < 0:
                print("\nHarga dan stok tidak boleh negatif!")
                return
        except ValueError:
            print("\nHarga dan stok harus berupa angka!")
            return

        new_product = {
            "kode": kode,
            "nama": nama,
            "harga": harga,
            "stok": stok
        }
        
        self.data[kode] = new_product
        self.save_data()
        print("\nProduk berhasil ditambahkan!")

    def update_product(self):
        print("\n=== UPDATE PRODUK ===")
        
        kode = input("Masukkan kode produk: ")
        if kode not in self.data:
            print("\nProduk tidak ditemukan!")
            return
            
        product = self.data[kode]
        print(f"\nData produk saat ini:")
        print(f"Nama : {product['nama']}")
        print(f"Harga: {self.format_currency(product['harga'])}")
        print(f"Stok : {product['stok']}")
        
        nama = input("\nNama baru (kosongkan jika tidak diubah): ")
        if nama:
            product['nama'] = nama
            
        try:
            harga = input("Harga baru (kosongkan jika tidak diubah): ")
            if harga:
                harga = int(harga)
                if harga < 0:
                    print("\nHarga tidak boleh negatif!")
                    return
                product['harga'] = harga
                
            stok = input("Stok baru (kosongkan jika tidak diubah): ")
            if stok:
                stok = int(stok)
                if stok < 0:
                    print("\nStok tidak boleh negatif!")
                    return
                product['stok'] += stok
        except ValueError:
            print("\nHarga dan stok harus berupa angka!")
            return
            
        self.save_data()
        print("\nProduk berhasil diupdate!")

    def delete_product(self):
        print("\n=== HAPUS PRODUK ===")
        
        kode = input("Masukkan kode produk: ")
        if kode not in self.data:
            print("\nProduk tidak ditemukan!")
            return
            
        del self.data[kode]
        self.save_data()
        print("\nProduk berhasil dihapus!")

    def buy_product(self, username):
        print("\n=== BELI PRODUK ===")
        
        kode = input("Masukkan kode produk: ")
        if kode not in self.data:
            print("\nProduk tidak ditemukan!")
            return
            
        product = self.data[kode]
        print(f"\nDetail Produk:")
        print(f"Nama: {product['nama']}")
        print(f"Harga: {self.format_currency(product['harga'])}")
        print(f"Stok: {product['stok']}")
        
        try:
            jumlah = int(input("\nJumlah yang akan dibeli: "))
            if jumlah <= 0:
                print("\nJumlah pembelian harus lebih dari 0!")
                return
            if jumlah > product['stok']:
                print("\nStok tidak mencukupi!")
                return
        except ValueError:
            print("\nJumlah harus berupa angka!")
            return
            
        total = jumlah * product['harga']
        print(f"\nTotal: {self.format_currency(total)}")
        konfirmasi = input("Konfirmasi pembelian (y/n)? ").lower()
        
        if konfirmasi == 'y':
            product['stok'] -= jumlah
            self.save_data()
            
            transaction = {
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": username,
                "kode_produk": kode,
                "nama_produk": product['nama'],
                "jumlah": jumlah,
                "total": total
            }
            self.transactions.append(transaction)
            self.save_transactions()
            
            print("\nPembelian berhasil!")
        else:
            print("\nPembelian dibatalkan.")

    def show_transactions(self, username, is_admin=False):
        print("\n=== RIWAYAT TRANSAKSI ===")
        
        filtered_transactions = self.transactions
        if not is_admin:
            filtered_transactions = [t for t in self.transactions if t['username'] == username]
            
        if not filtered_transactions:
            print("\nBelum ada transaksi.")
            return
            
        print("\n" + "=" * 80)
        print(f"| {'Waktu':19} | {'Username':10} | {'Produk':20} | {'Jumlah':6} | {'Total':15} |")
        print("=" * 80)
        
        for t in filtered_transactions:
            print(f"| {t['waktu']:19} | {t['username']:10} | "
                  f"{t['nama_produk']:20} | {t['jumlah']:6} | "
                  f"{self.format_currency(t['total']):15} |")
        print("=" * 80)

def login():
    print("\n=== LOGIN SISTEM ===")
    username = input("Username: ")
    password = input("Password: ")

    if username == "admin" and password == "admin123":
        return "admin", username
    elif username == "user" and password == "user123":
        return "user", username
    else:
        print("\nLogin gagal!")
        return None, None

def main():
    role, username = login()
    if not role:
        return
        
    system = InventorySystem()
    while True:
        if role == "user":
            # Tampilkan produk langsung untuk user
            system.show_products(role=role)
        else:
            # Tampilkan menu untuk admin
            system.show_menu(role)

        try:
            choice = input().strip()
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
        except ValueError:
            print("\nPilihan tidak valid!")
            continue

        if role == "admin":
            if choice == 1:
                system.show_products(role=role)
            elif choice == 2:
                system.add_product()
            elif choice == 3:
                system.update_product()
            elif choice == 4:
                system.delete_product()
            elif choice == 5:
                system.show_products(filter_by="nama-asc", role=role)
            elif choice == 6:
                system.show_products(filter_by="nama-desc", role=role)
            elif choice == 7:
                system.show_products(filter_by="harga-asc", role=role)
            elif choice == 8:
                system.show_products(filter_by="harga-desc", role=role)
            elif choice == 9:
                system.show_transactions(username, True)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        else:  # User role
            if choice == 1:
                system.buy_product(username)
            elif choice == 2:
                system.show_transactions(username, False)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    print("\nTerima kasih telah menggunakan aplikasi ini!")

    role, username = login()
    if not role:
        return
        
    system = InventorySystem()
    while True:
        system.show_menu(role)  # Pastikan role diberikan
        
        try:
            choice = input().strip()
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
        except ValueError:
            print("\nPilihan tidak valid!")
            continue

        if role == "admin":
            if choice == 1:
                system.show_products(role=role)  # Tambahkan argumen `role`
            elif choice == 2:
                system.add_product()
            elif choice == 3:
                system.update_product()
            elif choice == 4:
                system.delete_product()
            elif choice == 5:
                system.show_products(filter_by="nama-asc", role=role)
            elif choice == 6:
                system.show_products(filter_by="nama-desc", role=role)
            elif choice == 7:
                system.show_products(filter_by="harga-asc", role=role)
            elif choice == 8:
                system.show_products(filter_by="harga-desc", role=role)
            elif choice == 9:
                system.show_transactions(username, True)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        else:  # User role
            if choice == 1:
                system.buy_product(username)
            elif choice == 2:
                system.show_transactions(username, False)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    print("\nTerima kasih telah menggunakan aplikasi ini!")

    role, username = login()
    if not role:
        return
        
    system = InventorySystem()
    while True:
        system.show_menu(role)
        
        try:
            choice = input().strip()
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
        except ValueError:
            print("\nPilihan tidak valid!")
            continue

        if role == "admin":
            if choice == 1:
                system.show_products()
            elif choice == 2:
                system.add_product()
            elif choice == 3:
                system.update_product()
            elif choice == 4:
                system.delete_product()
            elif choice == 5:
                system.show_products(filter_by="nama-asc")
            elif choice == 6:
                system.show_products(filter_by="nama-desc")
            elif choice == 7:
                system.show_products(filter_by="harga-asc")
            elif choice == 8:
                system.show_products(filter_by="harga-desc")
            elif choice == 9:
                system.show_transactions(username, True)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        else:  # User role
            if choice == 1:
                system.buy_product(username)
            elif choice == 2:
                system.show_transactions(username, False)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    print("\nTerima kasih telah menggunakan aplikasi ini!")

    role, username = login()
    if not role:
        return
        
    system = InventorySystem()
    while True:
        system.show_products()
        
        try:
            choice = input().strip()
            if not choice.isdigit():
                raise ValueError
            choice = int(choice)
        except ValueError:
            print("\nPilihan tidak valid!")
            continue

        if role == "admin":
            if choice == 1:
                continue
            elif choice == 2:
                system.add_product()
            elif choice == 3:
                system.update_product()
            elif choice == 4:
                system.delete_product()
            elif choice == 5:
                system.show_products(filter_by="nama-asc")
            elif choice == 6:
                system.show_products(filter_by="nama-desc")
            elif choice == 7:
                system.show_products(filter_by="harga-asc")
            elif choice == 8:
                system.show_products(filter_by="harga-desc")
            elif choice == 9:
                system.show_transactions(username, True)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        else:  # User role
            if choice == 1:
                system.buy_product(username)
            elif choice == 2:
                system.show_transactions(username, False)
            elif choice == 0:
                break
            else:
                print("\nPilihan tidak valid!")
        
        input("\nTekan Enter untuk melanjutkan...")
    
    print("\nTerima kasih telah menggunakan aplikasi ini!")

if __name__ == "__main__":
    main()