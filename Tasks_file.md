# Szkielet aplikacji

## Centralna aplikacja CLI

[-] GEN.MGMT.1 Opracować aplikację w języku Python z interfejsem CLI, która pozwoli na realizację
wskazanych wymagań. Moduł do tworzenia aplikacji CLI 

[-] GEN.MGMT.2 Aplikacja działa w trybie CLI z wypisywaniem akcji.

[-] GEN.MGMG.2.1 Automatycznie tworzony jest log z działania o nazwie składającej się z nazwy aplikacji
oraz znacznika czasu jej uruchomienia.

[-] GEN.MGMT.2.2 Efekty operacji są wypisywane jednocześnie na CLI oraz do otwartego pliku loga.

[-] GEN.MGMT.3 Aplikacja ma możliwość wskazania pojedynczych plików, folderu lub grupy folderów do
przeszukania w poszukiwaniu plików, które mają być wykorzystane do analizy

[-] GEN.MGMT.4 Obsługiwane formaty wejściowe plików do analizy:  
[-] pliki tekstowe w formatach .txt , .xml , .json  
[-] pliki ze zrzutami ruchu PCAP .pcap  
[-] pliki logów Sysmon Windows EVTX - .evtx   
[-] przetwarzane na format tekstowy JSON, XML lub
innych tekstowy (do wyboru według własnego uznania)

[-] GEN.MGMT.5 Wprowadzić komunikację ze zdalnym loggerem alertów.

[-] GEN.MGMT.5.1 Metodą komunikacji aplikacji głównej z loggerem alertów jest REST API.

[-] GEN.MGMT.6 Wprowadzić tryb zarządzania zdalnym agentem na potrzeby analizy online.

[-] GEN.MGMT.6.1 Metodą komunikacji aplikacji głównej z agentem jest REST API.

## Zdalny Logger Alertów

[-] GEN.LOG.1 Przygotować aplikację CLI (nie musi być oparta na Click jak w Wymaganiu
GEN.MGMT.1 ) do odbierania wiadomości po REST API i wypisywaniu ich na CLI - alert.


## Zdalny Agent

[-] GEN.AGT.1 Przygotować aplikację CLI (nie musi być oparta na Click jak w Wymaganiu
GEN.MGMT.1 ) realizującą funkcję zdalnego agenta.

[-] GEN.AGT.1.2 Aplikacja agenta ma realizować stronę zdalną dla wymagań ON.REM.1-1.2 ,
ON.REM.2-2.2 oraz ON.REM.3-3.2 .

# Scenariusze operacyjne 

## Analiza plików offline - PCAP

[-] OFF.PCAP.1 Aplikacja ma możliwość wyświetlania zawartości pakietów z wczytanych plików PCAP.

[-] OFF.PCAP.2 Aplikacja ma możliwość przekazania filtru zgodnego z formatem BPF
(wykorzystywanego przez libpcap / tshark / pyshark / Wireshark / Scapy ) do funkcji otwierającej i
wczytującej plik PCAP.


## Analiza plików offline TXT/Log

[-] OFF.LOG.1 Aplikacja ma możliwość wywołania operacji systemowej grep na wskazanych plikach
tekstowych. Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne.

[-] OFF.LOG.2 Aplikacja ma możliwość wywołania działania wyrażenia regularnego z modułu Python
re na wskazanych plikach tekstowych lub EVTX przetworzonych do formatu JSON/XML/inny
tekstowy. Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne.

##  Reguły analityczne jako funkcje języka Python

[-] OFF.DETPY.1 Aplikacja ma możliwość załadowania reguł analitycznych do detekcji zdarzeń
opisanych za pomocą tych reguł i przechowywania ich w wybranej strukturze danych. Każdorazowe
wywołanie ładowania reguł ma oznaczać usunięcie istniejących w pamięci programu i załadowanie
nowego zestawu reguł.

[-] OFF.DETPY.1.1 Reguły będą opisywane jako funkcje Pythona w pliku detection-rules.py (nazwa
na sztywno)

[-] OFF.DETPY.1.2 Każda reguła ma być zdefiniowana jako oddzielna funkcja w języku Python we
wskazanym pliku w OFF.DETPY.1.1 . Format pojedynczej reguły

[-] OFF.DETPY.1.3 Informacjami zwrotnymi z reguły są:  
[-] action_alert - jedna z dwóch akcji alertujących z grupy: local, remote  
[-] description - opis tekstowy według przyjętego formatu, może to być także JSON, XML czy
syslog.

[-] OFF.DETPY.2 Interfejs wywołania reguł analitycznych umożliwia ich użycie w dwóch trybach:

[-] OFF.DETPY.2.1 Wywołanie całego zestawu reguł na wybranym zestawie plików

[-] OFF.DETPY.2.2 Wywołanie wybranej reguły - poprzez wskazanie jej nazwy (nazwa funkcji z

[-] OFF.DETPY.1.2 ) - i na wybranym zestawie plików przekazanym do reguły

## Zarządzanie zdalnymi operacjami cyberbezpieczeństwa

[-] ON.REM.1 Aplikacja ma możliwość wskazania akcji i wykonania jej na zdalnym agencie w zakresie
przechwytywania ruchu sieciowego do pliku PCAP

[-] ON.REM.1.1 Pobierz informację o konfiguracji sieciowej zdalnego hosta.

[-] ON.REM.1.2 Zbierz plik PCAP ze wskazanymi parametrami: nazwa interfejsu, czas zbierania.
Przekazać za pomocą JSON konfigurację zbierania. Plik po zebraniu ma być transferowany na host
głównej aplikacji

[-] ON.REM.2 Aplikacja ma możliwość wskazania akcji i wykonania jej na zdalnym agencie w zakresie
zarządzania plikami logów

[-] ON.REM.2.1 Pobieraj listę plików logów na zdalnym hoście z agentem.

[-] ON.REM.2.2 Pobierz wskazany plik lub grupę plików logów ze zdalnego hosta z agentem.

[-] ON.REM.3 Aplikacja centralna ma możliwość wykonania polecenia powłoki systemowej na zdalnym
agencie.

[-] ON.REM.3.1 Zdefiniowanie komendy powłoki systemowej do wykonania na zdalnym hoście

[-] ON.REM.3.2 Przekazanie tej komendy do wykonania na zdalnym hoście i odebranie odpowiedzi.

## Wykorzystanie uniwersalnego formatu reguł - SIGMA

[-] REG.DET.1 W ramach środowiska stworzonej aplikacji należy zintegrować rozwiązanie do detekcji z
wykorzystaniem reguł SIGMA.

[-] REG.DET.1.1 Silnik dla reguł SIGMA w języku Python: https://github.com/wagga40/Zircolite

[-] REG.DET.1.2 Integracja taka może opierać się na wskazaniu pojedynczej reguły lub zestawu reguł.
Poza samą detekcją należy pamiętać o integracji związanej prezentacją alertu.

[-] REG.DET.2 Przetestować zintegrowane rozwiązanie dla reguł SIGMA.

[-] REG.DET.2.1 Wykonać na wybranym zestawie danych EVTX/JSON względem znanej reguły SIGMA
dla tego zestawu danych (szukać w podanych źródłach i w Internecie). Można też okroić regułę
SIGMA, aby na posiadanych danych zademonstrować działanie detekcji.