# pelican-embed-svg

[Pelican](https://blog.getpelican.com/) plugin for embedding SVG images/icons at generation time. The plugin currently supports FontAwesome 5 icons specified using `<i>` tags as well as arbitrary SVG image files.

Copyright (c) 2020 by Kevin Houlihan

License: MIT, see LICENSE for more details.

## Installation

The plugin can be installed from PyPI:

```bash
pip install pelican-embed-svg
```

To enable the plugin, add it to the `PLUGINS` list in your pelicanconf.py

```python
PLUGINS = [
    'pelican_embed_svg',
]
```

If you want to use [FontAwesome](https://fontawesome.com/) icons then you will need to [download](https://fontawesome.com/download) that as well. It is recommended to install that to a directory named `font-awesome` in the root of your pelican site. However, if you want to use FontAwesome's css (for sizing, etc.), then those files will need to be included in your site's static content, and referenced appropriately in your templates.

## Usage

SVG images to embed can be specified in three ways in your templates.

### FontAwsome `<i>` tags

`<i>` tags with base FontAwesome classes (`fas`, `fab` etc.) and an additional class specifying the icon.

```html
<i class="fas fa-heart"></i>
```

All the classes specified will be copied to the embedded `<svg>` element in the output.

### Custom `<i>` tags

`<i>` tags with the class `pi`, and an additional class specifying the name of the icon.

```html
<i class="pi my-heart"></i>
```

This will embed the first file named my-heart.svg that is found in your project output, or the svg icon path, if set (see the settings section below).

All the classes specified will be copied to the embedded `<svg>` element in the output.

### `<img>` tags

`<img>` tags with `src` attributes that specify svg files.

```html
<img src="http://localhost:8000/images/my-heart.svg">
```

The svg file in this case will be found by stripping out the `SITEURL`. As such, the file must be present in the project output.

## Settings

### FontAwesome path

By default, FontAwesome icons are looked for in a directory called `font-awesome` in the root of your pelican project. If you have FontAwesome installed somewhere else then you can specify the path by adding the `PES_FONT_AWESOME_PATH` setting to your pelicanconf.py.

### SVG icon path

When specifying icons using `<i>` tags and the `pi` class, by default the output directory is searched for the first svg file that matches. However, it is not strictly necessary for the svg files to be included in the output, so if you have them stored somewhere else the path can be specified using the `PES_SVG_ICON_PATH` setting.

### `<img>` embedding

If you don't want to process `<img>` tags then that can be turned off using the `PES_EMBED_IMG_TAGS` setting:

```python
PES_EMBED_IMG_TAGS = False
```

### Path fills

By default, the embedded svg paths have their `fill` attribute set to `currentColor` for `<i>` tags so that the image colours can be controlled using css `color` properties. If this is not desirable (such as if your svgs have their own colour information), this can be turned off using the `PES_SET_ICON_FILL` setting.

For `<img>` tags, the fill is not modified by default. If you want the fill to be set for these then you can enable it using the `PES_SET_IMG_FILL` setting.

## Caveats

This plugin is at an early stage of development, and largely untested outside of my own personal use-case.
