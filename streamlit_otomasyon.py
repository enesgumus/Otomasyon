import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# E-posta gönderme fonksiyonu
def send_email(sender_email, sender_password, subject, body, recipient_list):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            for recipient in recipient_list:
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = recipient
                message["Subject"] = subject
                message.attach(MIMEText(body, "plain"))
                server.sendmail(sender_email, recipient, message.as_string())
        return "E-posta başarıyla gönderildi!"
    except Exception as e:
        return f"E-posta gönderiminde hata: {e}"

# Streamlit arayüzü
st.title("Log Paylaşım ve E-posta Yönetim Uygulaması 📧")
st.markdown(
    "<h5 style='text-align: center; color: grey;'>Enes Gümüş tarafından geliştirildi</h5>",
    unsafe_allow_html=True
)

# Gönderici bilgilerinin giriş alanları
sender_email = st.text_input("Gönderici E-posta", placeholder="Gönderici e-posta adresini girin")
sender_password = st.text_input("Gönderici Şifre", type="password", placeholder="Gönderici e-posta şifresini girin")

# Kullanıcı E-posta Listesi Yönetimi
if "email_list" not in st.session_state:
    st.session_state.email_list = []  # Başlangıçta boş bir liste

st.subheader("E-posta Listesi Yönetimi")

# E-posta ekleme
new_email = st.text_input("Yeni E-posta Ekle", placeholder="E-posta adresini girin")
if st.button("Ekle"):
    if new_email:
        if new_email not in st.session_state.email_list:
            st.session_state.email_list.append(new_email)
            st.success(f"{new_email} e-posta listesine eklendi!")
        else:
            st.warning("Bu e-posta zaten listede.")
    else:
        st.error("E-posta adresi boş olamaz!")

# E-posta listesini checkbox ile gösterme ve seçim
st.subheader("E-posta Listesi")
selected_emails = []
if st.session_state.email_list:
    for email in st.session_state.email_list:
        if st.checkbox(email, key=email):
            selected_emails.append(email)
else:
    st.info("Henüz bir e-posta eklenmedi.")

# Seçilen e-postaları alıcılar listesine taşıma
recipient_input = st.text_area(
    "Alıcı E-posta Adresleri",
    ", ".join(selected_emails),  # Seçilenleri virgülle ayır
    placeholder="Seçilen e-posta adresleri burada görünecek"
)

# E-posta konusu ve içeriği
st.subheader("E-posta İçeriği")
subject = st.text_input("E-posta Konusu", placeholder="Konu girin")
selected_date = st.date_input("Log Tarihi", help="Bu tarih e-posta içeriğinde gösterilecek.")
work_hours = st.number_input("Çalışma Saati (Maksimum 11 saat)", min_value=0.0, max_value=11.0, step=0.5, help="Bu log için çalıştığınız saat.")
body = st.text_area("Log Açıklaması", placeholder="Loglarınızı buraya yazın")
additional_note = st.text_area("Ek Açıklama", placeholder="Ek açıklama girin (isteğe bağlı).")

# Girdi doğrulama fonksiyonu
def validate_inputs(sender_email, sender_password, subject, body, recipient_input, work_hours):
    errors = []
    if not sender_email: 
        errors.append("Gönderici e-posta adresi boş olamaz.")
    if not sender_password:
        errors.append("Gönderici şifre boş olamaz.")
    if not subject:
        errors.append("E-posta konusu boş olamaz.")
    if not body:
        errors.append("Log açıklaması boş olamaz.")
    if not recipient_input:
        errors.append("Alıcı e-posta adresleri boş olamaz.")
    if work_hours <= 0:
        errors.append("Çalışma saati 0 veya negatif olamaz.")
    if work_hours > 11:
        errors.append("Maksimum 11 saat çalışabilirsiniz. Eğer daha fazla çalıştıysanız, loglarınızı diğer günlere bölerek ekleyiniz.")
    return errors

# E-posta gönderim işlemi
def process_email_sending():
    recipient_list = [email.strip() for email in recipient_input.split(",")]
    full_body = f"📅 Log Tarihi: {selected_date}\n"
    full_body += f"⏳ Çalışma Saati: {work_hours} saat\n\n{body}"
    if additional_note:
        full_body += f"\n\n📝 Ek Açıklama:\n{additional_note}"
    return send_email(sender_email, sender_password, subject, full_body, recipient_list)

# Gönderim butonu
if st.button("Gönder"):
    validation_errors = validate_inputs(sender_email, sender_password, subject, body, recipient_input, work_hours)
    if validation_errors:
        for error in validation_errors:
            st.error(error)
    else:
        result = process_email_sending()
        if "başarıyla" in result:
            st.success(result)
        else:
            st.error(result)

# E-posta silme işlemi
st.subheader("E-posta Sil")
if st.session_state.email_list:
    email_to_remove = st.selectbox(
        "Silmek için bir e-posta seçin",
        st.session_state.email_list
    )
    if st.button("Sil"):
        st.session_state.email_list.remove(email_to_remove)
        st.success(f"{email_to_remove} e-posta listesinden silindi!")