from typing import Any
import requests
import json


class LifxAPI:

    api_token: str = ""

    def __init__(self, api_token: str) -> None:
        self.api_token = api_token

    def toggle_power(self, selector: str = "all", duration: float = 1.0) -> Any:
        """
        Turn off lights if any of them are on, or turn them on if they are all off.
        All lights matched by the selector will share the same power state after this action.
        Physically powered off lights are ignored.

        Parameters:
            selector (str): The selector to limit which lights are toggled.
            duration (float): The time is seconds to spend perfoming the power toggle.
        """
        headers = {
            "Authorization": "Bearer %s" % self.api_token,
            "Duration": str(duration),
        }

        response = requests.post(f"https://api.lifx.com/v1/lights/{selector}/toggle", headers=headers)
        return json.loads(response.text)

    def list_lights(this, selector: str = "all") -> Any:
        """
        Gets lights belonging to the authenticated account. Filter the lights using selectors.
        Properties such as id, label, group and location can be used in selectors.
        Most endpoints accept selectors when performing actions.

        Parameters:
            selector (str): The selector to limit which lights are toggled.
        """
        headers = {
            "Authorization": "Bearer %s" % this.api_token,
        }

        response = requests.get(f"https://api.lifx.com/v1/lights/{selector}", headers=headers)
        return json.loads(response.text)

    def set_state(
        self,
        selector: str = "all",
        power: str = "on",
        color: str = "white",
        brightness: float = 1.0,
        duration: float = 1.0,
        infrared: float = 1.0,
        fast: bool = False,
    ) -> Any:
        """
        Sets the state of the lights within the selector. All parameters (except for the selector) are optional.
        If you don't supply a parameter, the API will leave that value untouched.

        Parameters:
            selector (str): The selector to limit which lights are toggled.
            power (str): The power state you want to set on the selector. on or off
            color (str): The color to set the light to.
            brightness (float): The brightness level from 0.0 to 1.0. Overrides any brightness set in color (if any).

            duration (float): How long in seconds you want the power action to take. Range: 0.0 – 3155760000.0 (100 years).
            infrared (float): The maximum brightness of the infrared channel from 0.0 to 1.0.
            fast (bool): Execute the query fast, without initial state checks and wait for no results.

        """
        headers = {
            "Authorization": "Bearer %s" % self.api_token,
        }

        payload = {
            "power": power,
            "color": color,
            "brightness": str(brightness),
            "duration": str(duration),
            "infrared": str(infrared),
            "fast": fast,
        }

        response = requests.put(
            f"https://api.lifx.com/v1/lights/{selector}/state",
            data=payload,
            headers=headers,
        )

        # When fast is enabled there is no API response
        if not fast:
            return json.loads(response.text)
