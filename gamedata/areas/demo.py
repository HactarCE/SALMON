from game import Area

DEMO_1 = Area(
    name='Demo 1 (small)',
    s=r'''
    ~

         This.is.what.a.really
         small.area.looks.like

                                 ~
    '''
)

DEMO_2 = Area(
    name='Demo 2 (big)',
    s=r'''
    ~

        ._______..._......._..........._......................_..............._...................................
        |__...__|.|.|.....(_).........(_)....................|.|.............|.|..................................
        ...|.|....|.|__...._...___....._...___....__......__.|.|__.....__._..|.|_.................................
        ...|.|....|.'_.\..|.|./.__|...|.|./.__|...\.\./\././.|.'_.\.../._`.|.|.__|................................
        ...|.|....|.|.|.|.|.|.\__.\...|.|.\__.\....\.V..V./..|.|.|.|.|.(_|.|.|.|_.................................
        ...|_|....|_|.|_|.|_|.|___/...|_|.|___/.....\_/\_/...|_|.|_|._\__,_|..\__|_............._......._.........
        ..................................|.|.......................|.|..........|.|...........|.|.....(_)........
        ..__._....._.__.___.....___.....__|.|...___..._.__....__._..|.|_....___..|.|.._..._....|.|__...._....__._.
        ./._`.|...|.'_.`._.\.../._.\.../._`.|../._.\.|.'__|../._`.|.|.__|../._.\.|.|.|.|.|.|...|.'_.\..|.|../._`.|
        |.(_|.|...|.|.|.|.|.|.|.(_).|.|.(_|.|.|..__/.|.|....|.(_|.|.|.|_..|..__/.|.|.|.|_|.|...|.|_).|.|.|.|.(_|.|
        .\__,_|...|_|.|_|.|_|..\___/...\__,_|..\___|.|_|.....\__,_|..\__|..\___|_|_|_.\__,.|...|_.__/..|_|..\__,.|
        ................................|.|.................|.|............|.|.(_).|.|.__/.|.................__/.|
        ..__._..._.__....___....__._....|.|...___.....___...|.|.__..___....|.|.._..|.||___/.___.............|___/.
        ./._`.|.|.'__|../._.\../._`.|...|.|../._.\.../._.\..|.|/././.__|...|.|.|.|.|.|/./../._.\..................
        |.(_|.|.|.|....|..__/.|.(_|.|...|.|.|.(_).|.|.(_).|.|...<..\__.\...|.|.|.|.|...<..|..__/.._...............
        .\__,_|.|_|.....\___|..\__,_|...|_|..\___/...\___/..|_|\_\.|___/...|_|.|_|.|_|\_\..\___|.(_)..............

                                                                                                                     ~
    '''
)

