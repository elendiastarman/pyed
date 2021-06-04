# Pyedeas

Pied (many-colored) ideas, with Pyed as its core language.

Goal: customizable interfaces to info/data that can be embedded in many places.



## Stepping Stones

* Tiles snapping to each other: https://jsfiddle.net/elendiastarman/yd2jz48n/latest/
* Categorizing groups to look for oddities: https://jsfiddle.net/elendiastarman/94hb2wjL/latest/
* ... PyedASM
* ? Keyboard inputs



## General feature ideas

* Panels that can be freely moved around
  * ctx-specific functionality can be an attached panel
  * available keyboard shortcuts in corner
  * situated within `spatienv` - a spatial environment
* GUI layer, overlay layer, content layer, background layer
* Functionality can be tweaked and exposed via Pyed
  * context menu?
* Draggable tiles
  * located relative to each other
  * can snap along edges
* Input/output sockets that can be connected with wires/pipes
  * preview + snapping
  * long-range connections go into background layer
  * use color/shape/etc to help distinguish types
* Timeline
  * store snapshots + deltas to help with scrolling
  * adjustable scale
* Settings + keybindings
  * should be able to support controllers
    * ideal: support two buttons or one button with varying time
  * ideal: tweak settings and see effects live
* "Two options for everything" (where feasible, and it's really 2+)
  * Snapping grid - square or hex
  * Input device - keyboard and/or mouse, or controller
  * Language of choice - Pyed or JS
  * Panel choice - `<list>`
  * Features enabled/disabled
* Display more based on relative offset
  * ideal: fade in stuff
* Assistive AI?
  * Uses Pyed to do things
* Search based on similarity and/or correlation
* Keyboard selection of on-screen elements in manner like Sublime's Ctrl+P
* Optional cookies
* Feature completeness tiers
  * Scrap: the feature is deprecated
  * Raw: the feature is under development
  * Disrepair: the feature is broken
  * Tarnished: the feature has flaws
  * Tin: the feature exists
  * Bronze: the feature is usable
  * Silver: the feature reduces frustration
  * Gold: the feature adds convenience
  * Platinum: the feature expands