import os.path
import sublime
import sublime_plugin

# Sublime Text 2 API reference:
# http://www.sublimetext.com/docs/2/api_reference.html

# Acknowledgements:
# Several snippets inspired by WordHighlight plugin for
# Sublime Text (https://github.com/SublimeText/WordHighlight)

# TODO: detect long and complex sentences
# TODO: detect adverbs
# TODO: detect patterns that can be simplified

weasel_word_regions = []
passive_voice_regions = []

def mark_words(view, search_all=True):
    global settings, weasel_word_regions, passive_voice_regions

    def find_words(pattern):
        if search_all:
            if settings.debug:
                print('sublimewritingstyle: searching whole document')
            found_regions = view.find_all(pattern, sublime.IGNORECASE, '', [])
        else:
            if settings.debug:
                print('sublimewritingstyle: searching around visible region')
            found_regions = []
            chunk_size = 2 * 10 ** 3

            visible_region = view.visible_region()
            begin = max(visible_region.begin() - chunk_size, 0)
            end = min(visible_region.end() + chunk_size, view.size())
            from_point = begin
            while True:
                region = view.find(pattern, from_point, sublime.IGNORECASE)
                if region:
                    found_regions.append(region)
                    rend = region.end()
                    if rend > end:
                        break
                    else:
                        from_point = rend
                else:
                    break
        return found_regions
        # end of find_words

    def lazy_mark_regions(new_regions, old_regions, style_key, color_scope_name, symbol_name, draw_style):
        if old_regions != new_regions or True:
            # print 'adding new regions'
            view.erase_regions(style_key)
            # name, regions, style, symbol in gutter, draw outlined
            if settings.theme == 'none':
                view.add_regions(style_key, new_regions, color_scope_name, flags = draw_style)
            else:
                view.add_regions(style_key, new_regions, color_scope_name, symbol_name, draw_style) 
        return new_regions
        # end of lazy_mark_regions

    # passive words
    new_regions = find_words(settings.passive_voice_pattern)
    passive_voice_regions = lazy_mark_regions(
        new_regions,
        passive_voice_regions,
        'SublimeWritingStyle.Passive',
        'writingstyle.passive',
        os.path.join('Packages', 'SublimeWritingStyle', 'icons', 'pencil-dark.png' if settings.theme == 'dark' else 'pencil-light.png'),
        sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE  + sublime.DRAW_STIPPLED_UNDERLINE)

    # weasel words
    new_regions = find_words(settings.pattern)
    weasel_word_regions = lazy_mark_regions(
        new_regions,
        weasel_word_regions,
        'SublimeWritingStyle.Weasel',
        'writingstyle.weasel',
        os.path.join('Packages', 'SublimeWritingStyle', 'icons', 'weasel-dark.png' if settings.theme == 'dark' else 'weasel-light.png'),
        sublime.DRAW_NO_FILL + sublime.DRAW_NO_OUTLINE + sublime.DRAW_SQUIGGLY_UNDERLINE)


class SublimeWritingStyleListener(sublime_plugin.EventListener):
    enabled = False

    @classmethod
    def disable(cls):
        """
        marks package as disabled and removes marked words.
        """
        cls.enabled = False
        window = sublime.active_window()
        if window:
            view = window.active_view()
            if view:
                view.erase_regions("SublimeWritingStyle.Passive")
                view.erase_regions("SublimeWritingStyle.Weasel")

    def handle_event(self, view):
        """
        determines if the package status changed. marks words when turned on.
        """
        global settings

        # does settings enable package?
        if not settings.enabled:
            # ... no!
            SublimeWritingStyleListener.disable()
            return

        # check this file if either it's enabled or if the extensions list is empty
        file_name = view.file_name()

        ext = ''
        if file_name:
            # Use the extension if it exists, otherwise use the whole filename
            ext = os.path.splitext(file_name)
            if ext[1]:
                ext = ext[1]
            else:
                ext = os.path.split(file_name)[1]

        allowed_extensions = settings.get('extensions')
        if (not allowed_extensions) or ext in allowed_extensions:
            if not SublimeWritingStyleListener.enabled:
                SublimeWritingStyleListener.enabled = True

            mark_words(view)
            return

        SublimeWritingStyleListener.disable()  # turn off for this file!

    def on_activated(self, view):
        if not view.is_loading():
            self.handle_event(view)

    def on_post_save(self, view):
        self.handle_event(view)

    def on_load(self, view):
        self.handle_event(view)

    def on_modified(self, view):
        if SublimeWritingStyleListener.enabled:
            mark_words(view, search_all=False)


def load_settings():
    """
    runs when package loads.
    """
    settings = sublime.load_settings('SublimeWritingStyle.sublime-settings')

    def process_settings(settings):
        """
        add properties reflecting the loaded settings.
        """
        def build_passive_voice_regex(linking_verbs, irregulars):
            return r'(?<!\w)(' + '|'.join(linking_verbs) + r')\s+(\w+ed|' + '|'.join(irregulars) + r')(?!\w)'

        def build_regex_from_wordlist(words):
            word_to_expr = lambda w: r'(?<!\w)' + w + r'(?!\w)'
            exprs = map(word_to_expr, words)
            duplicate_words_regex = r'\b(\w+)\s\1\b'
            return "|".join(exprs) + "|" + duplicate_words_regex

        setattr(settings, "enabled", settings.get("enabled", True))
        setattr(settings, "debug", settings.get("debug", False))
        setattr(settings, "theme", settings.get("theme", "dark"))

        weasel_words = settings.get("weasel_words", ["many", "clearly"])
        if settings.has("extra_words"):
            weasel_words = weasel_words + settings.get("extra_words")
        setattr(settings, "pattern", build_regex_from_wordlist(weasel_words))

        extensions = settings.get('extensions', ['.tex'])
        if settings.has("extra_extensions"):
            extensions = extensions + settings.get('extra_extensions')
        setattr(settings, "extensions", extensions)

        linking_verbs = settings.get('passive_voice_linking_verbs', ['be', 'being'])
        irregulars = settings.get('passive_voice_irregulars', ['chosen', 'kept'])
        setattr(settings, "passive_voice_pattern", build_passive_voice_regex(linking_verbs, irregulars))

    process_settings(settings)
    if not settings.enabled:
        SublimeWritingStyleListener.disable()

    # reload when package specific preferences changes
    settings.add_on_change('reload', lambda: process_settings(settings))

    return settings

settings = None
# only do this for ST2, use plugin_loaded for ST3.
if int(sublime.version()) < 3000:
    settings = load_settings()  # read settings as package loads.

def plugin_loaded():
    """
    Seems that in ST3, plugins should read settings in this method.
    See: http://www.sublimetext.com/forum/viewtopic.php?f=6&t=15160
    """
    global settings
    settings = load_settings()  # read settings as package loads.


class ToggleSublimeWritingStyle(sublime_plugin.ApplicationCommand):
    """
    menu item that toggles the enabled status of this package.
    """
    def run(self):
        global settings
        settings.enabled = not settings.enabled
        if not settings.enabled:
            sublime.active_window().active_view().erase_regions("SublimeWritingStyle.Passive")
            sublime.active_window().active_view().erase_regions("SublimeWritingStyle.Weasel")
        else:
            mark_words(sublime.active_window().active_view())

    def description(self):
        """
        determines the text of the menu item.
        """
        global settings
        return 'Disable' if settings.enabled else 'Enable'