DEMO_3 = Area(
    name='Demo 3 (really big)',
    s=r'''
    ~

        TTTTTTTTTTTTTTTTTTTTTTThhhhhhh               iiii                          iiii                                                                 hhhhhhh                                        tttt
        T:::::::::::::::::::::Th:::::h              i::::i                        i::::i                                                                h:::::h                                     ttt:::t
        T:::::::::::::::::::::Th:::::h               iiii                          iiii                                                                 h:::::h                                     t:::::t
        T:::::TT:::::::TT:::::Th:::::h                                                                                                                  h:::::h                                     t:::::t
        TTTTTT  T:::::T  TTTTTT h::::h hhhhh       iiiiiii     ssssssssss        iiiiiii     ssssssssss        wwwwwww           wwwww           wwwwwww h::::h hhhhh         aaaaaaaaaaaaa   ttttttt:::::ttttttt
                T:::::T         h::::hh:::::hhh    i:::::i   ss::::::::::s       i:::::i   ss::::::::::s        w:::::w         w:::::w         w:::::w  h::::hh:::::hhh      a::::::::::::a  t:::::::::::::::::t
                T:::::T         h::::::::::::::hh   i::::i ss:::::::::::::s       i::::i ss:::::::::::::s        w:::::w       w:::::::w       w:::::w   h::::::::::::::hh    aaaaaaaaa:::::a t:::::::::::::::::t
                T:::::T         h:::::::hhh::::::h  i::::i s::::::ssss:::::s      i::::i s::::::ssss:::::s        w:::::w     w:::::::::w     w:::::w    h:::::::hhh::::::h            a::::a tttttt:::::::tttttt
                T:::::T         h::::::h   h::::::h i::::i  s:::::s  ssssss       i::::i  s:::::s  ssssss          w:::::w   w:::::w:::::w   w:::::w     h::::::h   h::::::h    aaaaaaa:::::a       t:::::t
                T:::::T         h:::::h     h:::::h i::::i    s::::::s            i::::i    s::::::s                w:::::w w:::::w w:::::w w:::::w      h:::::h     h:::::h  aa::::::::::::a       t:::::t
                T:::::T         h:::::h     h:::::h i::::i       s::::::s         i::::i       s::::::s              w:::::w:::::w   w:::::w:::::w       h:::::h     h:::::h a::::aaaa::::::a       t:::::t
                T:::::T         h:::::h     h:::::h i::::i ssssss   s:::::s       i::::i ssssss   s:::::s             w:::::::::w     w:::::::::w        h:::::h     h:::::ha::::a    a:::::a       t:::::t    tttttt
              TT:::::::TT       h:::::h     h:::::hi::::::is:::::ssss::::::s     i::::::is:::::ssss::::::s             w:::::::w       w:::::::w         h:::::h     h:::::ha::::a    a:::::a       t::::::tttt:::::t
              T:::::::::T       h:::::h     h:::::hi::::::is::::::::::::::s      i::::::is::::::::::::::s               w:::::w         w:::::w          h:::::h     h:::::ha:::::aaaa::::::a       tt::::::::::::::t
              T:::::::::T       h:::::h     h:::::hi::::::i s:::::::::::ss       i::::::i s:::::::::::ss                 w:::w           w:::w           h:::::h     h:::::h a::::::::::aa:::a        tt:::::::::::tt
              TTTTTTTTTTT       hhhhhhh     hhhhhhhiiiiiiii  sssssssssss         iiiiiiii  sssssssssss                    www             www            hhhhhhh     hhhhhhh  aaaaaaaaaa  aaaa          ttttttttttt








                                                                                                                                       bbbbbbbb
                                                                                         lllllll lllllll                               b::::::b              iiii
                                                                                         l:::::l l:::::l                               b::::::b             i::::i
                                                                                         l:::::l l:::::l                               b::::::b              iiii
                                                                                         l:::::l l:::::l                                b:::::b
          aaaaaaaaaaaaa        rrrrr   rrrrrrrrr       eeeeeeeeeeee      aaaaaaaaaaaaa    l::::l  l::::l yyyyyyy           yyyyyyy      b:::::bbbbbbbbb    iiiiiii    ggggggggg   ggggg
          a::::::::::::a       r::::rrr:::::::::r    ee::::::::::::ee    a::::::::::::a   l::::l  l::::l  y:::::y         y:::::y       b::::::::::::::bb  i:::::i   g:::::::::ggg::::g
          aaaaaaaaa:::::a      r:::::::::::::::::r  e::::::eeeee:::::ee  aaaaaaaaa:::::a  l::::l  l::::l   y:::::y       y:::::y        b::::::::::::::::b  i::::i  g:::::::::::::::::g
                   a::::a      rr::::::rrrrr::::::re::::::e     e:::::e           a::::a  l::::l  l::::l    y:::::y     y:::::y         b:::::bbbbb:::::::b i::::i g::::::ggggg::::::gg
            aaaaaaa:::::a       r:::::r     r:::::re:::::::eeeee::::::e    aaaaaaa:::::a  l::::l  l::::l     y:::::y   y:::::y          b:::::b    b::::::b i::::i g:::::g     g:::::g
          aa::::::::::::a       r:::::r     rrrrrrre:::::::::::::::::e   aa::::::::::::a  l::::l  l::::l      y:::::y y:::::y           b:::::b     b:::::b i::::i g:::::g     g:::::g
         a::::aaaa::::::a       r:::::r            e::::::eeeeeeeeeee   a::::aaaa::::::a  l::::l  l::::l       y:::::y:::::y            b:::::b     b:::::b i::::i g:::::g     g:::::g
        a::::a    a:::::a       r:::::r            e:::::::e           a::::a    a:::::a  l::::l  l::::l        y:::::::::y             b:::::b     b:::::b i::::i g::::::g    g:::::g
        a::::a    a:::::a       r:::::r            e::::::::e          a::::a    a:::::a l::::::ll::::::l        y:::::::y              b:::::bbbbbb::::::bi::::::ig:::::::ggggg:::::g
        a:::::aaaa::::::a       r:::::r             e::::::::eeeeeeee  a:::::aaaa::::::a l::::::ll::::::l         y:::::y               b::::::::::::::::b i::::::i g::::::::::::::::g
         a::::::::::aa:::a      r:::::r              ee:::::::::::::e   a::::::::::aa:::al::::::ll::::::l        y:::::y                b:::::::::::::::b  i::::::i  gg::::::::::::::g
          aaaaaaaaaa  aaaa      rrrrrrr                eeeeeeeeeeeeee    aaaaaaaaaa  aaaallllllllllllllll       y:::::y                 bbbbbbbbbbbbbbbb   iiiiiiii    gggggggg::::::g
                                                                                                               y:::::y                                                         g:::::g
                                                                                                              y:::::y                                              gggggg      g:::::g
                                                                                                             y:::::y                                               g:::::gg   gg:::::g
                                                                                                            y:::::y                                                 g::::::ggg:::::::g
                                                                                                           yyyyyyy                                                   gg:::::::::::::g
                                                                                                                                                                       ggg::::::ggg
                                                                                                                                                                          gggggg


                                                                                         lllllll                                   kkkkkkkk                                 lllllll   iiii  kkkkkkkk
                                                                                         l:::::l                                   k::::::k                                 l:::::l  i::::i k::::::k
                                                                                         l:::::l                                   k::::::k                                 l:::::l   iiii  k::::::k
                                                                                         l:::::l                                   k::::::k                                 l:::::l         k::::::k
          aaaaaaaaaaaaa   rrrrr   rrrrrrrrr       eeeeeeeeeeee      aaaaaaaaaaaaa         l::::l    ooooooooooo      ooooooooooo    k:::::k    kkkkkkk    ssssssssss         l::::l iiiiiii  k:::::k    kkkkkkk    eeeeeeeeeeee
          a::::::::::::a  r::::rrr:::::::::r    ee::::::::::::ee    a::::::::::::a        l::::l  oo:::::::::::oo  oo:::::::::::oo  k:::::k   k:::::k   ss::::::::::s        l::::l i:::::i  k:::::k   k:::::k   ee::::::::::::ee
          aaaaaaaaa:::::a r:::::::::::::::::r  e::::::eeeee:::::ee  aaaaaaaaa:::::a       l::::l o:::::::::::::::oo:::::::::::::::o k:::::k  k:::::k  ss:::::::::::::s       l::::l  i::::i  k:::::k  k:::::k   e::::::eeeee:::::ee
                   a::::a rr::::::rrrrr::::::re::::::e     e:::::e           a::::a       l::::l o:::::ooooo:::::oo:::::ooooo:::::o k:::::k k:::::k   s::::::ssss:::::s      l::::l  i::::i  k:::::k k:::::k   e::::::e     e:::::e
            aaaaaaa:::::a  r:::::r     r:::::re:::::::eeeee::::::e    aaaaaaa:::::a       l::::l o::::o     o::::oo::::o     o::::o k::::::k:::::k     s:::::s  ssssss       l::::l  i::::i  k::::::k:::::k    e:::::::eeeee::::::e
          aa::::::::::::a  r:::::r     rrrrrrre:::::::::::::::::e   aa::::::::::::a       l::::l o::::o     o::::oo::::o     o::::o k:::::::::::k        s::::::s            l::::l  i::::i  k:::::::::::k     e:::::::::::::::::e
         a::::aaaa::::::a  r:::::r            e::::::eeeeeeeeeee   a::::aaaa::::::a       l::::l o::::o     o::::oo::::o     o::::o k:::::::::::k           s::::::s         l::::l  i::::i  k:::::::::::k     e::::::eeeeeeeeeee
        a::::a    a:::::a  r:::::r            e:::::::e           a::::a    a:::::a       l::::l o::::o     o::::oo::::o     o::::o k::::::k:::::k    ssssss   s:::::s       l::::l  i::::i  k::::::k:::::k    e:::::::e
        a::::a    a:::::a  r:::::r            e::::::::e          a::::a    a:::::a      l::::::lo:::::ooooo:::::oo:::::ooooo:::::ok::::::k k:::::k   s:::::ssss::::::s     l::::::li::::::ik::::::k k:::::k   e::::::::e
        a:::::aaaa::::::a  r:::::r             e::::::::eeeeeeee  a:::::aaaa::::::a      l::::::lo:::::::::::::::oo:::::::::::::::ok::::::k  k:::::k  s::::::::::::::s      l::::::li::::::ik::::::k  k:::::k   e::::::::eeeeeeee   ......
         a::::::::::aa:::a r:::::r              ee:::::::::::::e   a::::::::::aa:::a     l::::::l oo:::::::::::oo  oo:::::::::::oo k::::::k   k:::::k  s:::::::::::ss       l::::::li::::::ik::::::k   k:::::k   ee:::::::::::::e   .::::.
          aaaaaaaaaa  aaaa rrrrrrr                eeeeeeeeeeeeee    aaaaaaaaaa  aaaa     llllllll   ooooooooooo      ooooooooooo   kkkkkkkk    kkkkkkk  sssssssssss         lllllllliiiiiiiikkkkkkkk    kkkkkkk    eeeeeeeeeeeeee   ......

                                                                                                                                                                                                                                             ~
    '''
)
