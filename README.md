# Home Assistant Blueprints - Alexa Devices

A collection of Home Assistant [blueprints](https://www.home-assistant.io/docs/blueprint/)
centered around the official
[`alexa_devices` integration](https://www.home-assistant.io/integrations/alexa_devices/#list-of-actions).

The first blueprint in this repository is **Alexa Devices - Send Action**: a single
`script` blueprint that wraps all three actions of the `alexa_devices` integration
into one configurable script.

- `alexa_devices.send_info_skill` - run a built-in info skill (weather, date,
  time, flash briefing, ...)
- `alexa_devices.send_sound` - play a built-in Alexa sound (doorbell chime,
  barking dog, ...)
- `alexa_devices.send_text_command` - send a text command as if you had spoken
  it aloud ("set volume to 5", "what's the time", ...)

Inspired by [TheAppleFreak/home-assistant-blueprints](https://github.com/TheAppleFreak/home-assistant-blueprints).

## Add this blueprint

[![Open your Home Assistant instance and import this blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fgourmet-jets%2Fhome-assistant-blueprints%2Fblob%2Fmain%2Fscripts%2Falexa_devices.yaml)

> The button works with any HA instance that has the
> [My Home Assistant](https://my.home-assistant.io/) integration enabled
> (default for installations created via the onboarding wizard). It opens your
> HA instance and imports `scripts/alexa_devices.yaml` in one click.

## Repository layout

```text
scripts/
└── alexa_devices.yaml    # the blueprint
README.md                 # this file
```

## Prerequisites

- **Home Assistant 2025.6.0 or later** (requires `field.condition:` support for
  showing/hiding input fields based on the selected action type).
- The [**Alexa Devices integration**](https://www.home-assistant.io/integrations/alexa_devices/)
  installed, configured and enabled. At least one Alexa device (Echo, Echo Dot,
  Echo Show, ...) must be paired so the `alexa_devices` entity domain is
  available.

## Installation

### Option 1: One-click import (recommended)

Click the **Add this blueprint** button at the top of this README. Home
Assistant fetches the blueprint from this repository and adds it to your local
`blueprints/script/alexa_devices.yaml`.

### Option 2: Manual copy

1. Download [`scripts/alexa_devices.yaml`](scripts/alexa_devices.yaml) from this
   repository.
2. Place it in your HA config directory at
   `blueprints/script/alexa_devices.yaml`.
3. Reload blueprints (or restart Home Assistant):
   **Settings** -> **Automations & Scenes** -> **Blueprints** -> three-dot menu
   -> **Reload Blueprints**, or via the `blueprint.reload` service.

## Usage

1. Go to **Settings** -> **Automations & Scenes** -> **Scripts**.
2. Click **+ Add Script** -> select **Use Blueprint**.
3. Pick **"Alexa Devices - Send Action"** from the list.
4. Give the script a name.
5. Configure:
   - **Action Type** - choose one of `info_skill` / `send_sound` /
     `send_text_command`.
   - The relevant parameter field for the chosen action type appears (the
     others stay hidden, toggled by the conditional field checkboxes).
   - **Alexa Devices** - select one or more devices (shows the real Alexa
     device names, not entities), or leave empty to broadcast to every Alexa
     device known to Home Assistant.
6. Save the script.
7. Run it from the Scripts overview, a dashboard button, an automation, or by
   calling `script.turn_on` with the script's entity id.

### Example use cases

- **Tell every Echo the weather:** Action Type = `info_skill`, skill =
  `weather`, devices = (leave empty).
- **Doorbell chime on a specific Echo:** Action Type = `send_sound`, sound =
  `Doorbell Chime 01`, devices = one Echo.
- **Set volume by text command:** Action Type = `send_text_command`,
  text_command = `set the volume to 5`, devices = one Echo.

## Raw blueprint URL

For manual download, `!include`, or referencing from another repo:

```text
https://github.com/gourmet-jets/home-assistant-blueprints/blob/main/scripts/alexa_devices.yaml
```

## License

See [LICENSE](LICENSE).
