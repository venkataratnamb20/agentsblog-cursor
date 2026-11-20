"""Consent banner that stores a local choice only.

The banner does not set a cookie and does not call the network.
Non-essential storage stays off until the reader clicks Accept or
Reject.
"""

from __future__ import annotations

_STORAGE_KEY = "agentsblog-consent"
_NOTE = "This preview does not set cookies."


def consent_markup() -> str:
    """Return the consent banner and its local-only script.

    The script reads ``agentsblog-consent`` from localStorage. A saved
    choice hides the banner. Accept stores ``accepted`` and Reject
    stores ``rejected``.

    Returns:
        HTML for the banner. The script does not set a cookie or call
        the network.
    """
    return _banner() + _script()


def _banner() -> str:
    """Return the banner element without its script.

    Returns:
        The banner markup, with Accept and Reject buttons.
    """
    return (
        '<div id="cookie-consent">'
        f"<p>{_NOTE}</p>"
        '<button id="consent-accept" type="button">Accept</button>'
        '<button id="consent-reject" type="button">Reject</button>'
        "</div>"
    )


def _script() -> str:
    """Return the script that records the reader's choice.

    Returns:
        An inline script. It writes localStorage and then hides the
        banner. It does not set ``document.cookie`` or call the network.
    """
    return f"""\
<script>
(function () {{
  var banner = document.getElementById("cookie-consent");
  var key = "{_STORAGE_KEY}";
  function hide() {{
    banner.setAttribute("hidden", "");
  }}
  function chosen() {{
    try {{
      return localStorage.getItem(key);
    }} catch (error) {{
      return "";
    }}
  }}
  if (chosen()) {{
    hide();
    return;
  }}
  function choose(value) {{
    try {{
      localStorage.setItem(key, value);
    }} catch (error) {{
      return;
    }}
    hide();
  }}
  document.getElementById("consent-accept").addEventListener(
    "click",
    function () {{
      choose("accepted");
    }}
  );
  document.getElementById("consent-reject").addEventListener(
    "click",
    function () {{
      choose("rejected");
    }}
  );
}})();
</script>
"""
