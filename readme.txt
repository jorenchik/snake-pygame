UZDEVUMA CHEKLIST

[spēle sākas no faila main.py]
[iestatījumus maina ar ENTER vai bultiņām]

1)Izlasi nosacījumus un izvēlies gana lielu laukumu spēles izveidei – laukums 1920x1080px^2

2)Min laukums 20x30 lauciņi, lauciņiem jābūt gana lieliem,
lai bez problēmām visi visu varētu saskatīt un spēle ielīstu FullHD ekrānā – laukums ir 30x20

3)Masīvs čūskiņas koordinātēm, 0tais elements jau eksistē,
tālāk ar append pievieno jaunus lauciņus čūskas garumam
var būt x[ ] un y [ ] vai snake [ ], kur katrā saglabā x un y - 
sākumā tiek izveidoti 2 SnakePart klases objekti ar x un y koordinātām kā attiecīgā objekta lauki

4)pygame.draw.rect() ļaus uzzīmēt kvadrātiņu, bet droši drīkst arī ar bildītēm -
čuska realizēta no bildītēm, tāpēc draw.rect() šim nolūkam nebija izmantots

5)Spiežot virzienu pagriežas čūskiņa, poga nav jātur piespiesta, lai tā pārvietotos. čūska nevar iet pati sev pa virsu.- 
bultiņas un wasd maina 1. un 2. spēlētāja čūskas virzienu attiecīgi, čūska nevar iet ne sev,
ne citai spēlētāja čūskai pa virsu, čūskas turpina kustību pastāvīgi

6)Ēdiena x un y koordināte, ēdiena koordinātes veidojas random -nedrīkst veidoties virsū čūskai!-
 jebkurš jauns objekts, kas parādās spēles laukumā, nevar parādīties aizņemtajā vietā,
 jauni ēdieni parādās pieejamās random pozīcijās

7)Apēdot ēdienu tiek skaitīti punkti. Ja čūska ieskrien pati sevī, spēle beidzas –
 tiek pieskaitīti 10 punkti, ja ir apēsts ēdiens, un atskaitīti 10 punkti indīga ēdiena
  apēšanas gadījumā, ja ir vairāk par 2 daļām čūskai, Game Over ekrāns parādās zaudēšanas gadījumā

8)Jābūt iespējai sākt jaunu spēli - jaunu spēli pēc tās beigām var uzsākt,
sekojot norādēm Game Over ekrānā

9)Spēli atverot jābūt iespējai norādīt vai būs 1 vai 2 spēlētāji - 
settings->mode (1 player/2 players)

10)1.spēlētājs wasd 2.spēlētājs bultiņas -  2 player režīmā

11)Spēli atverot spēlētājs var izvēlēties krāsu - zils vai violets -
settings->player 1 color/player 2 color (otrais parādās tikai 2 player režīmā)

12)gadījumā, ja ir 2 spēlētāji, krāsas nedrīkst atkārtoties -
nevar izvēlēties divas vienādas krāsas  spēlētājiem

13)Spēles sākumā jābūt izvēlei vai čūska var iziet cauri sienai vai nē - settings->portal mode

14)Spēles sākumā jābūt izvēlei ātrumam un vai ātrums palielināsies pēc katra apēstā gabala –
settings->initial speed (no 1 līdz 7) un settings->speed increase after eating

15)Ēdienam ir jābūt zaļam vai tml krāsai – ēdiens ir zaļš

16)Indīgajiem ēdieniem jābūt sarkaniem - indīgs ēdiens ir sarkans
pēdējie 10%:

17)3% par ēdiena un indes un sienām kā bildei – ēdiens, indīgs ēdiens un sienas veidotas no bildēm

18)4% par čūskiņu no bildītēm - čūskas bildītes - galva, ķermenis, aste

19)3% scoreboard ar ierakstāmu vārdu - ja kāds no spēlētājiem iegūst vairāk par 0 punktiem,
var ierakstīt vārdu scoreboard, rezultāti saglabājas failā,
kurus var apskatīties scoreboard sadaļā, kurā var tikt caur izvēlni