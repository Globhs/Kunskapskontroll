# Person Counter

En person-räknare som använder YOLOv8 för att detektera och spåra personer i videoströmmar. Programmet räknar automatiskt hur många personer som passerar en fördefinierad linje i videon.

## Funktionalitet

- **Persondetektion**: Använder YOLOv8 (nano-modell) för att detektera personer i videostream
- **Personspårning**: Spårar individers rörelse mellan frames med unika ID:n
- **Räkning**: Räknar personer som passerar en horisontell linje
- **Visualisering**: Visar:
  - Bounding boxes omkring detekterade personer
  - Unikt ID för varje person
  - Räkningslinje
  - Totalt antal personer som passerat linjen

## Förkunskaper/Installation

### Systemkrav
- Python 3.8 eller senare
- Webcam eller videofil

### Installera dependencies
```bash
pip install -r requirements.txt
```

Detta installerar:
- `opencv-python` - För videobehandling
- `ultralytics` - För YOLOv8-modellen

## Konfiguration

Öppna `config.py` och justera följande inställningar enligt dina behov:

```python
MODEL_PATH = "yolov8n.pt"      # Sökväg till YOLOv8-modell
VIDEO_PATH = "Door_Test4.mp4"  # Sökväg till din videofil
LINE_Y = 350                    # Y-koordinat för räkningslinje (pixlar)
MARGIN = 0                      # Margin för räkningsmatchning
COOLDOWN_FRAMES = 10            # Antal frames innan en person kan räknas igen
CONFIDENCE = 0.4                # Konfidenströskle för detektioner (0.0-1.0)
```

### Konfigurationsparametrar förklarade

- **MODEL_PATH**: Sökväg till den förtränade YOLOv8-modellen. Modellen laddas ned automatiskt vid första körning.
- **VIDEO_PATH**: Sökväg till din videofil (stöder mp4, avi, mov, etc.) eller webcam (använd `0` för webcam)
- **LINE_Y**: Y-koordinaten för den horisontella linje där personer räknas. Justera detta värde baserat på din videohöjd.
- **CONFIDENCE**: Lägre värde = fler detektioner men mer falskt positiva. Höga värden = färre men säkrare detektioner.

## Hur man kör programmet

### Från terminal/kommandotolken

```bash
cd path/to/person-counter
python main.py
```

### Avsluta programmet

Tryck på **Q** för att avsluta programmet.

## Programstruktur

- **main.py**: Huvudprogrammet som kör hela pipeline
- **config.py**: Konfigurationsfil med parametrar
- **detector.py**: YOLOv8-detektion av personer
- **tracker.py**: Spårning av personer mellan frames
- **counter.py**: Logik för räkning av personer
- **person_identification.py**: ID-tilldelning och spårning av individer
- **yolov8n.pt**: Förtränad YOLOv8 nano-modell (laddas ned automatiskt)

## Felsökning

### Programmet är långsamt
- Minska videoupplösningen
- Öka `COOLDOWN_FRAMES` för snabbare bearbetning
- Använd en mer kraftfull GPU om tillgänglig

### För många falskt positiva detektioner
- Öka värdet på `CONFIDENCE` (t.ex. från 0.4 till 0.6)

### Linjen är på fel plats
- Justera `LINE_Y` i config.py (öka för lägre på skärmen, minska för högre)

### Modellen laddas inte
- Kontrollera internetanslutningen (modellen laddas ned från Ultralytics)
- Se till att `yolov8n.pt` finns i mappen eller att internetanslutningen fungerar

## Licens

Projektet använder YOLOv8 från Ultralytics (licens: AGPL-3.0)
