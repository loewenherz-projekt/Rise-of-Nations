
# Official Repository of the Rise of Nations Mod
### Media
[![Steam][steam-badge]][steam-link]   [![Discord][discord-badge]][discord-link]   [![Patreon][patreon-badge]][patreon-link]   [![Youtube][youtube-badge]][youtube-link]   [![Reddit][reddit-badge]][reddit-link]

### Git Info
![github-size]  ![github-activity] ![github-latest] ![github-beta-backlog] ![github-stars]

### Localization
To translate the entire English localization directory into German run:

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
pip install google-cloud-translate
python scripts/translate_directory_to_german.py localisation/english localisation/german
```

These helper scripts rely on the official **Google Translate API**. You will
need a service account JSON key to authenticate. Create a Google Cloud project,
enable the **Cloud Translation API** and download a service account key file.
Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to that
file before running the translation commands. Each English `.yml` file is then
converted into its German counterpart (with `_l_german` filenames) using
Google's translation service.

[patreon-badge]: https://img.shields.io/static/v1?label=Patreon&message=Donate&color=orange&logo=patreon&style=for-the-badge
[patreon-link]: http://patreon.com/RONMOD

[steam-badge]: https://img.shields.io/static/v1?label=Steam&message=Download&color=lightgrey&logo=steam&style=for-the-badge
[steam-link]: https://steamcommunity.com/sharedfiles/filedetails/?id=2026448968

[youtube-badge]: https://img.shields.io/static/v1?label=Youtube&message=Watch&color=red&logo=youtube&style=for-the-badge
[youtube-link]: https://www.youtube.com/channel/UCgWkliJFfrhy4yHePtkmrzw

[discord-badge]: https://img.shields.io/static/v1?label=Discord&message=Chat&color=blue&logo=discord&style=for-the-badge
[discord-link]: https://discord.gg/3VpWTnDn8B

[reddit-badge]: https://img.shields.io/static/v1?label=Reddit&message=Discuss&color=orange&logo=reddit&style=for-the-badge
[reddit-link]: https://www.reddit.com/r/RiseOfNationMod/

[github-size]: https://img.shields.io/github/repo-size/stuffi3000/Rise-of-Nations?label=MOD%20SIZE&style=for-the-badge
[github-stars]: https://img.shields.io/github/stars/stuffi3000/Rise-of-Nations?style=for-the-badge

[github-latest]: https://img.shields.io/github/last-commit/stuffi3000/Rise-of-Nations?label=Latest%20Commit&color=blue&style=for-the-badge
[github-activity]: https://img.shields.io/github/commit-activity/m/stuffi3000/Rise-of-Nations?label=Team%20Activity&style=for-the-badge
[github-beta-backlog]: https://img.shields.io/github/commits-since/stuffi3000/Rise-of-Nations/1.6.5?label=Ahead%20Of%20Steam&style=for-the-badge&color=blue
[discord-link]: https://img.shields.io/discord/696379419895398411?color=lightgrey&label=DISCORD&style=for-the-badge
