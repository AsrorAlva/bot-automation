from playwright.sync_api import sync_playwright
import os, re, random, time
from urllib.parse import urljoin
from app.helpers.Helpers import random_wait, human_type
from app.bot.PengajuanBaru import isi_form_pengajuan_baru
from app.bot.PengisianDetilBarang import isi_detil_barang

EBPOM_URL = "https://e-bpom.pom.go.id/"

def run(headless=False):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless, args=["--start-maximized"])
        context = browser.new_context(viewport=None)
        page = context.new_page()
        page.goto(EBPOM_URL)
        page.evaluate("document.body.style.zoom='0.9'")
        print("Zoom ke 90%")

        # Tutup popup awal (jika ada)
        try:
            page.wait_for_selector("span.messi-closebtn", timeout=3000)
            page.click("span.messi-closebtn")
            print("Popup informasi berhasil ditutup.")
        except:
            print("Tidak ada popup informasi.")

        page.evaluate("document.body.style.zoom='1.0'")

        # Klik tombol login di menu utama
        try:
            page.click("div.main-content-main-menu-login")
            random_wait(0.5, 1.0)
        except Exception as e:
            print("Gagal klik tombol login:", e)
            
        print("\n🪪 Silakan ketik username dan password Anda di sini:")
        USERNAME = input("Username: ").strip()
        PASSWORD = input("Password: ").strip()

        # Isi username & password
        try:
            human_type(page, "#login_username", USERNAME, min_delay=0.06, max_delay=0.12)
            human_type(page, "#login_password", PASSWORD, min_delay=0.08, max_delay=0.14)
            random_wait(0.6, 1.2)
        except Exception as e:
            print("Gagal mengetik username/password:", e)

        # Ambil captcha
        captcha_value = None
        try:
            page.wait_for_selector("img#captcha", timeout=5000)
            src = page.get_attribute("img#captcha", "src")
            full_src = urljoin(page.url, src)
            print("Captcha URL:", full_src)

            # Simpan key
            m = re.search(r"[?&]key=([^&]+)", full_src)
            captcha_value = m.group(1) if m else None
            print("Captcha key:", captcha_value)

            if captcha_value:
                human_type(page, "#login_security_code", captcha_value)
            else:
                print("Tidak ada captcha otomatis, masukkan manual.")
        except Exception as e:
            print("Captcha error:", e)

        # Login
        try:
            page.click("button[type=submit]")
            print("Tombol login diklik.")
        except Exception as e:
            print("Gagal klik tombol login:", e)

        page.wait_for_timeout(2500)

        # Cek apakah login gagal
        if page.query_selector("div.messi-box"):
            msg = page.inner_text("div.messi-content").strip()
            print(f"❌ Login gagal: {msg}")
            page.click("button#btn_messi_1")
            browser.close()
            return

        print("✅ Login berhasil.")

        # Navigasi ke Pengajuan Baru
        try:
            page.click("div#trigger")
            random_wait(0.8, 1.2)
            page.click("a.icon.icon-mail:has-text('Pengajuan Impor')")
            random_wait(0.8, 1.2)
            page.click("a.icon.icon-mail[onclick*='frm-pengajuan.php']")
            print("➡️ Masuk ke halaman Pengajuan Baru.")
        except Exception as e:
            print("Gagal buka Pengajuan Baru:", e)
            browser.close()
            return

        # Jalankan form pengajuan
        isi_form_pengajuan_baru(page)
        
        # Jalankan form Pengisian Detail
        isi_detil_barang(page)

        # # Logout
        # try:
        #     page.click("div#trigger", timeout=5000)
        #     print("Klik Menu")
        #     random_wait(0.8,1.5)
            
        #     page.click('a.icon.icon-lock[onclick="logout()"]')
        #     print("Logout Berhasil")
        #     random_wait(0.8,1.5)
            
        #     if page.locator("div.messi-box").is_visible(timeout=5000):
        #         print("Muncul Popup")
                
        #         page.click("#btn_messi_1")
        #         print("Pencet Ya")
        #         random_wait(0.8,1.5)
        #     else:
        #         print("")
                
        #     print("Berhasil Logout")
            
        # except Exception as e:
        #     print("Gagal logout:", e)
            

        time.sleep(10)
        browser.close()
        print("🧹 Browser ditutup, sesi selesai.")


if __name__ == "__main__":
    run(headless=False)
