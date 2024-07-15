import tkinter as tk
from tkinter import filedialog, messagebox

def save_dataframe_to_csv(df):
    # Tkinter penceresi oluşturalım (dosya seçimini yapmak için)
    root = tk.Tk()
    root.withdraw()  # Tkinter penceresini göstermeyelim, sadece dosya seçimini yapalım

    # Kullanıcıya dosya konumunu seçtirerek dataframe'i CSV formatında kaydedelim
    try:
        file_path = filedialog.asksaveasfilename(
            title="CSV dosyasını kaydetmek için bir konum seçin",
            defaultextension='.csv',
            filetypes=[('CSV Files', '*.csv')]
        )
        
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Başarılı", f"Dataframe başarıyla '{file_path}' konumuna kaydedildi.")
        else:
            messagebox.showwarning("İptal Edildi", "Dosya kaydetme işlemi iptal edildi.")
    
    except Exception as e:
        messagebox.showerror("Hata", f"Dosya kaydedilirken bir hata oluştu: {e}")
    
    finally:
        # Tkinter penceresini kapat
        root.destroy()