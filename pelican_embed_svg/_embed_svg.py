
from pathlib import Path
import bs4
from pelican import signals


def _load_svg(path):
    svg_soup = None
    with open(path) as svg:
        svg_soup = bs4.BeautifulSoup(svg.read(), features="lxml")
    return svg_soup


def _find_svg(available, name):
    for svg in available:
        if svg.stem == name:
            return svg


def _replace_icon(icon, name, classes, available, set_fill):
    modified = False
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
    return modified


def _handle_icons(soup, icons, custom, fa_path, set_fill):
    modified = False

    def fa(style):
        name = classes[1][3:]
        fa_specific = fa_path / 'svgs' / style
        fa_available = sorted(fa_specific.glob('**/*.svg'))
        return _replace_icon(icon, name, classes, fa_available, set_fill)

    for icon in icons:
        classes = icon['class']
        if 'pi' in classes:
            modified = _replace_icon(icon, classes[1], classes, custom, set_fill) or modified
        elif 'fa' in classes:
            # TODO: This could also be ForkAwesome - need to look into how to support that
            modified = fa('solid') or modified
        elif 'fas' in classes:
            modified = fa('solid') or modified
        elif 'far' in classes:
            modified = fa('regular') or modified
        elif 'fal' in classes:
            # Don't know if this is the correct path!
            modified = fa('light') or modified
        elif 'fad' in classes:
            # Don't know if this is the correct path!
            modified = fa('duotone') or modified
        elif 'fab' in classes:
            modified = fa('brands') or modified
        elif classes[0].startswith('fi-'):
            # TODO: Friconix
            pass

    return modified


def _handle_imgs(soup, imgs, output_path, root_url, set_fill):
    modified = False

    for img in imgs:
        print (img)
        src = img['src']
        if src.endswith('.svg'):
            if root_url and src.startswith(root_url):
                src = src[len(root_url):]
            src = src.lstrip('/')
            src = output_path / src
            svg_element = _load_svg(src)
            if svg_element:
                classes = img.get('class', None)
                svg_element.svg['class'] = classes
                if set_fill:
                    svg_element.path['fill'] = 'currentColor'
                img.replace_with(svg_element)
                modified = True

    return modified


def _finalized(p):
    output_path = Path(p.output_path)
    root_url = p.settings.get('SITEURL', '')
    process_img = p.settings.get('PES_EMBED_IMG_TAGS', True)
    set_img_fill = p.settings.get('PES_SET_IMG_FILL', False)
    set_icon_fill = p.settings.get('PES_SET_ICON_FILL', True)
    # Default is to search the entire output directory, though there is
    # actually no need for the images to be included in the output
    svg_path = Path(p.settings.get('PES_SVG_ICON_PATH', p.output_path))
    # The default here is a 'font-awesome' directory in the project root.
    fa_path = Path(p.settings.get('PES_FONT_AWESOME_PATH', Path('font-awesome')))
    svg_available = sorted(svg_path.glob('**/*.svg'))
    for f in output_path.glob('**/*.htm*'):
        soup = None
        with open(f) as input:
            soup = bs4.BeautifulSoup(input.read(), features="lxml")

        modified = False
        icons = soup.find_all('i')
        modified = _handle_icons(soup, icons, svg_available, fa_path, set_icon_fill) or modified
        if process_img:
            imgs = soup.find_all('img')
            modified = _handle_imgs(soup, imgs, output_path, root_url, set_img_fill) or modified

        if modified:
            with open(f, 'w') as output:
                output.write(str(soup))


def register():
    signals.finalized.connect(_finalized)
