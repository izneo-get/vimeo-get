# vimeo-get
Scripts pour aider à la récupération de fichiers avec un hébergement de style Vimeo.


## vimeo-get
Ce script télécharge les parties audio et vidéo d'une vidéo de type Vimeo et prépare la ligne de commande FFmpeg qui fera la fusion des deux.
### Utilisation
```
python vimeo_get.py <MASTER_JSON_URL>
```
* MASTER_JSON_URL : l'URL du fichier "master.json"


L'URL du fichier "master.json" se trouve en regardant le réseau sur la page de la vidéo lorsqu'elle a commencé à se jouer : 
![url](https://i.imgur.com/HfmuM7P.png)

Exemple :  
Pour récupérer la vidéo qui se trouve à l'URL :
```
https://72vod-adaptive.akamaized.net/exp=1586026074~acl=%2F76979871%2F%2A~hmac=8be6837340fa8b9cfaeb45cead4a837c90324a975dfce02e34090c85a83ca62b/76979871/sep/video/468975811,449262797,449260574,449260571/master.json?base64_init=1
```
on exécute :
```
python vimeo_get.py "https://72vod-adaptive.akamaized.net/exp=1586026074~acl=%2F76979871%2F%2A~hmac=8be6837340fa8b9cfaeb45cead4a837c90324a975dfce02e34090c85a83ca62b/76979871/sep/video/468975811,449262797,449260574,449260571/master.json?base64_init=1"
```
Le script demandera quel flux vidéo on souhaite récupérer :  
![video](https://i.imgur.com/kP00VDC.png)
Il faut saisir l'identifiant du flux souhaité (ici "1", "2", "3" ou "4") ou "S" si on ne souhaite pas récupérer de flux vidéo. 

Le script demandera quel flux audio on souhaite récupérer :  
![audio](https://i.imgur.com/i6wAehD.png)
Il faut saisir l'identifiant du flux souhaité (ici "5" ou "6") ou "S" si on ne souhaite pas récupérer de flux audio. 

Le script téléchargera les flux sélectionnés, puis retournera la commande à utliser pour faire le merge : 
```
ffmpeg -i "c:\Python\vimeo-get/tmp/1_468975811_video_mp4.tmp" -i "c:\Python\vimeo-get/DOWNLOADS/5_449260574_audio_mp4.tmp" -c copy output.mkv
```



## Installation
### Prérequis
- Python 3.7+ (non testé avec les versions précédentes)
- pip
- Librairies SSL
- (pour exécuter la commande générée) FFmpeg

#### Sous Windows
##### Python
Allez sur ce site :  
https://www.python.org/downloads/windows/  
et suivez les instructions d'installation de Python 3.

##### Pip
- Téléchargez [get-pip.py](https://bootstrap.pypa.io/get-pip.py) dans un répertoire.
- Ouvrez une ligne de commande et mettez vous dans ce répertoire.
- Entrez la commande suivante :  
```
python get-pip.py
```
- Voilà ! Pip est installé !
- Vous pouvez vérifier en tapant la commande :  
```
pip -v
```

##### Librairies SSL
- Vous pouvez essayer de les installer avec la commande :  
```
pip install pyopenssl
```
- Vous pouvez télécharger [OpenSSL pour Windows](http://gnuwin32.sourceforge.net/packages/openssl.htm). 

##### FFmpeg
- Téléchargez l'archive qui contient le fichier "ffmpeg.exe" sur le [site officiel](http://ffmpeg.org/download.html).

#### Sous Linux
Si vous êtes sous Linux, vous n'avez pas besoin de moi pour installer Python, Pip ou SSL...  

### Téléchargement
- Vous pouvez cloner le repo git :  
```
git clone https://github.com/izneo-get/vimeo-get.git
```
ou  
- Vous pouvez télécharger uniquement le binaire Windows (expérimental).  


### Configuration
(pour la version "script" uniquement)
```
pip install -r requirements.txt
```
