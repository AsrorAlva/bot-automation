from app.helpers.Helpers import human_type, random_wait
from playwright.sync_api import Keyboard

def isi_detil_barang(page):
    print("Mulai isi detil barang...")

    try:
        print("Mengisi Data Detil Barang...")
        page.click("#search_noreg")
        random_wait(0.8, 1.2)

        input_selector = "#src_txt_src-reg-prod-otkos"
        human_type(page, input_selector, "NA22241300064")
        random_wait(0.5, 1.0)

        page.press(input_selector, "Enter")
        print("Tekan Enter untuk mencari produk...")
        random_wait(2.0, 3.0)

        page.wait_for_selector("tr[id^='src-reg-prod-otkos_']", timeout=8000)
        print("Hasil pencarian produk muncul.")

        page.click("tr#src-reg-prod-otkos_1")
        print("Produk dipilih dari hasil pencarian.")

        random_wait(1.0, 1.5)
        print("Semua data detil barang berhasil diisi.")
        
        # HS Code
        page.click("#search_hs")
        random_wait(0.8, 1.2)
        
        selected_hs = "A.HS_NO"  
        # selected_hs = "A.HS_DESC"  
        
        page.select_option("#src_by_src-hs", value=selected_hs)
        print(f"Select HS Code berdasarkan: {selected_hs}")
        random_wait(0.8, 1.5)

        hs_input = "#src_txt_src-hs"
        human_type(page, hs_input, "33041000")
        random_wait(0.5, 1.0)
        
        page.press(hs_input, "Enter")
        print("Cari HS Code dengan menekan Enter...")
        random_wait(2.0, 3.0)
        print("Hasil pencarian HS Code muncul.")
        
        page.click("tr#src-hs_1")
        print("HS Code dipilih dari hasil pencarian.")
        random_wait(1.0, 1.5)

        # kemasan
        page.click("#search_kemasan")
        random_wait(0.8, 1.2)
        
        selected_kemasan = "KEMASAN_DESC"
        # selected_kemasan = "KEMASAN_KODE"
        
        page.select_option("#src_by_src-kemasan", value=selected_kemasan)
        print(f"Select Kemasan berdasarkan: {selected_kemasan}")
        random_wait(0.8, 1.5)
        
        kemasan_input = "#src_txt_src-kemasan"
        human_type(page, kemasan_input, "CQ")
        random_wait(0.5, 1.0)
        
        page.press(kemasan_input, "Enter")
        print("Cari Kemasan dengan menekan Enter...")
        random_wait(2.0, 3.0)
        
        page.click("tr#src-kemasan_1")
        print("Kemasan dipilih dari hasil pencarian.")
        random_wait(1.0, 1.5)
        
        # satuan
        page.click("#search_satuan")
        selected_satuan = "SATUAN_DESC"
        # selected_satuan = "SATUAN_KODE"
        page.select_option("#src_by_src-satuan", value=selected_satuan)
        print(f"Select Satuan berdasarkan: {selected_satuan}")
        random_wait(0.8, 1.5)
        
        satuan_input = "#src_txt_src-satuan"
        human_type(page, satuan_input, "PCE")
        random_wait(0.5, 1.0)
        
        page.press(satuan_input, "Enter")
        print("Cari Satuan dengan menekan Enter...")
        random_wait(2.0, 3.0)
        
        page.click("tr#src-satuan_1")
        print("Satuan dipilih dari hasil pencarian.")
        random_wait(1.0, 1.5)
        
        # Data Produsen
        page.click("#search_produsen")
        random_wait(0.8, 1.2)
        
        selected_produsen = "X.PRODUSEN_NAMA"
        
        page.select_option("#src_by_src-produsen", value=selected_produsen)
        print(f"Select Produsen berdasarkan: {selected_produsen}")
        random_wait(0.8, 1.5)
        
        produsen_input = "#src_txt_src-produsen"
        human_type(page, produsen_input, "1 Fois 1 Jour")
        random_wait(0.5, 1.0)
        
        page.press(produsen_input, "Enter")
        print("Cari Produsen dengan menekan Enter...")
        random_wait(2.0, 3.0)
        
        page.click("tr#src-produsen_1")
        print("Produsen dipilih dari hasil pencarian.")
        random_wait(1.0, 1.5)
        
        # batch
        
        # pilih kurs
        selected_kurs = "USD"
        page.select_option("#KURS_KODE", value=selected_kurs)
        print(f"Kurs dipilih: {selected_kurs}")
        random_wait(0.8, 1.5)
        
        
        batch_data = [
            {"no_batch": "B001", "jml_kemasan": "10", "jml_satuan": "100", "harga_satuan": "12.00"},
            {"no_batch": "B002", "jml_kemasan": "8", "jml_satuan": "80", "harga_satuan": "15.00"},
            {"no_batch": "B003", "jml_kemasan": "12", "jml_satuan": "120", "harga_satuan": "27.00"},
        ]

        for idx, batch in enumerate(batch_data, start=1):
            # isi batch
            page.fill(f"#no_batch_{idx}", batch["no_batch"])
            page.fill(f"#jml_kemasan_{idx}", batch["jml_kemasan"])
            page.fill(f"#jml_satuan_{idx}", batch["jml_satuan"])
            
            # tunggu hasil jml_total muncul
            page.wait_for_selector(f"#jml_total_{idx}", timeout=5000)
            
            page.fill(f"#harga_satuan_{idx}", batch["harga_satuan"])
            
            # tunggu hasil jml_harga muncul
            page.wait_for_selector(f"#jml_harga_{idx}", timeout=5000)
            
            print(f"Batch {idx} terisi: {batch}")
            
            # hanya tambah batch baru jika ada batch berikutnya
            if idx < len(batch_data):
                page.click("button.button.icon.add[onclick='add_batch()']")
                print(f"Menambah batch ke-{idx+1}")
                random_wait(0.5, 1.0)

        

    except Exception as e:
        print(f"Gagal isi detil barang: {e}")
    print("Form detil barang selesai diisi.")