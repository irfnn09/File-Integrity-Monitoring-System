
import os
import hashlib
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime




# Fungsi kira hash
def kira_hash(laluan):
    sha256 = hashlib.sha256()

    with open(laluan, "rb") as fail:
        kandungan = fail.read()
        sha256.update(kandungan)

    return sha256.hexdigest()


# Fungsi scan folder
def scan_folder():
    print("\nScanning folder...")

    jumlah = 0

    for root, folders, files in os.walk(folder):
        for nama in files:
            laluan = os.path.join(root, nama)

            print(laluan)
            jumlah += 1

    print("\nJumlah fail:", jumlah)



# Fungsi save baseline

def save_baseline():
    data_fail = {}

    for root, folders, files in os.walk(folder):
        for nama in files:
            laluan = os.path.join(root, nama)

            hasil = kira_hash(laluan)
            data_fail[laluan] = hasil

    with open("baseline.json", "w") as fail:
        json.dump(data_fail, fail, indent=4)

    print("\nBaseline berjaya disimpan!")
    print("Jumlah fail disimpan:", len(data_fail))



# Fungsi check changes


def check_changes():
    if not os.path.exists("baseline.json"):
        print("\nBaseline belum wujud!")
        return

    with open("baseline.json", "r") as fail:
        baseline = json.load(fail)

    fail_semasa = {}

    for root, folders, files in os.walk(folder):
        for nama in files:
            laluan = os.path.join(root, nama)
            fail_semasa[laluan] = kira_hash(laluan)

    fail_asal = set(baseline.keys())
    fail_terkini = set(fail_semasa.keys())

    fail_baharu = fail_terkini - fail_asal
    fail_dipadam = fail_asal - fail_terkini

    fail_diubah = []
    fail_tidak_berubah = []

    for laluan in fail_terkini & fail_asal:
        if fail_semasa[laluan] != baseline[laluan]:
            fail_diubah.append(laluan)
        else:
            fail_tidak_berubah.append(laluan)

    # Paparkan keputusan
    for laluan in fail_baharu:
        print(laluan, "- FAIL BAHARU DIKESAN")

    for laluan in fail_diubah:
        print(laluan, "- FAIL TELAH DIUBAH")

    for laluan in fail_dipadam:
        print(laluan, "- FAIL TELAH DIPADAM")

    for laluan in fail_tidak_berubah:
        print(laluan, "- TIADA PERUBAHAN")

    # Jana laporan
    masa = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open("monitoring_report.txt", "a") as report:
        report.write("\n==============================\n")
        report.write("FILE MONITORING REPORT\n")
        report.write("Date: " + masa + "\n")
        report.write("==============================\n")

        report.write("\nNew Files:\n")
        for laluan in fail_baharu:
            report.write(laluan + "\n")

        report.write("\nModified Files:\n")
        for laluan in fail_diubah:
            report.write(laluan + "\n")

        report.write("\nDeleted Files:\n")
        for laluan in fail_dipadam:
            report.write(laluan + "\n")

        report.write("\nUnchanged Files:\n")
        for laluan in fail_tidak_berubah:
            report.write(laluan + "\n")

    print("\nMonitoring report berjaya dijana!")



# Bina window utama
window = tk.Tk()

# Tetapkan tajuk window
window.title("File Integrity Monitoring System")

# Tetapkan saiz window
window.geometry("750x650")
window.configure(bg="#DDE3EA")

tajuk = tk.Label(
    window,
    text="FILE INTEGRITY MONITORING SYSTEM",
    font=("Arial", 16, "bold"),
    bg="#F0F2F5",
    fg="#1B263B",
)

tajuk.pack(pady=20)
lokasi = tk.Label(
    window, 
    text="Tiada folder dipilih",
    bg="#DDE3EA",
    fg="#34495E")
lokasi.pack(pady=5)

def pilih_folder():
    folder = filedialog.askdirectory()

    if folder:
        lokasi.config(text=folder)


butang_browse = tk.Button(
    window,
    text="Browse Folder",
    command=pilih_folder,
    bg="#2D6A4F",
    fg="white",
    font=("Arial", 10, "bold"),
    width=16,
)

butang_browse.pack(pady=5)

def scan_gui():
    status.config(text="● SCANNING...", fg="#E09F3E")
    window.update()
    folder = lokasi.cget("text")

    if folder == "Tiada folder dipilih":
        messagebox.showwarning("Warning", "Sila pilih folder dahulu!")
        return

    hasil = ""

    for root, folders, files in os.walk(folder):
        for nama in files:
            hasil += os.path.join(root, nama) + "\n"

    output.delete("1.0", tk.END)
    output.insert(tk.END, hasil)
    status.config(text="● SCAN COMPLETED", fg="#2D6A4F")



