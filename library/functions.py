import os, ssl, smtplib, random, string
from email.message import EmailMessage

def borrow_mail(book_name):

    email_sender = 'yunussdelibass@gmail.com'
    email_password = os.environ.get('EMAIL_PASSWORD')
    email_receiver = 'yunusdelibas@outlook.com'

    subject = 'Ödünç Kitap Alımı.....!!!'
    body = f'''
        Merhaba,
    {book_name} adlı kitabı ödünç aldınız. Mutlu günlerde okumanızı dileriz.
        100.Yıl Kütüphanesi
    '''
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

def generate_pass(length=6):
    # Define characters to choose from
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate random string
    random_string = ''.join(random.choice(characters) for _ in range(length))
    
    return random_string

# Generate a random string of 6 characters

def change_pass(user, email, new_pass):

    email_sender = 'yunussdelibass@gmail.com'
    email_password = os.environ.get('EMAIL_PASSWORD')
    #email_receiver = email
    email_receiver = 'yunusdelibas@outlook.com'

    subject = 'Şifre Değişikliği.....!!!'
    body = f'''
        Merhaba,
    {user} adlı kullanıcınızın şifresi talebiniz üzerine değiştirilmiştir.
    Yeni şifreniz: {new_pass}  
        100.Yıl Kütüphanesi
    '''
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
