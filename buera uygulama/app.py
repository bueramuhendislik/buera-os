import streamlit as st
import pandas as pd
import numpy as np
import math
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="BUERA OS", page_icon="🚀", layout="centered")

# --- YAN MENÜ (SIDEBAR) TASARIMI ---


st.sidebar.title("BUERA OS")
st.sidebar.markdown("**v2.1 Pro Dashboard**")
st.sidebar.markdown("---")

# Menü Seçenekleri
menu = [
    "💰 Kârlılık Analizi", 
    "📦 Stok (EOQ)", 
    "📉 İndirim Simülatörü", 
    "📊 Portföy (ABC)", 
    "🔮 Gelecek Tahmini",
    "🎁 Paket (Bundle)",
    "📢 Reklam (ROAS)",
    "⚖️ Başabaş (Genel)"
]

secim = st.sidebar.radio("MODÜLLER:", menu)

st.sidebar.markdown("---")
st.sidebar.info("Endüstri Mühendisliği Tabanlı Karar Destek Sistemi")
st.sidebar.caption("Designed by Buğrahan") 

# --- ANA BAŞLIK ---
st.title("🚀 BUERA E-Ticaret İşletim Sistemi")
st.markdown(f"**Aktif Modül:** :blue[{secim}]")
st.markdown("---")

# ==========================================
# MODÜL 1: KÂRLILIK ANALİZİ
# ==========================================
if secim == "💰 Kârlılık Analizi":
    st.header("Tekli Ürün Analizi")
    st.info("Bir ürünün maliyet yapısını detaylı inceleyin.")
    
    col1, col2 = st.columns(2)
    with col1:
        urun_adi = st.text_input("Ürün Adı", "Örnek Tişört", key="m1_ad")
        satis_fiyati = st.number_input("Satış Fiyatı (TL)", 0.0, value=500.0, key="m1_satis")
        alis_maliyeti = st.number_input("Alış Maliyeti (TL)", 0.0, value=250.0, key="m1_alis")
        kargo_ucreti = st.number_input("Kargo (TL)", 0.0, value=60.0, key="m1_kargo")
    with col2:
        komisyon_orani = st.slider("Komisyon (%)", 0, 50, 20, key="m1_kom") / 100
        iade_orani = st.slider("İade Riski (%)", 0, 30, 10, key="m1_iade") / 100
        reklam_gideri = st.number_input("Reklam (TL)", 0.0, value=20.0, key="m1_reklam")

    if st.button("Analiz Et 🔍", type="primary", key="btn1"):
        komisyon_tutari = satis_fiyati * komisyon_orani
        iade_maliyeti = (kargo_ucreti * 2) * iade_orani
        toplam_kesinti = alis_maliyeti + komisyon_tutari + kargo_ucreti + iade_maliyeti + reklam_gideri
        net_kar = satis_fiyati - toplam_kesinti
        marj = (net_kar / satis_fiyati) * 100 if satis_fiyati > 0 else 0
        
        st.divider()
        c1, c2, c3 = st.columns(3)
        c1.metric("Toplam Maliyet", f"{toplam_kesinti:.1f} TL")
        c2.metric("Net Kâr", f"{net_kar:.1f} TL")
        c3.metric("Kâr Marjı", f"%{marj:.1f}")
        if marj > 20: st.success("🟢 **YILDIZ ÜRÜN**")
        elif marj < 5: st.error("🔴 **ZOMBİ ÜRÜN**")
        else: st.warning("🟡 **STANDART**")

