# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the EnabledSoftware is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

############## IMPORTS

import os
import re
import socket
import subprocess
import iwlib
import psutil
from libqtile import qtile
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile import layout, bar, widget, hook
from libqtile.utils import guess_terminal
from typing import List
# from libqtile.backend.wayland import InputConfig


# wl_input_rules = {
#     "ELAN050A:00 04F3:3158 Touchpad": InputConfig(left_handed=True,tap=True,click_method="clickfinger"),
#     "*": InputConfig(left_handed=True, pointer_accel=True, tap=True),
#     "type:keyboard": InputConfig(kb_options="ctrl:nocaps,compose:ralt"),
# }
########## ENVIRONMENT VARIABLES #############

mod = "mod4"
terminal = guess_terminal()
myTerm = terminal
myBrowser = "firefox"

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

############ KEYS ########################

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    # Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "l", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "h", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "l", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "h", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "h", lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(), desc="shrink the window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="toggle fullscreen"),
    Key([mod], "m", lazy.window.toggle_floating()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod, "control"], "b", lazy.spawn(myBrowser),
        desc="opens up a default browser"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "amixer -c 0 sset Master 1- unmute")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "amixer -c 0 sset Master 1+ unmute")),
    Key([mod,"shift"],"P",lambda: qtile.cmd_spawn(myTerm + " -e xfce4-screenshooter")),
    Key([mod, "shift"], "Print", lazy.spawn('gnome-screenshot --interactive')),
]

groups = [Group(i) for i in "123456789"]

######### EXTENDED KEYS ######################

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(
                    i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": "#ea1cff",
    "border_normal": "1d2330"
}

########## LAYOUTS #################

layouts = [
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
        font="Ubuntu",
        fontsize="16",
        sections=["FIRST", "SECOND", "THIRD", "FOURTH"],
        section_fontsize=14,
        border_width=3,
        bg_color="1c1f24",
        active_bg="c678dd",
        active_fg="000000",
        inactive_bg="a9a1e1",
        inawctive_fg="1c1f240",
        padding_left=0,
        padding_x=0,
        padding_y=5,
        section_top=15,
        section_bottom=15,
        level_shift=8,
        vspace=3,
        panel_width=200
    ),
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

############ WIDGET DEFAULTS

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

########## BACKGROUND COLORS

background_colors = {
    "primary": "#66a6ff",
    "dark":"#000000",
    "blue-100":"#66a6ff",
    "purple-100":"#9932cc"
}

######### COLORS ###############

colors = {
    "primary": "#ffffff",
    "separator":"#ff1493",
    "dark":"#000000"
}

################ WIDGETS #############

def init_widgets_list():
    widgets_list = [
        widget.Image(
            filename="~/.config/qtile/icons/arch.jpg",
            margin_x=0,
            margin_y=0,
            scale=True,
            mouse_callbacks={'Button1': lazy.spawn(myTerm)}
        ),
        widget.Battery(
            background=background_colors["primary"],
            charge_char="^",
            discharge_char="V",
            empty_char="x",
            font="Fira Code",
            fontsize=14,
            foreground=colors["primary"],
            format='{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f} W',
            full_char="=",
            padding=15
        ),
        widget.TextBox(
	text = "▶",
	padding = -5,
	fontsize = 37,
	background = background_colors["purple-100"],
	foreground = background_colors["blue-100"]
	),
        widget.CheckUpdates(
update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors["primary"],
                       colour_have_updates = colors["primary"],
                       colour_no_updates = colors["primary"],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = background_colors["purple-100"],
		       no_update_string = "no updates",
		       font="Fira Code",
		       fontsize = 14

        ),
	widget.TextBox(
	text="▶",
	padding=-5,
	fontsize=37,
	background=background_colors["blue-100"],
	foreground=background_colors["purple-100"]
	),
        widget.Clock(
            background=background_colors["blue-100"],
            fontsize=14,
            font="Fira Code",
            format='%Y-%M-%D',
            padding=25
        ),
        widget.TextBox(
            padding=-5,
            background=background_colors["purple-100"],
            foreground=background_colors["blue-100"],
	    fontsize=37,
    	    text="▶"
        ),
        widget.Clock(
            background=background_colors["purple-100"],
            fontsize=14,
            font="Fira Code",
            format='%H:%M:%S',
            padding=25
        ),
        widget.TextBox(
            text = "▶",
            background = background_colors["blue-100"],
            foreground =  background_colors["purple-100"],
            padding = -5,
            fontsize = 37
        ),
        widget.Memory(
            background=background_colors["primary"],
            foreground=colors["primary"],
            font="Fira Code",
            measure_mem="G",
            format="  {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}   ",
            mouse_callbacks={'Button1': lazy.spawn(myTerm + " -e htop")},
        ),
	widget.TextBox(
            padding=-5,
            background=background_colors["purple-100"],
            foreground=background_colors["blue-100"],
	    fontsize=37,
    	    text="▶"
        ),
        widget.CPU(
            background=background_colors["purple-100"],
            foreground=colors["primary"],
            fontsize=13,
            format="CPU {freq_current}GHz {load_percent}%",
            padding=15,
            font="Fira Code",
            mouse_callbacks={
                "Button1": lambda: qtile.cmd_spawn(myTerm + "-e htop")}
        ),
	 widget.TextBox(
            text = "▶",
            background = background_colors["blue-100"],
            foreground =  background_colors["purple-100"],
            padding = -5,
            fontsize = 37
        ),
        widget.Wlan(
            background=background_colors["blue-100"],
            font="Fira Code",
            fontsize=14,
            disconnected_message="Disconnected :(",
            format="{essid} {percent:2.0%}",
            interface="wlan0",
            padding=15
        ),
	
	widget.TextBox(
            padding=-5,
            background="#000000",
            foreground=background_colors["blue-100"],
	    fontsize=37,
    	    text="▶"
        ),
        widget.Image(
            filename = "~/.config/qtile/icons/obs.png",
            margin_x = 0,
            margin_y = 0,
            scale = 2,
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(myTerm + " -e flatpak run com.obsproject.Studio")}
        ),
        widget.Image(
            filename = "~/.config/qtile/icons/vscode.png",
            margin_x = 0,
            margin_y = 0,
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(myTerm + " -e code")}
        ),
        widget.Image(
                filename = "~/.config/qtile/icons/telegram.png",
            margin_x = 0,
            margin_y = 0,
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(myTerm + " -e telegram-desktop")}
        ),
        widget.Image(
            filename = "~/.config/qtile/icons/firefox.png",
            margin_x = 0,
            margin_y = 0,
            mouse_callbacks = {"Button1": lambda: qtile.cmd_spawn(myTerm + " -e firefox")}
        ),
	widget.Image(
	   filename="~/.config/qtile/icons/telegram.svg",
	   margin_x = 15,
	   margin_y = 0,
	  mouse_callbacks = {"Button1":lambda: qtile.cmd_spawn(myTerm  + " -e telegram-desktop")}	
	),
    ]
    return widgets_list


def init_widgets_screen():
    widgets_screen = init_widgets_list()
    return widgets_screen


####### SCREENS #############

def init_screens():
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen(), opacity=1.0, size=20))
    ]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
