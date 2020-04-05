
from pathlib import Path
import bs4
from pelican import signals

__all__ = ['register']

# Settings and context
_output_path = None
_root_url = None
_process_imgs = None
_set_img_fill = None
_set_icon_fill = None
_svg_path = None
_fa_path = None

# State
_custom_svg_icons = None


def _retrieve_settings(p):
    global _output_path, _root_url, _process_imgs, _set_img_fill, _set_icon_fill
    global _svg_path, _fa_path, _custom_svg_icons

    _output_path = Path(p.output_path)
    _root_url = p.settings.get('SITEURL', '')
    _process_imgs = p.settings.get('PES_EMBED_IMG_TAGS', True)
    _set_img_fill = p.settings.get('PES_SET_IMG_FILL', False)
    _set_icon_fill = p.settings.get('PES_SET_ICON_FILL', True)
    # Default is to search the entire output directory, though there is
    # actually no need for the images to be included in the output
    _svg_path = Path(p.settings.get('PES_SVG_ICON_PATH', p.output_path))
    # The default here is a 'font-awesome' directory in the project root.
    _fa_path = Path(p.settings.get('PES_FONT_AWESOME_PATH', Path('font-awesome')))

    _custom_svg_icons = sorted(_svg_path.glob('**/*.svg'))


def _load_svg(path):
    svg_soup = None
    with open(path) as svg:
        svg_soup = bs4.BeautifulSoup(svg.read(), features="lxml")
    return svg_soup


def _find_svg(available, name):
    for svg in available:
        if svg.stem == name:
            return svg


def _process_file(f):
    soup = None
    modified = False

    def _replace_icon(icon, name, classes, available, set_fill):
        nonlocal modified
        svg = _find_svg(available, name)
        svg_element = None
        if svg:
            svg_element = _load_svg(svg)
            svg_element.svg['role'] = 'img'
            svg_element.svg['class'] = classes[:]
            # Font-awesome adds some additional classes when it embeds the SVG
            # with Javascript. Unclear what the purpose of theese classes are
            # at this point.
            #svg_element.svg['class'].extend(['svg-inline--fa', 'fa-w-16'])
            if set_fill:
                svg_element.path['fill'] = 'currentColor'
            modified = True
            icon.replace_with(svg_element)
        else:
            print("SVG not found")

    def _handle_icons(icons):
        nonlocal soup, modified
        global _custom_svg_icons, _fa_path, _set_icon_fill

        def fa(style):
            name = classes[1][3:]
            fa_specific = _fa_path / 'svgs' / style
            fa_available = sorted(fa_specific.glob('**/*.svg'))
            _replace_icon(icon, name, classes, fa_available, _set_icon_fill)

        for icon in icons:
            classes = icon['class']
            if 'pi' in classes:
                _replace_icon(icon, classes[1], classes, custom, set_fill)
            elif 'fa' in classes:
                # TODO: This could also be ForkAwesome - need to look into how to support that
                fa('solid')
            elif 'fas' in classes:
                fa('solid')
            elif 'far' in classes:
                fa('regular')
            elif 'fal' in classes:
                # Don't know if this is the correct path!
                fa('light')
            elif 'fad' in classes:
                # Don't know if this is the correct path!
                fa('duotone')
            elif 'fab' in classes:
                fa('brands')
            elif classes[0].startswith('fi-'):
                # TODO: Friconix
                pass

    def _handle_imgs(imgs):
        nonlocal modified, soup
        global _output_path, _root_url, _set_img_fill

        for img in imgs:
            src = img['src']
            if src.endswith('.svg'):
                if _root_url and src.startswith(_root_url):
                    src = src[len(_root_url):]
                src = src.lstrip('/')
                src = _output_path / src
                svg_element = _load_svg(src)
                if svg_element:
                    classes = img.get('class', None)
                    svg_element.svg['class'] = classes
                    if _set_img_fill:
                        svg_element.path['fill'] = 'currentColor'
                    img.replace_with(svg_element)
                    modified = True

    def _process():
        nonlocal soup, modified
        with open(f) as input:
            soup = bs4.BeautifulSoup(input.read(), features="lxml")

        icons = soup.find_all('i')
        _handle_icons(icons)
        if _process_imgs:
            imgs = soup.find_all('img')
            _handle_imgs(imgs)

        if modified:
            with open(f, 'w') as output:
                output.write(str(soup))

    _process()


# Signal handler
def _finalized(p):
    _retrieve_settings(p)

    for f in _output_path.glob('**/*.htm*'):
        _process_file(f)


# Register function expected by pelican
def register():
    signals.finalized.connect(_finalized)
