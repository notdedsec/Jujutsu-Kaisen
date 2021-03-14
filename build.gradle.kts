import myaa.subkt.ass.*
import myaa.subkt.tasks.*
import myaa.subkt.tasks.Mux.*
import myaa.subkt.tasks.Nyaa.*
import java.awt.Color
import java.time.*

plugins {
    id("myaa.subkt")
}

subs {
    readProperties("sub.properties", "private.properties")
    episodes(getList("episodes"))
    release(arg("release") ?: "TV")

    merge {
        from(get("dialogue")) {
            incrementLayer(10)
        }

        from(getList("typesets"))

        if(propertyExists("OP")) {
            from(get("OP")) {
                syncTargetTime(getAs<Duration>("opsync"))
            }
        }

        if(propertyExists("EC")) {
            from(get("EC")) {
                syncTargetTime(getAs<Duration>("ecsync"))
            }
        }

        if(propertyExists("ED")) {
            from(get("ED")) {
                syncTargetTime(getAs<Duration>("edsync"))
            }
        }
    }

    swap {
        from(merge.item())
    }

    chapters {
        from(get("dialogue"))
    }

    mux {
        title(get("title"))

        from(get("premux")) {
            tracks {
                lang("jpn")

                if(track.type == TrackType.VIDEO){
                    name("1080p x264 WEB")
                }

                if(track.type == TrackType.AUDIO){
                    name("128k AAC WEB")
                }
            }

            attachments {
                include(false)
            }
        }

        from(merge.item()) {
            tracks {
                name("Kaizoku")
                lang("eng")
                default(true)
            }
        }

        from(swap.item()) {
            tracks {
                name("Kaizoku (Honorifics)")
                lang("enm")
            }
        }

        chapters(chapters.item()) {
            lang("eng")
            charset("UTF-8")
        }

        attach(get("fonts")) {
            includeExtensions("ttf", "otf")
        }

        attach(get("commonfonts")) {
            includeExtensions("ttf", "otf")
        }

        skipUnusedFonts(true)
        out(get("muxfile"))
    }

    torrent {
        trackers(getList("tracker"))
        from(mux.item())
        out(get("torrent"))
    }

    nyaa {
        from(torrent.item())
        username(get("nyaauser"))
        password(get("nyaapass"))
        category(NyaaCategories.ANIME_ENGLISH)
        information(get("gitrepo"))
        torrentDescription(getFile("description.vm"))
        hidden(false)
    }
}
