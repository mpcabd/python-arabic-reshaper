## Python Arabic Reshaper
Reconstruct Arabic sentences to be used in applications that don't support
Arabic script.

Works with Python 2.x and 3.x

## Description

Arabic script is very special with two essential features:

1. It is written from right to left.
2. The characters change shape according to their surrounding characters.

So when you try to print text written in Arabic script in an application
– or a library – that doesn’t support Arabic you’re pretty likely to end up
with something that looks like this:

![Arabic text written from left to right with no reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-1.png)

We have two problems here, first, the characters are in the isolated form,
which means that every character is rendered regardless of its surroundings,
and second is that the text is written from left to right.

To solve the latter issue we had to use the
[Unicode bidirectional algorithm](http://unicode.org/reports/tr9/), which is
implemented purely in Python in
[python-bidi](https://github.com/MeirKriheli/python-bidi).
Which ended us up with something that looks like this:

![Arabic text written from right to left with no reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-6.png)

The only issue left to solve is to reshape those characters and replace them
with their correct shapes according to their surroundings. Using this library
helps with the reshaping so we can get the proper result like this:

![Arabic text written from right to left with reshaping](http://mpcabd.xyz/wp-content/uploads/2012/05/arabic-3.png)

## Installaion

    pip install git+https://github.com/mpcabd/python-arabic-reshaper

## Usage

```
import arabic_reshaper

text_to_be_reshaped = 'اللغة العربية رائعة'
reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped)

# At this stage the text is reshaped, all letters are in their correct form
# based on their surroundings, but if you are going to print the text in a
# left-to-right context, which usually happens in libraries/apps that do not
# support Arabic and/or right-to-left text rendering, then you need to use
# get_display.
# Note that this is optional and depends on your usage of the reshaped text.

bidi_text = arabic_reshaper.get_display(reshaped_text)

# At this stage the text in bidi_text can be easily rendered in any library
# that doesn't support Arabic and/or right-to-left, so use it as you'd use
# any other string. For example if you're using PIL.ImageDraw.text to draw
# text over an image you'd just use it like this...

image = Image.new('RGBA', base.size, (255,255,255,0))
image_draw = ImageDraw.Draw(image)
image_draw.text((10,10), bidi_text, fill=(255,255,255,128))

# See http://pillow.readthedocs.io/en/3.1.x/reference/ImageDraw.html?#PIL.ImageDraw.PIL.ImageDraw.Draw.text

```

## Settings

You can configure the reshaper to your preferences, it has the following
settings defined:

* `language` (Default: `'Arabic'`): Currently it's ignored, but the reshaper
might be extended in the future to work with other languages that use the
Arabic script (Farsi, Urdu, etc.)
* `support_ligatures` (Default: `True`): When this is set to `False`, the
reshaper will not replace any ligatures, otherwise it will replace enabled
ligatures.
* `delete_harakat` (Default: `True`): When this is set to `False` the reshaper
will not delete the harakat from the text, this will result in them showing up
in the reshaped text, you should enable this option if you are going to pass
the reshaped text to `bidi.algorithm.get_display` because it will reverse the
text and you'd end up with harakat applied to the next letter instead of the
previous letter.

Besides the settings above, you can enable/disable supported ligatures. For a
full list of supported ligatures and their default status check the file
[default-config.ini](default-config.ini).

There are multiple ways that you can configure the reshaper in, choose the one
that suits your deployment:

### Via ArabicReshaper instance `configuration`

Instead of directly using `arabic_reshaper.reshape` function, define an
instance of `arabic_reshaper.ArabicReshaper`, and pass your config dictionary
to its constructor's `configuration` parameter like this:

```
from arabic_reshaper import ArabicReshaper
configuration = {
    'delete_harakat': False,
    'support_ligatures': True,
    'RIAL SIGN': True,  # Replace ريال with ﷼
}
reshaper = ArabicReshaper(configuration=configuration)
text_to_be_reshaped = 'سعر المنتج ١٥٠ ريال'
reshaped_text = reshaper.reshape(text_to_be_reshaped)
```

### Via ArabicReshaper instance `configuration_file`

You can separte the configuration from your code, by copying the file
[default-config.ini](default-config.ini) and change its settings,
then save it somewhere in your project, and then you can tell the reshaper
to use your new config file, just pass the path to your config file to its
constructor's `configuration_file` parameter like this:

```
from arabic_reshaper import ArabicReshaper
configuration = {
    'delete_harakat': False,
    'support_ligatures': True,
    'RIAL SIGN': True,  # Replace ريال with ﷼
}
reshaper = ArabicReshaper(configuration_file='/path/to/your/config.ini')
text_to_be_reshaped = 'سعر المنتج ١٥٠ ريال'
reshaped_text = reshaper.reshape(text_to_be_reshaped)
```

Where in you `config.ini` you can have something like this:

```
[ArabicReshaper]
delete_harakat = no
support_ligatures = yes
RIAL SIGN = yes
```

### Via `PYTHON_ARABIC_RESHAPER_CONFIGURATION_FILE` environment variable

Instead of having to rewrite your old code to configure it like above, you can
define an environment variable with the name
`PYTHON_ARABIC_RESHAPER_CONFIGURATION_FILE` and in its value put the full path
to the configuration file. This way the reshape function will pick it
automatically, and you won't have to change your old code.

## Known Issue

When using a library/app that doesn't support right-to-left text rendering,
[Harakat or Tashkeel](http://en.wikipedia.org/wiki/Arabic_diacritics#Tashkil_.28marks_used_as_phonetic_guides.29)
cannot be supported, because their unicode characters are non-spacing marks
(i.e. they don't take space, they are rendered in the same space of the
character before them), which means that when you keep them and pass the
reshaped text to `bidi.algorithm.get_display`, they will end up being rendered
on the next character not the character they should be on as the text is
reversed.

## License

This work is licensed under
[GNU General Public License v3](http://www.gnu.org/licenses/gpl.txt).

## Demo

Online Arabic Reshaper: http://pydj.mpczbd.xyz/arabic-reshaper/

## Download

https://github.com/mpcabd/python-arabic-reshaper/tarball/master

## Version History

### 2.0.0

* Totally rewrote the code;
* Faster and better performance;
* Added the ability to configure and customise the reshaper.

### 1.0.1

* New glyphs for Farsi;
* Added setup.py;
* Bugfixes.

### 1.0

* Ported [Better Arabic Reshaper](https://github.com/agawish/Better-Arabic-Reshaper/)
to Python.

## Contact

Abdullah Diab (mpcabd)
Email: 	mpcabd@gmail.com
Blog:	http://mpcabd.xyz

For more info visit my blog
[post here](http://mpcabd.xyz/python-arabic-text-reshaper/)