# ==========================================
# MODÜL 2: STOK OPTİMİZASYONU (EOQ)
# ==========================================
elif secim == "📦 Stok (EOQ)":
    st.header("EOQ Stok Modeli")
    st.warning("Optimum sipariş adedini hesaplar.")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        yillik_talep = st.number_input("Yıllık Satış (Adet)", min_value=1, value=1200)
        birim_maliyet = st.number_input("Birim Alış (TL)", min_value=1.0, value=100.0)
    with col_s2:
        siparis_maliyeti = st.number_input("Sipariş Maliyeti (TL)", min_value=1.0, value=500.0)
        tasima_maliyeti_orani = st.slider("Depolama (%)", 1, 50, 20) / 100

    if st.button("Hesapla 📦", key="btn2"):
        H = birim_maliyet * tasima_maliyeti_orani
        eoq = math.sqrt((2 * yillik_talep * siparis_maliyeti) / H)
        c1, c2 = st.columns(2)
        c1.metric("Optimum Sipariş", f"{round(eoq)} Adet")
        c2.metric("Sıklık", f"{round(yillik_talep/eoq, 1)} Kez/Yıl")

# ==========================================
# MODÜL 3: İNDİRİM SİMÜLATÖRÜ
# ==========================================
elif secim == "📉 İndirim Simülatörü":
    st.header("İndirim Senaryosu")
    st.info("İndirim yapıldığında kârı korumak için gereken satış artışı.")
    col_i1, col_i2 = st.columns(2)
    with col_i1:
        sim_fiyat = st.number_input("Mevcut Fiyat", value=500.0)
        sim_maliyet = st.number_input("Maliyet", value=300.0)
    with col_i2:
        indirim_orani = st.slider("İndirim Oranı", 0, 50, 15) / 100
        sim_satis_adedi = st.number_input("Mevcut Satış", value=100)

    if st.button("Simüle Et 🎲", key="btn3"):
        yeni_kar = (sim_fiyat * (1 - indirim_orani)) - sim_maliyet
        eski_kar = sim_fiyat - sim_maliyet
        if yeni_kar <= 0: st.error("ZARAR EDERSİNİZ!")
        else:
            artis = (eski_kar / yeni_kar) - 1
            st.metric("Gereken Satış Artışı", f"%{artis*100:.0f}", delta="Hedef")

# ==========================================
# MODÜL 4: ABC ANALİZİ
# ==========================================
elif secim == "📊 Portföy (ABC)":
    st.header("📊 Portföy Analizi (ABC)")
    veri_kaynagi = st.radio("Veri Modu:", ["🧪 Demo Veri", "📝 Manuel Giriş"], horizontal=True, key="abc_radio")
    df_analiz = None
    if veri_kaynagi == "🧪 Demo Veri":
        if st.button("Örnek Veri Yükle", key="btn_demo"):
            np.random.seed(42)
            urunler = [f"Ürün-{i}" for i in range(1, 15)]
            satislar = np.random.randint(20, 500, 14)
            fiyatlar = np.random.randint(100, 1000, 14)
            maliyetler = [f * np.random.uniform(0.4, 0.9) for f in fiyatlar]
            df_analiz = pd.DataFrame({"Ürün Adı": urunler, "Satış Adedi": satislar, "Satış Fiyatı": fiyatlar, "Birim Maliyet": maliyetler})
    else:
        sablon_data = pd.DataFrame([{"Ürün Adı": "Tişört Basic", "Satış Adedi": 100, "Satış Fiyatı": 250, "Birim Maliyet": 120}])
        edited_df = st.data_editor(sablon_data, num_rows="dynamic", use_container_width=True)
        if st.button("Analizi Başlat 🚀", key="btn_manual"): 
             if not edited_df.empty: df_analiz = edited_df.copy()

    if df_analiz is not None:
        df_analiz["Ciro"] = df_analiz["Satış Adedi"] * df_analiz["Satış Fiyatı"]
        df_analiz["Toplam Maliyet"] = df_analiz["Satış Adedi"] * df_analiz["Birim Maliyet"]
        df_analiz["Brüt Kâr"] = df_analiz["Ciro"] - df_analiz["Toplam Maliyet"]
        df_analiz = df_analiz.sort_values(by="Brüt Kâr", ascending=False).reset_index(drop=True)
        df_analiz["Kümülatif"] = df_analiz["Brüt Kâr"].cumsum()
        df_analiz["Pay %"] = (df_analiz["Kümülatif"] / df_analiz["Brüt Kâr"].sum()) * 100
        df_analiz["Sınıf"] = df_analiz["Pay %"].apply(lambda y: "A" if y <= 80 else ("B" if y <= 95 else "C"))
        st.bar_chart(df_analiz, x="Ürün Adı", y="Brüt Kâr", color="#00FF00")
        st.dataframe(df_analiz)

