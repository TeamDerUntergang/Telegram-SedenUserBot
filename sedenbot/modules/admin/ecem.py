# Copyright (C) 2020-2024 TeamDerUntergang <https://github.com/TeamDerUntergang>
#
# This file is part of TeamDerUntergang project,
# and licensed under GNU Affero General Public License v3.
# See the GNU Affero General Public License for more details.
#
# All rights reserved. See COPYING, AUTHORS.
#

from random import choice

from sedenbot import HELP
from sedenecem.core import edit, get_translation, sedenify

# ================= CONSTANT =================
ECEM_STRINGS = [
    "Çocukluk aşkımsın",
    "Erkek arkadaşlarımın arkadaşlarının adlarını bilmem normal bir şey",
    "Şu an acele işim var, daha sonra çekilsek olmaz mı? Zaten yine geleceğim.",
    "Yok kızmadım",
    "Bunun farkına vardıysan benim için artık problem yok",
    "Bundan sonra artık hayatında Ecem diye biri yok!",
    "Yağmurlu havada sweatini veren arkadaşlarınız olsun 👅",
    "Yalnız çiçek açar mısın? Yalnız, çiçek.",
    "Affetmiyorum, annemi çağıracağım. O gereğini yapacak.",
    "Saçımla oynama",
    "Saçımla oynamamanı söylediğim halde oynuyorsun. Arkamdan git lütfen.",
    "Ben gelmiyorum bedene falan, kenarda ölmeyi bekleyeceğim",
    "Düşman değiliz sadece onun olduğu yerde rahat edemem",
    "Git arkamdan, istemiyorum seni",
    "Murat Boz şarkıları beni hiç eğlendirmiyor",
    "Tövbe tövbe kapatın şunu çarpılacağız",
    "Üç kızım olsun istiyorum",
    "Eğer onunla evlenirsem nikah şahidim sen ol",
    "Ehehehe çok komik, hadi defolun gidin",
    "Gidip onunla konuşsana?",
    "Ne oldu sana? Anlatmak ister misin?",
    "Lütfen anlat işte. Çok mu özel ki?",
    "Hadi gel erkeklerin yanına geçelim",
    "İyi misin?",
    "Teşekkür ederim 😊",
    "Daha sonra yine geleceğim, o zaman çekiliriz, olmaz mı?",
    "Grubu dağıtıyoruz gençler",
    "Grubu dağıtıyoruz gençler??? Ne ara dedim onu ya ben?",
    "Allah belanı vermesin",
    "Hadi yönetici sensin, dağıt grubu",
    "İyi akşamlar",
    "Her şeyi ben söylüyorum, biraz da siz söyleyin",
    "Ben onu esprisine demiştim diyette değilim",
    "Sizde var mı bilmiyorum sorim dedim birkaç kişiye daha sordum, çıktı alabilme şansın var mı?",
    "Üçgende çıkmış sorular, 3. site",
    "Eğer olmadıysa gerek kalmadı",
    "Yok yani, ben buldum birinden",
    "Evet evet hallettim ben sağol",
    "Atim sen de kontrol et bir, o mu diye",
    "Neyse sen çıkarttığını da getirirsin olmadı",
    "Kim ne dedi sana?",
    "Onlar benim kardeşim gibi olduğu için sahipleniyorlar",
    "Kötü bir durum yok",
    "Bir anda yapınca rahatsız oldum ama sonra sana zaten sorun yok dedim",
    "Onlar da biliyor, ondan tepki vermiştir",
    "Sorun yok yani",
    "Rica ederim",
    "Teşekkür ederim kusura bakma telefonum bozuktu yeni görebildim 😊",
    "Evet. Yalan borcum mu var size? Evet, yalan borcum mu var? Yalan borcum mu var?",
    "Ne malsın ya",
    "Testleri bitirmeyin Allah aşkına",
    "Sen mesajı silsen de bildirimde gözüküyor",
    "O ne demişti ki?",
    "Ben birine bir şey yazmştım, sonra sildim. Ne yazdın dedi, söylemedim. Sonra yazdığım şeyi bildirimden açıp bana yazdı.",
    "Mzkddkslslldldldldld",
    "Toplu olarak yapıyoruz değil mi, hiç hoş olmayan şeyler çıkmasın sonra.",
    "Lan sen konuşma",
    "Abi yalan değil ki, yetişmiyor",
    "Ya hep mi korktuğum başıma gelir ya?",
    "Bende şans olsa zaten",
    "Ben oyuna falan katılamam",
    "Tövbe, hep olmaması gereken sınıfları söylüyorsun",
    "Neyse ben konuşmuyorum sizinle zaten",
    "Ne uzattınız ya, değişmiş işte",
    "Sen sus, seninle konuşan yok",
    "Çok özledim 😔 ♥️",
    "Saygı, minnet ve özlemle",
    "Canım, dayım, her şeyim yolun açık olsun askerim ♥️",
    "#NoFilter",
    "Yorgunum ve ağrılar",
    "Sıkıldım ya, konuşun. Söz valla terslemeyeceğim.",
    "Çok kaptırmış kendini o",
    "Okul mal o zaman, o kadar yanlışla 11. olduysam",
    "Kime diyorsunuz, ben bir şey anlamadım",
    "Sen hani hastaydın Lan",
    "Sen ne diyon ya sksödödödöföfçgçgçhçhş",
    "Hiç bu kadar güldüğümü hatırlamıyorum",
    "Kaç dakika uğraştın, gerizekalı ya",
    "Lan sus sende sabahtan beri Ecem Ecem dmdkdmdmdmföfögö",
    "Evde gerizekalı gibi gülüyorum susun artık",
    "Tövbe yarabbim",
    "Üstüme gitmeyin şu saatlerde benim",
    "Sakn ol raki",
    "5 saattir anlamaya çalışıyor",
    "Yeter, gidin yatın",
    "Sus lan mal",
    "Gahahaha diye gülenin dediğine bak",
    "Yarın hiç hoş olmayacaksın",
    "Sinirliyim zaten, uğraşmayın benimle sjdkdkkdmfgm",
    "Bu arada yüzümü telefon gözükmesin diye öyle tutmuyordum sebebini bilmiyorum djjd",
    "Doğum günü kızıyım ben şşş. Nasıl bir değişiklik bekliyordunuz dkdkdk",
    "İnternetten baksana",
    "Müzik dersi hangi gün? Hocaya söz vermiştim.",
    "Hem arkamdan kaşar diyorsun, hem de kardeşim diyorsun",
    "Böyle böyle yürüyor ya ahahahahahahaha",
    "Her an'ımda",
    "BFF♥️",
    "Yine, yeni, yeniden ♥️",
    "Buraya sığdıramayacağım milyon tane iyi anımız var, hep de olsun.",
    "İyi ki doğdun kız kardeşim, seni çok seviyorum ♥️",
    "Best gün ilan ediyorum ♥️",
    "Beraber uyuyoruz ama yine de sen bilirsin sjskskksksks️",
    "Özledik be️",
    "Ula 😔",
    "Konum yeterli",
    "Yazdan kalmalarla avunmaya devam",
    "Kanka ben zaten tetikteyim ağlamak için yapma bak yanarız️",
    "Ben de çok özledim nolacak şimdi",
    "Kajsjskskskskdksksdsjjsksks istemiyom bırak beni️",
    "O olsaydı iki güldürür kendime gelirdim kafayı yicem dayanamıyorum️",
    "Hemde nasılll",
    "😔 her seferinde düşürür",
    "Yaz gelsin artıkkkkk",
    "YERİM SENİ",
    "Sen niye beni sinirlendiriyorsun 😠😠",
    "Sensin 1.55",
    "Bak aferin nasıl biliyor",
    "Gevezelik yapma sjsjkskskskskkslslsksksksklsks",
    "Güldür güldür",
    "Allah allah çok özledim bir şaşırdım",
    "Ne demek 2 yıl geçmiş",
    "Her şeyi anladım da Çin ne sjdjdkmdmxmxmmxmxkc",
    "Her yere atacam",
    "Işık bulursam 37478383 tane fotoğraf çekilirim mutlaka",
    "Aşkım olduğunu söylemiş miydim ??",
    "Ya salak mısın sjdjdkdkkdkdkdkdkd",
    "Bana bu kadar kilo aldıran hayat size neler yapmaz - '2018",
    "Hatırla çabuk",
    "Ayyyyyyy 😳 ♥️",
    "Biz bunu hangi kafayla çekilmişiz asksksksllslsldkd",
    "Asıl kesmeseydim o zaman küserdik sjskkdkdksksmdk",
    "Olay benim kilomdan buraya nasıl geldi",
    "Kanka beni bir yıldır görmüyorsun ya hani",
    "Salın artık bizi",
    "Çatalla",
    "Diyete başlıyorum konu kapanmıştır",
    "Bakılır neden olmasınn",
    "Main storyden vazgeçilmiştir",
    "Bilen bilir mutlu olduğum dönemler - işte anca 2018 -",
    "Yorum yapmıyorum artıkkk",
    "Az dalgası dönmedi şu aynanın 👅",
    "Hadi bay",
    "Aşırı aşırı aşırı özledim",
    "Hikayede kalmasın",
    "Bulduğu her yerde fotoğraf çekmeyen de ne bilim",
    "Nasıl orada havalar",
    "Sana sahip olduğum için çok şanslıyım",
    "En acilinden bu günlere geri dönebilir miyiz",
    "Buralar artık benim",
    "Seni ve uzun saçlarımı özledim 😔",
    "Sonunda kauvştuk ♥️",
    "Sizi bile özledim 😔",
    "Allahım yine çok mutluyum",
    "1 yıl önce mutluymuşum",
    "Yaaaaaa 😔 ♥️",
    "HER ŞEYİİİM ❤️💜🧡🖤💗💙💖💕💝💛💘♥💓",
    "Hikayede kalmasın serisinden devam",
    "Abi ben niye her fotoğrafta farklı çıkıyorum",
    "Benim küçük sevgilim ♥️",
    "Göz altı morluklarım ve ben bunları hak etmedik",
    "Sjskdksksjdksl gergin olmadığım tek bir saniye yok",
    "Gözlerimden yorgunluk akmadığı bir gün bile yok",
    "Yaz geri gelsin ve biz her gün içelim",
    "Köpeğin yılışıklığı yüzünden kavga ettiğimiz günlerden biri djjdjdjd",
    "Bu da senin için skskkdkdkdlskskd",
    "Ne demiş kumarda kazanan",
    "SJSKKDKSKSKSKS DÜNYANIN EN DELİ ARKADAŞLARI BENDE iyi ki varsınız ♥️♥️♥️♥️",
    "Canlarım asla normal duramazlar ♥️♥️♥️♥️",
    "Anasının kuzusuuuu",
    "Barbie değil harbi",
    "Özledim be bu zamanları",
    "9. sınıf, canım İzmir 😔 ♥️",
    "377383843. Deneme sanırım neysss bugünlük yeterr",
    "Çokçokçok özledimm",
    "Post olmaya hak kazandı",
    "Birthday baby ♥️♥️",
    "Daha haklı bir tweet görmedim",
    "Bu dediğime kendim bile inanamıyorum ama çok özlediiim ♥️♥️♥️",
    "Sanırım eski saçımı özledim",
    "10 yıl da geçse aynı espriye devamke",
    "Başladık yine",
    "Sosyal medyaya sjskskskdkkdkdkdk",
    "Bir ara ben de",
    "Yeter laaan",
    "Sjskjdkdkskskskskkskks",
    "Ben de nerde kaldın diye merak ettim",
    "Ararsın bu günleri",
    "GN",
    "gn",
    "Dünyanın en tatlı varlığı",
    "Ya hahahahahahahahaha o benim tek aşkım",
    "Hadi İzmire",
    "Buyrun Seden hanım",
    "Arkada yeni farketmem djskskskskskkssksk",
    "Okulun güzel yanı",
    "Kes önce benim mesajlarıma bak sen",
    "Sonunda kavuştuk",
    "Kuzeniz çünkü 👅😘♥",
    "Şşş",
    "Abartmaya bayılıyorsun",
    "İg",
    "BARIŞALIM ARTIK",
    "Aşkım ♥♥♥",
    "Geceden kalan",
    "Oooo kanka büyük laf soktun o nası laf sokmak",
    "Canımmsınn♥",
    "Djdkdkkd çektirenler utansın",
    "Bebeğiiiiim♥♥♥♥♥",
    "Goodnighttttt♥♥♥♥♥",
    "Aşk hayatımın özeti",
    "Bağışıklık yapınca böyle oluyor",
    "Aşkımmm♥♥♥♥♥",
    "İyi gecelerrr",
    "Tecrübe konuşuyor",
    "Ben de 😔😔♥♥",
    "Sevdaaaa çiçeğiim♥♥♥",
    "Bu da senin için skskkdkdkdlskskd",
    "Ksnkskzksls ♥♥♥♥",
    "Hasta ve yorgun",
    "Ksjsksksksksks",
    "Canlarımmm♥♥♥♥",
    "Msmsksks",
    "Bir konserimiz daha yok mu ama",
    "Aşkımaşkımm♥♥",
    "Aynen",
    "Ya defol git djdkdmfmgöögmdmdmdmd",
    "Lan tamam bin pişman ettiniz ya sjskdkkskskslsmskldmdlddk",
    "Seri üzgün sjkdkdkdksls",
    "Bir oyun kazandık onu da çok gördünüz",
    "Benim sayemde",
    "Bütün maçları bana sorup oynuyon sonra bir de benim privimde artisli yapıyorsun ",
    "Ksksksksksksksksks",
    "SHJSJSKDKDKSKDK",
    "Yeter uyuyun hadi dersiniz var sabah",
    "kdkdkdkdkdkdmdmdmdm lan sınıfta öksürmekten canım çıktı bu kadarı da fazla sjskkfksks",
    "Tamam",
    "Sjkdkdkdkdlskdkxkdkdkdld şela en son bir kus istersen demişti ama yine de sen bilirsin",
    "SJDKFKLGLDKDKDLSLDKDKDKDLDLDLLD",
    "Toplu igg",
    "Hatırım kalır",
    "Bir dahakine kafamı kırmayın ama",
    "NSSNMDMDMDMSMSMDM",
    "Nsnsmsmdmdmdmskkdms",
    "İyi kiii♥♥♥♥",
    "Senin sesin yüzünden sesi kapalı attım haykırmışsın arkadaş gibi arkadaş kskskskskkdmsksmsmsmmdmddk",
    "Dağa taşa yazacan yakında bir olsaydık şu sınavı skskdkdkksksks",
    "Düşünsene yarın hoca sayıları değiştiriyor",
    "Kalırım sjjdjfjdkskskdkdkdkkdksks",
    "Olay beraber okumak değilmiş abi beraber geçirdiğimiz ortammış",
    "Skskskksks sadece bunlar var elimdee ♥♥",
    "Kordonun dili olsa da konuşsa",
    "Bende serisi var sjsjskdmmsksks",
    "Abartttttt",
    "Babuş açı iyi bir de biz de zayıftık bir zamanlar",
    "Tabi koçç",
    "Yuh 2 sene önceydi o",
    "Aslan 2 ay sonra barıştık biz onun üzerinden",
    "Djdjdkkdkdkdkd çünkü o Seden",
    "Uğraşmaaa",
    "Yayaya♥♥♥",
    "Birthday baby♥♥ -acil fotoğraf @sedenogen",
    "Sjsjdjjsksksks özlediğime değil ÇOK özlediğime",
    "Yaaaaa",
    "Deme bak gider boyatırım",
    "Sen kesinlikle benim ilerideki çocuğumsun",
    "Ayyyyyyy♥♥",
    "Bu fotoğrafta çöktüğümü fark etmişimdir",
    "Current mood: DAY OFF!",
    "Sıkıntıdan patlamama ramak kaldı",
    "Bir bihter ziyagil değildik ama biz de çok acı çektik sjjsjsjskd",
    "Efektten bıkana kadar devam",
    "Şov başlasın dedi",
    "Bir pijamamı bir de seni♥",
    "Yeni yıla evde tek başına girmek mi 0/10",
    "Seri yorgun",
    "10/10",
    "Black is my favorite color",
    "Çok şükür bugün de yorgunluktan öldük",
    "Best couple",
    "İggg♥",
    "Definitely Tired",
    "Good night",
    "Saç kestirmek net pişmanlıktır",
    "Güne puanım 0",
    "Teyzoşuuuum♥",
    "Aşşkııım♥♥♥",
    "Sensin en güzelllll♥♥♥",
    "Bebeğiiim♥",
    "Bir kere ya bir kere güzel bir şey at",
    "Canımm♥",
    "Aşkımmm♥",
    "Ben de seni çokk seviyorum birtanem♥",
    "Emoji yanlış oldu sanırım 👅 ♥",
    "Teşekkürler ♥",
    "Birtanemm♥",
    "Hem de çokk♥",
    "En özell♥",
    "Balll♥",
    "Seviyorum seniii♥",
    "Psikolojik tedavi için dm",
    "Çözüyormuş gibi çek knk",
    "Yalan söyleme dakika sayıyordun bitsin diye",
    "Seninle arkada marş söyleyip çerez yemeği özledim",
    "Gözümü galatasaray marşıyla açıyordum sjsjdkdkdkkdkd",
    "Aferin böyle yola gel sjskkfskdkfdkkdkddk",
    "Gn priv ailemm♥️♥️♥️",
    "Uyumuyorum çaktırma sjskkskdkdkd",
    "Kara gözlüm ölesim var",
    "Bu bağlantıyı kimse anlamayacak sjsksksksksk",
    "Yapma yanarız",
    "skamaksksksksksks",
    "inşallahh bence de görelim artık",
    "hem de nasılllll",
    "Konumumuz belli",
    "Herkes böyle bacı bulamaz şanslıyım tabi 👅 ♥️♥️♥️♥️",
    "En değerlilerim misiniz nesinizz????",
    "😳♥️♥️",
    "Pardon da neyin var acabaaa",
    "Bebekkkk gibisin aşkımm",
    "Şşş sus yoksa inanırım",
    "İyi geceler canlarım️♥♥♥",
    "Sizi seveni üzün, düzene uyun",
    "Tanıyamadım",
    "Hangi sınıf",
    "Okuldan kimse takip etmiyor?",
    "12 dahil takip ettiğim kişiler var",
    "Ama seninle hiçbiri takipleşmiyor",
    "Kavuştukkkk♥",
    "Kuzucuğumla💘",
    "Bu özlemin tarifi yok♥",
    "Mood.",
    "Sondaki gülüşe düşmeyen de ne bilim",
    "Herkes bu kadar bencil olmak zorunda mı?",
    "❔",
    "Bekle dedi gitti 👅♥",
    "Bu da burda kalsın",
    "SENİİİN👅",
    "Aşşşşşkkıım",
    "💗💗",
    "Ah Seden'im... küçük civcivim",
    "💓💓💓💓",
    "Özlemini tişörtünle gideriyorum.",
    "Sus ya sen çok farklısın sanki",
    "Seden'e derdimi anlatıyorumdur. Seden:",
    "Canımın içiiiii 💙",
    "😘😘",
    "Anlık sinir krizleri geçirildi",
    "Çevrimiçi olup olmadığımızı test ediyoruzdur #whatsapp yaktın bizi",
    "Djjdkdkmdöödööd",
    "Ben almadım Seden almış",
    "Hocam lütfen bir sonraki dersimize olsun",
    "Biraz da şerefsiz arkadaşlarımızı paylaşalım ♥️♥️♥️♥️",
    "sadece Doğum günümde yazıyorsunuz",
    "Yalansa yalan de djjdjdkdkksks",
    "👅♥️♥️♥️",
    "SJSJJDJDKSKSKSKKSKSKDK yok artık hala mı",
    "Bütün okul anladı @CiyanogenOneTeams ona yâr olmayacağımı anlamadı Jsjsjdkskskskskskl",
    "KSKDKDKDKDKSKKSKDKDKKD",
    "LAN HATIRLATMA sjjdjdjdkdkdkdkdk bir fotoğraf çekilelim mi NE SJSKSKSKSK",
    "Yemin ederim daha fazla sevenini görmedim jdjdkdkdkd",
]
# ================= CONSTANT =================
'''Copyright (c) @Sedenogen | 2020'''


@sedenify(pattern='^.ecem$')
def ecemify(message):
    ecem(message)


def ecem(message):
    # Ecem'in sözlüğü
    edit(message, choice(ECEM_STRINGS))


HELP.update({'ecem': get_translation('ecemInfo')})
