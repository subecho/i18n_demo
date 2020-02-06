# Internationalization with Python and Babel

This is a brief demonstration of the workflow required to mark string literals
in your code as translatable, how to generate a template file that can then be
used as the basis for all of your translations, and then how to automatically
generate files that will be used for translations for the locales that you
specify. I'll be using Python and the [Babel](http://babel.pocoo.org/en/latest/)
tool for helping to make this process a lot easier.

## Marking your Strings for Internationalization
Python has a builtin way of dealing with internationalized strings through the
[GNU gettext](https://www.gnu.org/software/gettext/) library and its own hooks
for it through the 
[gettext module](https://docs.python.org/3/library/gettext.html). The `gettext`
module provides the "lookup" service for finding the localized version of a
string literal through something akin to a standard dictionary lookup. There
is a minimal amount of setup needed to tell `gettext` where to look for
translations and what to do if there is not a translation to get. I've put
these steps in `main.py` but I will reproduce them below and walk through
them.

```python
import gettext
import os
import sys

locale_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locale")
translate = gettext.translation("messages", locale_dir, fallback=True)
_ = translate.gettext
```

The first things we have to do are import the `gettext` and `os` modules. These
allow us to determine where the locale directory is as well as having the means
to look up translations in that directory. We then set the path to the
`locale_dir` by getting the path to that file and then appending `locale` to the
end of it. We then specify in which file to look for the translations. In this
case, we're looking for files named `messages` as this is the standard for
GNU `gettext`. The final line is the "standard" shorthand for tranlating strings
which is to "alias" the `gettext` method to `_` as it is used frequently (and
most other Python developers will know what you're doing when they see that.)

Once we've done that we can now do some simple Python to mark strings as
translatable. Look at the following code snippet:

```python
if __name__ == "__main__":
    args = sys.argv
    print(_("This is a translatable string."))
    print(_("Hello world."))
    print(_("Sphinx of black quartz, judge my vow!"))
    print(_("The args are {}.").format(args))
```

Note that we preface our string literals with `_` to indicate that they should
be translated if possible.

## Creating `base.pot`
The file `base.pot` is the basis for all translations that will be done. We will
use `pybabel` from `Babel` to generate this file by running the following
commands.

```bash
# First make the directory where our translations will live
mkdir locale
pybabel extract <files_or_directories> -o locale/base.pot
```

This will extract the strings that we've marked with `_` and create a file
called `base.pot`. The `.pot` file extension stands for **"Portable Object
Template"** as it will form the basis for any future translations that we will
make.

## Creating a New Message Catalog
Now that we have our template file, we can now use it to create a new message
catalog to store our actual translations for different locales. We do this by
using `pybabel` to create a new message catalog from our template. We specify
the locale in the general style of `language.country_code` For example, if
we wanted to specify American English, we would specify our locale as `en_US` or
if we wanted Brazilian Portuguese, we would use `pt_BR`. You can look up the
locale identifiers using
[this tool](http://demo.icu-project.org/icu-bin/locexp).

```bash
pybabel init -l <name_of_locale> -i locale/base.pot -d locale
```

This will create a new series of directories and a file as follows:

```bash
locale/<name_of_locale>/LC_MESSAGES/messages.po
```

The `messages.po` file is where our translations will go for the locale
specified. 

## Compiling the Messages So They Can be Used
Before we're able to use our new translations, we have to compile our `.po`
files into the binary format that `gettext` uses. The following command will
compile our `messages.po` files in each locale directory under `locale` and
generate the corresponding `messages.mo` files. The `.mo` extension stands for
**"Machine Object"**.

```bash
pybabel compile -d locale
```

## Testing our Changes
To test our changes, we can set our locale on the command line to another one
temporarily by setting the environment variable `LANGUAGE` before specifying the
command we want to run.

```bash
LANGUAGE=de_DE python main.py
```

## Updating `base.pot`

Simply run the `pybabel extract` command from above again!

## Updating `messages.po` in the Locale Directories
If we've changed the strings in our code, we will need to update `base.pot` and
then use that to update the individual `message.po` files in each of our
supported locales.

```bash
pybabel extract <files_or_directories> -o locale/base.py
pybabel update -i locale/base.pot -d locale
```