# ==========================================
# MODÜL 5: TALEP TAHMİNİ
# ==========================================
elif secim == "🔮 Gelecek Tahmini":
    st.header("🔮 Gelecek Tahmini")
    forecast_source = st.radio("Veri Kaynağı:", ["🧪 Demo Veri", "📝 Manuel Geçmiş Verisi"], horizontal=True, key="fc_radio")
    df_history = None
    if forecast_source == "🧪 Demo Veri":
        if st.button("Rastgele Geçmiş Oluştur", key="btn_fc_demo"):
            months = range(1, 13)
            sales = [100 + (10 * m) + np.random.randint(-20, 20) for m in months]
            df_history = pd.DataFrame({"Ay (Sıra)": months, "Satış Adedi": sales})
    else:
        fc_sablon = pd.DataFrame([{"Ay (Sıra)": 1, "Satış Adedi": 120}, {"Ay (Sıra)": 2, "Satış Adedi": 135}])
        df_history = st.data_editor(fc_sablon, num_rows="dynamic", use_container_width=True)
        if st.button("Geleceği Tahmin Et 🚀", key="btn_fc_manual"): pass

    if df_history is not None and not df_history.empty:
        X = df_history["Ay (Sıra)"].values
        y = df_history["Satış Adedi"].values
        if len(X) > 1:
            z = np.polyfit(X, y, 1) 
            p = np.poly1d(z)
            next_month = X[-1] + 1
            prediction = p(next_month)
            st.metric("Gelecek Ay Tahmini", f"{int(prediction)} Adet")
            df_future = pd.DataFrame({"Ay (Sıra)": [next_month], "Satış Adedi": [prediction]})
            st.line_chart(pd.concat([df_history, df_future]).set_index("Ay (Sıra)"))

# ==========================================
# MODÜL 6: BUNDLE MÜHENDİSLİĞİ
# ==========================================
elif secim == "🎁 Paket (Bundle)":
    st.header("🎁 Paket (Bundle) Oluşturucu")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        fiyat_a = st.number_input("Satış Fiyatı (A)", value=500.0, key="b_fa")
        maliyet_a = st.number_input("Maliyet (A)", value=250.0, key="b_ma")
    with col_b2:
        fiyat_b = st.number_input("Satış Fiyatı (B)", value=200.0, key="b_fb")
        maliyet_b = st.number_input("Maliyet (B)", value=80.0, key="b_mb")
    
    col_st1, col_st2 = st.columns(2)
    with col_st1: bundle_indirim = st.slider("Paket İndirimi (%)", 0, 50, 15) / 100
    with col_st2: kargo_tasarrufu = st.number_input("Kargo Tasarrufu (TL)", value=60.0)

    if st.button("Paketi Analiz Et 🎁", key="btn_bundle"):
        ayri_kar = (fiyat_a + fiyat_b) - (maliyet_a + maliyet_b + kargo_tasarrufu)
        paket_fiyati = (fiyat_a + fiyat_b) * (1 - bundle_indirim)
        paket_kar = paket_fiyati - (maliyet_a + maliyet_b)
        
        c1, c2 = st.columns(2)
        c1.metric("Paket Başı Kâr", f"{paket_kar:.2f} TL", delta=f"{paket_kar - ayri_kar:.1f} TL Fark")
        if paket_kar > ayri_kar: st.success("✅ MÜKEMMEL STRATEJİ")
        else: st.warning("⚖️ MAKUL / ZARARLI")

