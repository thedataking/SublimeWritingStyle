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
                region = view.find(pattern, from_point)
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

    def lazy_mark_regions(new_regions, old_regions, style_key, color_scope_name, symbol_name):
        if old_regions != new_regions or True:
            # print 'adding new regions'
            view.erase_regions(style_key)
            # name, regions, style, symbol in gutter, draw outlined
            view.add_regions(style_key, new_regions, color_scope_name, symbol_name, True)
        return new_regions

    # weasel words
    new_regions = find_words(settings.pattern)
    weasel_word_regions = lazy_mark_regions(
        new_regions,
        weasel_word_regions,
        'SublimeWritingStyle',
        settings.color_scope_name,
        'dot')

    # passive words
    new_regions = find_words(settings.passive_voice_pattern)
    passive_voice_regions = lazy_mark_regions(
        new_regions,
        passive_voice_regions,
        'SublimeWritingStyle-Passive',
        'string',
        'circle')


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
                view.erase_regions("SublimeWritingStyle")
                view.erase_regions("SublimeWritingStyle-Passive")

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

        # is package enabled for this file type?
        file_name = view.file_name()
        for ext in settings.extensions:
            if file_name and file_name.endswith(ext):
                # ... yes!
                if not SublimeWritingStyleListener.enabled:
                    # enabling... mark words.
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
            return "|".join(exprs)

        setattr(settings, "enabled", settings.get("enabled", True))
        setattr(settings, "debug", settings.get("debug", False))
        weasel_words = settings.get("weasel_words", ["many", "clearly"])
        if settings.has("extra_words"):
            weasel_words = weasel_words + settings.get("extra_words")
        setattr(settings, "pattern", build_regex_from_wordlist(weasel_words))
        extensions = settings.get('extensions', ['.tex'])
        if settings.has("extra_extensions"):
            extensions = settings.get('extra_extensions')
        setattr(settings, "extensions", extensions)
        setattr(settings, "color_scope_name", settings.get('color_scope_name', "comment"))
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
            sublime.active_window().active_view().erase_regions("SublimeWritingStyle")
            sublime.active_window().active_view().erase_regions("SublimeWritingStyle-Passive")
        else:
            mark_words(sublime.active_window().active_view())

    def description(self):
        """
        determines the text of the menu item.
        """
        global settings
        return 'Disable' if settings.enabled else 'Enable'
