## Python Arabic Reshaper
Reconstruct Arabic sentences to be used in applications that don't support Arabic

Based on [Better Arabic Reshaper](https://github.com/agawish/Better-Arabic-Reshaper/), ported to Python, tweaked a little bit.

Arabic is a very special script language with two essential features:

1. It is written from right to left.
2. The characters change shape according to their surrounding characters.

So when you try to print Arabic text in an application – or a library – that doesn’t support Arabic you’re pretty likely to end up with something that looks like this:

![Arabic text written from left to right with no reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-1.png)

We have two problems here, first, the characters are in the isolated form, which means that every character is rendered regardless of its surroundings, and second is that the text is written from left to right.

To solve the latter issue all we have to do is to use the [Unicode bidirectional algorithm](http://unicode.org/reports/tr9/), which is implemented purely in Python in [python-bidi](https://github.com/MeirKriheli/python-bidi). If you use it you’ll end up with something that looks like this:

![Arabic text written from right to left with no reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-6.png)

The only issue left to solve is to reshape those characters and replace them with their correct shapes according to their surroundings. Using this library helps with the reshaping so we can get the proper result like this:

![Arabic text written from right to left with reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-3.png)

## Usage

```
import arabic_reshaper
from bidi.algorithm import get_display
 
#...
reshaped_text = arabic_reshaper.reshape(u'اللغة العربية رائعة')
bidi_text = get_display(reshaped_text)
pass_arabic_text_to_render(bidi_text)
#...
```

The `pass_arabic_text_to_render` function here is an imaginary function, it is just here to say that the variable `bidi_text` is the variable that you would need to use in your code afterwards, for example to print it in PDF, or to write it in an Image, etc.

For more info visit my blog [post here](http://mpcabd.xyz/python-arabic-text-reshaper/)

## Known Issue

[Harakat or Tashkeel](http://en.wikipedia.org/wiki/Arabic_diacritics#Tashkil_.28marks_used_as_phonetic_guides.29) are not supported, and I think that they can't be supported as their unicode characters are non-spacing marks (i.e. they don't take space, they are rendered in the same space of the character before them), which means that when used in a reshaper, they will be rendered on the next character as the text is reversed.

## License

This work is licensed under [GNU General Public License v3](http://www.gnu.org/licenses/gpl.txt).

## Demo

Online Arabic Reshaper: http://pydj.igeex.biz/arabic-reshaper/

## Download

https://github.com/mpcabd/python-arabic-reshaper/tarball/master

## Contact

Abdullah Diab (mpcabd)
Email: 	mpcabd@gmail.com
Blog:	http://mpcabd.xyz