baris_butang = tk.Frame(window, bg="#DDE3EA")
baris_butang.pack(pady=10)
butang_scan = tk.Button(
    baris_butang,
    text="Scan Folder",
    command=scan_gui,
    bg="#2D6A4F",
    fg="white",
    font=("Arial", 10, "bold"),
    width=16,
    
)

butang_scan.pack(side="left", padx=10)

output = tk.Text(
    window,
    height=18,
    width=85,
    font=("Consolas", 10),
    bg="#FFFFFF",
    fg="#1B263B",
    relief="solid",
    bd=1,
    padx=10,
    pady=10,
    highlightthickness=2,
    highlightbackground="#7A8694",
)
status = tk.Label(
    window,
    text="● READY",
    font=("Arial", 10, "bold"),
    bg="#DDE3EA",
    fg="#2D6A4F"
)
status.pack(pady=(15, 5))

label_output = tk.Label(
    window,
    text="SCAN RESULTS",
    font=("Arial", 11, "bold"),
    bg="#F0F2F5",
    fg="#1B263B"
)
label_output.pack(anchor="center", padx=(25,5))
output.pack(pady=15, padx=20)

def save_gui():
    status.config(text="● SAVING BASELINE...", fg="#E09F3E")
    window.update()
    folder = lokasi.cget("text")

    if folder == "Tiada folder dipilih":
        messagebox.showwarning("Warning", "Sila pilih folder dahulu!")
        return

    data_fail = {}

    for root, folders, files in os.walk(folder):
        for nama in files:
            laluan = os.path.join(root, nama)
            data_fail[laluan] = kira_hash(laluan)

    with open("baseline.json", "w") as fail:
        json.dump(data_fail, fail, indent=4)

    status.config(text="● BASELINE SAVED", fg="#2D6A4F")
    messagebox.showinfo("Success", "Baseline berjaya anjay!")


butang_baseline = tk.Button(
    baris_butang,
    text="Save Baseline",
    command=save_gui,
    bg="#2D6A4F",
    fg="white",
    font=("Arial", 10, "bold"),
    width=16,
)

butang_baseline.pack(side="left", padx=10)

def check_gui():
    status.config(text="● CHECKING FILES...", fg="#E09F3E")
    window.update()
    folder = lokasi.cget("text")
    

    if folder == "Tiada folder dipilih":
        messagebox.showwarning("Warning", "Sila pilih folder dahulu!")
        return

    if not os.path.exists("baseline.json"):
        messagebox.showwarning("Warning", "Baseline belum disimpan!")
        return

    with open("baseline.json", "r") as fail:
        baseline = json.load(fail)

    fail_semasa = {}

    for root, folders, files in os.walk(folder):
        for nama in files:
            laluan = os.path.join(root, nama)
            fail_semasa[laluan] = kira_hash(laluan)

    fail_baharu = set(fail_semasa) - set(baseline)
    fail_dipadam = set(baseline) - set(fail_semasa)

    fail_diubah = []
    fail_tidak_berubah = []

    for laluan in set(fail_semasa) & set(baseline):
        if fail_semasa[laluan] != baseline[laluan]:
            fail_diubah.append(laluan)
        else:
            fail_tidak_berubah.append(laluan)

    hasil = ""

    for fail in fail_baharu:
        hasil += "[NEW] " + fail + "\n"

    for fail in fail_diubah:
        hasil += "[MODIFIED] " + fail + "\n"

    for fail in fail_dipadam:
        hasil += "[DELETED] " + fail + "\n"

    for fail in fail_tidak_berubah:
        hasil += "[UNCHANGED] " + fail + "\n"

    output.delete("1.0", tk.END)
    output.insert(tk.END, hasil)

    if fail_baharu or fail_diubah or fail_dipadam:
            status.config(text="● CHANGES DETECTED", fg="#D97706")
    else:
            status.config(text="● NO CHANGES", fg="#2D6A4F")

    os.makedirs("reports", exist_ok=True)
    masa = datetime.now().strftime("%Y%m%d_%H%M%S")
    nama_report = f"reports/report_{masa}.txt"

    with open(nama_report, "w", encoding="utf-8") as report:
        report.write("FILE INTEGRITY MONITORING REPORT\n")
        report.write("=" * 40 + "\n")
        report.write(f"Date & Time: {datetime.now()}\n")
        report.write(f"Folder: {folder}\n")
        report.write("=" * 40 + "\n\n")
        report.write(hasil)
        
    messagebox.showinfo(
        "Complete",
        f"Pemeriksaan fail selesai hadeh!\nReport disimpan di :\n{nama_report}"
        )


butang_check = tk.Button(
    baris_butang,
    text="Check File Changes",
    command=check_gui,
    bg="#2D6A4F",
    fg="white",
    font=("Arial", 10, "bold"),
    width=16,
)

butang_check.pack(side="left", padx=10)

# Jalankan aplikasi
window.mainloop()



