# vimeo-get
Scripts pour aider à la récupération de fichiers avec un hébergement de style Vimeo ("master.json") ou streaming ("master.m3u").  

Si vous recherchez quelque chose de bien plus complet, orientez vous directement vers [youtube-dl](https://github.com/ytdl-org/youtube-dl) qui, comme son nom ne l'indique pas, permet de récupérer des flux de plein de plateformes.  


## vimeo_get
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


## m3u_master_get
Ce script télécharge et concatène les fichiers présents dans un m3u et prépare la ligne de commande FFmpeg qui encapsulera correctement le fichier. 
On retrouve ce type de streaming un peu partout (Audible, France TV, ...).
### Utilisation
```
python m3u_master_get.py <MASTER_M3U_URL> [FILE_OUT]
```
* MASTER_M3U_URL : l'URL du fichier "master.m3u" ou "master.m3u8"
* FILE_OUT : le nom du fichier de sortie. Si non renseigné, un nom au hasard sera donné. 


L'URL du fichier "master.m3u" se trouve en regardant le réseau sur la page de la vidéo lorsqu'elle a commencé à se jouer : 
![url](https://i.imgur.com/q4MTuj6.png)

Exemple :  
Pour récupérer la vidéo qui se trouve à l'URL :
```
https://ftvingest-vh.akamaihd.net/i/evt/streaming-adaptatif_france-dom-tom/2020/S14/J4/0c88132d-3183-4d81-b3b2-d68398ab339a_1585824346-h264-web-,398k,934k,1500k,2176k,.mp4.csmil/master.m3u8?audiotrack=0%3Afra%3AFrancais&hdnea=exp=1586093420~acl=%2fi%2fevt%2fstreaming-adaptatif_france-dom-tom%2f2020%2fS14%2fJ4%2f0c88132d-3183-4d81-b3b2-d68398ab339a_1585824346-h264-web-,398k,934k,1500k,2176k,.mp4.csmil*~hmac=cac37e83227d51e1ad1af23da12954ac41bf938170c5d487f679fabe046b1246
```
on exécute :
```
python m3u_master_get.py "https://ftvingest-vh.akamaihd.net/i/evt/streaming-adaptatif_france-dom-tom/2020/S14/J4/0c88132d-3183-4d81-b3b2-d68398ab339a_1585824346-h264-web-,398k,934k,1500k,2176k,.mp4.csmil/master.m3u8?audiotrack=0%3Afra%3AFrancais&hdnea=exp=1586093420~acl=%2fi%2fevt%2fstreaming-adaptatif_france-dom-tom%2f2020%2fS14%2fJ4%2f0c88132d-3183-4d81-b3b2-d68398ab339a_1585824346-h264-web-,398k,934k,1500k,2176k,.mp4.csmil*~hmac=cac37e83227d51e1ad1af23da12954ac41bf938170c5d487f679fabe046b1246"
```
Le script demandera quel flux on souhaite récupérer :  
![video](https://i.imgur.com/ZgT1SRA.png)
Il faut saisir l'identifiant du flux souhaité (ici "1", "2", "3" ou "4") ou "S" si on ne souhaite pas récupérer de flux. 

Le script téléchargera le flux sélectionné, puis retournera la commande à utliser pour l'encapsuler dans un meilleur container (surtout utile quand le fichier de sortie est un ".ts") : 
```
Done!

You can clean your file with:
ffmpeg -i "tmp/20200405_153608_1.ts" -map 0 -c copy "tmp/20200405_153608_1.mkv"
```



## m3u_get
Ce script télécharge et concatène les fichiers présents dans un m3u et prépare la ligne de commande FFmpeg qui encapsulera correctement le fichier.  
La différence avec `m3u_master_get.py`, c'est qu'il prend directement l'URL d'un m3u final (et non pas un m3u qui contient une liste de m3u).  
On retrouve ce type de streaming un peu partout (Audible, France TV, ...).  
### Utilisation en ligne de commande
```
python m3u_get.py <M3U_URL> [FILE_OUT]
```
* M3U_URL : l'URL du fichier ".m3u" ou ".m3u8"
* FILE_OUT : le nom du fichier de sortie. Si non renseigné, un nom au hasard sera donné. 


L'URL du fichier ".m3u" se trouve en regardant le réseau sur la page de la vidéo lorsqu'elle a commencé à se jouer : 
![url](https://i.imgur.com/q4MTuj6.png)
  
Le script téléchargera le flux, puis retournera la commande à utliser pour l'encapsuler dans un meilleur container (surtout utile quand le fichier de sortie est un ".ts") : 
```
Done!

You can clean your file with:
ffmpeg -i "tmp/20200405_153608_1.ts" -map 0 -c copy "tmp/20200405_153608_1.mkv"
```
  
  
### Utilisation en mode interactif
Il est possible d'utiliser le script en mode interactif si on l'appelle sans aucun argument.  
L'outil demandera alors l'URL du m3u ainsi que le nom du fichier de destination.  
Il proposera aussi d'exécuter la commande de nettoyage du fichier.  
  
  
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
