USER_MANUAL ="""
            **⚽ Premier Lig Asistanı Kullanım Kılavuzu:**
            1. **Sorularınızı Sorun:** 
               - Sağdaki 'Örnek Sorular' bölümünden bir soru seçebilir veya kendi sorunuzu yazabilirsiniz.
               - Her soru için tek cevap üretilir ve hafıza tutulmaz.
            2. **Yanıt Alın:**
               - Sorunuzu yazdıktan veya örnek soru seçtikten sonra 'Enter' tuşuna basarak sistemden yanıt alabilirsiniz.
               - Yanıtınızı aldıktan sonra sistem hafızası 0'lanır ve yeni sorunuzda geçmiş bilgiler tutulmaz.
            3. **Örnek Soru Kategorileri:**
               - Örnek Sorular, farklı kategorilere ayrılmıştır (örn: Maç Sonucu, Alt/Üst, Kart Soruları).
               - İlgili kategoriden soru seçerek detaylı bilgi alabilirsiniz.
            4. **Analiz ve Tahminler:**
               - Sistem, yalnızca mevcut istatistiklere dayalı analiz ve tahminler yapar. Spekülasyon içermez.
            5. **mAI Entegrasyon:**
               - Sistem, mAI'ye gelen haftalık maçlarla ilgili tahmin sorularında tetikleneceği için genel istatistik sorularına cevap veremez.
               -örn: gol kralı kimdir? sorusu mAI'den dönecek bir cevaptır ve bu agenta gelmeyecektir. 
               ancak city maçında kimler gol atar? sorusu için agent tetiklenip cevap üretecektir.


            **Önemli Not:** Yanıtlar, veri tabanındaki mevcut bilgilere dayanır ve kesin tahmin garantisi vermez.
        """

CATEGORIES = {
    "Maç Sonucu Soruları": [
        "Londrada oynananacak maçları kimler kazanır",
        "Everton maçı ne olur?",
        "Merseyside takımları kazanır mı?",
        "City kötü gidişata son verir mi?",
    ],
    "Alt/Üst Soruları": [
        "Hangi maçlar üst olur?",
        "3.5 üst ihtimali yüksek maçlar",
        "LFC maçı 1.5 alt mı biter üst mü?",
        "Bu hafta 2.5 gol altı bitme ihtimali en yüksek olan maç hangisi?",
    ],
    "Korner Soruları": [
        "Liverpool maçında kaç köşe vuruşu kullanılır?",
        "Hangi maçlar 11.5 üst korner olur?",
    ],
    "Kart Soruları": [
        "En çok sarı kart hangi maçlarda çıkar?",
        "En çok kırmızı kart hangi maçlarda çıkar?",
        "City maçında kaç kart çıkar?",
    ],
    "Gol Dakikaları Soruları": [
        "Chelsea maçında hangi dakikalarda gol olma ihtimali en yüksek?",
        "ilk 15 dakikada gol olması en muhtemel maç hangisidir?",
    ],
    "Handikaplı Maç Sonucu Soruları": [
        "Bu hafta hangi takımlar 2 handikaplı kazanır?",
        "Arsenalin 1 handikaplı kazanma şansı nedir?"
    ],
    "Oyuncu Gol Soruları": [
        "Bu hafta en çok golü hangi oyuncular atar?",
    ],
    "Ofsayt Soruları": [
        "Bu hafta hangi maçta çok ofsayt olur?",
        "Tottınhım kaç kez ofsayta yakalanır?"
    ],
    "Gol Yemeden Kazanma Soruları": [
        "Chelsea'nin gol yemeden kazanma şansı nedir?",
        "Bu hafta hangi takımlar gol yemeden kazanır?"
    ],
    "Karşılıklı Gol Soruları": [
        "Hangi maçlarda iki takımda gol atar?",
        "Spurs maçında karşılıklı gol olur mu?",
    ],
     "Diğer": [
        "Bu hafta izlenmesi en keyifli maç hangisi olur?",
        "Bu hafta bir maçın ilk yarısıSnı ve başta bir maçın 2. yarısını izlesen hangi maçları izlemek isterdin?"
    ]
}