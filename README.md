##    Python Arabic Reshaper
Reconstruct Arabic sentences to be used in applications that don't support Arabic

Based on [Better Arabic Reshaper](https://github.com/agawish/Better-Arabic-Reshaper/), ported to Python, tweaked a little bit.

For more info visit my blog [post here](http://mpcabd.xyz/python-arabic-text-reshaper/)

## Known Issue
[Harakat or Tashkeel](http://en.wikipedia.org/wiki/Arabic_diacritics#Tashkil_.28marks_used_as_phonetic_guides.29) are not supported, and I think that they can't be supported as their unicode characters are non-spacing marks (i.e. they don't take space, they are rendered in the same space of the character before them), which means that when used in a reshaper, they will be rendered on the next character as the text is reversed.

##    License
This work is licensed under [GNU General Public License v3](http://www.gnu.org/licenses/gpl.txt).

##    Demo
*    Online Arabic Reshaper: http://pydj.igeex.biz/arabic-reshaper/

##    Download
*    Source Code:  	https://github.com/mpcabd/python-arabic-reshaper/tarball/master

##    Contact
*    Abd Allah Diab (mpcabd)
*    Email: 	mpcabd {AT} G Mail (dot) COM
*    Blog:	http://mpcabd.xyz