# ==========================================
# MODÜL 7: REKLAM MÜHENDİSLİĞİ (ROAS)
# ==========================================
elif secim == "📢 Reklam (ROAS)":
    st.header("📢 Reklam Analizi (ROAS)")
    col_roas1, col_roas2 = st.columns(2)
    with col_roas1:
        reklam_harcamasi = st.number_input("Reklam Bütçesi (TL)", value=5000.0)
        reklam_cirosu = st.number_input("Reklam Cirosu (TL)", value=20000.0)
    with col_roas2:
        ortalama_kar_marji = st.slider("Ort. Kâr Marjı (%)", 5, 80, 25) / 100

    if st.button("Reklamı Analiz Et 📢", key="btn_roas"):
        gerceklesen_roas = reklam_cirosu / reklam_harcamasi if reklam_harcamasi > 0 else 0
        break_even_roas = 1 / ortalama_kar_marji if ortalama_kar_marji > 0 else 999
        operasyonel_kar = (reklam_cirosu * ortalama_kar_marji) - reklam_harcamasi
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Gerçekleşen ROAS", f"{gerceklesen_roas:.2f}")
        m2.metric("Min Hedef ROAS", f"{break_even_roas:.2f}", delta_color="inverse")
        m3.metric("Reklam Sonrası Net", f"{operasyonel_kar:,.0f} TL")
        if gerceklesen_roas > break_even_roas: st.success("✅ KÂRLI REKLAM")
        else: st.error("🛑 ZARARLI REKLAM")

# ==========================================
# MODÜL 8: ÇOKLU ÜRÜN İÇİN BAŞABAŞ ANALİZİ
# ==========================================
elif secim == "⚖️ Başabaş (Genel)":
    st.header("⚖️ Genel Dükkan Başabaş Analizi")
    st.markdown("Dükkanınızın sabit giderlerini karşılamak için yapmanız gereken **Minimum Ciro Hedefini** bulun.")
    
    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        sabit_gider = st.number_input("Aylık Sabit Giderler (TL)", value=30000.0, step=1000.0, help="Kira, Maaş, Faturalar vb.")
    with col_gen2:
        genel_kar_marji = st.slider("Ortalama Brüt Kâr Marjı (%)", 5, 100, 30) / 100
        suanki_ciro = st.number_input("Bu Ayki Ciro (TL)", value=80000.0, step=1000.0)

    if st.button("Ölüm Çizgisini Hesapla ⚖️", type="primary", key="btn_cvp_gen"):
        if genel_kar_marji > 0:
            basabas_cirosu = sabit_gider / genel_kar_marji
            tahmini_net_kar = (suanki_ciro * genel_kar_marji) - sabit_gider
            fark = suanki_ciro - basabas_cirosu
            
            st.divider()
            c1, c2, c3 = st.columns(3)
            c1.metric("Gereken Minimum Ciro", f"{basabas_cirosu:,.0f} TL")
            c2.metric("Şu Anki Ciro", f"{suanki_ciro:,.0f} TL", delta=f"{fark:,.0f} TL", delta_color="normal")
            c3.metric("Tahmini Net Durum", f"{tahmini_net_kar:,.0f} TL")

            if suanki_ciro >= basabas_cirosu:
                st.success("✅ GÜVENLİ BÖLGE: Dükkan kâra geçti.")
            else:
                st.error(f"🚨 ZARAR BÖLGESİ: Dükkanı döndürmek için {abs(fark):,.0f} TL daha ciro lazım.")
            
            chart_data = pd.DataFrame({
                "Gereken Ciro (Hedef)": [basabas_cirosu],
                "Şu Anki Ciro": [suanki_ciro]
            })
            st.bar_chart(chart_data, color=["#FF0000", "#00FF00"])
        else:
            st.error("Kâr marjı 0 olamaz.")