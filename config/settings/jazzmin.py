# JAZZMIN_UI_TWEAKS = {
#     'theme': 'cosmo',
# }
JAZZMIN_SETTINGS: dict = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    'site_title': 'Admin',
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_header': 'Admin',
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    'site_brand': 'Admin',
    # Logo to use for your site, must be present in static files, used for brand on top left
    # 'site_logo': 'logo.svg',
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    # 'login_logo': 'logo.svg',
    # Logo to use for login form in dark themes (defaults to login_logo)
    # 'login_logo_dark': None,
    # CSS classes that are applied to the logo above
    # 'site_logo_classes': 'img-squares',
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    # 'site_icon': None,
    # Welcome text on the login screen
    'welcome_sign': 'Musiqa Maktablari',
    # Copyright on the footer
    'copyright': 'Madaniyat Vazirligi',
    # The model admin to search from the search bar, search bar omitted if excluded
    'search_model': '',
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    # 'user_avatar': None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    'topmenu_links': [
        # Url that gets reversed (Permissions can be added)
        # {
        #     'name': 'Parolni o\'zgartirish',
        #     'url': 'admin:password_change',
        # },
        # external url that opens in a new window (Permissions can be added)
        # {'name': 'Support', 'url': 'https://github.com/farridav/django-jazzmin/issues', 'new_window': True},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ('app' url type is not allowed)
    'usermenu_links': [{'model': 'auth.user'}],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    'show_sidebar': True,
    # Whether to aut expand the menu
    'navigation_expanded': True,
    # Hide these apps when generating side menu e.g (auth)
    'hide_apps': [],
    # Hide these models when generating side menu (e.g auth.user)
    'hide_models': [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)

    'order_with_respect_to': ['auth', 'user', 'main', 'main.school', 'main.menu', 'main.banner', 'main.schoollife' ],
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    'icons': {
        'auth': 'fas fa-users-cog',
        'main.school': 'fas fa-school',
        'user.user': 'fas fa-duotone fa-user-tie',
        'main.menu': 'fas fa-grip-lines',
        'auth.Group': 'fas fa-duotone fa-users',
        'main.banner': 'fas fa-duotone fa-image',
        'main.schoollife': 'fas fa-book-medical',
        # 'artist.Category': 'fas fa-grip-lines',
        # 'artist.Artist': 'fas fa-users',
        # 'artist.Project': 'fas fa-vote-yea',

        # 'common.Contact': 'fas fa-address-card',
        # 'common.Menu': 'fas fa-grip-lines',
        # 'common.SocialMedia': 'fas fa-share-alt-square',
        # 'common.Organizer': 'fas fa-sitemap',
        # 'common.About': 'fas fa-info-circle',
        # 'common.Statistic': 'fas fa-chart-line',
        # 'common.Policy': 'fas fa-info',

    },
    # Icons that are used when one is not manually specified
    'default_icon_parents': 'fas fa-chevron-circle-right',
    'default_icon_children': 'fas fa-circle',
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    'related_modal_active': False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    # 'custom_css': 'css/main.css',
    # 'custom_js': None,
    # Whether to show the UI customizer on the sidebar
    'show_ui_builder': False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    'changeform_format': 'horizontal_tabs',
    # override change forms on a per modeladmin basis
    'changeform_format_overrides': {
        'auth.user': 'collapsible',
        'auth.group': 'vertical_tabs',
        'media.mediaimage': 'vertical_tabs',
        'media.mediavideo': 'vertical_tabs',
        'media.mediacollection': 'single',
    },
    
    # Add a language dropdown into the admin
    'language_chooser': True,
}

# JAZZMIN_UI_TWEAKS: dict = {
#     'navbar_small_text': False,
#     'footer_small_text': False,
#     'body_small_text': False,
#     'brand_small_text': False,
#     'brand_colour': 'navbar-primary',
#     'accent': 'accent-navy',
#     'navbar': 'navbar-primary navbar-dark',
#     'no_navbar_border': False,
#     'navbar_fixed': False,
#     'layout_boxed': False,
#     'footer_fixed': False,
#     'sidebar_fixed': False,
#     'sidebar': 'sidebar-light-primary',
#     'sidebar_nav_small_text': False,
#     'sidebar_disable_expand': False,
#     'sidebar_nav_child_indent': False,
#     'sidebar_nav_compact_style': False,
#     'sidebar_nav_legacy_style': True,
#     'sidebar_nav_flat_style': True,
#     'theme': 'yeti',
#     'dark_mode_theme': None,
#     'button_classes': {
#         'primary': 'btn-primary',
#         'secondary': 'btn-secondary',
#         'info': 'btn-info',
#         'warning': 'btn-outline-warning',
#         'danger': 'btn-outline-danger',
#         'success': 'btn-success',
#     },
# }

