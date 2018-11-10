import os
import sys
import ConfigParser

from jinja2 import Environment, FileSystemLoader


def main():
    colors = (
        ("white", "White"),
        ("orange", "Orange"),
        ("magenta", "Magenta"),
        ("light_blue", "Light Blue"),
        ("yellow", "Yellow"),
        ("lime_green", "Lime Green"),
        ("pink", "Pink"),
        ("gray", "Gray"),
        ("light_gray", "Light Gray"),
        ("cyan", "Cyan"),
        ("purple", "Purple"),
        ("blue", "Blue"),
        ("brown", "Brown"),
        ("green", "Green"),
        ("red", "Red"),
        ("black", "Black"),
    )

    dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    config = ConfigParser.SafeConfigParser()

    tmpl_dir = os.path.join(dir, 'templates')
    pkg_dir = os.path.dirname(os.path.realpath(__file__))

    config.read(os.path.join(pkg_dir, 'allstuff.cfg'))

    env = Environment(
        loader=FileSystemLoader(tmpl_dir)
    )
    for tmpl_name in env.list_templates(extensions=['mctmpl']):
        func_name = os.path.splitext(tmpl_name)[0]
        print '----- %s' % func_name
        tmpl = env.get_template(tmpl_name)
        print tmpl.render(
            func=func_name,
            colors=colors,
        )


if __name__ == '__main__':
    main()
