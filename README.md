# [Kaizoku] Jujutsu Kaisen

## Scripts used for Kaizoku's release of [Jujutsu Kaisen](https://anidb.net/anime/15275)

The subtitles are based on Crunchyroll's translation, with a fair bit of editing and some translation checking, timing fixes, song translations and ~~lazy~~ creative typesetting with ~~stolen~~ borrowed masks. An alternate honorifics track is included too. They're muxed with a descaled and somewhat scene-filtered encode, the base scripts for which can be found inside the [common](https://github.com/notdedsec/Jujutsu-Kaisen/blob/master/common) folder.

---

The terminology here is closer to the manga's. For character names, Gojou is Gojo, Yuuji is Yuji and so on. Technique names are mostly from the anime. We've picked the option that reads better, like Veil instead of Curtain. The official scripts are just as you'd expect. Not getting the point and failing hard at memes. About the typesetting, we've done some signs by ourselves and taken some from other releases, mostly from Asahi-Anime Land and Kuro Diamond, and modified them as needed. We also looked into typesetting from StormFS, Pantsu and Devil.

---

This project utilizes [SubKt](https://github.com/Myaamori/subkt/) for handling all the post-processing work, like merging songs, dialogue and typesetting scripts, generating chapters, release muxing, creating torrents as well as posting them.

It uses another little [script](https://github.com/notdedsec/Jujutsu-Kaisen/blob/main/preprocess.py) I made for saving me a few clicks each week by pre-processing files and setting up the work folder and scripts for every episode, among other things, based on SubKt configuration. It's not intended to be a general purpose script but I've left some docstrings so modifying it for other projects shouldn't be too difficult if you can make sense of my garbage code.

---

Feel free to use any part of this release as you wish, just not before release. I'll be forced to make this repository private otherwise. Also, note that we've made a slight shift in the ED1 audio to make everything sync better. I hope you apply the same in any remuxes that use these subs. The code for doing so is [right here](https://github.com/notdedsec/Jujutsu-Kaisen/blob/main/common/jujutsu.py#L26).

Spot any mistakes? Feel free to open an issue or just let us know on [Discord](https://discord.animekaizoku.com).

You can find this release and all our [other releases](https://github.com/notdedsec/Fansubbing) on Nyaa and AnimeKaizoku.
