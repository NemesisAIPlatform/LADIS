## 🎉 Felicitari (inca o data) pentru proiectul vostru ! 🚀🔥
Sper ca ati ajuns cu bine acasa.
Dupa cum am discutat @AFT va las aici un exemplu simplu de AI detection + tracking pentru "face"

#### Instructiuni de folosire:
- Git clone ...
- Copiati fisierele pe Rpi5 (sau puteti rula pe computerul vostru)
- Pentru instalare de dependinte puteti rula: `pip install -r requirements.txt`
- Ca sa rulati programul: `python3 detect_ai.py`

Note: 
`detect_ai.py` citeste camera de la index 0. Modificati daca aveti alta camera.
Pentru alte tipuri de tinte se inlocuieste fisierul `yolo12n...` (care este reteaua neuronala) cu alta retea pregatita/antrenata pentru alta tinta.
Daca aveti NVidia pe laptop puteti incerca sa inlocuiti `DetectAI("yolov12n-face_ncnn_model")` cu `DetectAI("yolov12n-face.pt")`
Daca aveti intrebari putem face un call si/sau puteti deschide 'Issue' aici si discutam.


BAFTA !

