# Text-editor
### *Zero step: install python3 and create spec folder for our project installation*
##### download python from offical web site [python.org](https://www.python.org/)
#### *First step: download or clone our code from github repository*
```console
git clone https://github.com/EtherDaler/Text-editor.git
```
#### *Intermediate step: create virtual environment*
```console
foo@bar:~$ pip install virtualenv
foo@bar:~$ virtualenv myvenv
foo@bar:~$ source myvenv\bin\activate
```
#### *Second step: install requirements.txt*
```console
(myvenv)foo@bar:~$ pip install requirements.txt
```
#### *Third step: run command*
```console
(myvenv)foo@bar:~$ python3 main.py
```
#### *Finally: enjoy our text-editor!*

### How to use Text-editor:

If you run it you will see a new clear file you can write in it smth.  
![new file](./static/images/new_file.png)  
Then, if you press ctr + s file will be save in the text-editor work directory
named 'Untitled*'.txt  
  
![Untitled.txt in code catalog](./static/images/untitled.png)  
  
Although you can use menu bar at the top of the editor it can help you to
save file in another directory.  
![open](./static/images/save_as.png)  
![open](./static/images/saving_as.png)  
  
By the way, you can open another files in your computer and work with it.
You can do it with command 'open file', wich stayed in the menu bar.  
![open](./static/images/open.png)  
![open](./static/images/openning.png) 
  
### Hot Keys:

ctr + a - выделить все  
ctr + s - сохраняет файл  
ctr + q - выход  
ctr + f - поиск  
ctr + r - замена слов