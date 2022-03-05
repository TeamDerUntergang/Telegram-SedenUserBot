from pydrive.auth import GoogleAuth

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
gauth.SaveCredentialsFile('creds.txt')

print(f'creds.txt Dosyası oluşturuldu.Dosyayı kontrol edin.')