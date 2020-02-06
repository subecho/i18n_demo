import gettext
import os
import sys

localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "locale")
translate = gettext.translation("messages", localedir, fallback=True)
_ = translate.gettext


if __name__ == '__main__':
    args = sys.argv
    print(_("This is a translatable string."))
    print(_("Hello world."))
    print(_("Sphinx of black quartz, judge my vow!"))
    print(_("The args are {}.").format(args))
