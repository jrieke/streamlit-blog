---
title: "Accessible color themes for Streamlit apps"
subtitle: "Control your app\u2019s color scheme and visual accessibility"
date: 2023-05-05
authors:
  - "Yuichiro Tachibana (Tsuchiya)"
category: "Advocate Posts"
---

![Accessible color themes for Streamlit apps](https://streamlit.ghost.io/content/images/size/w2000/2023/04/Community-Option-2--1--2.svg)


One great feature of Streamlit is theming, so you can control your app's color scheme. But creating a new color scheme can be hard. And making it visually accessible can be even harder.

So I made a color theme editor app with four color parameters of the Streamlit themes, which general-purpose color editors/generators don't even consider: `primaryColor`, `backgroundColor`, `secondaryBackgroundColor`, and `textColor`. I also followed the color contrast guidelines from the [Web Content Accessibility Guidelines (WCAG) 2.0 standard](https://www.w3.org/TR/WCAG20/?ref=streamlit.ghost.io) for the app's visual accessibility.

![streamlit-theme-editor](https://streamlit.ghost.io/content/images/2023/05/streamlit-theme-editor.gif#browser)

In this post, I'll show you how to build this app in eight steps:

1. Define preset colors
2. If set, load the theme config
3. Manage the edited color parameters in the session state
4. Set colors programmatically
5. Define a composed widget of a color picker and a slider
6. Use the WCAG contrast table
7. Show generated configs
8. Apply the edited theme to the app

👉

You can assess the app [here](https://editcolor.streamlit.app/?ref=streamlit.ghost.io) and the source code [here](https://github.com/whitphx/streamlit-theme-editor?ref=streamlit.ghost.io). This article is based on the revision `7213dbb`.

## Five key components of the color theme editor app

The app consists of five components to help you create and test accessible color themes:

1. **"Generate a random color scheme" button.** Click this button to update the color theme with randomly selected colors that maintain high contrast between foreground and background.
2. **Color pickers.** Use these components to adjust colors and their luminance parameters. Use the luminance slider to adjust contrast while preserving the color's aesthetic.
3. **WCAG contrast ratio table.** Display a 2x2 matrix of contrast ratios for the selected colors and the corresponding WCAG 2.0 level (AA or AAA) for each ratio to make your color theme accessible.
4. **Config generator.** Generate content for the `.streamlit/config.toml` config file and a shell command with color theme arguments. Just copy/paste it into your project to apply the edited theme.
5. **"Apply theme on this page" checkbox.** Check this box to apply the color theme you are editing to the whole application, letting you preview the colors in a real Streamlit app and synchronize the changes.

## 1. Define preset colors

The app has preset colors that I picked from the Streamlit source code below:

* [Base theme](https://github.com/streamlit/streamlit/blob/1.19.0/frontend/src/theme/baseTheme/themeColors.ts?ref=streamlit.ghost.io)
* [Light theme](https://github.com/streamlit/streamlit/blob/1.19.0/frontend/src/theme/lightTheme/themeColors.ts?ref=streamlit.ghost.io)
* [Dark theme](https://github.com/streamlit/streamlit/blob/1.19.0/frontend/src/theme/darkTheme/themeColors.ts?ref=streamlit.ghost.io)

```
preset_colors: list[tuple[str, ThemeColor]] = [
    ("Default light", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#ffffff",
            secondaryBackgroundColor="#f0f2f6",
            textColor="#31333F",
        )),
    ("Default dark", ThemeColor(
            primaryColor="#ff4b4b",
            backgroundColor="#0e1117",
            secondaryBackgroundColor="#262730",
            textColor="#fafafa",
    ))
]
```

## 2. If set, load the theme config

This is a bit of a hack. You can access the global config object via `st._config` to get the `theme` config from it and to use it as a preset color:

```
@st.cache_resource
def get_config_theme_color():
    config_theme_primaryColor = st._config.get_option('theme.primaryColor')
    config_theme_backgroundColor = st._config.get_option('theme.backgroundColor')
    config_theme_secondaryBackgroundColor = st._config.get_option('theme.secondaryBackgroundColor')
    config_theme_textColor = st._config.get_option('theme.textColor')
    if config_theme_primaryColor and config_theme_backgroundColor and config_theme_secondaryBackgroundColor and config_theme_textColor:
        return ThemeColor(
            primaryColor=config_theme_primaryColor,
            backgroundColor=config_theme_backgroundColor,
            secondaryBackgroundColor=config_theme_secondaryBackgroundColor,
            textColor=config_theme_textColor,
        )

    return None
```

```
theme_from_initial_config = util.get_config_theme_color()
if theme_from_initial_config:
    preset_colors.append(("From the config", theme_from_initial_config))
```

## 3. Manage the edited color parameters in the session state

Store the RGB color values in the session state using the same keys as the color picker widgets. This lets you programmatically set the color picker values. It's useful when updating them with new values from the random color generator. These values are synced with the color picker widgets, so they must be compatible with their `#RRGGBB` format.

Aside from managing RGB values, you also maintain the HSL values in the session state to control the slider widgets. Using the HSL format makes it easier to edit colors more intuitively. To synchronize these two formats, create a utility function named `set_color` and use it every time you update the color values:

```
def sync_rgb_to_hls(key: str):
    # HLS states are necessary for the HLS sliders.
    rgb = util.parse_hex(st.session_state[key])
    hls = colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    st.session_state[f"{key}H"] = round(hls[0] * 360)
    st.session_state[f"{key}L"] = round(hls[1] * 100)
    st.session_state[f"{key}S"] = round(hls[2] * 100)

def set_color(key: str, color: str):
    st.session_state[key] = color
    sync_rgb_to_hls(key)

if 'preset_color' not in st.session_state or 'backgroundColor' not in st.session_state or 'secondaryBackgroundColor' not in st.session_state or 'textColor' not in st.session_state:
    set_color('primaryColor', default_color.primaryColor)
    set_color('backgroundColor', default_color.backgroundColor)
    set_color('secondaryBackgroundColor', default_color.secondaryBackgroundColor)
    set_color('textColor', default_color.textColor)
```

## 4. Set colors programmatically

To set the currently edited colors from the selectbox widget with the preset colors, use `set_color()`:

```
def on_preset_color_selected():
    _, color = preset_colors[st.session_state.preset_color]
    set_color('primaryColor', color.primaryColor)
    set_color('backgroundColor', color.backgroundColor)
    set_color('secondaryBackgroundColor', color.secondaryBackgroundColor)
    set_color('textColor', color.textColor)

st.selectbox("Preset colors", key="preset_color", options=range(len(preset_colors)), format_func=lambda idx: preset_colors[idx][0], on_change=on_preset_color_selected)
```

You can also implement a random color generator button:

```
if st.button("🎨 Generate a random color scheme 🎲"):
    primary_color, text_color, basic_background, secondary_background = util.generate_color_scheme()
    set_color('primaryColor', primary_color)
    set_color('backgroundColor', basic_background)
    set_color('secondaryBackgroundColor', secondary_background)
    set_color('textColor', text_color)
```

To implement `util.generate_color_scheme`, refer to [this code](https://github.com/whitphx/streamlit-theme-editor/blob/7213dbb379b63f4d97ed0da31765ee12773c3696/util.py?ref=streamlit.ghost.io#L77-L84). It generates colors with the constraint that the colors' luminance (the "L" in the HSL format) parameters have enough difference.

## 5. Define a composed widget of a color picker and a slider

This app provides a pair of a color picker and a slider to control the color's luminance parameter (to adjust the color contrast while maintaining its original appearance). There are four pairs of components. Each is defined by a function called `color_picker` to make it reusable.

One trick here is to set the `on_change` callback of each component to synchronize the RGB data and the HSL data in the session state:

![color-picker-and-slider](https://streamlit.ghost.io/content/images/2023/04/color-picker-and-slider.png#border)

```
def color_picker(label: str, key: str, default_color: str) -> None:
    col1, col2 = st.columns([1, 3])
    with col1:
        color = st.color_picker(label, key=key, on_change=sync_rgb_to_hls, kwargs={"key": key})
    with col2:
        r,g,b = util.parse_hex(default_color)
        h,l,s = colorsys.rgb_to_hls(r,g,b)
        if f"{key}H" not in st.session_state:
            st.session_state[f"{key}H"] = round(h * 360)

        st.slider(f"L for {label}", key=f"{key}L", min_value=0, max_value=100, value=round(l * 100), format="%d%%", label_visibility="collapsed", on_change=sync_hls_to_rgb, kwargs={"key": key})

        if f"{key}S" not in st.session_state:
            st.session_state[f"{key}S"] = round(s * 100)

    return color
```

```
primary_color = color_picker('Primary color', key="primaryColor", default_color=default_color.primaryColor)
text_color = color_picker('Text color', key="textColor", default_color=default_color.textColor)
background_color = color_picker('Background color', key="backgroundColor", default_color=default_color.backgroundColor)
secondary_background_color = color_picker('Secondary background color', key="secondaryBackgroundColor", default_color=default_color.secondaryBackgroundColor)
```

## 6. Use the WCAG contrast table

This table layout is created using stacked `st.column()`. The content of each cell is encapsulated within a reusable helper function, such as `synced_color_picker` or `fragments.contrast_summary`:

![WCAG-contrast-table](https://streamlit.ghost.io/content/images/2023/04/WCAG-contrast-table.png#border)

```
col1, col2, col3 = st.columns(3)
with col2:
    synced_color_picker("Background color", value=background_color, key="backgroundColor")
with col3:
    synced_color_picker("Secondary background color", value=secondary_background_color, key="secondaryBackgroundColor")

col1, col2, col3 = st.columns(3)
with col1:
    synced_color_picker("Primary color", value=primary_color, key="primaryColor")
with col2:
    fragments.contrast_summary("Primary/Background", primary_color, background_color)
with col3:
    fragments.contrast_summary("Primary/Secondary background", primary_color, secondary_background_color)

col1, col2, col3 = st.columns(3)
with col1:
    synced_color_picker("Text color", value=text_color, key="textColor")
with col2:
    fragments.contrast_summary("Text/Background", text_color, background_color)
with col3:
    fragments.contrast_summary("Text/Secondary background", text_color, secondary_background_color)
```

`synced_color_picker()` is just a color picker component, but its value is synchronized with the relevant color picker component that appeared above. Its value is also managed in the session state with the `value` argument and the `on_change` callback:

```
def synced_color_picker(label: str, value: str, key: str):
    def on_change():
        st.session_state[key] = st.session_state[key + "2"]
        sync_rgb_to_hls(key)
    st.color_picker(label, value=value, key=key + "2", on_change=on_change)
```

`fragments.contrast_summary()` renders the WCAG contrast info. See [this code](https://github.com/whitphx/streamlit-theme-editor/blob/7213dbb379b63f4d97ed0da31765ee12773c3696/fragments.py?ref=streamlit.ghost.io#L7-L22) for its implementation.

## 7. Show generated configs

The app shows these ready-to-use code snippets and is done with `st.code()`:

![config-file](https://streamlit.ghost.io/content/images/2023/04/config-file.png#border)

```
st.subheader("Config file (`.streamlit/config.toml`)")
st.code(f"""
[theme]
primaryColor="{primary_color}"
backgroundColor="{background_color}"
secondaryBackgroundColor="{secondary_background_color}"
textColor="{text_color}"
""", language="toml")

st.subheader("Command line argument")
st.code(f"""
streamlit run app.py \\\\
    --theme.primaryColor="{primary_color}" \\\\
    --theme.backgroundColor="{background_color}" \\\\
    --theme.secondaryBackgroundColor="{secondary_background_color}" \\\\
    --theme.textColor="{text_color}"
""")
```

## 8. Apply the edited theme to the app

For reviewing purposes, this app can apply the currently edited theme to itself. You can do it with the `st._config` object, as shown below:

```
if st.checkbox("Apply theme to this page"):
    st.info("Select 'Custom Theme' in the settings dialog to see the effect")

    def reconcile_theme_config():
        keys = ['primaryColor', 'backgroundColor', 'secondaryBackgroundColor', 'textColor']
        has_changed = False
        for key in keys:
            if st._config.get_option(f'theme.{key}') != st.session_state[key]:
                st._config.set_option(f'theme.{key}', st.session_state[key])
                has_changed = True
        if has_changed:
            st.experimental_rerun()

    reconcile_theme_config()

    fragments.sample_components("body")
    with st.sidebar:
        fragments.sample_components("sidebar")
```

Use `st._config.set_option()` to update the configuration values. Reload the app for the changes to take effect by using `st.experimental_rerun()`. It was inspired by `jrieke/streamlit-theme-generator` (here is the [code](https://github.com/jrieke/streamlit-theme-generator/blob/79861b81e415a97590e69d4a0a2efe624a91ad0b/streamlit_app.py?ref=blog.streamlit.io#L86-L99)).

## Wrapping up

The Streamlit color theme editor app offers a simple and effective solution for creating visually appealing and accessible color themes for your apps. Thanks to the WCAG 2.0 standard and the real-time preview, your themes will now be attractive and accessible to all users.

Happy app-building! 🧑‍💻
