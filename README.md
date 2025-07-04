## Python Arabic Reshaper

[![Build Status](https://app.travis-ci.com/mpcabd/python-arabic-reshaper.svg?branch=master)](https://app.travis-ci.com/mpcabd/python-arabic-reshaper)

Reconstruct Arabic sentences to be used in applications that don't support
Arabic script.

Works with Python 3.x

## Description

Arabic script is very special with two essential features:

1. It is written from right to left.
2. The characters change shape according to their surrounding characters.

So when you try to print text written in Arabic script in an application
– or a library – that doesn’t support Arabic you’re pretty likely to end up
with something that looks like this:

![Arabic text written from left to right with no reshaping](https://mpcabd.xyz/wp-content/uploads/2012/05/arabic-1.png)

We have two problems here, first, the characters are in the isolated form,
which means that every character is rendered regardless of its surroundings,
and second is that the text is written from left to right.

To solve the latter issue all we have to do is to use the
[Unicode bidirectional algorithm](http://unicode.org/reports/tr9/), which is
implemented purely in Python in
[python-bidi](https://github.com/MeirKriheli/python-bidi).
If you use it you’ll end up with something that looks like this:

![Arabic text written from right to left with no reshaping](https://mpcabd.xyz/wp-content/uploads/2012/05/arabic-6.png)

The only issue left to solve is to reshape those characters and replace them
with their correct shapes according to their surroundings. Using this library
helps with the reshaping so we can get the proper result like this:

![Arabic text written from right to left with reshaping](https://mpcabd.xyz/wp-content/uploads/2012/05/arabic-3.png)

## Installation

    pip install --upgrade arabic-reshaper

If you're using Anaconda you can use

    conda install -c mpcabd arabic-reshaper

## Usage

```python
import arabic_reshaper

text_to_be_reshaped = 'اللغة العربية رائعة'
reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped)
```

### Example using PIL Image

PIL Image does not support reshaping out of the box, so to draw Arabic text on an `Image` instance you would need to reshape
the text for sure.

For this example to work you need to run `pip install --upgrade arabic-reshaper python-bidi pillow`

```python

import arabic_reshaper

text_to_be_reshaped = 'اللغة العربية رائعة'
reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped)

# At this stage the text is reshaped, all letters are in their correct form
# based on their surroundings, but if you are going to print the text in a
# left-to-right context, which usually happens in libraries/apps that do not
# support Arabic and/or right-to-left text rendering, then you need to use
# get_display from python-bidi.
# Note that this is optional and depends on your usage of the reshaped text.

from bidi.algorithm import get_display
bidi_text = get_display(reshaped_text)

# At this stage the text in bidi_text can be easily rendered in any library
# that doesn't support Arabic and/or right-to-left, so use it as you'd use
# any other string. For example if you're using PIL.ImageDraw.text to draw
# text over an image you'd just use it like this...

from PIL import Image, ImageDraw, ImageFont

# We load Arial since it's a well known font that supports Arabic Unicode
font = ImageFont.truetype('Arial', 40)

image = Image.new('RGBA', (800, 600), (255,255,255,0))
image_draw = ImageDraw.Draw(image)
image_draw.text((10,10), bidi_text, fill=(255,255,255,128), font=font)

# Now the text is rendered properly on the image, you can save it to a file or just call `show` to see it working
image.show()

# For more details on PIL.Image and PIL.ImageDraw check the documentation
# See http://pillow.readthedocs.io/en/5.1.x/reference/ImageDraw.html?#PIL.ImageDraw.PIL.ImageDraw.Draw.text

```

## Settings

You can configure the reshaper to your preferences, it has the following
settings defined:

* `language` (Default: `'Arabic'`): Ignored, the reshaper works with Arabic,
Farsi, and Urdu, and most probably all other languages that use Arabic script.
* `support_ligatures` (Default: `True`): When this is set to `False`, the
reshaper will not replace any ligatures, otherwise it will replace enabled
ligatures.
* `delete_harakat` (Default: `True`): When this is set to `False` the reshaper
will not delete the harakat from the text, this will result in them showing up
in the reshaped text, you should enable this option if you are going to pass
the reshaped text to `bidi.algorithm.get_display` because it will reverse the
text and you'd end up with harakat applied to the next letter instead of the
previous letter.
* `delete_tatweel` (Default `False`): When this is set to `True` the reshaper
will delete the Tatweel character (U+0640) from the text before reshaping, this
can be useful when you want to support ligatures and don't care about Tatweel
getting deleted.
* `shift_harakat_position` (Default `False`): Whether to shift the Harakat
(Tashkeel) one position so they appear correctly when string is reversed, this
might solve the problem of Tashkeel in some systems, although for `PIL.Image`
for example, this is not needed.
* `support_zwj` (Default `True`): Whether to support ZWJ (`U+200D`) or not.
* `use_unshaped_instead_of_isolated` (Default `False`): Use unshaped form
instead of isolated form, useful in some fonts that are missing the isolated
form of letters.

Besides the settings above, you can enable/disable supported ligatures. For a
full list of supported ligatures and their default status check the file
[default-config.ini](https://github.com/mpcabd/python-arabic-reshaper/blob/32f7497aa24a68ab880d0248b21715928f0ce212/arabic_reshaper/default-config.ini).

There are multiple ways that you can configure the reshaper in, choose the one
that suits your deployment:

### Via ArabicReshaper instance `configuration`

Instead of directly using `arabic_reshaper.reshape` function, define an
instance of `arabic_reshaper.ArabicReshaper`, and pass your config dictionary
to its constructor's `configuration` parameter like this:

```python
from arabic_reshaper import ArabicReshaper
configuration = {
    'delete_harakat': False,
    'support_ligatures': True,
    'RIAL SIGN': True,  # Replace ر ي ا ل with ﷼
}
reshaper = ArabicReshaper(configuration=configuration)
text_to_be_reshaped = 'سعر المنتج ١٥٠ ر' + 'يال'  # had to split the string for display
reshaped_text = reshaper.reshape(text_to_be_reshaped)
```

### Via ArabicReshaper instance `configuration_file`

You can separte the configuration from your code, by copying the file
[default-config.ini](default-config.ini) and change its settings,
then save it somewhere in your project, and then you can tell the reshaper
to use your new config file, just pass the path to your config file to its
constructor's `configuration_file` parameter like this:

```python
from arabic_reshaper import ArabicReshaper
reshaper = ArabicReshaper(configuration_file='/path/to/your/config.ini')
text_to_be_reshaped = 'سعر المنتج ١٥٠ ر' + 'يال'  # had to split the string for display
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

## Settings based on a TrueType® font

If you intend to render the text in a TrueType® font, you can tell the library
to generate its configuration by reading the font file to figure out what's
supported in the font and what's not.

To use this feature you need to install the library with an extra option
(not necessary when you install it with conda):

    pip install --upgrade arabic-reshaper[with-fonttools]

Then you can use the reshaper like this:

```python
import arabic_reshaper

reshaper = arabic_reshaper.ArabicReshaper(
    arabic_reshaper.config_for_true_type_font(
        '/path/to/true-type-font.ttf',
        arabic_reshaper.ENABLE_ALL_LIGATURES
    )
)
```

This will parse the font file, and figure out what ligatures it supports and enable them,
as well as whether it has isolated forms or `use_unshaped_instead_of_isolated` should be
enabled.

The second parameter to `config_for_true_type_font` can be one of

- `ENABLE_NO_LIGATURES`
- `ENABLE_SENTENCES_LIGATURES`
- `ENABLE_WORDS_LIGATURES`
- `ENABLE_LETTERS_LIGATURES`
- `ENABLE_ALL_LIGATURES` (default)

which controls what ligatures to look for, depending on your usage,
see [default-config.ini](default-config.ini) to know what ligatures are there.

## Tashkeel/Harakat issue

[Harakat or Tashkeel](http://en.wikipedia.org/wiki/Arabic_diacritics#Tashkil_.28marks_used_as_phonetic_guides.29)
might not show up properly in their correct place, depending on the application
or the library that is doing the rendering for you, so you might want to enable
the `shift_harakat_position` option if you face this problem.

## License

This work is licensed under
[MIT License](https://opensource.org/licenses/MIT).

## Demo

Online Arabic Reshaper: http://pydj.mpcabd.xyz/arabic-reshaper/

## Download

https://github.com/mpcabd/python-arabic-reshaper/tarball/master

## Version History

### 3.0.0
* Stop supporting Python 2.7
* Remove dependency on `future`. See #88.

### 2.1.4

* Fix unparseable version bound for `fonttools` under Python 2

### 2.1.3

* Remove dependency on `__version__.py` and `default-config.ini` files, as they were causing problems for people who package their apps using pyinstaller or buildozer.

### 2.1.1

* Fix a warning. See #57. Thanks @fbernhart

### 2.1.0

* Added support for settings based on a TrueType® font

### 2.0.14

* New option `use_unshaped_instead_of_isolated` to get around some fonts missing the isolated form for letters.

### 2.0.13

**BROKEN** please make sure not to use this version.

### 2.0.12

* Updated letters and ligatures
* New option `shift_harakat_position` to try to get around the Tashkeel problem

### 2.0.11

* Proper support for ZWJ

### 2.0.10

* Fix Shadda ligatures

### 2.0.9

* Added support for ZWJ (Zero-width Joiner) (U+200D)

### 2.0.8

* Added `delete_tatweel`
* Added more test cases

### 2.0.7

* Fix tests for Python 2.7

### 2.0.6

* Fixed a bug with Harakat breaking the reshaping
* Wrote two small unit tests, more to come
* Moved letters and ligatures to separate files for readability/maintainability
* Moved package to its own folder for readability/maintainability

### 2.0.5

Fix error message formatting

### 2.0.4

Fix error message formatting

### 2.0.3

Use `Exception` instead of `Error`.

### 2.0.2

Use `pkg_resources.resource_filename` instead of depending on `__file__` to access `default-config.ini`.

### 2.0.1

Include default-config.ini in setup.py

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
Email:  mpcabd@gmail.com
Blog:   http://mpcabd.xyz

For more info visit my blog
[post here](http://mpcabd.xyz/python-arabic-text-reshaper/)
